from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DecisionCreate(BaseModel):
    scenario_id: UUID

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    description: str | None = None

    decision_type: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )


class DecisionUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    description: str | None = None

    status: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    decision_type: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    is_active: bool | None = None


class DecisionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    scenario_id: UUID
    organization_id: UUID
    title: str
    description: str | None
    status: str
    decision_type: str
    is_active: bool
    created_by: UUID
    created_at: datetime
    updated_at: datetime