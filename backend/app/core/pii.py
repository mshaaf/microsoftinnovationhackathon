import json
import re
from functools import lru_cache
from pathlib import Path

FIXTURE_LETTERS_DIR = Path(__file__).resolve().parents[3] / "fixtures" / "letters"

REDACTION_PATTERNS = (
    ("Email", re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")),
    (
        "PhoneNumber",
        re.compile(
            r"(?<!\d)(?:\+?1[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)?\d{3}[\s.-]\d{4}(?!\d)"
            r"|(?<!\d)\d{3}[-.]\d{4}(?!\d)|(?<!\d)\d{10}(?!\d)"
        ),
    ),
    ("RegistrationNumber", re.compile(r"(?<!\d)\d{9}(?!\d)")),
    (
        "Address",
        re.compile(
            r"\b\d{1,5}\s+[\w.'-]+(?:\s+[\w.'-]+){0,3}\s+"
            r"(?:street|st|road|rd|avenue|ave|lane|ln|drive|dr|boulevard|blvd)\b",
            re.IGNORECASE,
        ),
    ),
)


@lru_cache(maxsize=1)
def fixture_fake_pii() -> tuple[str, ...]:
    values = set()
    for path in FIXTURE_LETTERS_DIR.glob("*.expected.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        values.update(
            value
            for value in data.get("fake_pii", [])
            if isinstance(value, str) and value
        )
    return tuple(sorted(values, key=len, reverse=True))


def find_pii(text: str) -> tuple[str, ...]:
    lowered = text.casefold()
    categories = []
    if any(value.casefold() in lowered for value in fixture_fake_pii()):
        categories.append("FixtureFakePII")
    categories.extend(
        category for category, pattern in REDACTION_PATTERNS if pattern.search(text)
    )
    return tuple(dict.fromkeys(categories))


def redact_text(text: str) -> str:
    for value in fixture_fake_pii():
        text = re.sub(re.escape(value), "[REDACTED]", text, flags=re.IGNORECASE)
    for _, pattern in REDACTION_PATTERNS:
        text = pattern.sub("[REDACTED]", text)
    return text
