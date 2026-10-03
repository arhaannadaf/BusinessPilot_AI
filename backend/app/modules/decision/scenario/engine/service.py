from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.decision.decision import Decision
from app.database.models.decision.option import DecisionOption
from app.modules.decision.metric.repository import DecisionMetricRepository
from app.modules.decision.recommendation.service import RecommendationService
from app.modules.decision.recommendation.repository import RecommendationRepository

from app.modules.decision.engine.engine import DecisionEngine

from app.modules.decision.scenario.engine.engine import (
    ScenarioEngine,
    ScenarioMetricResult,
    )

from app.modules.decision.scenario.engine.schemas import (
    ScenarioEvaluationRequest,
    ScenarioEvaluationResult,
)
from app.modules.decision.engine.schemas import (
    MetricInput,
    OptionInput,
    OptionScore,
    RankedOption,
    BestOption,
)

class ScenarioEngineService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.metric_repository = DecisionMetricRepository(session)
        self.engine = ScenarioEngine()
        self.decision_engine = DecisionEngine()
        self.recommendation_service = RecommendationService(
            repository=RecommendationRepository(session),
            session=session,
        )

    async def evaluate_scenario(
        self,
        scenario_id: UUID,
        decision_id: UUID,
        request: ScenarioEvaluationRequest,
    ) -> ScenarioEvaluationResult:

        # Verify that the decision exists
        result = await self.session.execute(
            select(Decision).where(
                Decision.id == decision_id,
                Decision.scenario_id == scenario_id,
            )
        )

        decision = result.scalar_one_or_none()

        if decision is None:
            raise ValueError(
                "Decision does not belong to the specified scenario."
            )

        # Get all decision options
        result = await self.session.execute(
            select(DecisionOption).where(
                DecisionOption.decision_id == decision_id,
                DecisionOption.is_active.is_(True),
            )
        )

        options = list(result.scalars().all())

        if not options:
            raise ValueError(
                "Decision has no active options."
            )

        results = []

        for option in options:
            metrics = await self.metric_repository.list_by_option(
                decision_option_id=option.id,
            )

            if not metrics:
                raise ValueError(
                    f"Option {option.id} has no metrics."
                )

            for metric in metrics:
                for change in request.changes:

                    if change.metric_name != metric.metric_name:
                        continue

                    results.append(
                        self.engine.evaluate_metric(
                            option_id=option.id,
                            original_value=metric.value,
                            direction=metric.direction,
                            change=change,
                        )
                    )

        best_option = self.evaluate_with_decision_engine(
            results=results,
            weights=request.weights,
        )
        await self.recommendation_service.create_scenario_recommendation(
            decision_id=decision_id,
            organization_id=decision.organization_id,
            recommended_option_id=best_option.option_id,
            score=best_option.score,
            weights=request.weights,
            scenario_metrics=[
            {
                **metric.model_dump(),
                "option_id": str(metric.option_id),
            }
            for metric in results
        ],
        )

        return ScenarioEvaluationResult(
            scenario_id=scenario_id,
            metrics=results,
            recommended_option_id=best_option.option_id,
            score=best_option.score,
        )

    def build_decision_inputs(
        self,
        results: list[ScenarioMetricResult],
        weights: dict[str, float],
    ) -> list[OptionInput]:

        DIRECTION_MAP = {
            "increase": "maximize",
            "decrease": "minimize",
        }

        if not results:
            raise ValueError("No scenario results provided.")

        metric_names = {
            result.metric_name
            for result in results
        }

        missing_metrics = metric_names - set(weights.keys())

        if missing_metrics:
            raise ValueError(
                "No weights provided for metric(s): "
                + ", ".join(sorted(missing_metrics))
            )

        unknown_metrics = set(weights.keys()) - metric_names

        if unknown_metrics:
            raise ValueError(
                "Weights provided for unknown metrics: "
                + ", ".join(sorted(unknown_metrics))
            )

        options: dict[UUID, list[MetricInput]] = {}

        for result in results:

            direction = DIRECTION_MAP.get(result.direction)

            if direction is None:
                raise ValueError(
                    f"Invalid scenario metric direction: "
                    f"{result.direction}"
                )

            if result.option_id not in options:
                options[result.option_id] = []

            options[result.option_id].append(
                MetricInput(
                    metric_name=result.metric_name,
                    value=result.adjusted_value,
                    direction=direction,
                    weight=weights[result.metric_name],
                )
            )

        return [
            OptionInput(
                option_id=option_id,
                metrics=metrics,
            )
            for option_id, metrics in options.items()
        ]

    def evaluate_with_decision_engine(
        self,
        results: list[ScenarioMetricResult],
        weights: dict[str, float],
    ) -> BestOption:

        option_inputs = self.build_decision_inputs(
            results=results,
            weights=weights,
        )

        scores: list[OptionScore] = self.decision_engine.calculate_option_scores(
            option_inputs
        )

        ranked_options: list[RankedOption] = (
            self.decision_engine.rank_options(scores)
        )

        return self.decision_engine.select_best_option(
            ranked_options
        )
    