from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.data.data_import import DataImport


class DataImportRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        data_import: DataImport,
    ) -> DataImport:
        self.session.add(data_import)
        await self.session.flush()
        await self.session.refresh(data_import)

        return data_import

    async def get_by_id(
        self,
        import_id: UUID,
    ) -> DataImport | None:
        result = await self.session.execute(
            select(DataImport).where(
                DataImport.id == import_id
            )
        )

        return result.scalar_one_or_none()

    async def list_by_data_source(
        self,
        data_source_id: UUID,
    ) -> list[DataImport]:
        result = await self.session.execute(
            select(DataImport)
            .where(
                DataImport.data_source_id == data_source_id
            )
            .order_by(DataImport.created_at.desc())
        )

        return list(result.scalars().all())

    async def update(
        self,
        data_import: DataImport,
    ) -> DataImport:
        await self.session.flush()
        await self.session.refresh(data_import)

        return data_import