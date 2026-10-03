from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.modules.decision.scenario.repository import ScenarioRepository
from app.modules.decision.scenario.service import ScenarioService
from app.modules.decision.scenario.engine.service import ScenarioEngineService

def get_scenario_repository(
        session: AsyncSession = Depends(get_db),
) -> ScenarioRepository:
    return ScenarioRepository(session)

def get_scenario_service(
        repository: ScenarioRepository = Depends(
            get_scenario_repository
        ),
) -> ScenarioService:
    return ScenarioService(repository)

def get_scenario_engine_service(
    session: AsyncSession = Depends(get_db),
) -> ScenarioEngineService:
    return ScenarioEngineService(session)