from uuid import UUID

from app.modules.decision.feedback.repository import (
    DecisionFeedbackRepository,
)
from app.modules.decision.outcome.analysis.service import (
    OutcomeAnalysisService,
)


class DecisionFeedbackAnalysisService:

    def __init__(
        self,
        outcome_analysis_service: OutcomeAnalysisService,
        feedback_repository: DecisionFeedbackRepository,
    ):
        self.outcome_analysis_service = outcome_analysis_service
        self.feedback_repository = feedback_repository

    async def generate_feedback(
        self,
        outcome_id: UUID,
    ):

        metrics = await self.outcome_analysis_service.analyze_outcome(
            outcome_id
        )

        if not metrics:
            raise ValueError(
                "No outcome metrics found for this outcome"
            )

        above = sum(
            1
            for metric in metrics
            if metric["performance"] == "ABOVE_EXPECTATION"
        )

        below = sum(
            1
            for metric in metrics
            if metric["performance"] == "BELOW_EXPECTATION"
        )

        meets = sum(
            1
            for metric in metrics
            if metric["performance"] == "MEETS_EXPECTATION"
        )

        total = len(metrics)

        if above == total:
            overall_performance = "ABOVE_EXPECTATION"

        elif below == total:
            overall_performance = "BELOW_EXPECTATION"

        elif meets == total:
            overall_performance = "MEETS_EXPECTATION"

        elif above > below:
            overall_performance = "ABOVE_EXPECTATION"

        elif below > above:
            overall_performance = "BELOW_EXPECTATION"

        else:
            overall_performance = "MIXED"

        summary = (
            f"Outcome analysis evaluated {total} metric(s): "
            f"{above} above expectation, "
            f"{meets} meeting expectation, and "
            f"{below} below expectation."
        )

        existing_feedback = (
            await self.feedback_repository.get_by_outcome(
                outcome_id
            )
        )

        if existing_feedback:
            return await self.feedback_repository.update(
                feedback=existing_feedback,
                overall_performance=overall_performance,
                summary=summary,
            )

        return await self.feedback_repository.create(
            outcome_id=outcome_id,
            overall_performance=overall_performance,
            summary=summary,
        )