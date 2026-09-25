import json
import os
from typing import Any

from app.adapters.base import NotConfigured, ServiceStatus
from app.adapters.model.base import ModelAdapter


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise NotConfigured(f"{name} is not set; model live adapter is not configured")
    return value


class Adapter(ModelAdapter):
    def health_status(self) -> ServiceStatus:
        _require("FOUNDRY_PROJECT_ENDPOINT")
        _require("FOUNDRY_MODEL")
        return "ok"

    async def run(self, payload: Any) -> Any:
        endpoint, model = (
            _require("FOUNDRY_PROJECT_ENDPOINT"),
            _require("FOUNDRY_MODEL"),
        )
        # Imported here only (decision 0002); mock mode never loads the framework.
        from agent_framework import Agent
        from agent_framework.foundry import FoundryChatClient
        from azure.identity import AzureCliCredential, ManagedIdentityCredential

        # ponytail: sources are retrieved before the call, so no tools yet.
        # Add declarations/checklist tools when P1-02/P1-07 land.
        credential = (
            ManagedIdentityCredential()
            if os.getenv("WEBSITE_SITE_NAME") or os.getenv("CONTAINER_APP_NAME")
            else AzureCliCredential()
        )
        client = FoundryChatClient(
            project_endpoint=endpoint, model=model, credential=credential
        )
        agent = Agent(client=client, name="Navigator", instructions=payload["rules"])
        if payload.get("task") == "letter_classifier":
            try:
                result = await agent.run(
                    json.dumps(
                        {
                            "lang": payload["lang"],
                            "allowed_reasons": payload["allowed_reasons"],
                            "untrusted_letter_text": payload["letter_text"],
                        },
                        ensure_ascii=False,
                    ),
                    options={"response_format": payload["response_format"]},
                )
            except Exception:  # noqa: BLE001 - SDK errors must not expose letter content.
                raise NotConfigured("Letter classification is unavailable") from None
            return result.value
        sources = "\n".join(
            f'<source n="{i}" title="{s["title"]}" url="{s["url"]}">{s["content"]}</source>'
            for i, s in enumerate(payload["sources"], 1)
        )
        result = await agent.run(
            f"Reply in English.\n{sources}\n<question>{payload['question']}</question>"
        )
        return {"text": result.text}
