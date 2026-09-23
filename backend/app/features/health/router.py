from uuid import uuid4

from fastapi import APIRouter

from app.adapters import service_statuses
from app.core.config import get_app_mode

router = APIRouter()


@router.get("/health")
def health() -> dict:
    mode = get_app_mode()
    return {
        "request_id": str(uuid4()),
        "mode": mode,
        "version": "0.1.0",
        "services": service_statuses(mode),
    }
