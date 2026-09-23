import json
from typing import Any

from app.adapters import get_adapter
from app.core.config import get_app_mode


class PIILeakError(ValueError):
    """Raised when a model payload contains personal information."""


def guard(payload: Any, mode: str | None = None) -> None:
    text = (
        payload
        if isinstance(payload, str)
        else json.dumps(payload, ensure_ascii=False, default=str)
    )
    detector = get_adapter("pii", mode or get_app_mode())
    if detector.detect(text):
        raise PIILeakError("Model payload contains personal information")


async def run(payload: Any, mode: str | None = None) -> Any:
    selected_mode = mode or get_app_mode()
    guard(payload, selected_mode)
    model = get_adapter("model", selected_mode)
    return await model.run(payload)
