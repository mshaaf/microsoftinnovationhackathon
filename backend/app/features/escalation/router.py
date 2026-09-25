from uuid import uuid4

from fastapi import APIRouter

from .models import EscalateRequest, EscalateResponse
from .service import build_card

router = APIRouter()


@router.post("/escalate", response_model=EscalateResponse)
async def escalate(req: EscalateRequest) -> EscalateResponse:
    return EscalateResponse(
        request_id=str(uuid4()), card=build_card(req.reason, req.lang)
    )
