import os

import httpx
from azure.core.exceptions import AzureError

from app.adapters.base import NotConfigured, ServiceStatus
from app.adapters.safety.base import SafetyAdapter, ShieldResult

API_VERSION = "2024-09-01"
SCOPE = "https://cognitiveservices.azure.com/.default"


class Adapter(SafetyAdapter):
    def __init__(self, client: httpx.AsyncClient | None = None):
        self._client = client

    def health_status(self) -> ServiceStatus:
        if not os.getenv("AZURE_AI_SERVICES_ENDPOINT"):
            raise NotConfigured("safety live adapter is not configured")
        return "ok"

    async def shield_prompt(
        self, user_prompt: str = "", documents: list[str] | None = None
    ) -> ShieldResult:
        self.health_status()
        documents = documents or []
        if len(documents) > 5:
            raise NotConfigured("Prompt Shield accepts at most five documents")

        endpoint = os.environ["AZURE_AI_SERVICES_ENDPOINT"].rstrip("/")
        key = os.getenv("AZURE_AI_SERVICES_KEY")
        headers = {"Content-Type": "application/json"}
        credential = None
        client = self._client
        try:
            if key:
                headers["Ocp-Apim-Subscription-Key"] = key
            else:
                from azure.identity.aio import (
                    AzureCliCredential,
                    ManagedIdentityCredential,
                )

                credential = (
                    ManagedIdentityCredential()
                    if os.getenv("CONTAINER_APP_NAME")
                    else AzureCliCredential()
                )
                headers["Authorization"] = (
                    f"Bearer {(await credential.get_token(SCOPE)).token}"
                )

            if client is None:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await self._post(
                        client, endpoint, headers, user_prompt, documents
                    )
            else:
                response = await self._post(
                    client, endpoint, headers, user_prompt, documents
                )
            response.raise_for_status()
            body = response.json()
            user_attack = body["userPromptAnalysis"]["attackDetected"]
            document_results = body["documentsAnalysis"]
            if (
                not isinstance(user_attack, bool)
                or not isinstance(document_results, list)
                or len(document_results) != len(documents)
                or any(
                    not isinstance(row["attackDetected"], bool)
                    for row in document_results
                )
            ):
                raise ValueError("invalid Prompt Shield response")
            return {
                "user_prompt_attack": user_attack,
                "document_attacks": [row["attackDetected"] for row in document_results],
            }
        except NotConfigured:
            raise
        except (
            AzureError,
            httpx.HTTPError,
            AttributeError,
            IndexError,
            KeyError,
            TypeError,
            ValueError,
        ):
            # Never include user or letter text in dependency errors.
            raise NotConfigured("Prompt Shield is unavailable") from None
        finally:
            if credential is not None:
                await credential.close()

    @staticmethod
    async def _post(client, endpoint, headers, user_prompt, documents):
        return await client.post(
            f"{endpoint}/contentsafety/text:shieldPrompt",
            params={"api-version": API_VERSION},
            headers=headers,
            json={"userPrompt": user_prompt, "documents": documents},
            timeout=10.0,
        )
