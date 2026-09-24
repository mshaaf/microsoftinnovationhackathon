import json

import httpx
import pytest

from app.adapters.base import NotConfigured
from app.adapters.pii.live import Adapter
from app.core import model_gateway
from app.core.model_gateway import PIILeakError


def test_live_adapter_uses_unicode_offsets_and_overlapping_chunks(monkeypatch):
    requests = []
    name = "María Samplewell"
    source = "🌀" * 5110 + name + " lives here"

    def respond(request):
        requests.append(request)
        body = json.loads(request.content)
        document = body["analysisInput"]["documents"][0]
        chunk = document["text"]
        entities = []
        offset = chunk.find(name)
        if offset >= 0:
            entities.append(
                {
                    "category": "Person",
                    "offset": offset,
                    "length": len(name),
                    "text": name,
                }
            )
        return httpx.Response(
            200,
            json={
                "results": {
                    "documents": [{"id": document["id"], "entities": entities}],
                    "errors": [],
                }
            },
        )

    monkeypatch.setenv(
        "AZURE_AI_SERVICES_ENDPOINT", "https://example.cognitiveservices.azure.com/"
    )
    monkeypatch.setenv("AZURE_AI_SERVICES_KEY", "test-key")
    client = httpx.Client(transport=httpx.MockTransport(respond))
    adapter = Adapter(client=client)
    try:
        entities = adapter.entities(source, language="es")
    finally:
        client.close()

    assert [(entity.category, entity.offset, entity.length) for entity in entities] == [
        ("Person", 5110, len(name))
    ]
    assert len(requests) == 2
    for request in requests:
        body = json.loads(request.content)
        assert request.url.path == "/language/:analyze-text"
        assert request.url.params["api-version"] == "2024-11-01"
        assert request.headers["Ocp-Apim-Subscription-Key"] == "test-key"
        assert body["kind"] == "PiiEntityRecognition"
        assert body["analysisInput"]["documents"][0]["language"] == "es"
        assert len(body["analysisInput"]["documents"][0]["text"]) <= 5120
        assert body["parameters"]["stringIndexType"] == "UnicodeCodePoint"
        assert "DateTime" not in body["parameters"].get("piiCategories", [])


def test_live_adapter_fails_closed_on_service_error(monkeypatch):
    def fail(_request):
        raise httpx.ConnectError("connection failed")

    monkeypatch.setenv(
        "AZURE_AI_SERVICES_ENDPOINT", "https://example.cognitiveservices.azure.com/"
    )
    monkeypatch.setenv("AZURE_AI_SERVICES_KEY", "test-key")
    client = httpx.Client(transport=httpx.MockTransport(fail))
    adapter = Adapter(client=client)
    try:
        with pytest.raises(NotConfigured, match="PII"):
            adapter.entities("private letter text")
    finally:
        client.close()


@pytest.mark.parametrize(
    "sensitive_text",
    ["FEMA registration 987654321", "Call 555-0199", "ZIP 12345-6789"],
)
def test_live_model_guard_applies_regex_backstop_when_azure_finds_nothing(
    monkeypatch, sensitive_text
):
    def respond(request):
        document = json.loads(request.content)["analysisInput"]["documents"][0]
        return httpx.Response(
            200,
            json={
                "results": {
                    "documents": [{"id": document["id"], "entities": []}],
                    "errors": [],
                }
            },
        )

    monkeypatch.setenv(
        "AZURE_AI_SERVICES_ENDPOINT", "https://example.cognitiveservices.azure.com/"
    )
    monkeypatch.setenv("AZURE_AI_SERVICES_KEY", "test-key")
    client = httpx.Client(transport=httpx.MockTransport(respond))
    adapter = Adapter(client=client)
    monkeypatch.setattr(model_gateway, "get_adapter", lambda *_args, **_kwargs: adapter)
    try:
        with pytest.raises(PIILeakError):
            model_gateway.guard({"letter_text": sensitive_text}, mode="live")
    finally:
        client.close()
