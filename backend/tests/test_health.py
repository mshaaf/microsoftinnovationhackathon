from fastapi.testclient import TestClient

from app.main import app


def test_health_returns_mock_service_statuses():
    response = TestClient(app).get("/api/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["mode"] == "mock"
    assert payload["version"] == "0.1.0"
    assert payload["request_id"]
    assert payload["services"] == {
        "openfema": "mock",
        "geo": "ok",
        "search": "mock",
        "model": "mock",
        "ocr": "mock",
        "pii": "mock",
        "translator": "mock",
        "safety": "mock",
    }


def test_p0_02_ci_failure_proof():
    assert False, "intentional failure to verify CI blocks a PR"
