
from uuid import UUID

from app.modules.data.imports.repository import DataImportRepository
from app.modules.data.imports.staging_repository import StagingRowRepository
from app.modules.data.profiling.processor import DataProfilingProcessor
from app.modules.data.profiling.repository import DataProfileRepository


class DataProfilingService:
    """Coordinate profiling and persist every profiling run."""

    def __init__(
        self,
        data_import_repository: DataImportRepository,
        staging_repository: StagingRowRepository,
        profile_repository: DataProfileRepository,
    ):
        self.data_import_repository = data_import_repository
        self.staging_repository = staging_repository
        self.profile_repository = profile_repository
        self.processor = DataProfilingProcessor()

    async def profile_import(self, import_id: UUID) -> dict:
        # 1. Verify that the import exists.
        data_import = await self.data_import_repository.get_by_id(
            import_id
        )

        if data_import is None:
            raise ValueError("Data import not found.")

        # 2. Retrieve staged rows.
        staged_rows = await self.staging_repository.list_by_import(
            import_id
        )

        rows = [staged_row.row_data for staged_row in staged_rows]

        # 3. Generate the profiling report.
        report = self.processor.profile(rows)

        # 4. Add import metadata.
        report["import_id"] = str(data_import.id)
        report["data_source_id"] = str(data_import.data_source_id)
        report["file_name"] = data_import.file_name

        # 5. Persist this profiling run as a new record.
        profile = await self.profile_repository.create(
            data_import_id=data_import.id,
            report=report,
        )

        # 6. Return the report with its history record ID.
        report["profile_id"] = str(profile.id)
        report["profiled_at"] = profile.created_at.isoformat()

        return report
