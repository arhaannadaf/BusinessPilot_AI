from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.reference.country import Country

class CountryRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(
            self,
            *,
            is_active: bool | None = True
    ) -> list[Country]:

        query = select(Country)

        if is_active is not None:
            query = query.where(
                Country.is_active == is_active
            )

        query = query.order_by(Country.name)

        result = await self.db.execute(query)

        return result.scalars().all()