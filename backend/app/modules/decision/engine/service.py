from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession 

from app.modules.decision.engine.engine import DecisionEngine
from app.modules.decision.engine.schemas import (
    MetricInput,
    OptionInput,
    OptionScore,
    RankedOption,
    BestOption,
    DecisionEvaluationRequest,
)

from app.modules.decision.decision.repository import DecisionRepository
from app.modules.decision.option.repository import DecisionOptionRepository
from app.modules.decision.metric.repository import DecisionMetricRepository


class DecisionEngineService:
    def __init__(self, session: AsyncSession):
        self.session =session
        self.decision_repository = DecisionRepository(session)
        self.option_repository = DecisionOptionRepository(session)
        self.metric_repository = DecisionMetricRepository(session)
        self.engine = DecisionEngine()

    async def evaluate_decision(
            self,
            decision_id: UUID,
            organization_id: UUID,
            request: DecisionEvaluationRequest
    ) -> BestOption:

        decision = await self.decision_repository.get_by_id(
            decision_id=decision_id,
            organization_id=organization_id,
        )
        DIRECTION_MAP = {
            "increase": "maximize",
            "decrease": "minimize",
            }

        if decision is None:
            raise ValueError(
                "Decison not found."
            )

        options = await self.option_repository.list_by_decision(
            decision_id=decision_id
        )

        if not options:
            raise ValueError(
                "Decision has no options."
            )

        option_inputs: list[OptionInput] = []

        decision_metric_names: set[str] = set()

        option_metrics = []

        for option in options:

            metrics = await self.metric_repository.list_by_option(decision_option_id=option.id,)

            if not metrics:
                raise ValueError(
                    f"Option {option.id} has no metrics."
                )

            option_metrics.append((option, metrics))

            for metric in metrics:
                decision_metric_names.add(metric.metric_name)

        missing_metrics = ( decision_metric_names - set(request.weights.keys()))

        if missing_metrics:
            raise ValueError(
                "No weights provided for metric(s): "
                + ", ".join(sorted(missing_metrics))
            )

        unknown_metrics = (
            set(request.weights.keys())
            - decision_metric_names
        )

        if unknown_metrics:
            raise ValueError(
                "Weights provided for unknown metrics: "
                + ", ".join(sorted(unknown_metrics))
            )
        for option, metrics in option_metrics:

            metric_inputs: list[MetricInput] = []

            for metric in metrics:

                direction = DIRECTION_MAP.get(metric.direction)

                if direction is None:
                    raise ValueError(
                        f"Invalid metric direction from database: "
                        f"{metric.direction}"
                    )

                metric_inputs.append(
                    MetricInput(
                        metric_name=metric.metric_name,
                        value=metric.value,
                        direction=direction,
                        weight=request.weights[
                            metric.metric_name
                        ],
                    )
                )

            option_inputs.append(
                OptionInput(
                    option_id=option.id,
                    metrics=metric_inputs,
                )
            )

        scores: list[OptionScore] = (
            self.engine.calculate_option_scores(
                option_inputs
            )
        )

        ranked_options: list[RankedOption] = (
            self.engine.rank_options(
                scores
            )
        )

        best_option: BestOption = (
            self.engine.select_best_option(
                ranked_options
            )
        )

        return best_option