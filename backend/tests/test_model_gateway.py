import pytest

from app.adapters.base import NotConfigured
from app.core import model_gateway, pii


def test_mock_guard_blocks_a_seeded_fixture_pii_string(tmp_path, monkeypatch):
    (tmp_path / "L01.expected.json").write_text(
        '{"fake_pii": ["Jordan Samplewell"]}', encoding="utf-8"
    )
    monkeypatch.setattr(pii, "FIXTURE_LETTERS_DIR", tmp_path, raising=False)
    pii.fixture_fake_pii.cache_clear()

    try:
        with pytest.raises(model_gateway.PIILeakError):
            model_gateway.guard(
                {"letter_text": "Letter for Jordan Samplewell"}, mode="mock"
            )
    finally:
        pii.fixture_fake_pii.cache_clear()


def test_live_guard_blocks_pii_reported_by_the_detector(monkeypatch):
    class PiiDetector:
        def detect(self, text):
            return ("Person",)

    monkeypatch.setattr(
        model_gateway, "get_adapter", lambda service, mode=None: PiiDetector()
    )

    with pytest.raises(model_gateway.PIILeakError):
        model_gateway.guard({"prompt": "redacted text"}, mode="live")


def test_live_guard_fails_closed_when_detector_is_not_configured(monkeypatch):
    def no_detector(service, mode=None):
        raise NotConfigured("PII detection is not configured")

    monkeypatch.setattr(model_gateway, "get_adapter", no_detector)

    with pytest.raises(NotConfigured):
        model_gateway.guard({"prompt": "text"}, mode="live")
