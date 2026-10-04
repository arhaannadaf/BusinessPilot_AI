from uuid import UUID

from pydantic import BaseModel


class DecisionFeedbackCreate(BaseModel):
    outcome_id: UUID
    overall_performance: str
    summary: str


class DecisionFeedbackResponse(BaseModel):
    id: UUID
    outcome_id: UUID
    overall_performance: str
    summary: str

    model_config = {
        "from_attributes": True
    }

class DecisionFeedbackUpdate(BaseModel):
    overall_performance: str
    summary: str