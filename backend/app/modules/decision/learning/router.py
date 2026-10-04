from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.decision_learning import (
    get_decision_learning_service,
)
from app.modules.decision.learning.schemas import (
    DecisionLearningCreate,
    DecisionLearningResponse,
)
from app.modules.decision.learning.service import (
    DecisionLearningService,
)


router = APIRouter(
    prefix="/decision-learning",
    tags=["Decision Learning"],
)


@router.post(
    "/generate",
    response_model=list[DecisionLearningResponse],
    status_code=status.HTTP_201_CREATED,
)
async def generate_learning(
    data: DecisionLearningCreate,
    service: DecisionLearningService = Depends(
        get_decision_learning_service
    ),
):
    try:
        return await service.generate_learning(
            decision_id=data.decision_id,
            outcome_id=data.outcome_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "/decision/{decision_id}",
    response_model=list[DecisionLearningResponse],
)
async def get_learning_by_decision(
    decision_id: UUID,
    service: DecisionLearningService = Depends(
        get_decision_learning_service
    ),
):
    learning_records = (
        await service.learning_repository.get_by_decision(
            decision_id
        )
    )

    return learning_records