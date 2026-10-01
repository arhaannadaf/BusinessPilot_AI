from uuid import UUID

from app.database.models.decision.scenario import Scenario

from app.modules.decision.scenario.repository import ScenarioRepository
from app.modules.decision.scenario.schemas import (
    ScenarioCreate,
    ScenarioUpdate,
)

class ScenarioService:

    def __init__(
            self,
            repository:ScenarioRepository
    ):
        self.repository = repository

    async def create_scenario(
            self,
            data:ScenarioCreate,
            organization_id: UUID,
            created_by: UUID,
    ) -> Scenario:

        scenario = Scenario(
            organization_id=organization_id,
            name=data.name,
            description=data.description,
            scenario_type=data.scenario_type,
            assumptions=data.assumptions,
            created_by=created_by
        )
        return await self.repository.create(scenario)

    async def get_scenario(
            self,
            scenario_id:UUID,
            organization_id:UUID,
    ) -> Scenario | None:

        return await self.repository.get_by_id(
            scenario_id=scenario_id,
            organization_id=organization_id,
        )
    async def list_scenarios(
            self,
            organization_id : UUID,
            skip: int = 0,
            limit: int = 100,
    ) -> list[Scenario]:
        return await self.repository.list(
            organization_id=organization_id,
            skip=skip,
            limit=limit,
        )
        

    async def update_scenario(
            self,
            scenario_id:UUID,
            data: ScenarioUpdate,
            organization_id: UUID,
    ) -> Scenario | None:

        scenario = await self.repository.get_by_id(scenario_id, organization_id)

        if scenario is None:
            return None

        update_data = data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(scenario, field, value)

        return await self.repository.update(scenario)


    async def delete_scenario(
            self,
            scenario_id: UUID,
            organization_id: UUID,
    ) -> bool:
        scenario =await self.repository.get_by_id(scenario_id,organization_id)

        if scenario is None:
            return False

        await self.repository.delete(scenario)
        return True