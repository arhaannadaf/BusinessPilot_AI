from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.reference.company_status import CompanyStatus

class CompanyStatusRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(
            self,
            *,
            is_active: bool | None = True,

    ) -> list[CompanyStatus]:

        query = select(CompanyStatus)

        if is_active is not None:
            query = query.where(
                CompanyStatus.is_active == is_active
            )

        query = query.order_by(CompanyStatus.name)

        result = await self.db.execute(query)

        return result.scalars().all()