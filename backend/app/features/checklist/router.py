from uuid import uuid4

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.adapters.openfema.base import OpenFEMAUnavailable
from app.features.checklist.service import build_checklist

router = APIRouter()


def _error(request_id: str, status: int, code: str, message: str, retryable=False):
    return JSONResponse(
        status_code=status,
        content={
            "request_id": request_id,
            "error": {"code": code, "message": message, "retryable": retryable},
        },
    )


def _valid(body) -> bool:
    if not isinstance(body, dict):
        return False
    number = body.get("disaster_number")
    answers = body.get("answers")
    return (
        isinstance(number, int)
        and not isinstance(number, bool)
        and number > 0
        and body.get("lang") in {"en", "es"}
        and isinstance(answers, dict)
        and answers.get("housing") in {"own", "rent"}
        and answers.get("insured") in {"yes", "no", "not_sure"}
        and isinstance(answers.get("lost_id"), bool)
        and isinstance(answers.get("displaced"), bool)
    )


@router.post("/checklist")
async def checklist(request: Request):
    request_id = str(uuid4())
    try:
        body = await request.json()
    except ValueError:
        body = None
    if not _valid(body):
        return _error(
            request_id, 400, "invalid_input", "Check your answers and try again."
        )

    try:
        result = build_checklist(body["disaster_number"], body["lang"], body["answers"])
    except LookupError:
        return _error(
            request_id, 400, "invalid_input", "The disaster number was not found."
        )
    except OpenFEMAUnavailable:
        return _error(
            request_id,
            503,
            "dependency_unavailable",
            "FEMA declaration data is temporarily unavailable. Try again.",
            retryable=True,
        )
    return {"request_id": request_id, **result}
