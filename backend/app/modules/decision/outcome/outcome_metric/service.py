from uuid import UUID

from app.database.models.decision.outcome.outcome_metric import OutcomeMetric
from app.modules.decision.outcome.repository import OutcomeRepository
from app.modules.decision.outcome.outcome_metric.repository import OutcomeMetricRepository
from app.modules.decision.execution.repository import ExecutionRepository
from app.modules.decision.recommendation.repository import RecommendationRepository

class OutcomeMetricService:

    def __init__(
        self,
        outcome_metric_repository: OutcomeMetricRepository,
        outcome_repository: OutcomeRepository,
        execution_repository: ExecutionRepository,
        recommendation_repository: RecommendationRepository,
    ):
        self.outcome_metric_repository = outcome_metric_repository
        self.outcome_repository = outcome_repository
        self.execution_repository = execution_repository
        self.recommendation_repository = recommendation_repository

    async def create_metric(
        self,
        outcome_id: UUID,
        metric_name: str,
        actual_value: float,
        unit: str | None = None,
    ) -> OutcomeMetric:

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

        recommendation = (
            await self.recommendation_repository.get_by_id_only(
                execution.recommendation_id
            )
        )

        if not recommendation:
            raise ValueError("Recommendation not found")

        supporting_metrics = recommendation.supporting_metrics or {}

        expected_metrics = supporting_metrics.get(
            "expected_metric",
            [],
        )

        expected_value = None
        direction = None

        recommended_option_id = str(
            recommendation.recommended_option_id
        )

        for metric in expected_metrics:
            if (
                metric.get("metric_name") == metric_name
                and str(metric.get("option_id")) == recommended_option_id
            ):
                expected_value = metric.get("adjusted_value")
                direction = metric.get("direction")
                break

        if expected_value is None:
            raise ValueError(
                f"Expected value not found for metric: {metric_name}"
            )

        if direction is None:
            raise ValueError(
                f"Direction not found for metric: {metric_name}"
            )

        variance = actual_value - expected_value

        variance_percentage = None

        if expected_value != 0:
            variance_percentage = (
                (actual_value - expected_value)
                / expected_value
            ) * 100

        metric = OutcomeMetric(
            outcome_id=outcome_id,
            metric_name=metric_name,
            direction=direction,
            expected_value=expected_value,
            actual_value=actual_value,
            unit=unit,
            variance=variance,
            variance_percentage=variance_percentage,
        )

        return await self.outcome_metric_repository.create(metric)

    async def get_metric(
        self,
        metric_id: UUID,
    ) -> OutcomeMetric:

        metric = await self.outcome_metric_repository.get_by_id(
            metric_id
        )

        if not metric:
            raise ValueError("Outcome metric not found")

        return metric

    async def get_metrics_by_outcome(
        self,
        outcome_id: UUID,
    ) -> list[OutcomeMetric]:

        outcome = await self.outcome_repository.get_by_id(
            outcome_id
        )

        if not outcome:
            raise ValueError("Outcome not found")

        return await self.outcome_metric_repository.get_by_outcome(
            outcome_id
        )