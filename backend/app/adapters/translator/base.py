from app.adapters.base import BaseAdapter, NotConfigured, ServiceStatus

SERVICE_NAME = "translator"


class TranslatorAdapter(BaseAdapter):
    def translate(self, text: str) -> str:
        raise NotImplementedError


__all__ = [
    "SERVICE_NAME",
    "BaseAdapter",
    "NotConfigured",
    "ServiceStatus",
    "TranslatorAdapter",
]
