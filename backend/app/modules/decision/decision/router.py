from uuid import UUID

from fastapi import(
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status
)

from app.api.dependencies.decision import get_decision_service

from app.modules.decision.decision.schemas import (
    DecisionUpdate,
    DecisionCreate,
    DecisionResponse,
)

from app.modules.decision.decision.service import DecisionService

router = APIRouter(
    prefix="/decisions",
    tags=["Decisions"],
)

@router.post(
    "",
    response_model=DecisionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_decision(
    data: DecisionCreate,
    service: DecisionService = Depends(
        get_decision_service
    ),
):

   # Temporary development context.
    organization_id = UUID(
            "f98e1fc6-ca56-488e-988d-2fbace1c7640"
        )
    created_by = UUID(
            "4421a369-a8e1-4e80-9de0-94e9913d0af5"
        )

    try:
        return await service.create_decision(
            data=data,
            organization_id=organization_id,
            created_by=created_by,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

@router.get(
    "",
    response_model=list[DecisionResponse],
    )

async def list_decisions(
    page: int = Query(
        default=1,
        ge=1,    
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    service: DecisionService = Depends(
        get_decision_service
    ),
):
    organization_id = UUID(
         "f98e1fc6-ca56-488e-988d-2fbace1c7640"   
    )

    skip = (page - 1) * page_size

    return await service.list_decisions(
        organization_id=organization_id,
        skip=skip,
        limit=page_size,
    )

@router.get(
    "/{decision_id}",
    response_model=DecisionResponse,
)

async def get_decision(
    decision_id: UUID,
    service: DecisionService = Depends(
        get_decision_service
    ),
):

    organization_id = UUID(
         "f98e1fc6-ca56-488e-988d-2fbace1c7640"   
    )

    decision = await service.get_decision(
        decision_id=decision_id,
        organization_id=organization_id
    )

    if decision_id is None:
        raise HTTPException(
            status_code==status.HTTP_404_NOT_FOUND,
            detail="Decision Not found",
        )

    return decision


@router.patch(
    "/{decision_id}",
    response_model=DecisionResponse,
)

async def update_decision(
    decision_id: UUID,
    data: DecisionUpdate,
    service: DecisionService =Depends(
        get_decision_service
    )
):

    organization_id = UUID(
         "f98e1fc6-ca56-488e-988d-2fbace1c7640"   
    )

    decision = await service.update_decision(
        decision_id=decision_id,
        data=data,
        organization_id=organization_id
    )

    if decision is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Decision Not found",
        )

    return decision

@router.delete(
    "/{decision_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_decision(
    decision_id: UUID,
    service: DecisionService = Depends(
        get_decision_service,
    ),
):

    organization_id = UUID(
         "f98e1fc6-ca56-488e-988d-2fbace1c7640"   
    )

    deleted = await service.delete_decision(
        decision_id=decision_id,
        organization_id=organization_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Decision not found",
        )

    return None