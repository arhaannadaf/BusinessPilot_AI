
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.modules.data.imports.repository import DataImportRepository
from app.modules.data.imports.staging_repository import StagingRowRepository
from app.modules.data.profiling.repository import DataProfileRepository
from app.modules.data.profiling.service import DataProfilingService
from app.modules.data.profiling.alert_repository import (
    DataQualityAlertRepository,
)

def get_data_profiling_service(
    session: AsyncSession = Depends(get_db),
) -> DataProfilingService:
    data_import_repository = DataImportRepository(session)
    staging_repository = StagingRowRepository(session)
    profile_repository = DataProfileRepository(session)
    alert_repository = DataQualityAlertRepository(session)

    return DataProfilingService(
        data_import_repository=data_import_repository,
        staging_repository=staging_repository,
        profile_repository=profile_repository,
        alert_repository=alert_repository,
    )
