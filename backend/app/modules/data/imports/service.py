import csv

from pathlib import Path
from uuid import UUID
from fastapi import UploadFile


from app.database.models.data.data_import import DataImport
from app.modules.data.imports.repository import DataImportRepository
from app.modules.data.source.repository import DataSourceRepository
from app.modules.data.storage.local_storage import LocalStorage
from app.modules.data.imports.processor import CSVProcessor

from app.database.models.data.staging_row import StagingRow
from app.modules.data.imports.staging_repository import (
    StagingRowRepository,
)


class DataImportService:

    def __init__(
        self,
        repository: DataImportRepository,
        data_source_repository: DataSourceRepository,
        storage: LocalStorage,
        staging_repository: StagingRowRepository,
        
    ):
        self.repository = repository
        self.data_source_repository = data_source_repository
        self.storage = storage
        self.staging_repository = staging_repository
        self.processor = CSVProcessor()

    async def create(
        self,
        data_source_id: UUID,
        file: UploadFile,
    ) -> DataImport:
        data_source = await self.data_source_repository.get_by_id(
            data_source_id
        )

        if not data_source:
            raise ValueError("Data source not found.")

        if not data_source.is_active:
            raise ValueError("Data source is inactive.")

        stored_path, file_size_bytes = await self.storage.save_upload(
            file
        )

        data_import = DataImport(
            data_source_id=data_source_id,
            file_name=Path(file.filename or "").name,
            stored_path=stored_path,
            file_size_bytes=file_size_bytes,
            status="PENDING",
            total_rows=0,
            successful_rows=0,
            failed_rows=0,
        )

        try:
            return await self.repository.create(data_import)
        except Exception:
            Path(stored_path).unlink(missing_ok=True)
            raise

    async def get_by_id(
        self,
        import_id: UUID,
    ) -> DataImport:
        data_import = await self.repository.get_by_id(
            import_id
        )

        if not data_import:
            raise ValueError(
                "Data import not found."
            )

        return data_import

    async def list_by_data_source(
        self,
        data_source_id: UUID,
    ) -> list[DataImport]:
        data_source = await self.data_source_repository.get_by_id(
            data_source_id
        )

        if not data_source:
            raise ValueError(
                "Data source not found."
            )

        return await self.repository.list_by_data_source(
            data_source_id
        )

    
    async def process_import(
        self,
        import_id: UUID,
    ) -> DataImport:
        data_import = await self.get_by_id(import_id)

        if data_import.status != "PENDING":
            raise ValueError(
                "Only PENDING imports can be processed."
            )

        if not data_import.stored_path:
            raise ValueError(
                "Import has no stored file path."
            )

        data_import.status = "PROCESSING"
        await self.repository.update(data_import)

        try:
            result = self.processor.process(
                data_import.stored_path
            )

            staged_rows = []

            with open(
                data_import.stored_path,
                "r",
                encoding="utf-8-sig",
                newline="",
            ) as csv_file:
                reader = csv.DictReader(csv_file)

                columns = [
                    column.strip()
                    for column in reader.fieldnames
                ]

                for row_number, row in enumerate(reader, start=1):
                    if None in row or any(
                        value is None for value in row.values()
                    ):
                        continue

                    row_data = {
                        column: row[original_column]
                        for column, original_column in zip(
                            columns,
                            reader.fieldnames,
                        )
                    }

                    staged_rows.append(
                        StagingRow(
                            data_import_id=data_import.id,
                            data_source_id=data_import.data_source_id,
                            row_number=row_number,
                            row_data=row_data,
                        )
                    )

            await self.staging_repository.create_many(
                staged_rows
            )

            data_import.total_rows = result["total_rows"]
            data_import.successful_rows = result["successful_rows"]
            data_import.failed_rows = result["failed_rows"]
            data_import.status = (
                "COMPLETED"
                if result["failed_rows"] == 0
                else "FAILED"
            )
            data_import.error_message = None

        except (ValueError, FileNotFoundError) as exc:
            data_import.status = "FAILED"
            data_import.error_message = str(exc)

        await self.repository.update(data_import)

        return data_import
