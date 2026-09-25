from typing import cast
from uuid import uuid4

from app.features.escalation.models import HandoffReason
from app.features.escalation.service import build_card, keyword_handoff

from .models import ChatResponse

PROMPT_INJECTION_REDIRECT = {
    "en": "I can help with disaster assistance questions. Please ask about FEMA or other help after a disaster.",
    "es": "Puedo ayudar con preguntas sobre asistencia por desastre. Pregunta sobre FEMA u otra ayuda después de un desastre.",
}


def handoff_response(reason: str, lang: str) -> ChatResponse:
    card = build_card(cast(HandoffReason, reason), lang)
    return ChatResponse(
        request_id=str(uuid4()),
        reply=card.steps[0],
        citations=[],
        handoff=reason,
    )


def keyword_response(message: str, lang: str) -> ChatResponse | None:
    reason = keyword_handoff(message)
    return handoff_response(reason, lang) if reason else None


def prompt_injection_response(lang: str) -> ChatResponse:
    return ChatResponse(
        request_id=str(uuid4()),
        reply=PROMPT_INJECTION_REDIRECT[lang],
        citations=[],
        handoff=None,
    )
