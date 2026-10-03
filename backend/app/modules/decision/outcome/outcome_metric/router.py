from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.outcome_metric import (
    get_outcome_metric_service,
)
from app.modules.decision.outcome.outcome_metric.schemas import (
    OutcomeMetricCreate,
    OutcomeMetricResponse,
)
from app.modules.decision.outcome.outcome_metric.service import (
    OutcomeMetricService,
)


router = APIRouter(
    prefix="/outcome-metrics",
    tags=["Outcome Metrics"],
)


@router.post(
    "",
    response_model=OutcomeMetricResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_outcome_metric(
    data: OutcomeMetricCreate,
    service: OutcomeMetricService = Depends(
        get_outcome_metric_service
    ),
):
    try:
        return await service.create_metric(
        outcome_id=data.outcome_id,
        metric_name=data.metric_name,
        actual_value=data.actual_value,
        unit=data.unit,
    )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "/{metric_id}",
    response_model=OutcomeMetricResponse,
)
async def get_outcome_metric(
    metric_id: UUID,
    service: OutcomeMetricService = Depends(
        get_outcome_metric_service
    ),
):
    try:
        return await service.get_metric(metric_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.get(
    "/outcome/{outcome_id}",
    response_model=list[OutcomeMetricResponse],
)
async def get_outcome_metrics(
    outcome_id: UUID,
    service: OutcomeMetricService = Depends(
        get_outcome_metric_service
    ),
):
    try:
        return await service.get_metrics_by_outcome(
            outcome_id
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )