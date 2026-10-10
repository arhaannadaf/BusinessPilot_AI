from uuid import UUID

from app.database.models.data.data_source import DataSource
from app.modules.data.source.repository import DataSourceRepository
from app.modules.data.source.schemas import DataSourceCreate


class DataSourceService:

    def __init__(
        self,
        repository: DataSourceRepository,
    ):
        self.repository = repository

    async def create(
        self,
        data: DataSourceCreate,
    ) -> DataSource:
        data_source = DataSource(
            organization_id=data.organization_id,
            name=data.name,
            source_type=data.source_type,
            description=data.description,
            connection_config=data.connection_config,
            is_active=True,
        )

        return await self.repository.create(data_source)

    async def get_by_id(
        self,
        data_source_id: UUID,
    ) -> DataSource:
        data_source = await self.repository.get_by_id(
            data_source_id
        )

        if not data_source:
            raise ValueError(
                "Data source not found."
            )

        return data_source

    async def list_by_organization(
        self,
        organization_id: UUID,
    ) -> list[DataSource]:
        return await self.repository.list_by_organization(
            organization_id
        )