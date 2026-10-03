from uuid import UUID
from typing import Literal
from pydantic import BaseModel, Field, field_validator



class ScenarioChange(BaseModel):
    metric_name: str = Field(..., min_length=1, max_length=100)
    change_type: str = Field(
        ...,
        description="Percentage or absolute change.",
    )
    change_value: float


class ScenarioEvaluationRequest(BaseModel):
    scenario_id: UUID
    changes: list[ScenarioChange] = Field(..., min_length=1)
    weights: dict[str, float]

    @field_validator("weights")
    @classmethod
    def validate_weights(cls, weights):
        if not weights:
            raise ValueError(
                "At least one metric weight is required."
            )

        for metric_name, weight in weights.items():

            if not metric_name.strip():
                raise ValueError(
                    "Metric name cannot be empty."
                )

            if weight <= 0:
                raise ValueError(
                    f"Weight for metric '{metric_name}' "
                    "must be greater than zero."
                )

        return weights


class ScenarioMetricResult(BaseModel):
    option_id: UUID
    metric_name: str
    original_value: float
    adjusted_value: float
    change_value: float
    change_type: str
    direction: Literal["increase", "decrease"]


class ScenarioEvaluationResult(BaseModel):
    scenario_id: UUID
    metrics: list[ScenarioMetricResult]
    recommended_option_id: UUID
    score: float