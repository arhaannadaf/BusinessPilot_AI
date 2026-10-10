from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.data.data_source import DataSource


class DataSourceRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        data_source: DataSource,
    ) -> DataSource:
        self.session.add(data_source)
        await self.session.flush()
        await self.session.refresh(data_source)

        return data_source

    async def get_by_id(
        self,
        data_source_id: UUID,
    ) -> DataSource | None:
        result = await self.session.execute(
            select(DataSource).where(
                DataSource.id == data_source_id
            )
        )

        return result.scalar_one_or_none()

    async def list_by_organization(
        self,
        organization_id: UUID,
    ) -> list[DataSource]:
        result = await self.session.execute(
            select(DataSource)
            .where(
                DataSource.organization_id == organization_id
            )
            .order_by(DataSource.created_at.desc())
        )

        return list(result.scalars().all())

    async def update(
        self,
        data_source: DataSource,
    ) -> DataSource:
        await self.session.flush()
        await self.session.refresh(data_source)

        return data_source