import httpx
import pytest

from app.adapters.safety.live import Adapter


@pytest.mark.asyncio
async def test_prompt_shield_posts_user_text_and_redacted_documents(monkeypatch):
    requests = []

    def respond(request):
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "userPromptAnalysis": {"attackDetected": False},
                "documentsAnalysis": [{"attackDetected": True}],
            },
        )

    monkeypatch.setenv("AZURE_AI_SERVICES_ENDPOINT", "https://safety.example")
    monkeypatch.setenv("AZURE_AI_SERVICES_KEY", "test-key")
    client = httpx.AsyncClient(transport=httpx.MockTransport(respond))
    try:
        result = await Adapter(client=client).shield_prompt(
            user_prompt="How do I appeal?", documents=["redacted letter"]
        )
    finally:
        await client.aclose()

    assert result == {"user_prompt_attack": False, "document_attacks": [True]}
    assert str(requests[0].url) == (
        "https://safety.example/contentsafety/text:shieldPrompt?api-version=2024-09-01"
    )
    assert requests[0].headers["Ocp-Apim-Subscription-Key"] == "test-key"
    assert requests[0].read() == (
        b'{"userPrompt":"How do I appeal?","documents":["redacted letter"]}'
    )
