import json
import logging
from typing import Any

from app.adapters import get_adapter
from app.adapters.base import NotConfigured
from app.core.config import get_app_mode

logger = logging.getLogger(__name__)


class PIILeakError(ValueError):
    """Raised when a model payload contains personal information."""


class PromptInjectionDetected(ValueError):
    """Raised when user text is flagged as a prompt injection."""


class ModelHandoffDetected(ValueError):
    """Raised when the chat model requests a supported human handoff."""

    def __init__(self, reason: str):
        self.reason = reason
        super().__init__("Model requested a handoff")


def guard(payload: Any, mode: str | None = None) -> None:
    text = (
        payload
        if isinstance(payload, str)
        else json.dumps(payload, ensure_ascii=False, default=str)
    )
    language = payload.get("lang", "en") if isinstance(payload, dict) else "en"
    try:
        detector = get_adapter("pii", mode or get_app_mode())
        categories = (
            detector.detect(text, language=language)
            if language == "es"
            else detector.detect(text)
        )
    # Any detector failure must stop the model call without exposing its details.
    except Exception as error:
        if isinstance(error, NotConfigured):
            raise
        raise NotConfigured("PII detection is unavailable") from None
    if categories:
        raise PIILeakError("Model payload contains personal information")


async def shield_chat_input(question: str, mode: str) -> None:
    result = await get_adapter("safety", mode).shield_prompt(question, [])
    if result["user_prompt_attack"]:
        logger.warning(
            "prompt_injection_detected",
            extra={"category": "prompt_injection_detected"},
        )
        raise PromptInjectionDetected("Prompt injection detected")


async def run(payload: Any, mode: str | None = None) -> Any:
    selected_mode = mode or get_app_mode()
    guard(payload, selected_mode)
    task = payload.get("task") if isinstance(payload, dict) else None
    if task == "chat":
        await shield_chat_input(payload.get("question", ""), selected_mode)
    elif task == "letter_classifier":
        result = await get_adapter("safety", selected_mode).shield_prompt(
            "", [payload.get("letter_text", "")]
        )
        if result["user_prompt_attack"]:
            logger.warning(
                "prompt_injection_detected",
                extra={"category": "prompt_injection_detected"},
            )
        if any(result["document_attacks"]):
            logger.warning(
                "prompt_injection_detected",
                extra={"category": "prompt_injection_detected"},
            )
    model = get_adapter("model", selected_mode)
    result = await model.run(payload)
    if (
        task == "chat"
        and isinstance(result, dict)
        and result.get("handoff")
        in {"emergency", "shelter", "sensitive", "low_confidence", "user_request"}
    ):
        raise ModelHandoffDetected(result["handoff"])
    return result
