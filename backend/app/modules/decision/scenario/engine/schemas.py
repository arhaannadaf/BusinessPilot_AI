from uuid import UUID

from pydantic import BaseModel, Field


class ScenarioChange(BaseModel):
    metric_name: str = Field(..., min_length=1, max_length=100)
    change_type: str = Field(
        ...,
        description="Percentage or absolute change.",
    )
    change_value: float


class ScenarioEvaluationRequest(BaseModel):
    scenario_id: UUID
    changes: list[ScenarioChange] = Field(
        ...,
        min_length=1,
    )


class ScenarioMetricResult(BaseModel):
    metric_name: str
    original_value: float
    adjusted_value: float
    change_value: float
    change_type: str


class ScenarioEvaluationResult(BaseModel):
    scenario_id: UUID
    metrics: list[ScenarioMetricResult]