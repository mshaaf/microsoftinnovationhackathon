import re
from typing import Any

from app.adapters.base import ServiceStatus
from app.adapters.model.base import ModelAdapter

PROMISE = re.compile(
    r"\b(promise|guarantee|guaranteed|definitely|for sure)\b", re.IGNORECASE
)


class Adapter(ModelAdapter):
    def health_status(self) -> ServiceStatus:
        return "mock"

    async def run(self, payload: Any) -> dict[str, str]:
        if not (isinstance(payload, dict) and payload.get("task") == "chat"):
            return {"text": "This is a mock response."}
        first = payload["sources"][0]
        if PROMISE.search(payload["question"]):
            return {
                "text": "No one can promise you will get money. You may qualify, "
                f"but FEMA decides. See: {first['title']}."
            }
        # Canned but grounded: quote the top source's first section body.
        body = re.sub(r"^## .*\n", "", first["content"]).strip().replace("\n", " ")
        return {"text": f"{first['title']}: {body[:400]}"}
