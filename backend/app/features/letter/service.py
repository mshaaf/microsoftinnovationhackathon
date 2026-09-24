from app.adapters.ocr.base import OCRResult, OCRUnavailable
from app.features.letter.redact_step import RedactionResult, redact


def redact_ocr_result(ocr: OCRResult, language: str = "en") -> RedactionResult:
    return redact(ocr.text, language)


async def decode_ocr() -> None:
    # Wait until the full pipeline can respond without exposing OCR text or fake dates.
    raise OCRUnavailable("Letter review is not complete")
