import json
from datetime import date
from functools import lru_cache
from pathlib import Path

from app.adapters import get_adapter
from app.adapters.openfema.base import OpenFEMAUnavailable
from app.features.rules.service import rules_for_declaration

ROOT = Path(__file__).resolve().parents[4]
ITEMS_PATH = ROOT / "data/checklist_items.json"


@lru_cache(maxsize=1)
def _items() -> dict[str, dict]:
    rows = json.loads(ITEMS_PATH.read_text(encoding="utf-8"))["items"]
    return {row["id"]: row for row in rows}


def _declaration_date(disaster_number: int) -> date:
    row = get_adapter("openfema").declaration_by_number(disaster_number)
    if row is None:
        raise LookupError(f"disaster {disaster_number} was not found")
    try:
        return date.fromisoformat(row["declarationDate"][:10])
    except (KeyError, TypeError, ValueError) as error:
        raise OpenFEMAUnavailable("Declaration date was unavailable") from error


def build_checklist(disaster_number: int, lang: str, answers: dict) -> dict:
    regime = rules_for_declaration(_declaration_date(disaster_number))["rules_regime"]
    ids = [
        "proof_of_ownership" if answers["housing"] == "own" else "proof_of_occupancy"
    ]
    if answers["insured"] != "no":
        ids.append("insurance_decision_letter")
    if answers["lost_id"]:
        ids.append("identity_document")
    if answers["displaced"]:
        ids.append("temporary_housing_information")
    if regime == "pre-2024-03-22":
        ids.append("sba_application")

    items = _items()
    return {
        "rules_regime": regime,
        "items": [
            {
                "id": item_id,
                "text": items[item_id]["text"][lang],
                "why": items[item_id]["why"][lang],
                "source_url": items[item_id]["source_url"],
            }
            for item_id in ids
        ],
    }
