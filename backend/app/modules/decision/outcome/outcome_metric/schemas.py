from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OutcomeMetricCreate(BaseModel):
    outcome_id: UUID
    metric_name: str
    actual_value: float
    unit: str | None = None

class OutcomeMetricResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    outcome_id: UUID
    metric_name: str
    expected_value: float
    actual_value: float
    unit: str | None
    variance: float
    variance_percentage: float | None
    created_at: datetime
    updated_at: datetime