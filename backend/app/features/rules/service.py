import json
from datetime import date, timedelta
from functools import lru_cache
from pathlib import Path

RULES_PATH = Path(__file__).resolve().parents[4] / "data/ihp_rules.json"


@lru_cache(maxsize=1)
def _rules() -> dict:
    return json.loads(RULES_PATH.read_text(encoding="utf-8"))


def rules_for_declaration(declaration_date: date) -> dict:
    for regime in _rules()["regimes"]:
        if "declared_before" in regime:
            matches = declaration_date < date.fromisoformat(regime["declared_before"])
        else:
            matches = declaration_date >= date.fromisoformat(
                regime["declared_on_or_after"]
            )
        if not matches:
            continue

        serious_needs = regime["serious_needs"]
        result = {
            "rules_regime": regime["id"],
            "serious_needs": {"available": serious_needs["available"]},
        }
        if serious_needs["available"]:
            # The amount tier is based on the disaster's declaration date.
            source_url = next(
                source["url"]
                for source in _rules()["sources"]
                if source["fact"]
                == "Serious Needs Assistance application window and extension"
            )
            amount = max(
                (
                    item
                    for item in serious_needs["amounts"]
                    if date.fromisoformat(item["effective"]) <= declaration_date
                ),
                key=lambda item: item["effective"],
            )
            result["serious_needs"].update(
                {
                    "amount_usd": amount["amount_usd"],
                    "apply_by": (
                        declaration_date + timedelta(days=serious_needs["window_days"])
                    ).isoformat(),
                    "extension_possible": (
                        serious_needs["extension_max_days"]
                        > serious_needs["window_days"]
                    ),
                    "source_url": source_url,
                }
            )
        return result

    raise ValueError(f"no IHP rules regime for declaration date {declaration_date}")
