from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.modules.decision.outcome.repository import OutcomeRepository
from app.modules.decision.outcome.outcome_metric.repository import (
    OutcomeMetricRepository,
)
from app.modules.decision.outcome.analysis.service import (
    OutcomeAnalysisService,
)


async def get_outcome_analysis_service(
    session: AsyncSession = Depends(get_db),
) -> OutcomeAnalysisService:

    outcome_repository = OutcomeRepository(session)

    outcome_metric_repository = OutcomeMetricRepository(
        session
    )

    return OutcomeAnalysisService(
        outcome_repository=outcome_repository,
        outcome_metric_repository=outcome_metric_repository,
    )