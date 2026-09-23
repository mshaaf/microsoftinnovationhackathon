from typing import Literal

ServiceStatus = Literal["ok", "mock", "down", "not_configured"]
SERVICE_NAMES = (
    "openfema",
    "geo",
    "search",
    "model",
    "ocr",
    "pii",
    "translator",
    "safety",
)


class NotConfigured(RuntimeError):
    """A live adapter cannot run until its service configuration is available."""


class BaseAdapter:
    def health_status(self) -> ServiceStatus:
        raise NotImplementedError


class MockAdapter(BaseAdapter):
    def health_status(self) -> ServiceStatus:
        return "mock"


class UnconfiguredLiveAdapter(BaseAdapter):
    service_name = "service"

    def health_status(self) -> ServiceStatus:
        raise NotConfigured(f"{self.service_name} live adapter is not configured")
