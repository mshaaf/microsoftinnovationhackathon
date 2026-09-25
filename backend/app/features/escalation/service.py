import json
from functools import lru_cache
from pathlib import Path

from .models import EscalationCard, HandoffReason

ROOT = Path(__file__).resolve().parents[4]
RULES_PATH = ROOT / "data/escalation_rules.json"
KEYWORD_REASONS: tuple[HandoffReason, ...] = ("emergency", "sensitive", "shelter")


@lru_cache(maxsize=1)
def _rules() -> dict:
    return json.loads(RULES_PATH.read_text(encoding="utf-8"))


def keyword_handoff(message: str) -> HandoffReason | None:
    normalized = message.casefold()
    if normalized.strip(" \t\r\n.!?") == "fire":
        return "emergency"
    # ponytail: phrase matching can miss paraphrases; expand only when scenario evals show gaps.
    for reason in KEYWORD_REASONS:
        if any(term in normalized for term in _rules()["triggers"][reason]):
            return reason
    return None


def build_card(reason: HandoffReason, lang: str = "en") -> EscalationCard:
    return EscalationCard.model_validate(_rules()["cards"][reason][lang])
