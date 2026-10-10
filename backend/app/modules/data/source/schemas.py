from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DataSourceCreate(BaseModel):
    organization_id: UUID
    name: str = Field(min_length=1, max_length=255)
    source_type: str = Field(min_length=1, max_length=50)
    description: str | None = None
    connection_config: dict = Field(default_factory=dict)


class DataSourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    name: str
    source_type: str
    description: str | None
    connection_config: dict
    is_active: bool
    created_at: datetime
    updated_at: datetime