from dataclasses import dataclass

from app.adapters.base import BaseAdapter, NotConfigured, ServiceStatus

SERVICE_NAME = "ocr"


@dataclass(frozen=True)
class OCRResult:
    text: str
    pages: int
    confidence: float


class OCRUnavailable(RuntimeError):
    pass


class UnreadableLetter(RuntimeError):
    pass


class OCRAdapter(BaseAdapter):
    async def read(self, data: bytes, filename: str) -> OCRResult:
        raise NotImplementedError


__all__ = [
    "SERVICE_NAME",
    "NotConfigured",
    "OCRAdapter",
    "OCRResult",
    "OCRUnavailable",
    "ServiceStatus",
    "UnreadableLetter",
]
