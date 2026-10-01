from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.reference.company_size import CompanySize

class CompanySizeRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(
            self,
            *,
            is_active: bool | None = True,

    ) -> list[CompanySize]:

        query = select(CompanySize)

        if is_active is not None:
            query = query.where(
                CompanySize.is_active == is_active
            )

        query = query.order_by(CompanySize.name)

        result = await self.db.execute(query)

        return result.scalars().all()