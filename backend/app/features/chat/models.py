from typing import Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str
    message: str = Field(min_length=1, max_length=2000)
    lang: Literal["en", "es"] = "en"
    context: dict = Field(default_factory=dict)


class Citation(BaseModel):
    title: str
    url: str


class ChatResponse(BaseModel):
    request_id: str
    reply: str
    citations: list[Citation]
    handoff: Literal["low_confidence", "user_request"] | None = None
