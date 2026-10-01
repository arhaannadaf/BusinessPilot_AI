from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

from app.modules.decision.recommendation.repository import (
    RecommendationRepository,
)

from app.modules.decision.recommendation.service import (
    RecommendationService,
)


def get_recommendation_repository(
    session: AsyncSession = Depends(get_db),
) -> RecommendationRepository:

    return RecommendationRepository(session)


def get_recommendation_service(
    session: AsyncSession = Depends(get_db),
    repository: RecommendationRepository = Depends(
        get_recommendation_repository
    ),
) -> RecommendationService:

    return RecommendationService(
        repository=repository,
        session=session,
    )