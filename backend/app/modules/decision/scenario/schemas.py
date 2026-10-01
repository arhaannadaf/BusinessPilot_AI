from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

class ScenarioCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    description: str | None = None

    scenario_type: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    assumptions:dict = Field(
        default_factory=dict,
    )

class ScenarioUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    ) 
    description: str | None = None

    scenario_type: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    ) 

    assumptions: dict | None = None

    is_active: bool | None = None

class ScenarioResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id:UUID
    name:str
    description: str | None
    scenario_type: str
    assumptions: dict
    is_active: bool
    created_by: UUID
    created_at: datetime
    updated_at: datetime