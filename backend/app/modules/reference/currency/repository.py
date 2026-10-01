from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.reference.currency import Currency


class CurrencyRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(
        self,
        *,
        is_active: bool | None = True,
    ) -> list[Currency]:

        query = select(Currency)

        if is_active is not None:
            query = query.where(
                Currency.is_active == is_active
            )

        query = query.order_by(Currency.name)

        result = await self.db.execute(query)

        return result.scalars().all()