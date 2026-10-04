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
from app.modules.decision.execution.repository import (
    ExecutionRepository,
)
from app.modules.decision.recommendation.repository import (
    RecommendationRepository,
)

class DecisionLearningService:

    def __init__(
        self,
        learning_repository: DecisionLearningRepository,
        feedback_repository: DecisionFeedbackRepository,
        outcome_repository: OutcomeRepository,
        outcome_analysis_service: OutcomeAnalysisService,
        execution_repository: ExecutionRepository,
        recommendation_repository: RecommendationRepository,
    ):
        self.learning_repository = learning_repository
        self.feedback_repository = feedback_repository
        self.outcome_repository = outcome_repository
        self.outcome_analysis_service = outcome_analysis_service
        self.execution_repository = execution_repository
        self.recommendation_repository = recommendation_repository

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

        execution = await self.execution_repository.get_by_id(
            outcome.execution_id
        )

        if not execution:
            raise ValueError("Execution not found")

        recommendation = await self.recommendation_repository.get_by_id_only(
            execution.recommendation_id
        )

        if not recommendation:
            raise ValueError("Recommendation not found")

        decision_option_id = recommendation.recommended_option_id

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
            direction = metric["direction"]

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
                decision_option_id=decision_option_id,
                learning_type="PERFORMANCE_PATTERN",
                metric_name=metric["metric_name"],
                performance=performance,
                direction = direction,
                variance_percentage=metric["variance_percentage"],
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

    