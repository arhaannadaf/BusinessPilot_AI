from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies.auth import get_current_actor
from app.api.dependencies.decision import get_decision_service
from app.modules.decision.decision.schemas import (
    DecisionCreate,
    DecisionResponse,
    DecisionUpdate,
)
from app.modules.decision.decision.service import DecisionService
from app.modules.identity.schemas import CurrentActor

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
    actor: CurrentActor = Depends(get_current_actor),
):
    try:
        return await service.create_decision(
            data=data,
            organization_id=actor.organization_id,
            created_by=actor.user_id,
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
    actor: CurrentActor = Depends(get_current_actor),
):
    skip = (page - 1) * page_size

    return await service.list_decisions(
        organization_id=actor.organization_id,
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
    actor: CurrentActor = Depends(get_current_actor),
):
    decision = await service.get_decision(
        decision_id=decision_id,
        organization_id=actor.organization_id
    )

    if decision_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
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
    ),
    actor: CurrentActor = Depends(get_current_actor),
):
    decision = await service.update_decision(
        decision_id=decision_id,
        data=data,
        organization_id=actor.organization_id
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
    actor: CurrentActor = Depends(get_current_actor),
):
    deleted = await service.delete_decision(
        decision_id=decision_id,
        organization_id=actor.organization_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Decision not found",
        )

    return None