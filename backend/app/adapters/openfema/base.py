from app.adapters.base import BaseAdapter, NotConfigured, ServiceStatus

SERVICE_NAME = "openfema"


class OpenFEMAUnavailable(RuntimeError):
    """OpenFEMA could not return declaration data."""


class OpenFEMAAdapter(BaseAdapter):
    def declarations_for_county(self, state_fips: str, county_code: str) -> list[dict]:
        raise NotImplementedError


__all__ = [
    "SERVICE_NAME",
    "BaseAdapter",
    "NotConfigured",
    "OpenFEMAAdapter",
    "OpenFEMAUnavailable",
    "ServiceStatus",
]
