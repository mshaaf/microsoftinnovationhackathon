from fastapi import APIRouter

from app.core import model_gateway

from .models import ChatRequest, ChatResponse
from .safety import handoff_response, keyword_response, prompt_injection_response
from .service import answer

router = APIRouter()


@router.post("/chat")
async def chat(req: ChatRequest) -> ChatResponse:
    early = keyword_response(req.message, req.lang)
    if early:
        return early
    try:
        return await answer(req)
    except model_gateway.PromptInjectionDetected:
        return prompt_injection_response(req.lang)
    except model_gateway.ModelHandoffDetected as handoff:
        return handoff_response(handoff.reason, req.lang)
