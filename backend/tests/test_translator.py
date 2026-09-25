import json

import httpx

from app.adapters import get_adapter
from app.adapters.translator.live import Adapter as LiveTranslator

ENGLISH_REPLY = "Common disaster-related rumors: FEMA never charges fees."
SPANISH_REPLY = "Rumores comunes: FEMA nunca cobra tarifas."


def test_mock_translator_uses_reviewed_translation_fixture():
    assert get_adapter("translator", "mock").translate(ENGLISH_REPLY) == SPANISH_REPLY


def test_mock_translator_marks_an_unseeded_translation():
    assert get_adapter("translator", "mock").translate("New model reply.") == (
        "[es] New model reply."
    )


def test_live_translator_sends_glossary_and_region(monkeypatch):
    monkeypatch.setenv("AZURE_AI_SERVICES_KEY", "test-key")
    monkeypatch.setenv("AZURE_AI_SERVICES_REGION", "eastus2")
    requests = []

    def respond(request):
        requests.append(request)
        return httpx.Response(200, json=[{"translations": [{"text": "Traducido"}]}])

    with httpx.Client(transport=httpx.MockTransport(respond)) as client:
        translated = LiveTranslator(client).translate(
            "FEMA Individual Assistance: Serious Needs Assistance, Disaster Recovery Center, appeal."
        )

    request = requests[0]
    text = json.loads(request.content)[0]["Text"]
    assert translated == "Traducido"
    assert request.url.path == "/translate"
    assert request.url.params["api-version"] == "3.0"
    assert request.url.params["from"] == "en" and request.url.params["to"] == "es"
    assert request.headers["Ocp-Apim-Subscription-Region"] == "eastus2"
    for term in (
        'translation="Asistencia Individual">Individual Assistance',
        'translation="Asistencia por Necesidades Graves">Serious Needs Assistance',
        'translation="Centro de Recuperación por Desastre">Disaster Recovery Center',
        'translation="apelación">appeal',
    ):
        assert term in text
