from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.decision.decision import Decision

class DecisionRepository:

    def __init__(
            self,
            session:AsyncSession
    ):
        self.session =session

    async def create(
            self,
            decision: Decision,
    ) -> Decision:

        self.session.add(decision)

        await self.session.flush()
        await self.session.refresh(decision)

        return decision

    async def get_by_id(
            self,
            decision_id: UUID,
            organization_id: UUID
    ) -> Decision | None:

        result = await self.session.execute(
            select(Decision).where(
                Decision.id == decision_id,
                Decision.organization_id == organization_id,
            )
        )

        return result.scalar_one_or_none()

    async def list(
            self,
            organization_id: UUID,
            skip: int = 0,
            limit: int = 100,
    ) -> list[Decision]:

        result = await self.session.execute(
            select(Decision)
            .where(
                Decision.organization_id == organization_id
            )
            .order_by(Decision.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        return list(result.scalars().all())

    async def update(
        self,
        decision: Decision,
    ) -> Decision:

        await self.session.flush()
        await self.session.refresh(decision)

        return decision

    async def delete(
        self,
        decision: Decision,
    ) -> None:

        await self.session.delete(decision)
        await self.session.flush()