from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.modules.data.source.repository import DataSourceRepository
from app.modules.data.source.service import DataSourceService


def get_data_source_service(
    session: AsyncSession = Depends(get_db),
) -> DataSourceService:

    repository = DataSourceRepository(session)

    return DataSourceService(
        repository=repository,
    )