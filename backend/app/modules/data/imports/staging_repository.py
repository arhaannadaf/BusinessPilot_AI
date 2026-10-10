
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.data.staging_row import StagingRow


class StagingRowRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_many(
        self,
        rows: list[StagingRow],
    ) -> list[StagingRow]:
        if not rows:
            return []

        self.session.add_all(rows)
        await self.session.flush()

        return rows

    async def list_by_import(
        self,
        data_import_id: UUID,
    ) -> list[StagingRow]:
        result = await self.session.execute(
            select(StagingRow)
            .where(
                StagingRow.data_import_id == data_import_id
            )
            .order_by(StagingRow.row_number.asc())
        )

        return list(result.scalars().all())

    async def count_by_import(
        self,
        data_import_id: UUID,
    ) -> int:
        from sqlalchemy import func

        result = await self.session.execute(
            select(func.count(StagingRow.id)).where(
                StagingRow.data_import_id == data_import_id
            )
        )

        return result.scalar_one()
