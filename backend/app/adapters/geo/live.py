from app.adapters.base import UnconfiguredLiveAdapter

from .base import SERVICE_NAME, lookup


class Adapter(UnconfiguredLiveAdapter):
    service_name = SERVICE_NAME

    def lookup(self, zip_code: str):
        return lookup(zip_code)
