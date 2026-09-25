import re

from app.adapters.base import ServiceStatus
from app.adapters.safety.base import SafetyAdapter, ShieldResult

INJECTION_MARKER = re.compile(
    r"IGNORE(?:\s+ALL)?\s+PREVIOUS INSTRUCTIONS|\[\[INJECT\]\]", re.IGNORECASE
)


class Adapter(SafetyAdapter):
    def health_status(self) -> ServiceStatus:
        return "mock"

    async def shield_prompt(
        self, user_prompt: str = "", documents: list[str] | None = None
    ) -> ShieldResult:
        return {
            "user_prompt_attack": bool(INJECTION_MARKER.search(user_prompt)),
            "document_attacks": [
                bool(INJECTION_MARKER.search(document))
                for document in (documents or [])
            ],
        }
