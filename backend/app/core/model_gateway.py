import json
from typing import Any

from app.adapters import get_adapter
from app.adapters.base import NotConfigured
from app.core.config import get_app_mode


class PIILeakError(ValueError):
    """Raised when a model payload contains personal information."""


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


async def run(payload: Any, mode: str | None = None) -> Any:
    selected_mode = mode or get_app_mode()
    guard(payload, selected_mode)
    model = get_adapter("model", selected_mode)
    return await model.run(payload)
