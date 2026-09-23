from typing import Any

from app.adapters.base import BaseAdapter, NotConfigured, ServiceStatus


class ModelAdapter(BaseAdapter):
    async def run(self, payload: Any) -> Any:
        raise NotImplementedError


__all__ = ["ModelAdapter", "NotConfigured", "ServiceStatus"]
