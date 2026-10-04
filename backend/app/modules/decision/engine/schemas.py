from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from typing import Literal

class MetricInput(BaseModel):
    metric_name: str
    value: float
    direction: Literal["maximize","minimize"]
    weight: float = Field(
        gt=0,
        description="Relative importance of the metric in the decision."
        ) 

class OptionInput(BaseModel):
    option_id: UUID
    metrics: list[MetricInput]

class OptionScore(BaseModel):
    option_id: UUID
    score: float

class RankedOption(BaseModel):
    option_id:UUID
    score:float
    rank:int

class BestOption(BaseModel):
    option_id: UUID
    score: float

class DecisionEvaluationRequest(BaseModel):
    weights: dict[str, float]
    learning_weight: float = 0.0

    @field_validator("weights")
    @classmethod
    def validate_weights(
        cls,
        weights: dict[str, float],
    ) -> dict[str, float]:

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