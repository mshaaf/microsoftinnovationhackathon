import json
from datetime import date
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from jsonschema import Draft202012Validator, FormatChecker

from app.core.clock import use_today
from app.main import app

ROOT = Path(__file__).resolve().parents[4]
RULES_FILE = ROOT / "data/ihp_rules.json"
RULES_SCHEMA = json.loads(
    (ROOT / "contracts/schemas/ihp_rules.json").read_text(encoding="utf-8")
)
DECLARATIONS_SCHEMA = json.loads(
    (ROOT / "contracts/schemas/declarations.json").read_text(encoding="utf-8")
)
client = TestClient(app)


def rules_for(declared_on: str):
    from app.features.rules.service import rules_for_declaration

    return rules_for_declaration(date.fromisoformat(declared_on))


@pytest.mark.parametrize(
    ("declared_on", "regime", "available", "amount"),
    [
        ("2024-03-21", "pre-2024-03-22", False, None),
        ("2024-03-22", "2024-03-22", True, 750),
        ("2024-09-30", "2024-03-22", True, 750),
        ("2024-10-01", "2024-03-22", True, 770),
    ],
)
def test_regime_and_amount_use_declaration_date(declared_on, regime, available, amount):
    result = rules_for(declared_on)

    assert result["rules_regime"] == regime
    assert result["serious_needs"]["available"] is available
    assert result["serious_needs"].get("amount_usd") == amount


@pytest.mark.parametrize(
    ("declared_on", "apply_by"),
    [
        ("2024-03-31", "2024-04-30"),
        ("2024-08-31", "2024-09-30"),
        ("2028-02-29", "2028-03-30"),
    ],
)
def test_thirty_day_window_handles_month_end_and_leap_day(declared_on, apply_by):
    assert rules_for(declared_on)["serious_needs"]["apply_by"] == apply_by


def test_rules_file_matches_contract_and_has_source_for_every_fact():
    rules = json.loads(RULES_FILE.read_text(encoding="utf-8"))
    Draft202012Validator(RULES_SCHEMA, format_checker=FormatChecker()).validate(rules)

    facts = {source["fact"] for source in rules["sources"]}
    assert {
        "Individual Assistance reform effective date and requirements",
        "Appeal period and signing requirements",
        "Serious Needs Assistance amount for declarations through 2024-09-30",
        "Serious Needs Assistance amount for declarations on or after 2024-10-01",
        "Serious Needs Assistance application window and extension",
    } <= facts
    assert all(source["url"] for source in rules["sources"])
    assert "VERIFY" not in json.dumps(rules)


def test_declarations_route_attaches_sna_rules_and_matches_contract():
    with use_today(date(2026, 9, 23)):
        response = client.get("/api/declarations?state=HI&county_fips=15001")

    assert response.status_code == 200
    body = response.json()
    declaration = body["declarations"][0]
    assert declaration["rules_regime"] == "2024-03-22"
    assert declaration["serious_needs"] == {
        "available": True,
        "amount_usd": 770,
        "apply_by": "2026-10-01",
        "extension_possible": True,
        "source_url": "https://www.fema.gov/fact-sheet/serious-needs-assistance-0",
    }
    Draft202012Validator(DECLARATIONS_SCHEMA, format_checker=FormatChecker()).validate(
        body
    )
