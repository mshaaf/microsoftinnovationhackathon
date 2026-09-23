from importlib import import_module

from app.adapters.base import SERVICE_NAMES, NotConfigured, ServiceStatus
from app.core.config import get_app_mode


def get_adapter(service: str, mode: str | None = None):
    if service not in SERVICE_NAMES:
        raise ValueError(f"unknown adapter service: {service}")
    selected_mode = mode or get_app_mode()
    if selected_mode not in {"mock", "live"}:
        raise ValueError("adapter mode must be 'mock' or 'live'")
    module = import_module(f"app.adapters.{service}.{selected_mode}")
    return module.Adapter()


def service_statuses(mode: str | None = None) -> dict[str, ServiceStatus]:
    statuses = {}
    for service in SERVICE_NAMES:
        adapter = get_adapter(service, mode)
        try:
            statuses[service] = adapter.health_status()
        except NotConfigured:
            statuses[service] = "not_configured"
    return statuses


__all__ = ["NotConfigured", "get_adapter", "service_statuses"]
