from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)

from app.api.dependencies.recommendation import get_recommendation_service


from app.modules.decision.recommendation.schemas import (
    RecommendationCreate,
    RecommendationResponse,
    RecommendationUpdate,
)

from app.modules.decision.recommendation.service import RecommendationService

from app.modules.decision.recommendation.history_schemas import (
    RecommendationHistoryResponse,
)

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)

@router.post(
    "",
    response_model=RecommendationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_recommendation(
    data: RecommendationCreate,
    service: RecommendationService = Depends(
        get_recommendation_service
    ),
):

    # Temporary development organization.
    # Authentication will provide this later.
    organization_id = UUID(
        "f98e1fc6-ca56-488e-988d-2fbace1c7640"
    )

    try:
        return await service.create_recommendation(
            data=data,
            organization_id=organization_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
@router.post(
    "/generate",
    response_model=RecommendationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def generate_recommendation(
    decision_id: UUID,
    weights: dict[str, float],
    learning_weight: float = 0.0,
    service: RecommendationService = Depends(get_recommendation_service),
):
    try:
        return await service.generate_recommendation(
        decision_id=decision_id,
        organization_id="f98e1fc6-ca56-488e-988d-2fbace1c7640",
        weights=weights,
        learning_weight=learning_weight,
    )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
@router.get(
    "/{decision_id}/{recommendation_id}/history",
    response_model=list[RecommendationHistoryResponse],
)
async def list_recommendation_history(
    decision_id: UUID,
    recommendation_id: UUID,
    service: RecommendationService = Depends(
        get_recommendation_service
    ),
):
    history = await service.list_recommendation_history(
        recommendation_id=recommendation_id,
        decision_id=decision_id,
        organization_id="f98e1fc6-ca56-488e-988d-2fbace1c7640",
    )

    if history is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found.",
        )

    return history


@router.get(
    "/decision/{decision_id}",
    response_model=list[RecommendationResponse],
)
async def list_recommendations(
    decision_id: UUID,
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    service: RecommendationService = Depends(
        get_recommendation_service
    ),
):

    organization_id = UUID(
        "f98e1fc6-ca56-488e-988d-2fbace1c7640"
    )

    skip = (page - 1) * page_size

    return await service.list_recommendations(
        decision_id=decision_id,
        organization_id=organization_id,
        skip=skip,
        limit=page_size,
    )

@router.get(
    "/{decision_id}/{recommendation_id}",
    response_model=RecommendationResponse,
)
async def get_recommendation(
    decision_id: UUID,
    recommendation_id: UUID,
    service: RecommendationService = Depends(
        get_recommendation_service
    ),
):

    organization_id = UUID(
        "f98e1fc6-ca56-488e-988d-2fbace1c7640"
    )

    recommendation = await service.get_recommendation(
        recommendation_id=recommendation_id,
        decision_id=decision_id,
        organization_id=organization_id,
    )

    if recommendation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found",
        )

    return recommendation

@router.patch(
    "/{decision_id}/{recommendation_id}",
    response_model=RecommendationResponse,
)
async def update_recommendation(
    decision_id: UUID,
    recommendation_id: UUID,
    data: RecommendationUpdate,
    service: RecommendationService = Depends(
        get_recommendation_service
    ),
):

    organization_id = UUID(
        "f98e1fc6-ca56-488e-988d-2fbace1c7640"
    )

    recommendation = await service.update_recommendation(
        recommendation_id=recommendation_id,
        decision_id=decision_id,
        data=data,
        organization_id=organization_id,
    )

    if recommendation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found",
        )

    return recommendation

@router.delete(
    "/{decision_id}/{recommendation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_recommendation(
    decision_id: UUID,
    recommendation_id: UUID,
    service: RecommendationService = Depends(
        get_recommendation_service
    ),
):

    organization_id = UUID(
        "f98e1fc6-ca56-488e-988d-2fbace1c7640"
    )

    deleted = await service.delete_recommendation(
        recommendation_id=recommendation_id,
        decision_id=decision_id,
        organization_id=organization_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found",
        )

    return None