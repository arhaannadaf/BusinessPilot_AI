from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.modules.decision.feedback.repository import (
    DecisionFeedbackRepository,
)
from app.modules.decision.feedback.service import (
    DecisionFeedbackService,
)
from app.modules.decision.outcome.repository import OutcomeRepository


async def get_decision_feedback_service(
    session: AsyncSession = Depends(get_db),
) -> DecisionFeedbackService:

    feedback_repository = DecisionFeedbackRepository(session)
    outcome_repository = OutcomeRepository(session)

    return DecisionFeedbackService(
        feedback_repository=feedback_repository,
        outcome_repository=outcome_repository,
    )