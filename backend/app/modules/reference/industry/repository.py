from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.reference.industry import Industry

class IndustryRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(
            self,
            *,
            is_active: bool | None = True,

    ) -> list[Industry]:

        query = select(Industry)

        if is_active is not None:
            query = query.where(
                Industry.is_active == is_active
            )

        query = query.order_by(Industry.name)

        result = await self.db.execute(query)

        return result.scalars().all()