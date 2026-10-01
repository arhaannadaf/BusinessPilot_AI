from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies.scenario import get_scenario_service
from app.modules.decision.scenario.schemas import(
    ScenarioCreate,
    ScenarioUpdate,
    ScenarioResponse,
)
from app.modules.decision.scenario.service import ScenarioService

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
    service: ScenarioService = Depends(get_scenario_service)
):
   # Temporary development values.
    # Authentication will provide these later.
    organization_id = UUID(
        "f98e1fc6-ca56-488e-988d-2fbace1c7640"
    )
    created_by = UUID(
        "4421a369-a8e1-4e80-9de0-94e9913d0af5"
    )

    return await service.create_scenario(
        data=data,
        organization_id=organization_id,
        created_by=created_by,
    ) 

@router.get(
    "",
    response_model=list[ScenarioResponse],
)
async def list_scenarios(
    page: int = Query(default=1,ge=1),
    page_size: int = Query(default=20,ge=1,le=100),
    service:ScenarioService = Depends(get_scenario_service),
):
    organization_id = UUID(

        "f98e1fc6-ca56-488e-988d-2fbace1c7640"

    )
    skip = (page -1 ) * page_size

    return await service.list_scenarios(
        organization_id=organization_id,
        skip=skip,
        limit=page_size,
    )

@router.get(
    "/{scenario_id}",
    response_model=ScenarioResponse,
)
async def get_scenario(
    scenario_id: UUID,
    service: ScenarioService = Depends(get_scenario_service)
):
    organization_id = UUID(
         "f98e1fc6-ca56-488e-988d-2fbace1c7640"

    )
    scenario = await service.get_scenario(
        scenario_id=scenario_id,
        organization_id=organization_id
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
):
    organization_id = UUID(
        "f98e1fc6-ca56-488e-988d-2fbace1c7640"
    )

    scenario = await service.update_scenario(
        scenario_id=scenario_id,
        data=data,
        organization_id=organization_id,
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
):
    organization_id = UUID(
        "f98e1fc6-ca56-488e-988d-2fbace1c7640"
    )

    deleted = await service.delete_scenario(
        scenario_id=scenario_id,
        organization_id=organization_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found",
        )

    return None