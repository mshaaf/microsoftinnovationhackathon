from app.adapters import get_adapter
from app.adapters.ocr.base import OCRUnavailable


async def decode_ocr(data: bytes, filename: str) -> None:
    await get_adapter("ocr").read(data, filename)
    # The frozen success response needs classification and a real letter date.
    raise OCRUnavailable("Letter review needs the PII and classification steps")
