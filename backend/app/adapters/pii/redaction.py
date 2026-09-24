import re

from app.core.pii import REDACTION_PATTERNS

from .base import PiiEntity

MAX_CHUNK_CHARS = 5120
CHUNK_OVERLAP_CHARS = 512
# ponytail: 512-character overlap covers expected PII spans; widen it if supported entity limits grow.
PATTERNS = (
    *REDACTION_PATTERNS,
    ("ZipCode", re.compile(r"(?<!\d)\d{5}-\d{4}(?!\d)")),
    ("USSocialSecurityNumber", re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)")),
    (
        "USBankAccountNumber",
        re.compile(
            r"\b(?:bank\s+account(?:\s+(?:number|no\.?))?|account\s+(?:number|no\.?))"
            r"\s*[:#-]?\s*\d{8,17}\b",
            re.IGNORECASE,
        ),
    ),
    (
        "CreditCardNumber",
        re.compile(r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)"),
    ),
    (
        "USDriversLicenseNumber",
        re.compile(
            r"\b(?:driver'?s?\s+license|driver'?s?\s+licence|license(?:\s+number)?|"
            r"licence(?:\s+number)?)\s*[:#-]?\s*[A-Z0-9-]{4,20}\b",
            re.IGNORECASE,
        ),
    ),
    (
        "USUKPassportNumber",
        re.compile(
            r"\bpassport(?:\s+(?:number|no\.?))?\s*[:#-]?\s*[A-Z0-9]{6,12}\b",
            re.IGNORECASE,
        ),
    ),
)
DATE_OF_BIRTH_PATTERN = re.compile(
    r"\b(?:date\s+of\s+birth|birth\s+date|dob)\s*[:#-]?\s*"
    r"(?P<value>\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2})",
    re.IGNORECASE,
)


def text_chunks(text: str):
    start = 0
    step = MAX_CHUNK_CHARS - CHUNK_OVERLAP_CHARS
    while start < len(text):
        end = min(start + MAX_CHUNK_CHARS, len(text))
        yield start, text[start:end]
        if end == len(text):
            break
        start += step


def fallback_entities(text: str) -> tuple[PiiEntity, ...]:
    matches = [
        PiiEntity(category, match.start(), match.end() - match.start())
        for category, pattern in PATTERNS
        for match in pattern.finditer(text)
    ]
    matches.extend(
        PiiEntity(
            "DateOfBirth",
            match.start("value"),
            match.end("value") - match.start("value"),
        )
        for match in DATE_OF_BIRTH_PATTERN.finditer(text)
    )
    return tuple(matches)


def unique_entities(entities: tuple[PiiEntity, ...] | list[PiiEntity]):
    return tuple(
        sorted(
            set(entities),
            key=lambda entity: (entity.offset, -entity.length, entity.category),
        )
    )
