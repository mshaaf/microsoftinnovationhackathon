import os

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from app.adapters.base import NotConfigured, ServiceStatus

from .base import SERVICE_NAME, SearchAdapter

RESULT_KEYS = ("title", "url", "agency", "lang", "topic", "content")


class Adapter(SearchAdapter):
    def _client(self) -> SearchClient:
        endpoint, key = (
            os.getenv("AZURE_SEARCH_ENDPOINT"),
            os.getenv("AZURE_SEARCH_KEY"),
        )
        if not endpoint or not key:
            raise NotConfigured(f"{SERVICE_NAME} live adapter is not configured")
        index = os.getenv("AZURE_SEARCH_INDEX", "navigator-kb")
        return SearchClient(endpoint, index, AzureKeyCredential(key))

    def health_status(self) -> ServiceStatus:
        self._client()
        return "ok"

    def search(self, query: str, lang: str = "en", top: int = 5) -> list[dict]:
        hits = self._client().search(
            query,
            filter=f"lang eq '{lang}'",
            top=top,  # lang is validated by the caller
        )
        return [
            {**{k: h[k] for k in RESULT_KEYS}, "score": float(h["@search.score"])}
            for h in hits
        ]
