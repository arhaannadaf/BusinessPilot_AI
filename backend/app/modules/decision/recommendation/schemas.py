from datetime import datetime
from uuid import UUID
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

class RecommendationCreate(BaseModel):
    decision_id: UUID
    recommended_option_id: UUID

    status: Literal[
    "PROPOSED",
    "APPROVED",
    "REJECTED",
    "EXECUTED",
    ] | None = None

    rationale: str = Field(
        ...,
        min_length=50,
    )

    confidence: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )

    supporting_metrics: dict = Field(
        default_factory=dict,
    )

    source: str | None = Field(
        default=None,
        max_length=100,
    )

class RecommendationUpdate(BaseModel):
    status: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    rationale: str| None = Field(
        default=None,
        min_length=1,
    )

    confidence: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0
    )

    supporting_metrics:dict | None = None

    source: str |None = Field(
        default=None,
        max_length=100,
    )

    is_active: bool | None = None

class RecommendationResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID
    decision_id: UUID
    recommended_option_id: UUID
    status: str
    rationale: str
    confidence: float | None
    supporting_metrics: dict
    source: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime