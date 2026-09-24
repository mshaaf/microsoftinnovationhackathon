from uuid import uuid4

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.adapters.base import NotConfigured
from app.adapters.ocr.base import OCRUnavailable, UnreadableLetter
from app.adapters.openfema.base import OpenFEMAUnavailable

from .ocr_step import UploadError, read_upload
from .service import decode_ocr

router = APIRouter()


@router.post("/letter/decode")
async def decode(request: Request):
    request_id = str(uuid4())
    try:
        data, filename, lang = await read_upload(request)
        return await decode_ocr(data, filename, lang, request_id)
    except UploadError as error:
        status, code, message, retryable = (
            error.status,
            error.code,
            error.message,
            False,
        )
    except UnreadableLetter:
        status, code, message, retryable = (
            422,
            "unreadable_letter",
            "We could not read this letter. Try a clearer photo.",
            False,
        )
    except (OCRUnavailable, OpenFEMAUnavailable, NotConfigured):
        status, code, message, retryable = (
            503,
            "dependency_unavailable",
            "Letter review cannot be completed right now. Try again later.",
            True,
        )
    return JSONResponse(
        status_code=status,
        content={
            "request_id": request_id,
            "error": {"code": code, "message": message, "retryable": retryable},
        },
    )
