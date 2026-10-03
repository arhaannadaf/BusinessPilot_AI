from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.decision.execution import Execution


class ExecutionRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        execution: Execution,
    ) -> Execution:

        self.session.add(execution)

        await self.session.flush()
        await self.session.refresh(execution)

        return execution

    async def get_by_id(
        self,
        execution_id: UUID,
    ) -> Execution | None:

        result = await self.session.execute(
            select(Execution).where(
                Execution.id == execution_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_by_recommendation(
        self,
        recommendation_id: UUID,
    ) -> list[Execution]:

        result = await self.session.execute(
            select(Execution)
            .where(
                Execution.recommendation_id == recommendation_id,
            )
            .order_by(Execution.created_at.desc())
        )

        return list(result.scalars().all())

    async def update(
        self,
        execution: Execution,
    ) -> Execution:

        await self.session.flush()
        await self.session.refresh(execution)

        return execution