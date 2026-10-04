from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.decision_feedback import (
    get_decision_feedback_service,
)
from app.modules.decision.feedback.schemas import (
    DecisionFeedbackCreate,
    DecisionFeedbackUpdate,
    DecisionFeedbackResponse,
)
from app.modules.decision.feedback.service import (
    DecisionFeedbackService,
)
from app.api.dependencies.decision_feedback_analysis import (
    get_decision_feedback_analysis_service,
)
from app.modules.decision.feedback.analysis_service import (
    DecisionFeedbackAnalysisService,
)


router = APIRouter(
    prefix="/decision-feedback",
    tags=["Decision Feedback"],
)


@router.post(
    "",
    response_model=DecisionFeedbackResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_feedback(
    data: DecisionFeedbackCreate,
    service: DecisionFeedbackService = Depends(
        get_decision_feedback_service
    ),
):
    try:
        feedback = await service.create_feedback(
            outcome_id=data.outcome_id,
            overall_performance=data.overall_performance,
            summary=data.summary,
        )

        return feedback

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "/outcome/{outcome_id}",
    response_model=DecisionFeedbackResponse,
)
async def get_feedback_by_outcome(
    outcome_id: UUID,
    service: DecisionFeedbackService = Depends(
        get_decision_feedback_service
    ),
):
    try:
        return await service.get_feedback_by_outcome(
            outcome_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
    )

@router.put(
    "/{feedback_id}",
    response_model=DecisionFeedbackResponse,
)
async def update_feedback(
    feedback_id: UUID,
    data: DecisionFeedbackUpdate,
    service: DecisionFeedbackService = Depends(
        get_decision_feedback_service
    ),
):
    try:
        feedback = await service.update_feedback(
            feedback_id=feedback_id,
            overall_performance=data.overall_performance,
            summary=data.summary,
        )

        return feedback

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
@router.post(
    "/generate/{outcome_id}",
    response_model=DecisionFeedbackResponse,
)
async def generate_feedback(
    outcome_id: UUID,
    service: DecisionFeedbackAnalysisService = Depends(
        get_decision_feedback_analysis_service
    ),
):
    try:
        return await service.generate_feedback(
            outcome_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    