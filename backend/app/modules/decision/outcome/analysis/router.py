from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.modules.decision.outcome.analysis.schemas import (
    OutcomeAnalysisResponse,
)
from app.modules.decision.outcome.analysis.service import (
    OutcomeAnalysisService,
)
from app.api.dependencies.outcome_analysis import (
    get_outcome_analysis_service,
)


router = APIRouter(
    prefix="/outcome-analysis",
    tags=["Outcome Analysis"],
)


@router.get(
    "/{outcome_id}",
    response_model=OutcomeAnalysisResponse,
)
async def analyze_outcome(
    outcome_id: UUID,
    service: OutcomeAnalysisService = Depends(
        get_outcome_analysis_service
    ),
):
    try:
        metrics = await service.analyze_outcome(
            outcome_id
        )

        return OutcomeAnalysisResponse(
            outcome_id=outcome_id,
            metrics=metrics,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )