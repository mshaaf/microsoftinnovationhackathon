import os
from contextlib import nullcontext

import httpx
from azure.core.exceptions import AzureError
from azure.identity import AzureCliCredential, ManagedIdentityCredential

from app.adapters.base import NotConfigured, ServiceStatus
from app.adapters.pii.base import PiiAdapter, PiiEntity
from app.adapters.pii.redaction import text_chunks, unique_entities

API_VERSION = "2024-11-01"
PII_CATEGORIES = (
    "Person",
    "Address",
    "PhoneNumber",
    "Email",
    "USSocialSecurityNumber",
    "USBankAccountNumber",
    "CreditCardNumber",
    "USDriversLicenseNumber",
    "USUKPassportNumber",
    "DateOfBirth",
)
PII_SCOPE = "https://cognitiveservices.azure.com/.default"


class Adapter(PiiAdapter):
    def __init__(self, client: httpx.Client | None = None):
        self._client = client

    def health_status(self) -> ServiceStatus:
        if not os.getenv("AZURE_AI_SERVICES_ENDPOINT"):
            raise NotConfigured("pii live adapter is not configured")
        return "ok"

    def entities(self, text: str, language: str = "en") -> tuple[PiiEntity, ...]:
        self.health_status()
        endpoint = os.environ["AZURE_AI_SERVICES_ENDPOINT"].rstrip("/")
        key = os.getenv("AZURE_AI_SERVICES_KEY")
        credential = None
        headers = {"Content-Type": "application/json"}
        try:
            if key:
                headers["Ocp-Apim-Subscription-Key"] = key
            else:
                credential = (
                    ManagedIdentityCredential()
                    if os.getenv("CONTAINER_APP_NAME")
                    else AzureCliCredential()
                )
                headers["Authorization"] = (
                    f"Bearer {credential.get_token(PII_SCOPE).token}"
                )

            found = []
            client_context = (
                nullcontext(self._client)
                if self._client is not None
                else httpx.Client(timeout=10.0)
            )
            with client_context as client:
                for index, (start, chunk) in enumerate(text_chunks(text), start=1):
                    payload = {
                        "kind": "PiiEntityRecognition",
                        "parameters": {
                            "modelVersion": "latest",
                            "piiCategories": list(PII_CATEGORIES),
                            "stringIndexType": "UnicodeCodePoint",
                            "loggingOptOut": True,
                        },
                        "analysisInput": {
                            "documents": [
                                {"id": str(index), "language": language, "text": chunk}
                            ]
                        },
                    }
                    response = client.post(
                        f"{endpoint}/language/:analyze-text",
                        params={"api-version": API_VERSION},
                        headers=headers,
                        json=payload,
                        timeout=10.0,
                    )
                    response.raise_for_status()
                    result = response.json()["results"]
                    documents = result["documents"]
                    if result.get("errors") or len(documents) != 1:
                        raise ValueError("invalid PII response")
                    document = documents[0]
                    if document.get("id") != str(index):
                        raise ValueError("invalid PII document id")
                    for entity in document["entities"]:
                        offset, length = entity["offset"], entity["length"]
                        category, value = entity["category"], entity["text"]
                        if (
                            not isinstance(offset, int)
                            or isinstance(offset, bool)
                            or not isinstance(length, int)
                            or isinstance(length, bool)
                            or not isinstance(category, str)
                            or not isinstance(value, str)
                            or offset < 0
                            or length < 1
                            or offset + length > len(chunk)
                            or chunk[offset : offset + length] != value
                        ):
                            raise ValueError("invalid PII entity span")
                        found.append(PiiEntity(category, start + offset, length))
            return unique_entities(found)
        except (
            AzureError,
            httpx.HTTPError,
            AttributeError,
            IndexError,
            KeyError,
            TypeError,
            ValueError,
        ):
            # Never include request or response data in an exception or log.
            raise NotConfigured("PII detection is unavailable") from None
        finally:
            if credential is not None:
                credential.close()
