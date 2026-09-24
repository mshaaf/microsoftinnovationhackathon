import re
from uuid import uuid4

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.adapters import get_adapter

router = APIRouter()
ZIP_PATTERN = re.compile(r"[0-9]{5}")


def _error(request_id: str, status: int, code: str, message: str):
    return JSONResponse(
        status_code=status,
        content={
            "request_id": request_id,
            "error": {"code": code, "message": message, "retryable": False},
        },
    )


@router.post("/location")
async def resolve_location(request: Request):
    request_id = str(uuid4())
    try:
        body = await request.json()
    except ValueError:
        return _error(request_id, 400, "invalid_input", "Send a valid JSON request.")

    zip_code = body.get("zip") if isinstance(body, dict) else None
    if not isinstance(zip_code, str) or ZIP_PATTERN.fullmatch(zip_code) is None:
        return _error(
            request_id, 400, "invalid_input", "Enter a valid five-digit ZIP code."
        )

    counties = get_adapter("geo").lookup(zip_code)
    if counties is None:
        return _error(
            request_id,
            404,
            "zip_not_found",
            "This ZIP code is not in the Census map. Try another ZIP or call 211 for local help.",
        )

    return {
        "request_id": request_id,
        "zip": zip_code,
        "counties": counties,
        "needs_confirmation": len(counties) > 1,
    }
