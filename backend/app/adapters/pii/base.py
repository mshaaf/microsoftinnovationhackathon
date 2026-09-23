from app.adapters.base import BaseAdapter, NotConfigured, ServiceStatus


class PiiAdapter(BaseAdapter):
    def detect(self, text: str) -> tuple[str, ...]:
        raise NotImplementedError


__all__ = ["NotConfigured", "PiiAdapter", "ServiceStatus"]
