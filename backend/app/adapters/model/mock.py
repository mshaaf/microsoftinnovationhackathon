from typing import Any

from app.adapters.base import ServiceStatus
from app.adapters.model.base import ModelAdapter


class Adapter(ModelAdapter):
    def health_status(self) -> ServiceStatus:
        return "mock"

    async def run(self, payload: Any) -> dict[str, str]:
        return {"text": "This is a mock response."}
