from app.adapters.ocr.base import OCRUnavailable


async def decode_ocr() -> None:
    # Wait until the full pipeline can respond without exposing OCR text or fake dates.
    raise OCRUnavailable("Letter review is not complete")
