from dataclasses import dataclass

from app.adapters import get_adapter
from app.adapters.base import NotConfigured
from app.adapters.pii.base import PiiEntity
from app.adapters.pii.redaction import fallback_entities, unique_entities

MAX_PREVIEW_CHARS = 1200
LABELS = {
    "Person": "PERSON",
    "Address": "ADDRESS",
    "PhoneNumber": "PHONE",
    "Email": "EMAIL",
    "RegistrationNumber": "ID_NUMBER",
    "USSocialSecurityNumber": "ID_NUMBER",
    "USBankAccountNumber": "ID_NUMBER",
    "CreditCardNumber": "ID_NUMBER",
    "USDriversLicenseNumber": "ID_NUMBER",
    "USUKPassportNumber": "ID_NUMBER",
    "DateOfBirth": "DATE_OF_BIRTH",
    "ZipCode": "ZIP_CODE",
}


@dataclass(frozen=True)
class RedactionResult:
    redacted_text: str
    entities_removed: int
    categories: tuple[str, ...]

    def response_fields(self) -> dict:
        return {
            "redaction": {
                "entities_removed": self.entities_removed,
                "categories": list(self.categories),
            },
            "redacted_preview": self.redacted_text[:MAX_PREVIEW_CHARS],
        }


def _replacement_spans(entities: tuple[PiiEntity, ...]) -> list[tuple[int, int, str]]:
    spans = []
    for entity in entities:
        start, end = entity.offset, entity.offset + entity.length
        label = LABELS.get(entity.category, "PERSONAL_DATA")
        if spans and start < spans[-1][1]:
            old_start, old_end, old_label = spans[-1]
            spans[-1] = (
                old_start,
                max(old_end, end),
                old_label if old_label == label else "PERSONAL_DATA",
            )
        else:
            spans.append((start, end, label))
    return spans


def redact(text: str, language: str = "en", mode: str | None = None) -> RedactionResult:
    try:
        detector = get_adapter("pii", mode)
        entities = unique_entities(
            (*detector.entities(text, language), *fallback_entities(text))
        )
    # Any detector failure must stop the pipeline without exposing its details.
    except Exception as error:
        if isinstance(error, NotConfigured):
            raise
        raise NotConfigured("PII detection is unavailable") from None

    if any(
        entity.offset < 0
        or entity.length < 1
        or entity.offset + entity.length > len(text)
        for entity in entities
    ):
        raise NotConfigured("PII detection is unavailable")

    redacted = text
    spans = _replacement_spans(entities)
    for start, end, label in reversed(spans):
        redacted = f"{redacted[:start]}[{label}]{redacted[end:]}"
    return RedactionResult(
        redacted,
        len(spans),
        tuple(sorted({entity.category for entity in entities})),
    )
