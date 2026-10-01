from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.decision.option import DecisionOption


class DecisionOptionRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        option: DecisionOption,
    ) -> DecisionOption:

        self.session.add(option)

        await self.session.flush()
        await self.session.refresh(option)

        return option

    async def get_by_id(
        self,
        option_id: UUID,
        decision_id: UUID,
    ) -> DecisionOption | None:

        result = await self.session.execute(
            select(DecisionOption).where(
                DecisionOption.id == option_id,
                DecisionOption.decision_id == decision_id,
            )
        )

        return result.scalar_one_or_none()

    async def list_by_decision(
        self,
        decision_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[DecisionOption]:

        result = await self.session.execute(
            select(DecisionOption)
            .where(
                DecisionOption.decision_id == decision_id
            )
            .order_by(DecisionOption.created_at)
            .offset(skip)
            .limit(limit)
        )

        return list(result.scalars().all())

    async def update(
        self,
        option: DecisionOption,
    ) -> DecisionOption:

        await self.session.flush()
        await self.session.refresh(option)

        return option

    async def delete(
        self,
        option: DecisionOption,
    ) -> None:

        await self.session.delete(option)
        await self.session.flush()