from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.decision.scenario import Scenario

class ScenarioRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
            self,
            scenario: Scenario,
    ) -> Scenario:
        self.session.add(scenario)

        await self.session.flush()
        await self.session.refresh(scenario)

        return scenario

    async def get_by_id(
            self,
            scenario_id: UUID,
            organization_id: UUID,
    ) -> Scenario | None:

        result = await self.session.execute(
            select(Scenario).where(
                Scenario.id == scenario_id,
                Scenario.organization_id == organization_id,
            )
        )

        return result.scalar_one_or_none()

    async def list(
            self,
            organization_id: UUID,
            skip: int = 0,
            limit: int =100,
    ) -> list[Scenario]:

        result = await self.session.execute(
            select(Scenario)
            .where(
                Scenario.organization_id == organization_id
            )
            .order_by(Scenario.name)
            .offset(skip)
            .limit(limit)
        )

        return list(result.scalars().all())

    async def update(
            self,
            scenario:Scenario,
    ) -> Scenario:

        await self.session.flush()
        await self.session.refresh(scenario)

        return scenario

    async def delete(
            self,
            scenario:Scenario,
    ) -> None:

        await self.session.delete(scenario)
        await self.session.flush()