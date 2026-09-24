import json
from pathlib import Path

import pytest
import yaml
from fastapi.testclient import TestClient
from jsonschema import Draft202012Validator, FormatChecker

from app.main import create_app

ROOT = Path(__file__).resolve().parents[4]
SCHEMA = json.loads(
    (ROOT / "contracts/schemas/checklist.json").read_text(encoding="utf-8")
)


def _scenario_cases():
    cases = []
    for path in sorted((ROOT / "fixtures/scenarios").glob("S*.yaml")):
        scenario = yaml.safe_load(path.read_text(encoding="utf-8"))
        answers = {
            key: scenario["answers"][key]
            for key in ("housing", "insured", "lost_id", "displaced")
        }
        cases.append(pytest.param(scenario["lang"], answers, id=scenario["id"]))
    return cases


def _expected_ids(answers):
    expected = {
        "proof_of_ownership" if answers["housing"] == "own" else "proof_of_occupancy"
    }
    if answers["insured"] != "no":
        expected.add("insurance_decision_letter")
    if answers["lost_id"]:
        expected.add("identity_document")
    if answers["displaced"]:
        expected.add("temporary_housing_information")
    return expected


@pytest.mark.parametrize(("lang", "answers"), _scenario_cases())
def test_scenario_answer_combinations_return_expected_items(lang, answers):
    response = TestClient(create_app()).post(
        "/api/checklist",
        json={"disaster_number": 4936, "lang": lang, "answers": answers},
    )

    assert response.status_code == 200
    assert {item["id"] for item in response.json()["items"]} == _expected_ids(answers)


def test_checklist_response_matches_contract_and_localizes_items():
    client = TestClient(create_app())
    request = {
        "disaster_number": 4936,
        "lang": "en",
        "answers": {
            "housing": "rent",
            "insured": "not_sure",
            "lost_id": True,
            "displaced": True,
        },
    }

    english = client.post("/api/checklist", json=request)
    spanish = client.post("/api/checklist", json={**request, "lang": "es"})

    assert english.status_code == spanish.status_code == 200
    Draft202012Validator(SCHEMA, format_checker=FormatChecker()).validate(
        english.json()
    )
    assert [item["id"] for item in english.json()["items"]] == [
        item["id"] for item in spanish.json()["items"]
    ]
    assert [item["text"] for item in english.json()["items"]] != [
        item["text"] for item in spanish.json()["items"]
    ]


def test_sba_item_only_appears_for_pre_reform_declarations():
    client = TestClient(create_app())
    answers = {
        "housing": "rent",
        "insured": "no",
        "lost_id": False,
        "displaced": False,
    }

    before = client.post(
        "/api/checklist",
        json={"disaster_number": 9999, "lang": "en", "answers": answers},
    ).json()
    after = client.post(
        "/api/checklist",
        json={"disaster_number": 4936, "lang": "en", "answers": answers},
    ).json()

    assert before["rules_regime"] == "pre-2024-03-22"
    assert "sba_application" in {item["id"] for item in before["items"]}
    assert after["rules_regime"] == "2024-03-22"
    assert "sba_application" not in {item["id"] for item in after["items"]}


@pytest.mark.parametrize(
    "change",
    [
        {"disaster_number": 0},
        {"lang": "fr"},
        {
            "answers": {
                "housing": "camp",
                "insured": "no",
                "lost_id": False,
                "displaced": False,
            }
        },
    ],
)
def test_invalid_input_is_rejected(change):
    request = {
        "disaster_number": 4936,
        "lang": "en",
        "answers": {
            "housing": "rent",
            "insured": "no",
            "lost_id": False,
            "displaced": False,
        },
    }
    request.update(change)

    response = TestClient(create_app()).post("/api/checklist", json=request)

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "invalid_input"
