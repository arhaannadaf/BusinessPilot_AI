from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.decision.decision import Decision
from app.database.models.decision.option import DecisionOption

from app.modules.decision.option.repository import(
    DecisionOptionRepository
)
from app.modules.decision.option.schemas import (
    DecisionOptionCreate,
    DecisionOptionUpdate,
)

class DecisionOptionService:
    def __init__(
            self,
            repository: DecisionOptionRepository,
            session: AsyncSession,
    ):
        self.repository = repository
        self.session = session

    async def create_option(
            self,
            data: DecisionOptionCreate,
            organization_id: UUID,
    ) -> DecisionOption:
        
        result = await self.session.execute(
            select(Decision).where(
                Decision.id == data.decision_id,
                Decision.organization_id == organization_id
            )
        )
        decision = result.scalar_one_or_none()

        if decision is None:
            raise ValueError(
                "Decision not found for this organization."
            )
        option = DecisionOption(
            decision_id = data.decision_id,
            name=data.name,
            description=data.description,
            parameters=data.parameters
        )

        return await self.repository.create(option)

    async def get_option(
            self,
            option_id: UUID,
            decision_id: UUID,
            organization_id: UUID,
    ) -> DecisionOption | None:

        result = await self.session.execute(
            select(Decision).where(
                Decision.id == decision_id,
                Decision.organization_id == organization_id,
            )
        )

        decision = result.scalar_one_or_none()

        if decision is None:
            return None

        return await self.repository.get_by_id(
            option_id=option_id,
            decision_id=decision_id,
        )

    async def list_options(
        self,
        decision_id: UUID,
        organization_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[DecisionOption]:

        result = await self.session.execute(
            select(Decision).where(
                Decision.id == decision_id,
                Decision.organization_id == organization_id,
            )
        )

        decision = result.scalar_one_or_none()

        if decision is None:
            return []

        return await self.repository.list_by_decision(
            decision_id=decision_id,
            skip=skip,
            limit=limit,
        )

    async def update_option(
        self,
        option_id: UUID,
        decision_id: UUID,
        data: DecisionOptionUpdate,
        organization_id: UUID,
    ) -> DecisionOption | None:

        option = await self.get_option(
            option_id=option_id,
            decision_id=decision_id,
            organization_id=organization_id,
        )

        if option is None:
            return None

        update_data = data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(option, field, value)

        return await self.repository.update(option)

    async def delete_option(
        self,
        option_id: UUID,
        decision_id: UUID,
        organization_id: UUID,
    ) -> bool:

        option = await self.get_option(
            option_id=option_id,
            decision_id=decision_id,
            organization_id=organization_id,
        )

        if option is None:
            return False

        await self.repository.delete(option)

        return True