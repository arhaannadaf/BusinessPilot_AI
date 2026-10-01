from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DecisionMetricCreate(BaseModel):
    decision_option_id:UUID

    metric_name: str = Field(
        ...,
        min_length=1,
        max_length=100,

    ) 
    value: float

    unit: str | None = Field(
        default=None,
        max_length=50,
    )

    direction: str = Field(
        ...,
        min_length=1,
        max_length=20
    )

    source: str | None = None


    meta_data: dict = Field(
        default_factory=dict,
    )

class DecisionMetricUpdate(BaseModel):
    metric_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    value: float | None = None

    unit: str | None = Field(
        default=None,
        max_length=50
    )

    direction: str | None =Field(
        default=None,
        min_length=1,
        max_length=20,
    )
    source : str | None = None

    meta_data: dict | None = None

class DecisionMetricResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    decision_option_id: UUID
    metric_name: str
    value: float
    unit: str | None
    direction: str | None
    source: str | None
    meta_data: dict
    created_at: datetime
    updated_at : datetime