from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.decision.recommendation.recommendation_history import (
    RecommendationHistory,
)


class RecommendationHistoryRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_by_recommendation(
        self,
        recommendation_id: UUID,
    ) -> list[RecommendationHistory]:

        result = await self.session.execute(
            select(RecommendationHistory)
            .where(
                RecommendationHistory.recommendation_id
                == recommendation_id
            )
            .order_by(
                RecommendationHistory.created_at.asc()
            )
        )

        return list(result.scalars().all())