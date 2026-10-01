from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.decision.decision import Decision
from app.database.models.decision.scenario import Scenario

from app.modules.decision.decision.repository import DecisionRepository
from app.modules.decision.decision.schemas import (
    DecisionCreate,
    DecisionUpdate,
)

class DecisionService:

    def __init__(
            self,
            repository: DecisionRepository,
            session: AsyncSession,
    ):
        self.repository = repository
        self.session = session

    async def create_decision(
            self,
            data: DecisionCreate,
            organization_id: UUID,
            created_by: UUID,
    ) ->  Decision:

        result = await self.session.execute(
            select(Scenario).where(
                Scenario.id == data.scenario_id,
                Scenario.organization_id == organization_id
            )
        )

        scenario = result.scalar_one_or_none()

        if scenario is None:
            raise ValueError(
        "Scenario not found for this oragmnization"
        )

        decision = Decision(
            scenario_id = data.scenario_id,
            organization_id=organization_id,
            title=data.title,
            description=data.description,
            decision_type=data.decision_type,
            created_by=created_by
        )

        return await self.repository.create(decision)

    async def get_decision(
            self,
            decision_id:UUID,
            organization_id:UUID,

    ) -> Decision | None:

        return await self.repository.get_by_id(
            decision_id=decision_id,
            organization_id=organization_id,
        )

    async def list_decisions(
        self,
        organization_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Decision]:

        return await self.repository.list(
            organization_id=organization_id,
            skip=skip,
            limit=limit

        )

    async def update_decision(
            self,
            decision_id:UUID,
            data: DecisionUpdate,
            organization_id:UUID,
    ) -> Decision | None:

        decision =  await self.repository.get_by_id(
            decision_id=decision_id,
            organization_id=organization_id,
        )

        if decision is None:
            return None

        update_data = data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(decision, field,value)

        return await self.repository.update(decision)

    async def delete_decision(
            self,
            decision_id:UUID,
            organization_id:UUID,
    ) -> bool:

        decision =  await self.repository.get_by_id(
            decision_id=decision_id,
            organization_id=organization_id,
        )

        if decision is None:
            return False

        await self.repository.delete(decision)

        return True

    