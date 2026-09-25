from typing import TypedDict

from app.adapters.base import BaseAdapter, NotConfigured, ServiceStatus


class ShieldResult(TypedDict):
    user_prompt_attack: bool
    document_attacks: list[bool]


class SafetyAdapter(BaseAdapter):
    async def shield_prompt(
        self, user_prompt: str = "", documents: list[str] | None = None
    ) -> ShieldResult:
        raise NotImplementedError


SERVICE_NAME = "safety"

__all__ = [
    "SERVICE_NAME",
    "BaseAdapter",
    "NotConfigured",
    "SafetyAdapter",
    "ServiceStatus",
    "ShieldResult",
]
