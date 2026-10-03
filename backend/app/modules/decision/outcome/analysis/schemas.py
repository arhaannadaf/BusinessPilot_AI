from uuid import UUID

from pydantic import BaseModel


class OutcomeMetricAnalysis(BaseModel):
    metric_name: str
    direction: str
    expected_value: float
    actual_value: float
    variance: float
    variance_percentage: float | None
    performance: str


class OutcomeAnalysisResponse(BaseModel):
    outcome_id: UUID
    metrics: list[OutcomeMetricAnalysis]