from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RecommendationHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    recommendation_id: UUID
    previous_status: str | None
    new_status: str
    reason: str | None
    changed_by: UUID | None
    created_at: datetime