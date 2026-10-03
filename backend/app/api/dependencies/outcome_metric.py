from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.modules.decision.execution.repository import ExecutionRepository
from app.modules.decision.outcome.repository import OutcomeRepository
from app.modules.decision.outcome.outcome_metric.repository import (
    OutcomeMetricRepository,
)
from app.modules.decision.outcome.outcome_metric.service import (
    OutcomeMetricService,
)
from app.modules.decision.recommendation.repository import (
    RecommendationRepository,
)


def get_outcome_metric_service(
    session: AsyncSession = Depends(get_db),
) -> OutcomeMetricService:

    outcome_metric_repository = OutcomeMetricRepository(session)
    outcome_repository = OutcomeRepository(session)
    execution_repository = ExecutionRepository(session)
    recommendation_repository = RecommendationRepository(session)

    return OutcomeMetricService(
        outcome_metric_repository=outcome_metric_repository,
        outcome_repository=outcome_repository,
        execution_repository=execution_repository,
        recommendation_repository=recommendation_repository,
    )