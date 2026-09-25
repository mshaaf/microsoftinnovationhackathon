import json
import sys
from types import ModuleType, SimpleNamespace

import pytest
from pydantic import BaseModel

from app.adapters.model.live import Adapter as LiveAdapter
from app.adapters.model.mock import Adapter as MockAdapter
from app.features.letter.classify_step import taxonomy_data


class Reading(BaseModel):
    decision_type: str
    assistance_types: list[str]
    reasons: list[dict]
    letter_date: str | None
    disaster_number: int | None


@pytest.mark.parametrize(
    ("letter_text", "reason_id", "decision_type"),
    [
        (
            "Could not verify your identity. Date: 2026-09-10",
            "identity_not_verified",
            "not_approved",
        ),
        ("Decision [UNREADABLE]. Date: 2024-04-15", "other_or_unclear", "unclear"),
        (
            "We need more information to confirm residence. Date: 2026-09-18",
            "occupancy_not_verified",
            "needs_information",
        ),
    ],
)
async def test_mock_classifier_returns_deterministic_structured_output(
    letter_text, reason_id, decision_type
):
    result = await MockAdapter().run(
        {
            "task": "letter_classifier",
            "letter_text": letter_text,
            "response_format": Reading,
        }
    )

    assert result == {
        "decision_type": decision_type,
        "assistance_types": [],
        "reasons": [
            {
                "taxonomy_id": reason_id,
                "confidence": 0.92 if reason_id != "other_or_unclear" else 0.2,
            }
        ],
        "letter_date": "2026-09-10"
        if "2026-09-10" in letter_text
        else ("2024-04-15" if "2024-04-15" in letter_text else "2026-09-18"),
        "disaster_number": None,
    }


async def test_live_classifier_requests_structured_output_and_returns_parsed_value(
    monkeypatch,
):
    calls = []
    allowed_reasons = [
        {"id": row["id"], "match_hints": row["match_hints"]}
        for row in taxonomy_data()["reasons"]
    ]

    class Agent:
        def __init__(self, **kwargs):
            self.instructions = kwargs["instructions"]

        async def run(self, text, *, options):
            calls.append((text, options, self.instructions))
            return SimpleNamespace(
                value=Reading(
                    decision_type="not_approved",
                    assistance_types=["rental"],
                    reasons=[
                        {"taxonomy_id": "insurance_docs_missing", "confidence": 0.9}
                    ],
                    letter_date="2026-09-15",
                    disaster_number=4936,
                )
            )

    framework = ModuleType("agent_framework")
    framework.Agent = Agent
    foundry = ModuleType("agent_framework.foundry")
    foundry.FoundryChatClient = lambda **kwargs: object()
    identity = ModuleType("azure.identity")
    identity.AzureCliCredential = lambda: object()
    identity.ManagedIdentityCredential = lambda: object()
    azure = ModuleType("azure")
    azure.identity = identity
    monkeypatch.setitem(sys.modules, "agent_framework", framework)
    monkeypatch.setitem(sys.modules, "agent_framework.foundry", foundry)
    monkeypatch.setitem(sys.modules, "azure", azure)
    monkeypatch.setitem(sys.modules, "azure.identity", identity)
    monkeypatch.setenv("FOUNDRY_PROJECT_ENDPOINT", "https://example.test/project")
    monkeypatch.setenv("FOUNDRY_MODEL", "mock-deployment")

    result = await LiveAdapter().run(
        {
            "task": "letter_classifier",
            "rules": "Return the structured letter fields.",
            "letter_text": "redacted letter text",
            "lang": "es",
            "allowed_reasons": allowed_reasons,
            "response_format": Reading,
        }
    )

    assert isinstance(result, Reading)
    assert json.loads(calls[0][0]) == {
        "lang": "es",
        "allowed_reasons": allowed_reasons,
        "untrusted_letter_text": "redacted letter text",
    }
    assert [row["id"] for row in json.loads(calls[0][0])["allowed_reasons"]] == [
        row["id"] for row in taxonomy_data()["reasons"]
    ]
    assert calls[0][1]["response_format"] is Reading


async def test_live_chat_carries_structured_handoff_to_gateway(monkeypatch):
    calls = []

    class Agent:
        def __init__(self, **kwargs):
            self.instructions = kwargs["instructions"]

        async def run(self, text, *, options):
            calls.append((text, options, self.instructions))
            return SimpleNamespace(
                value={"text": "Please get help now.", "handoff": "sensitive"}
            )

    framework = ModuleType("agent_framework")
    framework.Agent = Agent
    foundry = ModuleType("agent_framework.foundry")
    foundry.FoundryChatClient = lambda **kwargs: object()
    identity = ModuleType("azure.identity")
    identity.AzureCliCredential = lambda: object()
    identity.ManagedIdentityCredential = lambda: object()
    azure = ModuleType("azure")
    azure.identity = identity
    monkeypatch.setitem(sys.modules, "agent_framework", framework)
    monkeypatch.setitem(sys.modules, "agent_framework.foundry", foundry)
    monkeypatch.setitem(sys.modules, "azure", azure)
    monkeypatch.setitem(sys.modules, "azure.identity", identity)
    monkeypatch.setenv("FOUNDRY_PROJECT_ENDPOINT", "https://example.test/project")
    monkeypatch.setenv("FOUNDRY_MODEL", "mock-deployment")

    result = await LiveAdapter().run(
        {
            "task": "chat",
            "rules": "Answer from official sources.",
            "lang": "en",
            "question": "I'm afraid for my safety tonight",
            "sources": [
                {"title": "FEMA", "url": "https://www.fema.gov/", "content": "Help"}
            ],
        }
    )

    assert result == {"text": "Please get help now.", "handoff": "sensitive"}
    assert "handoff" in calls[0][1]["response_format"].model_fields
    assert "safety" in calls[0][2].lower()
