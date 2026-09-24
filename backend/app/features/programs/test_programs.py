import json
from pathlib import Path

import pytest
import yaml
from fastapi.testclient import TestClient
from jsonschema import Draft202012Validator, FormatChecker

from app.features.programs.service import build_program_cards
from app.main import create_app

ROOT = Path(__file__).resolve().parents[4]
RESPONSE_SCHEMA = json.loads(
    (ROOT / "contracts/schemas/programs.json").read_text(encoding="utf-8")
)
DATA_SCHEMA = json.loads(
    (ROOT / "contracts/schemas/programs_data.json").read_text(encoding="utf-8")
)


def _program_scenarios():
    cases = []
    for path in sorted((ROOT / "fixtures/scenarios").glob("S*.yaml")):
        scenario = yaml.safe_load(path.read_text(encoding="utf-8"))
        programs = scenario.get("expected", {}).get("programs")
        if programs:
            cases.append(pytest.param(scenario, programs, id=scenario["id"]))
    return cases


@pytest.mark.parametrize(("scenario", "expected_tiers"), _program_scenarios())
def test_program_cards_match_scenario_and_response_contract(scenario, expected_tiers):
    response = TestClient(create_app()).post(
        "/api/programs",
        json={
            "disaster_number": 4936,
            "county_fips": "15001",
            "lang": scenario["lang"],
            "answers": scenario["answers"],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    Draft202012Validator(RESPONSE_SCHEMA, format_checker=FormatChecker()).validate(
        payload
    )
    cards = {card["program_id"]: card for card in payload["cards"]}
    assert {program_id: card["tier"] for program_id, card in cards.items()} == (
        expected_tiers
    )
    assert all(
        card[field]
        for card in cards.values()
        for field in ("title", "why", "how_to_apply", "source_url", "last_verified")
    )
    assert cards["fema_ihp"]["deadline"] == {
        "date": "2026-11-01",
        "label": "Solicítelo antes del",
    }
    assert cards["irs_relief"]["deadline"] == {
        "date": "2027-02-01",
        "label": "Fecha límite",
    }
    assert all(
        card["deadline"] is None
        for program_id, card in cards.items()
        if program_id in {"dua", "dsnap", "sba_loan"}
    )
    copy = " ".join(
        card[field]
        for card in cards.values()
        for field in ("title", "why", "how_to_apply")
    ).lower()
    assert "you are eligible" not in copy
    assert "eres elegible" not in copy


def test_program_data_matches_contract_schema():
    data = json.loads((ROOT / "data/programs.json").read_text(encoding="utf-8"))

    Draft202012Validator(DATA_SCHEMA, format_checker=FormatChecker()).validate(data)


def test_dua_and_dsnap_cards_follow_their_triggers():
    answers = {
        "housing": "rent",
        "lost_work_or_self_employed": False,
        "on_snap": True,
        "household_size": 1,
    }
    response = TestClient(create_app()).post(
        "/api/programs",
        json={
            "disaster_number": 4936,
            "county_fips": "15001",
            "lang": "en",
            "answers": answers,
        },
    )

    assert response.status_code == 200
    assert {card["program_id"] for card in response.json()["cards"]} == {
        "fema_ihp",
        "irs_relief",
        "sba_loan",
    }


def test_unknown_or_closed_deadlines_are_not_fabricated():
    declaration = {
        "individual_assistance": True,
        "registration_open": False,
        "registration_deadline": None,
        "rules_regime": "pre-2024-03-22",
    }
    answers = {
        "housing": "rent",
        "lost_work_or_self_employed": True,
        "on_snap": False,
        "household_size": 1,
    }

    cards = {
        card["program_id"]: card
        for card in build_program_cards(4930, declaration, answers, "en")
    }

    assert cards["fema_ihp"]["tier"] == "check_now"
    assert cards["fema_ihp"]["deadline"] is None
    assert cards["irs_relief"]["deadline"] is None
    assert cards["dua"]["deadline"] is None
    assert cards["dsnap"]["deadline"] is None
    assert cards["sba_loan"]["tier"] == "check_now"


def test_non_ia_disaster_can_show_triggered_dua_and_sba_cards():
    response = TestClient(create_app()).post(
        "/api/programs",
        json={
            "disaster_number": 4930,
            "county_fips": "28031",
            "lang": "en",
            "answers": {
                "housing": "rent",
                "lost_work_or_self_employed": True,
                "on_snap": False,
                "household_size": 1,
            },
        },
    )

    assert response.status_code == 200
    cards = {card["program_id"]: card for card in response.json()["cards"]}
    assert set(cards) == {"dua", "sba_loan"}
    assert cards["dua"]["tier"] == "check_now"
    assert cards["sba_loan"]["tier"] == "optional"


def test_sba_copy_only_says_application_does_not_affect_fema_eligibility():
    declaration = {
        "individual_assistance": True,
        "registration_open": True,
        "registration_deadline": "2026-11-01",
        "rules_regime": "2024-03-22",
    }
    answers = {
        "housing": "rent",
        "lost_work_or_self_employed": False,
        "on_snap": False,
        "household_size": 1,
    }

    english = {
        card["program_id"]: card
        for card in build_program_cards(4936, declaration, answers, "en")
    }
    spanish = {
        card["program_id"]: card
        for card in build_program_cards(4936, declaration, answers, "es")
    }

    assert "Applying does not affect FEMA eligibility" in english["sba_loan"]["why"]
    assert (
        "no afecta su elegibilidad para la ayuda de FEMA" in spanish["sba_loan"]["why"]
    )


def test_invalid_program_request_is_rejected():
    response = TestClient(create_app()).post(
        "/api/programs",
        json={
            "disaster_number": True,
            "county_fips": "15001",
            "lang": "en",
            "answers": {
                "housing": "rent",
                "lost_work_or_self_employed": False,
                "on_snap": False,
                "household_size": 1,
            },
        },
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "invalid_input"
