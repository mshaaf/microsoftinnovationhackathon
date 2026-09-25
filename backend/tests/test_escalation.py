from fastapi.testclient import TestClient

from app.features.escalation.service import keyword_handoff
from app.main import create_app
from tests.contract.helpers import assert_matches_schema

client = TestClient(create_app())


def _escalate(reason, lang="en"):
    return client.post(
        "/api/escalate",
        json={"session_id": "test-session", "reason": reason, "lang": lang},
    )


def test_emergency_card_matches_contract_and_lists_911_first():
    response = _escalate("emergency")

    assert response.status_code == 200
    assert_matches_schema(response, "escalate")
    assert response.json()["card"]["phones"][0]["number"] == "911"


def test_sensitive_card_uses_verified_crisis_lines():
    response = _escalate("sensitive")

    assert response.status_code == 200
    assert_matches_schema(response, "escalate")
    numbers = {phone["number"] for phone in response.json()["card"]["phones"]}
    assert {"1-800-985-5990", "988", "1-800-799-7233"} <= numbers


def test_fire_insurance_and_firing_are_not_immediate_danger():
    assert keyword_handoff("I need fire insurance after I was fired") is None
    assert keyword_handoff("My house is on fire") == "emergency"
    assert keyword_handoff("Fire!") == "emergency"
