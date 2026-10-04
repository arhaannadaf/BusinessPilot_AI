from uuid import UUID

from app.modules.decision.feedback.repository import (
    DecisionFeedbackRepository,
)
from app.modules.decision.learning.repository import (
    DecisionLearningRepository,
)
from app.modules.decision.outcome.analysis.service import (
    OutcomeAnalysisService,
)
from app.modules.decision.outcome.repository import (
    OutcomeRepository,
)


class DecisionLearningService:

    def __init__(
        self,
        learning_repository: DecisionLearningRepository,
        feedback_repository: DecisionFeedbackRepository,
        outcome_repository: OutcomeRepository,
        outcome_analysis_service: OutcomeAnalysisService,
    ):
        self.learning_repository = learning_repository
        self.feedback_repository = feedback_repository
        self.outcome_repository = outcome_repository
        self.outcome_analysis_service = outcome_analysis_service

    async def generate_learning(
        self,
        decision_id: UUID,
        outcome_id: UUID,
    ):
        outcome = await self.outcome_repository.get_by_id(
            outcome_id
        )

        if not outcome:
            raise ValueError("Outcome not found")

        metrics = await self.outcome_analysis_service.analyze_outcome(
            outcome_id
        )

        if not metrics:
            raise ValueError(
                "No outcome metrics found for this outcome"
            )

        feedback = await self.feedback_repository.get_by_outcome(
            outcome_id
        )

        if not feedback:
            raise ValueError(
                "Decision feedback not found for this outcome"
            )

        learning_records = []

        for metric in metrics:
            performance = metric["performance"]

            insight = (
                f"Metric '{metric['metric_name']}' was "
                f"{performance.lower().replace('_', ' ')}. "
                f"Expected value was {metric['expected_value']}, "
                f"actual value was {metric['actual_value']}, "
                f"with a variance of "
                f"{metric['variance_percentage']}%."
            )

            learning = await self.learning_repository.create(
                decision_id=decision_id,
                learning_type="PERFORMANCE_PATTERN",
                insight=insight,
            )

            learning_records.append(learning)

        return learning_records

    async def get_learning_by_decision(
        self,
        decision_id: UUID,
    ):
        return await self.learning_repository.get_by_decision(
            decision_id
    )

    