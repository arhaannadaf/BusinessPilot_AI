from uuid import UUID
from typing import Literal

from app.modules.decision.scenario.engine.schemas import (
    ScenarioChange,
    ScenarioMetricResult,
)


class ScenarioEngine:

    def apply_change(
        self,
        original_value: float,
        change: ScenarioChange,
    ) -> float:

        if change.change_type == "percentage":
            return original_value * (
                1 + change.change_value / 100
            )

        if change.change_type == "absolute":
            return original_value + change.change_value

        raise ValueError(
            f"Unsupported change type: {change.change_type}"
        )

    def evaluate_metric(
        self,
        option_id: UUID,
        original_value: float,
        direction: Literal["increase", "decrease"],
        change: ScenarioChange,
    ) -> ScenarioMetricResult:

        adjusted_value = self.apply_change(
            original_value=original_value,
            change=change,
        )

        return ScenarioMetricResult(
            option_id=option_id,
            metric_name=change.metric_name,
            original_value=original_value,
            adjusted_value=adjusted_value,
            change_value=change.change_value,
            change_type=change.change_type,
            direction=direction,
        )