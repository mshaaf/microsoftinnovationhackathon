from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

HandoffReason = Literal[
    "emergency", "shelter", "sensitive", "low_confidence", "user_request"
]


class EscalateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(min_length=1)
    reason: HandoffReason
    lang: Literal["en", "es"] = "en"


class Phone(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: str
    number: str


class EscalationCard(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    steps: list[str]
    phones: list[Phone]


class EscalateResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_id: str
    card: EscalationCard
