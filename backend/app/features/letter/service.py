import json
from datetime import date
from functools import lru_cache
from pathlib import Path
from typing import Any

from app.adapters import get_adapter
from app.adapters.base import NotConfigured
from app.adapters.ocr.base import OCRResult, UnreadableLetter
from app.core import model_gateway
from app.core.config import get_app_mode
from app.features.deadline.service import compute_deadline
from app.features.letter.classify_step import (
    LetterReading,
    classify_letter,
    taxonomy_data,
)
from app.features.letter.redact_step import RedactionResult, redact
from app.features.rules.service import rules_for_declaration

ROOT = Path(__file__).resolve().parents[4]
IHP_RULES_PATH = ROOT / "data/ihp_rules.json"


def _taxonomy() -> dict[str, Any]:
    data = taxonomy_data()
    return {row["id"]: row for row in data["reasons"]}


@lru_cache(maxsize=1)
def _ihp_rules() -> dict[str, Any]:
    return json.loads(IHP_RULES_PATH.read_text(encoding="utf-8"))


def redact_ocr_result(ocr: OCRResult, language: str = "en") -> RedactionResult:
    return redact(ocr.text, language)


def _parse_letter_date(value: str | None) -> date:
    if not isinstance(value, str):
        raise UnreadableLetter("We could not read this letter.")
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        raise UnreadableLetter("We could not read this letter.") from None
    if parsed.isoformat() != value:
        raise UnreadableLetter("We could not read this letter.")
    return parsed


def _deadline_regime(declaration: dict | None) -> dict[str, Any]:
    regimes = _ihp_rules()["regimes"]
    declaration_date = None
    if declaration is not None:
        try:
            declaration_date = date.fromisoformat(
                str(declaration["declarationDate"])[:10]
            )
        except (KeyError, TypeError, ValueError):
            pass
    if declaration_date is not None:
        regime_id = rules_for_declaration(declaration_date)["rules_regime"]
        return next(row for row in regimes if row["id"] == regime_id)

    # Every current IHP regime has the same appeal window. If that changes, an
    # unknown disaster cannot yield a truthful deadline until its regime is known.
    windows = {row["appeal_window_days"] for row in regimes}
    if len(windows) != 1:
        raise NotConfigured("Cannot determine the appeal window")
    return {"appeal_window_days": windows.pop()}


def _validated_reasons(reading: LetterReading) -> list[dict[str, Any]]:
    taxonomy = _taxonomy()
    reasons = []
    seen = set()
    for guess in reading.reasons:
        reason_id = (
            guess.taxonomy_id if guess.taxonomy_id in taxonomy else "other_or_unclear"
        )
        if reason_id in seen:
            continue
        seen.add(reason_id)
        reasons.append(
            {
                "taxonomy_id": reason_id,
                "confidence": (
                    guess.confidence if guess.taxonomy_id in taxonomy else 0.0
                ),
            }
        )
    if not reasons:
        reasons.append({"taxonomy_id": "other_or_unclear", "confidence": 0.0})
    return reasons


async def decode_ocr(
    data: bytes, filename: str, lang: str = "en", request_id: str = ""
) -> dict[str, Any]:
    ocr: OCRResult = await get_adapter("ocr").read(data, filename)
    redaction = redact_ocr_result(ocr, lang)
    try:
        reading = await classify_letter(redaction.redacted_text, lang)
    except model_gateway.PIILeakError:
        raise NotConfigured("Letter classification is unavailable") from None

    letter_date = _parse_letter_date(reading.letter_date)
    declaration = (
        get_adapter("openfema").declaration_by_number(reading.disaster_number)
        if reading.disaster_number is not None
        else None
    )
    synthetic_mock_row = (
        declaration is not None
        and get_app_mode() == "mock"
        and str(declaration.get("hash", "")).startswith("synthetic-")
    )
    verified = declaration is not None and not synthetic_mock_row
    reasons = _validated_reasons(reading)
    taxonomy = _taxonomy()
    language = lang if lang in {"en", "es"} else "en"
    reason_ids = [reason["taxonomy_id"] for reason in reasons]
    first_reason = reason_ids[0]
    checklist = []
    seen_items = set()
    for reason_id in reason_ids:
        for item in taxonomy[reason_id]["what_to_send"]:
            if item["id"] in seen_items:
                continue
            seen_items.add(item["id"])
            checklist.append(
                {
                    "id": item["id"],
                    "text": item["text"][language],
                    "source_url": taxonomy[reason_id]["source_url"],
                }
            )

    threshold = taxonomy_data()["confidence_threshold"]
    needs_handoff = (
        reading.decision_type == "unclear"
        or not verified
        or any(
            reason["taxonomy_id"] == "other_or_unclear"
            or reason["confidence"] < threshold
            for reason in reasons
        )
    )
    deadline = compute_deadline(
        letter_date, _deadline_regime(declaration), lang=language
    )
    return {
        "request_id": request_id,
        "ocr": {"confidence": ocr.confidence, "pages": ocr.pages},
        **redaction.response_fields(),
        "decision": {
            "type": reading.decision_type,
            "assistance_types": reading.assistance_types,
            "letter_date": letter_date.isoformat(),
            "disaster_number": reading.disaster_number,
            "disaster_number_verified": verified,
        },
        "reasons": reasons,
        "explanation": " ".join(
            dict.fromkeys(
                taxonomy[reason_id]["plain_explanation"][language]
                for reason_id in reason_ids
            )
        ),
        "checklist": checklist,
        "deadline": deadline.model_dump(mode="json"),
        "appeal_template_id": first_reason,
        "handoff": "low_confidence" if needs_handoff else None,
    }
