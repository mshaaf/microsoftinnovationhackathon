from app.adapters.base import ServiceStatus
from app.adapters.pii.base import PiiAdapter
from app.core.pii import find_pii


class Adapter(PiiAdapter):
    def health_status(self) -> ServiceStatus:
        return "mock"

    def detect(self, text: str) -> tuple[str, ...]:
        return find_pii(text)
