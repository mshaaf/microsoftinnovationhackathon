from app.adapters.base import BaseAdapter, NotConfigured, ServiceStatus

SERVICE_NAME = "search"


class SearchAdapter(BaseAdapter):
    """Result shape: {title, url, agency, lang, topic, content, score}."""

    def search(self, query: str, lang: str = "en", top: int = 5) -> list[dict]:
        raise NotImplementedError


__all__ = [
    "SERVICE_NAME",
    "BaseAdapter",
    "NotConfigured",
    "SearchAdapter",
    "ServiceStatus",
]
