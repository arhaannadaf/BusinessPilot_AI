from uuid import UUID

from fastapi import(
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)

from app.api.dependencies.metric import get_decision_metric_service

from app.modules.decision.metric.schemas import(
    DecisionMetricUpdate,
    DecisionMetricCreate,
    DecisionMetricResponse,
)

from app.modules.decision.metric.service import DecisionMetricService

router = APIRouter(
    prefix="/decision-metrics",
    tags=["Decision Metrics"]
)

@router.post(
    "",
    response_model=DecisionMetricResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_decision_metric(
    data: DecisionMetricCreate,
    service: DecisionMetricService =Depends(get_decision_metric_service),

): 
    organization_id = UUID(
        "f98e1fc6-ca56-488e-988d-2fbace1c7640"
    )

    try:
        return await service.create_metric(
            data=data,
            organization_id=organization_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

@router.get(
    "/option/{decision_option_id}",
    response_model=list[DecisionMetricResponse]
)
async def list_decision_metrics(
    decision_option_id: UUID,
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    service: DecisionMetricService = Depends(
        get_decision_metric_service
    ),
):
    organization_id = UUID(
        "f98e1fc6-ca56-488e-988d-2fbace1c7640"
    )

    skip = (page - 1) * page_size

    return await service.list_metrics(
        decision_option_id=decision_option_id,
        organization_id=organization_id,
        skip=skip,
        limit=page_size,
    )

@router.get(
     "/{decision_option_id}/{metric_id}",
    response_model=DecisionMetricResponse,
)
async def get_decision_metric(
    decision_option_id: UUID,
    metric_id: UUID,
    service: DecisionMetricService = Depends(
        get_decision_metric_service
    ),
):
    organization_id = UUID(
        "f98e1fc6-ca56-488e-988d-2fbace1c7640"
    )

    metric = await service.get_metric(
        metric_id=metric_id,
        decision_option_id=decision_option_id,
        organization_id=organization_id,
    )

    if metric is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Decision metric not found",
        )

    return metric

@router.patch(
    "/{decision_option_id}/{metric_id}",
    response_model=DecisionMetricResponse,
)
async def update_decision_metric(
    decision_option_id: UUID,
    metric_id: UUID,
    data: DecisionMetricUpdate,
    service: DecisionMetricService = Depends(
        get_decision_metric_service
    ),
):
    organization_id = UUID(
        "f98e1fc6-ca56-488e-988d-2fbace1c7640"
    )

    metric = await service.update_metric(
        metric_id=metric_id,
        decision_option_id=decision_option_id,
        data=data,
        organization_id=organization_id,
    )

    if metric is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Decision metric not found",
        )

    return metric

@router.delete(
    "/{decision_option_id}/{metric_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_decision_metric(
    decision_option_id: UUID,
    metric_id: UUID,
    service: DecisionMetricService = Depends(
        get_decision_metric_service
    ),
):
    organization_id = UUID(
        "f98e1fc6-ca56-488e-988d-2fbace1c7640"
    )

    deleted = await service.delete_metric(
        metric_id=metric_id,
        decision_option_id=decision_option_id,
        organization_id=organization_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Decision metric not found",
        )

    return None