from fastapi.testclient import TestClient

from app.main import app

SERVICE_NAMES = {
    "openfema",
    "geo",
    "search",
    "model",
    "ocr",
    "pii",
    "translator",
    "safety",
}
CONTRACT_STATUSES = {"ok", "mock", "down", "not_configured"}


def test_health_matches_contract_in_mock_mode(monkeypatch):
    monkeypatch.delenv("APP_MODE", raising=False)

    response = TestClient(app).get("/api/health")

    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"request_id", "mode", "version", "services"}
    assert body["request_id"]
    assert body["mode"] == "mock"
    assert body["version"] == "0.1.0"
    assert set(body["services"]) == SERVICE_NAMES
    assert set(body["services"].values()) == {"mock"}


def test_health_reports_unconfigured_services_in_live_mode(monkeypatch):
    monkeypatch.setenv("APP_MODE", "live")
    for key in (
        "FOUNDRY_PROJECT_ENDPOINT",
        "FOUNDRY_MODEL",
        "AZURE_AI_SERVICES_ENDPOINT",
        "AZURE_AI_SERVICES_KEY",
        "AZURE_AI_SERVICES_REGION",
        "AZURE_SEARCH_ENDPOINT",
        "AZURE_SEARCH_KEY",
    ):
        monkeypatch.delenv(key, raising=False)

    response = TestClient(app).get("/api/health")

    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "live"
    assert set(body["services"]) == SERVICE_NAMES
    assert set(body["services"].values()) == {"not_configured"}
    assert set(body["services"].values()) <= CONTRACT_STATUSES
