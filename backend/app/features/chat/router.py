from fastapi import APIRouter

from .models import ChatRequest, ChatResponse
from .service import answer

router = APIRouter()


@router.post("/chat")
async def chat(req: ChatRequest) -> ChatResponse:
    return await answer(req)
