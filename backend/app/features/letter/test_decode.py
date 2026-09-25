import json
from datetime import date, timedelta
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.adapters.openfema.mock import Adapter as MockOpenFEMA
from app.core import model_gateway
from app.features.letter.service import _deadline_regime
from app.main import create_app
from tests.contract.helpers import assert_matches_schema

ROOT = Path(__file__).resolve().parents[4]
LETTERS = ROOT / "fixtures" / "letters"
client = TestClient(create_app())


def _upload(letter_id: str, lang: str = "en"):
    path = LETTERS / f"{letter_id}.png"
    return client.post(
        "/api/letter/decode",
        data={"lang": lang},
        files={"file": (path.name, path.read_bytes(), "image/png")},
    )


@pytest.mark.parametrize("letter_id", [f"L{i:02d}" for i in range(1, 9)])
def test_decode_returns_frozen_contract_without_fixture_pii(
    letter_id, caplog, monkeypatch
):
    expected = json.loads((LETTERS / f"{letter_id}.expected.json").read_text())
    original_get_adapter = model_gateway.get_adapter
    payloads = []

    def get_adapter(service, mode=None):
        adapter = original_get_adapter(service, mode)
        if service != "model":
            return adapter

        class CapturingModel:
            async def run(self, payload):
                payloads.append(payload)
                return await adapter.run(payload)

        return CapturingModel()

    monkeypatch.setattr(model_gateway, "get_adapter", get_adapter)
    response = _upload(letter_id)

    assert response.status_code == 200, response.text
    assert_matches_schema(response, "letter-decode")
    result = response.json()
    assert result["decision"]["type"] == expected["decision_type"]
    assert result["decision"]["letter_date"] == expected["letter_date"]
    assert result["decision"]["disaster_number"] == expected["disaster_number"]
    assert [reason["taxonomy_id"] for reason in result["reasons"]] == expected[
        "reasons"
    ]
    assert (
        result["deadline"]["appeal_due"]
        == (
            date.fromisoformat(expected["letter_date"]) + timedelta(days=60)
        ).isoformat()
    )
    assert result["decision"]["disaster_number_verified"] is (
        expected["disaster_number"] == 4936
    )
    assert (result["handoff"] == "low_confidence") is (letter_id == "L07")
    exposed = json.dumps(result) + json.dumps(payloads, default=str) + caplog.text
    assert all(
        value.casefold() not in exposed.casefold() for value in expected["fake_pii"]
    )
    if letter_id == "L08":
        assert "prompt_injection_detected" in caplog.text
        assert "Ignore all previous instructions" not in caplog.text


def test_decode_derives_checklist_and_explanation_from_spanish_taxonomy():
    result = _upload("L03", lang="es").json()

    assert "aseguradora" in result["explanation"].casefold()
    assert result["checklist"] == [
        {
            "id": "insurance_decision_letter",
            "text": "La carta de pago o rechazo de su aseguradora. Si no cubrió su pérdida, incluya prueba de los gastos pendientes.",
            "source_url": "https://www.fema.gov/fact-sheet/understanding-fema-decision-letter",
        }
    ]


def test_synthetic_disaster_is_unverified_but_still_selects_its_deadline_regime():
    declaration = MockOpenFEMA().declaration_by_number(9999)
    result = _upload("L07").json()

    assert declaration["hash"].startswith("synthetic-")
    assert _deadline_regime(declaration)["id"] == "pre-2024-03-22"
    assert result["decision"]["disaster_number_verified"] is False
    assert result["handoff"] == "low_confidence"


def test_unknown_disaster_is_unverified_and_hands_off_with_valid_deadline(monkeypatch):
    disaster_number = 987654
    assert MockOpenFEMA().declaration_by_number(disaster_number) is None
    original_get_adapter = model_gateway.get_adapter

    class UnknownDisasterModel:
        async def run(self, payload):
            return {
                "decision_type": "not_approved",
                "assistance_types": ["rental"],
                "reasons": [
                    {"taxonomy_id": "insurance_docs_missing", "confidence": 0.9}
                ],
                "letter_date": "2026-09-15",
                "disaster_number": disaster_number,
            }

    monkeypatch.setattr(
        model_gateway,
        "get_adapter",
        lambda service, mode=None: (
            UnknownDisasterModel()
            if service == "model"
            else original_get_adapter(service, mode)
        ),
    )

    response = _upload("L03")

    assert response.status_code == 200, response.text
    result = response.json()
    assert result["decision"]["disaster_number"] == disaster_number
    assert result["decision"]["disaster_number_verified"] is False
    assert result["reasons"][0]["confidence"] == 0.9
    assert result["handoff"] == "low_confidence"
    assert result["deadline"]["appeal_due"] == "2026-11-14"


def test_invalid_model_date_returns_unreadable_letter(monkeypatch):
    original_get_adapter = model_gateway.get_adapter

    class InvalidDateModel:
        async def run(self, payload):
            return {
                "decision_type": "not_approved",
                "assistance_types": ["rental"],
                "reasons": [
                    {"taxonomy_id": "insurance_docs_missing", "confidence": 0.9}
                ],
                "letter_date": "2026-02-30",
                "disaster_number": 4936,
            }

    monkeypatch.setattr(
        model_gateway,
        "get_adapter",
        lambda service, mode=None: (
            InvalidDateModel()
            if service == "model"
            else original_get_adapter(service, mode)
        ),
    )

    response = _upload("L03")

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "unreadable_letter"


@pytest.mark.parametrize(
    ("confidence", "expected_handoff"), [(0.2, "low_confidence"), (0.6, None)]
)
def test_reason_confidence_threshold_controls_handoff(
    confidence, expected_handoff, monkeypatch
):
    original_get_adapter = model_gateway.get_adapter

    class LowConfidenceModel:
        async def run(self, payload):
            return {
                "decision_type": "not_approved",
                "assistance_types": [],
                "reasons": [
                    {
                        "taxonomy_id": "insurance_docs_missing",
                        "confidence": confidence,
                    }
                ],
                "letter_date": "2026-09-15",
                "disaster_number": 4936,
            }

    monkeypatch.setattr(
        model_gateway,
        "get_adapter",
        lambda service, mode=None: (
            LowConfidenceModel()
            if service == "model"
            else original_get_adapter(service, mode)
        ),
    )

    result = _upload("L03").json()

    assert result["handoff"] == expected_handoff
    assert result["reasons"][0]["confidence"] == confidence
