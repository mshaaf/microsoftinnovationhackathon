from functools import lru_cache
from hashlib import sha256
from pathlib import Path

from app.adapters.base import MockAdapter

from .base import OCRAdapter, OCRResult, UnreadableLetter

LETTERS = Path(__file__).resolve().parents[4] / "fixtures" / "letters"


@lru_cache(maxsize=1)
def _fixture_hashes() -> dict[str, str]:
    return {
        sha256(path.read_bytes()).hexdigest(): path.stem
        for path in LETTERS.glob("L*.png")
    }


class Adapter(MockAdapter, OCRAdapter):
    async def read(self, data: bytes, filename: str) -> OCRResult:
        name = Path(filename).name
        letter_id = (
            Path(name).stem
            if (LETTERS / name).is_file()
            else _fixture_hashes().get(sha256(data).hexdigest())
        )
        if not letter_id or not (LETTERS / f"{letter_id}.txt").is_file():
            raise UnreadableLetter("No mock OCR fixture matched the upload")
        return OCRResult(
            (LETTERS / f"{letter_id}.txt").read_text(encoding="utf-8"), 1, 0.97
        )
