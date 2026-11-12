from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies.auth import get_current_actor
from app.api.dependencies.scenario import get_scenario_engine_service, get_scenario_service
from app.modules.decision.scenario.engine.schemas import (
    ScenarioEvaluationRequest,
    ScenarioEvaluationResult,
)
from app.modules.decision.scenario.engine.service import ScenarioEngineService
from app.modules.decision.scenario.schemas import (
    ScenarioCreate,
    ScenarioResponse,
    ScenarioUpdate,
)
from app.modules.decision.scenario.service import ScenarioService
from app.modules.identity.schemas import CurrentActor

router = APIRouter(
    prefix="/scenarios",
    tags=["Scenarios"]

)

@router.post(
    "",
    response_model=ScenarioResponse,
    status_code=status.HTTP_201_CREATED,
)

async def create_scenario(
    data: ScenarioCreate,
    service: ScenarioService = Depends(get_scenario_service),
    actor: CurrentActor = Depends(get_current_actor),
):
    return await service.create_scenario(
        data=data,
        organization_id=actor.organization_id,
        created_by=actor.user_id,
    ) 

@router.get(
    "",
    response_model=list[ScenarioResponse],
)
async def list_scenarios(
    page: int = Query(default=1,ge=1),
    page_size: int = Query(default=20,ge=1,le=100),
    service:ScenarioService = Depends(get_scenario_service),
    actor: CurrentActor = Depends(get_current_actor),
):
    skip = (page -1 ) * page_size

    return await service.list_scenarios(
        organization_id=actor.organization_id,
        skip=skip,
        limit=page_size,
    )

@router.get(
    "/{scenario_id}",
    response_model=ScenarioResponse,
)
async def get_scenario(
    scenario_id: UUID,
    service: ScenarioService = Depends(get_scenario_service),
    actor: CurrentActor = Depends(get_current_actor),
):
    scenario = await service.get_scenario(
        scenario_id=scenario_id,
        organization_id=actor.organization_id
    )

    if scenario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sceanrio not found"
        )

    return scenario

@router.patch(
    "/{scenario_id}",
    response_model=ScenarioResponse,
)
async def update_scenario(
    scenario_id: UUID,
    data: ScenarioUpdate,
    service: ScenarioService = Depends(get_scenario_service),
    actor: CurrentActor = Depends(get_current_actor),
):
    scenario = await service.update_scenario(
        scenario_id=scenario_id,
        data=data,
        organization_id=actor.organization_id,
    )

    if scenario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found",
        )

    return scenario


@router.delete(
    "/{scenario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_scenario(
    scenario_id: UUID,
    service: ScenarioService = Depends(get_scenario_service),
    actor: CurrentActor = Depends(get_current_actor),
):
    deleted = await service.delete_scenario(
        scenario_id=scenario_id,
        organization_id=actor.organization_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found",
        )

    return None

@router.post(
    "/{scenario_id}/decisions/{decision_id}/evaluate",
    response_model=ScenarioEvaluationResult,
)
async def evaluate_scenario(
    scenario_id: UUID,
    decision_id: UUID,
    request: ScenarioEvaluationRequest,
    service: ScenarioEngineService = Depends(
        get_scenario_engine_service
    ),
    actor: CurrentActor = Depends(get_current_actor),
):
    if request.scenario_id != scenario_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Scenario ID in path and request body must match.",
        )

    return await service.evaluate_scenario(
        scenario_id=scenario_id,
        decision_id=decision_id,
        request=request,
        organization_id=actor.organization_id,
    )