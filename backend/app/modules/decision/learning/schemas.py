from uuid import UUID

from pydantic import BaseModel


class DecisionLearningCreate(BaseModel):
    decision_id: UUID
    outcome_id: UUID


class DecisionLearningResponse(BaseModel):
    id: UUID
    decision_id: UUID
    learning_type: str
    insight: str

    model_config = {
        "from_attributes": True
    }