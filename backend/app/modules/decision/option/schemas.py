from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

class DecisionOptionCreate(BaseModel):

    decision_id: UUID

    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    description: str | None = None

    parameters: dict  =Field(
        default_factory=dict,
    )

class DecisionOptionUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    description: str | None = None

    parameters: dict | None = None

    is_selected: bool | None = None

    is_active: bool | None = None

class DecisionOptionResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID
    decision_id: UUID
    name: str
    description: str | None
    parameters: dict
    is_selected: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
