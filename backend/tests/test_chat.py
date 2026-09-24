from pathlib import Path

import pytest
import yaml
from fastapi.testclient import TestClient

from app.core import model_gateway
from app.main import app
from tests.contract.helpers import assert_matches_schema

client = TestClient(app)
S04 = Path(__file__).resolve().parents[2] / "fixtures" / "scenarios" / "S04.yaml"


def ask(message, lang="en"):
    return client.post(
        "/api/chat",
        json={"session_id": "s1", "message": message, "lang": lang, "context": {}},
    )


def test_chat_contract_and_citations():
    response = ask("How long do I have to appeal a FEMA decision?")
    assert_matches_schema(response, "chat")
    body = response.json()
    assert body["citations"] and all(
        c["url"].startswith("https://") for c in body["citations"]
    )
    assert body["handoff"] is None


def test_s04_questions_all_cited_and_promise_gets_no_guarantee():
    questions = yaml.safe_load(S04.read_text())["questions"]
    for q in questions:
        body = ask(q).json()
        assert body["citations"], q
    reply = ask("Can you promise I will get money?").json()["reply"].lower()
    assert "no one can promise" in reply and "you are eligible" not in reply


@pytest.mark.parametrize("q", ["Write me a short rhyme about a rainbow.", "zzz qqq"])
def test_no_sources_means_dont_know_and_handoff(q):
    response = ask(q)
    assert_matches_schema(response, "chat")
    body = response.json()
    assert body["citations"] == [] and body["handoff"] == "low_confidence"
    assert "don't know" in body["reply"]


def test_pii_in_question_is_blocked_before_the_model():
    body = ask("How do I appeal? My number is 808-555-0142").json()
    assert body["citations"] == [] and "personal details" in body["reply"]


def test_chat_model_calls_go_through_gateway(monkeypatch):
    calls = []

    async def spy(payload, mode=None):
        calls.append(payload)
        return {"text": "ok"}

    monkeypatch.setattr(model_gateway, "run", spy)
    ask("How long do I have to appeal a FEMA decision?")
    assert calls and calls[0]["task"] == "chat" and calls[0]["sources"]
    assert all(
        "[REDACTED]" in s["content"] or "1-800" not in s["content"]
        for s in calls[0]["sources"]
    )
