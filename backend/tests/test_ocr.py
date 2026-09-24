import tempfile
from pathlib import Path

import pytest
from azure.core.exceptions import HttpResponseError
from fastapi.testclient import TestClient

from app.adapters.ocr.base import OCRUnavailable, UnreadableLetter
from app.adapters.ocr.mock import Adapter as MockOCR
from app.main import create_app
from tests.contract.helpers import assert_matches_schema

FIXTURES = Path(__file__).resolve().parents[2] / "fixtures" / "letters"
PNG = (FIXTURES / "L01.png").read_bytes()
client = TestClient(create_app())


def upload(data=PNG, name="L01.png", kind="image/png"):
    return client.post(
        "/api/letter/decode",
        data={"lang": "en"},
        files={"file": (name, data, kind)},
    )


async def test_mock_matches_name_and_hash():
    text = (FIXTURES / "L01.txt").read_text()
    by_name = await MockOCR().read(PNG, "L01.png")
    by_hash = await MockOCR().read(PNG, "renamed.png")
    assert by_name.text == by_hash.text == text
    assert by_name.pages == 1 and by_name.confidence == 0.97


def test_incomplete_pipeline_does_not_send_upload_to_ocr(monkeypatch, caplog):
    from app.adapters.ocr import mock

    def fail_if_called(*args, **kwargs):
        raise AssertionError("OCR must wait until the decode pipeline is complete")

    monkeypatch.setattr(mock.Adapter, "read", fail_if_called)
    response = upload()
    assert response.status_code == 503
    assert_matches_schema(response, "error")
    assert response.json()["error"]["code"] == "dependency_unavailable"
    assert response.json()["error"]["message"] == (
        "Letter review cannot be completed right now. Try again later."
    )
    assert "Jordan Samplewell" not in response.text + caplog.text


@pytest.mark.parametrize(
    ("data", "kind"),
    [(b"\xff\xd8\xffexample", "image/jpeg"), (b"%PDF-1.7\nexample", "application/pdf")],
)
def test_accepted_file_types(data, kind):
    response = upload(data, "L01.png", kind)
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "dependency_unavailable"


def test_accepts_exactly_10_megabytes():
    data = PNG + b" " * (10 * 1024 * 1024 - len(PNG))
    response = upload(data)
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "dependency_unavailable"


@pytest.mark.parametrize(
    ("case", "name", "kind", "status", "code"),
    [
        ("large", "L01.png", "image/png", 413, "file_too_large"),
        ("fixture", "L01.png", "text/plain", 415, "unsupported_file"),
        ("fixture", "L01.pdf", "application/pdf", 415, "unsupported_file"),
        ("invalid", "L01.png", "image/png", 415, "unsupported_file"),
    ],
)
def test_rejects_size_and_type(case, name, kind, status, code):
    data = {
        "large": b"x" * (10 * 1024 * 1024 + 1),
        "fixture": PNG,
        "invalid": b"invalid",
    }[case]
    response = upload(data, name, kind)
    assert response.status_code == status
    assert_matches_schema(response, "error")
    assert response.json()["error"]["code"] == code


def test_upload_never_spools_to_temp_files(monkeypatch, tmp_path):
    monkeypatch.setattr(tempfile, "tempdir", str(tmp_path))
    assert upload(b"x" * (11 * 1024 * 1024)).status_code == 413
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize(
    ("status_code", "expected_error"),
    [(400, UnreadableLetter), (503, OCRUnavailable)],
)
async def test_azure_document_errors_are_not_reported_as_outages(
    monkeypatch, status_code, expected_error
):
    from app.adapters.ocr import live

    class Credential:
        async def close(self):
            pass

    class Client:
        def __init__(self, endpoint, credential):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def begin_analyze_document(self, *args):
            class Response:
                reason = "Bad Request"

                def __init__(self):
                    self.status_code = status_code

                def text(self):
                    return ""

            raise HttpResponseError(
                message="document request failed",
                response=Response(),
            )

    monkeypatch.setenv("AZURE_AI_SERVICES_ENDPOINT", "https://example.test")
    monkeypatch.delenv("AZURE_AI_SERVICES_KEY", raising=False)
    monkeypatch.delenv("CONTAINER_APP_NAME", raising=False)
    monkeypatch.setattr(live, "AzureCliCredential", Credential)
    monkeypatch.setattr(live, "DocumentIntelligenceClient", Client)

    with pytest.raises(expected_error):
        await live.Adapter().read(PNG, "L01.png")
