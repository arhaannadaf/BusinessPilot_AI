from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.modules.data.imports.repository import DataImportRepository
from app.modules.data.imports.service import DataImportService
from app.modules.data.source.repository import DataSourceRepository
from app.modules.data.storage.local_storage import LocalStorage
from app.modules.data.imports.staging_repository import (
    StagingRowRepository,
)

def get_data_import_service(
    session: AsyncSession = Depends(get_db),
) -> DataImportService:

    repository = DataImportRepository(session)
    data_source_repository = DataSourceRepository(session)
    storage = LocalStorage()
    staging_repository = StagingRowRepository(session)

    return DataImportService(
        repository=repository,
        data_source_repository=data_source_repository,
        storage=storage,
        staging_repository=staging_repository,
    )