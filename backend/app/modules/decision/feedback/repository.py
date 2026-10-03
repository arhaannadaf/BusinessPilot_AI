from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.decision.feedback.decision_feedback import (
    DecisionFeedback,
)


class DecisionFeedbackRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        outcome_id: UUID,
        overall_performance: str,
        summary: str,
    ) -> DecisionFeedback:

        feedback = DecisionFeedback(
            outcome_id=outcome_id,
            overall_performance=overall_performance,
            summary=summary,
        )

        self.session.add(feedback)
        await self.session.flush()

        return feedback

    async def get_by_id(
        self,
        feedback_id: UUID,
    ) -> DecisionFeedback | None:

        result = await self.session.execute(
            select(DecisionFeedback).where(
                DecisionFeedback.id == feedback_id
            )
        )

        return result.scalar_one_or_none()

    async def get_by_outcome(
        self,
        outcome_id: UUID,
    ) -> DecisionFeedback | None:

        result = await self.session.execute(
            select(DecisionFeedback).where(
                DecisionFeedback.outcome_id == outcome_id
            )
        )

        return result.scalar_one_or_none()

    async def update(
        self,
        feedback: DecisionFeedback,
        overall_performance: str,
        summary: str,
    ) -> DecisionFeedback:

        feedback.overall_performance = overall_performance
        feedback.summary = summary

        await self.session.flush()

        return feedback