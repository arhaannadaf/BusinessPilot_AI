from uuid import UUID

from app.database.models.decision.outcome.outcome_metric import OutcomeMetric
from app.modules.decision.outcome.repository import OutcomeRepository
from app.modules.decision.outcome.outcome_metric.repository import (
    OutcomeMetricRepository,
)


class OutcomeAnalysisService:

    def __init__(
        self,
        outcome_repository: OutcomeRepository,
        outcome_metric_repository: OutcomeMetricRepository,
    ):
        self.outcome_repository = outcome_repository
        self.outcome_metric_repository = outcome_metric_repository

    async def analyze_outcome(
        self,
        outcome_id: UUID,
    ) -> list[dict]:

        outcome = await self.outcome_repository.get_by_id(
            outcome_id
        )

        if not outcome:
            raise ValueError("Outcome not found")

        metrics = await self.outcome_metric_repository.get_by_outcome(
            outcome_id
        )

        results = []

        for metric in metrics:

            if metric.direction == "increase":
                if metric.actual_value > metric.expected_value:
                    performance = "ABOVE_EXPECTATION"
                elif metric.actual_value < metric.expected_value:
                    performance = "BELOW_EXPECTATION"
                else:
                    performance = "MEETS_EXPECTATION"

            elif metric.direction == "decrease":
                if metric.actual_value < metric.expected_value:
                    performance = "ABOVE_EXPECTATION"
                elif metric.actual_value > metric.expected_value:
                    performance = "BELOW_EXPECTATION"
                else:
                    performance = "MEETS_EXPECTATION"

            else:
                raise ValueError(
                    f"Invalid direction for metric: {metric.metric_name}"
                )

            results.append(
                {
                    "metric_name": metric.metric_name,
                    "direction": metric.direction,
                    "expected_value": float(metric.expected_value),
                    "actual_value": float(metric.actual_value),
                    "variance": float(metric.variance),
                    "variance_percentage": (
                        float(metric.variance_percentage)
                        if metric.variance_percentage is not None
                        else None
                    ),
                    "performance": performance,
                }
            )

        return results