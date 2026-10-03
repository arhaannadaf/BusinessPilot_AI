from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.execution import get_execution_service
from app.modules.decision.execution.schemas import (
    ExecutionCreate,
    ExecutionResponse,
    ExecutionUpdate,
)
from app.modules.decision.execution.service import ExecutionService


router = APIRouter(
    prefix="/executions",
    tags=["Executions"],
)


@router.post(
    "",
    response_model=ExecutionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_execution(
    data: ExecutionCreate,
    service: ExecutionService = Depends(get_execution_service),
):
    try:
        return await service.create_execution(
            recommendation_id=data.recommendation_id,
            executed_by=data.executed_by,
            execution_details=data.execution_details,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.patch(
    "/{execution_id}",
    response_model=ExecutionResponse,
)
async def update_execution(
    execution_id: UUID,
    data: ExecutionUpdate,
    service: ExecutionService = Depends(get_execution_service),
):
    try:
        execution = await service.update_execution(
            execution_id=execution_id,
            status_value=data.status,
            result=data.result,
            error_message=data.error_message,
            execution_details=data.execution_details,
            started_at=data.started_at,
            completed_at=data.completed_at,
        )

        if execution is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Execution not found.",
            )

        return execution

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )