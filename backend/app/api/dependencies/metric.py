from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

from app.modules.decision.metric.repository import DecisionMetricRepository
from app.modules.decision.metric.service import DecisionMetricService

def get_decision_metric_repository(
        session: AsyncSession = Depends(get_db),
) -> DecisionMetricRepository:
    return DecisionMetricRepository(session)

def get_decision_metric_service(
        session: AsyncSession = Depends(get_db),
        repository: DecisionMetricRepository = Depends(
            get_decision_metric_repository
        ),
) -> DecisionMetricService:

    return DecisionMetricService(
        repository=repository,
        session=session
    )