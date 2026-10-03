from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ExecutionCreate(BaseModel):
    recommendation_id: UUID
    executed_by: UUID | None = None
    execution_details: dict = Field(default_factory=dict)


class ExecutionUpdate(BaseModel):
    status: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    result: str | None = None

    error_message: str | None = None

    execution_details: dict | None = None

    started_at: datetime | None = None

    completed_at: datetime | None = None


class ExecutionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    recommendation_id: UUID
    status: str
    executed_by: UUID | None
    started_at: datetime | None
    completed_at: datetime | None
    execution_details: dict
    result: str | None
    error_message: str | None
    created_at: datetime
    updated_at: datetime