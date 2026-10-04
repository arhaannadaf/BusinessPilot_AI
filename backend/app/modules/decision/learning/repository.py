from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.decision.learning.decision_learning import (
    DecisionLearning,
)


class DecisionLearningRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        decision_id: UUID,
        learning_type: str,
        insight: str,
    ) -> DecisionLearning:

        learning = DecisionLearning(
            decision_id=decision_id,
            learning_type=learning_type,
            insight=insight,
        )

        self.session.add(learning)
        await self.session.flush()

        return learning

    async def get_by_id(
        self,
        learning_id: UUID,
    ) -> DecisionLearning | None:

        result = await self.session.execute(
            select(DecisionLearning).where(
                DecisionLearning.id == learning_id
            )
        )

        return result.scalar_one_or_none()

    async def get_by_decision(
        self,
        decision_id: UUID,
    ) -> list[DecisionLearning]:

        result = await self.session.execute(
            select(DecisionLearning)
            .where(
                DecisionLearning.decision_id == decision_id
            )
            .order_by(
                DecisionLearning.created_at.desc()
            )
        )

        return list(result.scalars().all())