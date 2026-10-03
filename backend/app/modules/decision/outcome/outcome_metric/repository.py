from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.decision.outcome.outcome_metric import OutcomeMetric


class OutcomeMetricRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        metric: OutcomeMetric,
    ) -> OutcomeMetric:
        self.session.add(metric)
        await self.session.flush()
        await self.session.refresh(metric)
        return metric

    async def get_by_id(
        self,
        metric_id: UUID,
    ) -> OutcomeMetric | None:
        result = await self.session.execute(
            select(OutcomeMetric).where(
                OutcomeMetric.id == metric_id
            )
        )
        return result.scalar_one_or_none()

    async def get_by_outcome(
        self,
        outcome_id: UUID,
    ) -> list[OutcomeMetric]:
        result = await self.session.execute(
            select(OutcomeMetric)
            .where(
                OutcomeMetric.outcome_id == outcome_id
            )
            .order_by(OutcomeMetric.created_at)
        )
        return list(result.scalars().all())

    async def update(
        self,
        metric: OutcomeMetric,
    ) -> OutcomeMetric:
        await self.session.flush()
        await self.session.refresh(metric)
        return metric