import json
from pathlib import Path

import pytest

from app.adapters.base import NotConfigured
from app.adapters.ocr.base import OCRResult
from app.adapters.pii.base import PiiAdapter, PiiEntity
from app.core import model_gateway
from app.features.letter import redact_step
from app.features.letter.service import redact_ocr_result

LETTERS = Path(__file__).resolve().parents[2] / "fixtures" / "letters"


@pytest.mark.parametrize("letter_id", [f"L0{i}" for i in range(1, 9)])
async def test_fixture_pii_is_redacted_before_model_and_not_logged(
    letter_id, monkeypatch, caplog
):
    expected = json.loads((LETTERS / f"{letter_id}.expected.json").read_text())
    source = (LETTERS / f"{letter_id}.txt").read_text()
    captured = []

    class Model:
        async def run(self, payload):
            captured.append(payload)
            return {"ok": True}

    adapter_factory = model_gateway.get_adapter

    def get_adapter(service, mode=None):
        return Model() if service == "model" else adapter_factory(service, mode)

    monkeypatch.setattr(model_gateway, "get_adapter", get_adapter)
    result = redact_step.redact(source, mode="mock")
    await model_gateway.run({"letter_text": result.redacted_text}, mode="mock")

    fields = result.response_fields()
    assert fields["redaction"]["entities_removed"] >= 4
    assert set(fields) == {"redaction", "redacted_preview"}
    assert {"Person", "Address", "PhoneNumber", "RegistrationNumber"} <= set(
        result.categories
    )
    assert "[PERSON]" in result.redacted_text
    assert "[ADDRESS]" in result.redacted_text
    for fake_value in expected["fake_pii"]:
        assert fake_value.casefold() not in result.redacted_text.casefold()
        assert fake_value.casefold() not in json.dumps(captured).casefold()
        assert fake_value.casefold() not in caplog.text.casefold()
        assert fake_value.casefold() not in fields["redacted_preview"].casefold()


def test_service_redacts_ocr_before_exposing_response_fields():
    result = redact_ocr_result(
        OCRResult("To: Jordan Samplewell, 18 Example Lane", 1, 0.98),
        language="en",
    )

    assert "Jordan Samplewell" not in result.redacted_text
    assert result.response_fields() == {
        "redaction": {"entities_removed": 2, "categories": ["Address", "Person"]},
        "redacted_preview": "To: [PERSON], [ADDRESS]",
    }


def test_regex_fallback_redacts_phone_zip_plus_four_and_id_number():
    result = redact_step.redact(
        "Contact 555-0199 at 12345-6789; FEMA number 987654321", mode="mock"
    )

    assert result.redacted_text == (
        "Contact [PHONE] at [ZIP_CODE]; FEMA number [ID_NUMBER]"
    )
    assert {"PhoneNumber", "ZipCode", "RegistrationNumber"} <= set(result.categories)


def test_mock_redaction_offsets_survive_casefold_expansion():
    result = redact_step.redact("Straße. Jordan Samplewell", mode="mock")

    assert "Jordan Samplewell" not in result.redacted_text
    assert "[PERSON]" in result.redacted_text


def test_mock_covers_the_r05_identity_categories():
    source = (
        "DOB: 04/05/1980; SSN: 123-45-6789; bank account number: 123456789012; "
        "credit card 4111111111111111; driver's license: D1234567; "
        "passport number: X1234567"
    )
    result = redact_step.redact(source, mode="mock")

    assert {
        "DateOfBirth",
        "USSocialSecurityNumber",
        "USBankAccountNumber",
        "CreditCardNumber",
        "USDriversLicenseNumber",
        "USUKPassportNumber",
    } <= set(result.categories)
    for value in (
        "04/05/1980",
        "123-45-6789",
        "123456789012",
        "4111111111111111",
        "D1234567",
        "X1234567",
    ):
        assert value not in result.redacted_text


def test_overlapping_entities_count_as_one_removed_span(monkeypatch):
    class OverlappingPii:
        def entities(self, text, language="en"):
            return (PiiEntity("Person", 0, 4), PiiEntity("Address", 0, 4))

    monkeypatch.setattr(
        redact_step, "get_adapter", lambda *_args, **_kwargs: OverlappingPii()
    )
    result = redact_step.redact("John", mode="mock")

    assert result.entities_removed == 1
    assert result.redacted_text == "[PERSONAL_DATA]"


def test_pii_detection_failure_stops_redaction(monkeypatch):
    class BrokenPii:
        def entities(self, text, language="en"):
            raise RuntimeError("failure containing raw letter text")

    monkeypatch.setattr(
        redact_step, "get_adapter", lambda *_args, **_kwargs: BrokenPii()
    )

    with pytest.raises(NotConfigured, match="PII detection is unavailable") as error:
        redact_step.redact("A letter that must not reach a model", mode="live")
    assert "raw letter text" not in str(error.value)


async def test_model_gateway_fails_closed_before_calling_model(monkeypatch):
    model_calls = []

    class BrokenPii:
        def detect(self, text):
            raise RuntimeError("failure containing raw model text")

    class Model:
        async def run(self, payload):
            model_calls.append(payload)

    monkeypatch.setattr(
        model_gateway,
        "get_adapter",
        lambda service, _mode=None: BrokenPii() if service == "pii" else Model(),
    )

    with pytest.raises(NotConfigured, match="PII detection is unavailable") as error:
        await model_gateway.run({"letter_text": "private"}, mode="live")
    assert "raw model text" not in str(error.value)
    assert model_calls == []


def test_model_gateway_passes_payload_language_to_pii_detection(monkeypatch):
    detected_languages = []

    class LanguagePii(PiiAdapter):
        def entities(self, text, language="en"):
            detected_languages.append(language)
            return ()

    monkeypatch.setattr(
        model_gateway, "get_adapter", lambda *_args, **_kwargs: LanguagePii()
    )

    model_gateway.guard({"lang": "es", "letter_text": "texto redactado"}, mode="live")

    assert detected_languages == ["es"]
