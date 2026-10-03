from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class OutcomeCreate(BaseModel):
    execution_id: UUID
    summary: str | None = None
    meta_data: dict = Field(default_factory=dict)


class OutcomeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    execution_id: UUID
    status: str
    observed_at: datetime | None
    summary: str | None
    meta_data: dict
    created_at: datetime
    updated_at: datetime