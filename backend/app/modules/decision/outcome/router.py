from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.outcome import get_outcome_service
from app.modules.decision.outcome.schemas import (
    OutcomeCreate,
    OutcomeResponse,
)
from app.modules.decision.outcome.service import OutcomeService


router = APIRouter(
    prefix="/outcomes",
    tags=["Outcomes"],
)


@router.post(
    "",
    response_model=OutcomeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_outcome(
    data: OutcomeCreate,
    service: OutcomeService = Depends(get_outcome_service),
):
    try:
        return await service.create_outcome(
            execution_id=data.execution_id,
            summary=data.summary,
            meta_data=data.meta_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "/{outcome_id}",
    response_model=OutcomeResponse,
)
async def get_outcome(
    outcome_id: UUID,
    service: OutcomeService = Depends(get_outcome_service),
):
    try:
        return await service.get_outcome(outcome_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.get(
    "/execution/{execution_id}",
    response_model=OutcomeResponse,
)
async def get_outcome_by_execution(
    execution_id: UUID,
    service: OutcomeService = Depends(get_outcome_service),
):
    try:
        return await service.get_outcome_by_execution(
            execution_id
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )