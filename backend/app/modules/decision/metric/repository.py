from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.decision.metric import DecisionMetric

class DecisionMetricRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
            self,
            metric: DecisionMetric,
    ) -> DecisionMetric:

        self.session.add(metric)

        await self.session.flush()
        await self.session.refresh(metric)

        return metric
    async def get_by_id(
            self,
            metric_id: UUID,
            decision_option_id: UUID
    ) -> DecisionMetric | None:

        result = await self.session.execute(
            select(DecisionMetric).where(
                DecisionMetric.id == metric_id,
                DecisionMetric.decision_option_id == decision_option_id,
            )
        )

        return result.scalar_one_or_none()

    async def list_by_option(
            self,
            decision_option_id: UUID,
            skip: int = 0,
            limit: int = 100,
    ) -> list[DecisionMetric]:

        result = await self.session.execute(
            select(DecisionMetric)
            .where(
                DecisionMetric.decision_option_id == decision_option_id
            )
            .order_by(DecisionMetric.created_at)
            .offset(skip)
            .limit(limit)
        )

        return list(result.scalars().all())

    async def update(
            self,
            metric: DecisionMetric,
    ) -> DecisionMetric:

        await self.session.flush()
        await self.session.refresh(metric)

        return metric

    async def delete(
            self,
            metric: DecisionMetric,
    ) -> None:

        await self.session.delete(metric)
        await self.session.flush()