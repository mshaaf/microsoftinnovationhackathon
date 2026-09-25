import os
from contextlib import nullcontext

import httpx
from azure.core.exceptions import AzureError

from app.adapters.base import NotConfigured, ServiceStatus
from app.core.i18n import translator_text

from .base import SERVICE_NAME, TranslatorAdapter

ENDPOINT = "https://api.cognitive.microsofttranslator.com/translate"
TOKEN_SCOPE = "https://cognitiveservices.azure.com/.default"


class Adapter(TranslatorAdapter):
    service_name = SERVICE_NAME

    def __init__(self, client: httpx.Client | None = None):
        self._client = client

    def health_status(self) -> ServiceStatus:
        if not os.getenv("AZURE_AI_SERVICES_REGION"):
            raise NotConfigured("translator live adapter is not configured")
        return "ok"

    def translate(self, text: str) -> str:
        self.health_status()
        if len(text) > 50_000:
            raise NotConfigured("translation text is too long")

        key = os.getenv("AZURE_AI_SERVICES_KEY")
        region = os.environ["AZURE_AI_SERVICES_REGION"]
        credential = None
        headers = {"Content-Type": "application/json"}
        try:
            if key:
                headers["Ocp-Apim-Subscription-Key"] = key
            else:
                from azure.identity import AzureCliCredential, ManagedIdentityCredential

                credential = (
                    ManagedIdentityCredential()
                    if os.getenv("CONTAINER_APP_NAME")
                    else AzureCliCredential()
                )
                headers["Authorization"] = (
                    f"Bearer {credential.get_token(TOKEN_SCOPE).token}"
                )
            headers["Ocp-Apim-Subscription-Region"] = region
            context = (
                nullcontext(self._client)
                if self._client is not None
                else httpx.Client(timeout=10.0)
            )
            with context as client:
                response = client.post(
                    ENDPOINT,
                    params={"api-version": "3.0", "from": "en", "to": "es"},
                    headers=headers,
                    json=[{"Text": translator_text(text)}],
                    timeout=10.0,
                )
                response.raise_for_status()
                translations = response.json()[0]["translations"]
                result = translations[0]["text"]
                if not isinstance(result, str):
                    raise TypeError
                return result
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
            raise NotConfigured("translation is unavailable") from None
        finally:
            if credential is not None:
                credential.close()
