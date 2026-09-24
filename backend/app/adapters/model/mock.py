import re
from typing import Any

from app.adapters.base import ServiceStatus
from app.adapters.model.base import ModelAdapter

PROMISE = re.compile(
    r"\b(promise|guarantee|guaranteed|definitely|for sure)\b", re.IGNORECASE
)
LETTER_DATE = re.compile(r"\bDate:\s*(\d{4}-\d{2}-\d{2})", re.IGNORECASE)
DISASTER_NUMBER = re.compile(r"\bFEMA-(\d+)\b", re.IGNORECASE)


def _letter_reading(text: str) -> dict[str, Any]:
    lowered = text.casefold()
    if "unreadable" in lowered or "text missing" in lowered:
        decision, reason = "unclear", "other_or_unclear"
    elif "we need more information to confirm" in lowered:
        decision, reason = "needs_information", "occupancy_not_verified"
    elif "verify your identity" in lowered:
        decision, reason = "not_approved", "identity_not_verified"
    elif "owned the damaged home" in lowered:
        decision, reason = "not_approved", "ownership_not_verified"
    elif "insurance" in lowered and (
        "more information" in lowered or "already covers" in lowered
    ):
        decision, reason = "not_approved", "insurance_docs_missing"
    elif "main residence" in lowered or "main home" in lowered:
        decision, reason = "not_approved", "occupancy_not_verified"
    elif "enough damage" in lowered:
        decision, reason = "not_approved", "insufficient_damage"
    elif "inspection" in lowered and ("complete" in lowered or "reach you" in lowered):
        decision, reason = "not_approved", "missed_inspection_or_contact"
    else:
        decision, reason = "unclear", "other_or_unclear"

    date_match = LETTER_DATE.search(text)
    disaster_match = DISASTER_NUMBER.search(text)
    assistance_types = []
    if "rental assistance" in lowered:
        assistance_types.append("rental")
    if "home repair" in lowered:
        assistance_types.append("home_repair")
    return {
        "decision_type": decision,
        "assistance_types": assistance_types,
        "reasons": [
            {
                "taxonomy_id": reason,
                "confidence": 0.2 if reason == "other_or_unclear" else 0.92,
            }
        ],
        "letter_date": date_match.group(1) if date_match else None,
        "disaster_number": int(disaster_match.group(1)) if disaster_match else None,
    }


class Adapter(ModelAdapter):
    def health_status(self) -> ServiceStatus:
        return "mock"

    async def run(self, payload: Any) -> dict[str, Any]:
        if isinstance(payload, dict) and payload.get("task") == "letter_classifier":
            return _letter_reading(payload["letter_text"])
        if not (isinstance(payload, dict) and payload.get("task") == "chat"):
            return {"text": "This is a mock response."}
        first = payload["sources"][0]
        if PROMISE.search(payload["question"]):
            return {
                "text": "No one can promise you will get money. You may qualify, "
                f"but FEMA decides. See: {first['title']}."
            }
        # Canned but grounded: quote the top source's first section body.
        body = re.sub(r"^## .*\n", "", first["content"]).strip().replace("\n", " ")
        return {"text": f"{first['title']}: {body[:400]}"}
