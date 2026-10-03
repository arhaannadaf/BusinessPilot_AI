from uuid import UUID

from app.modules.decision.feedback.repository import (
    DecisionFeedbackRepository,
)
from app.modules.decision.outcome.repository import OutcomeRepository


class DecisionFeedbackService:

    def __init__(
        self,
        feedback_repository: DecisionFeedbackRepository,
        outcome_repository: OutcomeRepository,
    ):
        self.feedback_repository = feedback_repository
        self.outcome_repository = outcome_repository

    async def create_feedback(
        self,
        outcome_id: UUID,
        overall_performance: str,
        summary: str,
    ):

        allowed_performance = {
            "ABOVE_EXPECTATION",
            "MEETS_EXPECTATION",
            "BELOW_EXPECTATION",
            "MIXED",
        }

        if overall_performance not in allowed_performance:
            raise ValueError(
                "Invalid overall performance"
            )
        # Verify outcome exists
        outcome = await self.outcome_repository.get_by_id(
            outcome_id
        )

        if not outcome:
            raise ValueError("Outcome not found")

        # Prevent duplicate feedback
        existing_feedback = (
            await self.feedback_repository.get_by_outcome(
                outcome_id
            )
        )

        if existing_feedback:
            raise ValueError(
                "Feedback already exists for this outcome"
            )

        # Create feedback
        feedback = await self.feedback_repository.create(
            outcome_id=outcome_id,
            overall_performance=overall_performance,
            summary=summary,
        )

        return feedback

    async def get_feedback_by_outcome(
    self,
    outcome_id: UUID,
    ):
        feedback = await self.feedback_repository.get_by_outcome(
            outcome_id
        )

        if not feedback:
            raise ValueError(
                "Feedback not found for this outcome"
            )

        return feedback

    async def update_feedback(
        self,
        feedback_id: UUID,
        overall_performance: str,
        summary: str,
    ):
        allowed_performance = {
            "ABOVE_EXPECTATION",
            "MEETS_EXPECTATION",
            "BELOW_EXPECTATION",
            "MIXED",
        }

        if overall_performance not in allowed_performance:
            raise ValueError(
                "Invalid overall performance"
            )

        feedback = await self.feedback_repository.get_by_id(
            feedback_id
        )

        if not feedback:
            raise ValueError("Feedback not found")

        return await self.feedback_repository.update(
            feedback=feedback,
            overall_performance=overall_performance,
            summary=summary,
        )