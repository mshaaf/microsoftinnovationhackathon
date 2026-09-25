import sys
from types import ModuleType, SimpleNamespace

from fastapi.testclient import TestClient

from app.core import model_gateway
from app.main import app

client = TestClient(app)


def test_spanish_chat_translates_only_the_generated_reply(monkeypatch):
    from app.features.chat import service

    generated = "Common disaster-related rumors: FEMA never charges fees."
    translated = "Rumores comunes: FEMA nunca cobra tarifas."
    model_payloads = []
    translation_inputs = []

    class Search:
        def search(self, question, lang, top):
            return [
                {
                    "title": "Reviewed source",
                    "url": "https://example.gov/",
                    "content": "Reviewed Spanish data.",
                }
            ]

    class Translator:
        def translate(self, text):
            translation_inputs.append(text)
            return translated

    def adapter(name):
        return {"search": Search(), "translator": Translator()}[name]

    async def model(payload, mode=None):
        model_payloads.append(payload)
        return {"text": generated}

    monkeypatch.setattr(service, "get_adapter", adapter)
    monkeypatch.setattr(model_gateway, "run", model)

    reply = client.post(
        "/api/chat",
        json={
            "session_id": "s1",
            "message": "¿FEMA cobra tarifas?",
            "lang": "es",
            "context": {},
        },
    ).json()["reply"]

    assert model_payloads[0]["lang"] == "es"
    assert translation_inputs == [generated]
    assert reply == f"{translated} {service.DECISION_NOTE['es']}"


async def test_live_model_returns_english_for_spanish_translation(monkeypatch):
    from app.adapters.model.live import Adapter

    prompts = []

    class Credential:
        pass

    class Agent:
        def __init__(self, **kwargs):
            pass

        async def run(self, prompt):
            prompts.append(prompt)
            return SimpleNamespace(text="English generated reply")

    agent_framework = ModuleType("agent_framework")
    agent_framework.Agent = Agent
    foundry = ModuleType("agent_framework.foundry")
    foundry.FoundryChatClient = lambda **kwargs: object()
    identity = ModuleType("azure.identity")
    identity.AzureCliCredential = Credential
    identity.ManagedIdentityCredential = Credential
    monkeypatch.setitem(sys.modules, "agent_framework", agent_framework)
    monkeypatch.setitem(sys.modules, "agent_framework.foundry", foundry)
    monkeypatch.setitem(sys.modules, "azure.identity", identity)
    monkeypatch.setenv("FOUNDRY_PROJECT_ENDPOINT", "https://example.ai")
    monkeypatch.setenv("FOUNDRY_MODEL", "test-model")
    monkeypatch.delenv("CONTAINER_APP_NAME", raising=False)

    result = await Adapter().run(
        {
            "task": "chat",
            "lang": "es",
            "rules": "Answer safely.",
            "sources": [
                {"title": "Source", "url": "https://example.gov/", "content": "Facts."}
            ],
            "question": "¿Qué ayuda hay?",
        }
    )

    assert result == {"text": "English generated reply"}
    assert prompts[0].startswith("Reply in English.")
