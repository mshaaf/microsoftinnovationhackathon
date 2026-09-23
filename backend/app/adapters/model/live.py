from typing import Any

from app.adapters.base import NotConfigured, ServiceStatus
from app.adapters.model.base import ModelAdapter


class Adapter(ModelAdapter):
    def health_status(self) -> ServiceStatus:
        raise NotConfigured("model live adapter is not configured")

    async def run(self, payload: Any) -> Any:
        raise NotConfigured("model live adapter is not configured")
