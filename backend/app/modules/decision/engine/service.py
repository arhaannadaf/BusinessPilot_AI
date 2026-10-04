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
from app.modules.decision.learning.repository import (
    DecisionLearningRepository,
)

class DecisionEngineService:
    def __init__(self, session: AsyncSession):
        self.session =session
        self.decision_repository = DecisionRepository(session)
        self.option_repository = DecisionOptionRepository(session)
        self.metric_repository = DecisionMetricRepository(session)
        self.learning_repository = DecisionLearningRepository(session)
        self.engine = DecisionEngine()

    def calculate_learning_scores(
        self,
        learning_records,
    ) -> dict[UUID, float]:

        learning_scores: dict[UUID, list[float]] = {}

        for learning in learning_records:

            if learning.decision_option_id is None:
                continue

            if learning.variance_percentage is None:
                continue

            variance = float(learning.variance_percentage)

            if learning.direction == "increase":
                adjusted_variance = variance

            elif learning.direction == "decrease":
                adjusted_variance = -variance

            else:
                continue

            adjusted_variance = max(
                -50.0,
                min(50.0, adjusted_variance),
            )

            score = 0.5 + (adjusted_variance / 100.0)

            learning_scores.setdefault(
                learning.decision_option_id,
                [],
            ).append(score)

        return {
            option_id: sum(scores) / len(scores)
            for option_id, scores in learning_scores.items()
        }

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

        learning_records = await self.learning_repository.get_by_decision(
            decision.id
        )
        learning_scores = self.calculate_learning_scores(
    learning_records
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
        learning_weight = request.learning_weight

        if learning_weight < 0 or learning_weight > 1:
            raise ValueError(
                "Learning weight must be between 0 and 1."
            )

        if learning_weight == 0 or not learning_scores:
            final_scores = scores

        else:
            final_scores = [
                OptionScore(
                    option_id=score.option_id,
                    score=(
                        score.score * (1 - learning_weight)
                        + learning_scores.get(
                            score.option_id,
                            0.5,
                        ) * learning_weight
                    ),
                )
                for score in scores
            ]

        ranked_options = self.engine.rank_options(
            final_scores
        )

        best_option = self.engine.select_best_option(
            ranked_options
        )

        selected_option_id = best_option.option_id

        base_score = next(
            score.score
            for score in scores
            if score.option_id == selected_option_id
        )

        learning_score = learning_scores.get(
            selected_option_id,
            0.5,
        )

        return BestOption(
            option_id=selected_option_id,
            score=best_option.score,
            base_score=base_score,
            learning_score=learning_score,
            learning_weight=learning_weight,
        )