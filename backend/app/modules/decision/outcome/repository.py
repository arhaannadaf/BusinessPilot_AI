from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.decision.outcome.outcome import Outcome


class OutcomeRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, outcome: Outcome) -> Outcome:
        self.session.add(outcome)
        await self.session.flush()
        await self.session.refresh(outcome)
        return outcome

    async def get_by_id(self, outcome_id: UUID) -> Outcome | None:
        result = await self.session.execute(
            select(Outcome).where(
                Outcome.id == outcome_id
            )
        )
        return result.scalar_one_or_none()

    async def get_by_execution(
        self,
        execution_id: UUID,
    ) -> Outcome | None:
        result = await self.session.execute(
            select(Outcome).where(
                Outcome.execution_id == execution_id
            )
        )
        return result.scalar_one_or_none()

    async def update(self, outcome: Outcome) -> Outcome:
        await self.session.flush()
        await self.session.refresh(outcome)
        return outcome