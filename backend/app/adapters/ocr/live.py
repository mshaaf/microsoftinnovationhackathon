import os
from statistics import mean

from azure.ai.documentintelligence.aio import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError, HttpResponseError
from azure.identity.aio import AzureCliCredential, ManagedIdentityCredential

from app.adapters.base import NotConfigured, ServiceStatus

from .base import OCRAdapter, OCRResult, OCRUnavailable, UnreadableLetter


class Adapter(OCRAdapter):
    def health_status(self) -> ServiceStatus:
        if not os.getenv("AZURE_AI_SERVICES_ENDPOINT"):
            raise NotConfigured("OCR endpoint is not configured")
        return "ok"

    async def read(self, data: bytes, filename: str) -> OCRResult:
        self.health_status()
        endpoint = os.environ["AZURE_AI_SERVICES_ENDPOINT"]
        key = os.getenv("AZURE_AI_SERVICES_KEY")
        credential = (
            AzureKeyCredential(key)
            if key
            else (
                ManagedIdentityCredential()
                if os.getenv("CONTAINER_APP_NAME")
                else AzureCliCredential()
            )
        )
        try:
            async with DocumentIntelligenceClient(endpoint, credential) as client:
                poller = await client.begin_analyze_document(
                    "prebuilt-read", AnalyzeDocumentRequest(bytes_source=data)
                )
                result = await poller.result()
        except HttpResponseError as error:
            if error.status_code in {400, 415, 422}:
                raise UnreadableLetter(
                    "The uploaded document could not be read"
                ) from error
            raise OCRUnavailable("OCR service is unavailable") from error
        except AzureError as error:
            raise OCRUnavailable("OCR service is unavailable") from error
        finally:
            if not key:
                await credential.close()
        if not result.content or not result.pages:
            raise UnreadableLetter("No text was found in the letter")
        scores = [
            word.confidence
            for page in result.pages
            for word in (page.words or [])
            if word.confidence is not None
        ]
        return OCRResult(
            result.content, len(result.pages), mean(scores) if scores else 0.0
        )
