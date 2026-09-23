from app.adapters.base import NotConfigured, ServiceStatus
from app.adapters.pii.base import PiiAdapter


class Adapter(PiiAdapter):
    def health_status(self) -> ServiceStatus:
        raise NotConfigured("pii live adapter is not configured")

    def detect(self, text: str) -> tuple[str, ...]:
        raise NotConfigured("pii live adapter is not configured")
