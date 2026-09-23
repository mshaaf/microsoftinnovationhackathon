from app.adapters.base import UnconfiguredLiveAdapter

from .base import SERVICE_NAME


class Adapter(UnconfiguredLiveAdapter):
    service_name = SERVICE_NAME
