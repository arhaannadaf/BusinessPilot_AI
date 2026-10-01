from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.decision.recommendation import Recommendation


class RecommendationRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        recommendation: Recommendation,
    ) -> Recommendation:

        self.session.add(recommendation)

        await self.session.flush()
        await self.session.refresh(recommendation)

        return recommendation

    async def get_by_id(
        self,
        recommendation_id: UUID,
        decision_id: UUID,
    ) -> Recommendation | None:

        result = await self.session.execute(
            select(Recommendation).where(
                Recommendation.id == recommendation_id,
                Recommendation.decision_id == decision_id,
            )
        )

        return result.scalar_one_or_none()

    async def list_by_decision(
        self,
        decision_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Recommendation]:

        result = await self.session.execute(
            select(Recommendation)
            .where(
                Recommendation.decision_id == decision_id
            )
            .order_by(
                Recommendation.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
        )

        return list(result.scalars().all())

    async def update(
        self,
        recommendation: Recommendation,
    ) -> Recommendation:

        await self.session.flush()
        await self.session.refresh(recommendation)

        return recommendation

    async def delete(
        self,
        recommendation: Recommendation,
    ) -> None:

        await self.session.delete(recommendation)
        await self.session.flush()
        
    async def get_active_by_decision(
        self,
        decision_id: UUID,
    ) -> Recommendation | None:
        result = await self.session.execute(
            select(Recommendation)
            .where(
                Recommendation.decision_id == decision_id,
                Recommendation.is_active.is_(True),
            )
            .order_by(Recommendation.created_at.desc())
        )

        return result.scalars().first()