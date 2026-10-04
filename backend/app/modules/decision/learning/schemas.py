from uuid import UUID

from pydantic import BaseModel


class DecisionLearningCreate(BaseModel):
    decision_id: UUID
    outcome_id: UUID


class DecisionLearningResponse(BaseModel):
    id: UUID
    decision_id: UUID
    decision_option_id: UUID | None
    learning_type: str
    metric_name: str | None
    performance: str | None
    direction: str | None
    variance_percentage: float | None
    insight: str

    model_config = {
        "from_attributes": True
    }