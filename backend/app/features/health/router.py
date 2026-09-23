from uuid import uuid4

from fastapi import APIRouter

from app.core.config import APP_MODE

router = APIRouter()


@router.get("/health")
def health() -> dict:
    status = "mock" if APP_MODE == "mock" else "not_configured"
    return {
        "request_id": str(uuid4()),
        "mode": APP_MODE,
        "version": "0.1.0",
        "services": {
            "openfema": status,
            "geo": "ok",
            "search": status,
            "model": status,
            "ocr": status,
            "pii": status,
            "translator": status,
            "safety": status,
        },
    }
