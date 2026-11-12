import csv
from pathlib import Path
from uuid import UUID

from fastapi import UploadFile

from app.database.models.data.data_import import DataImport
from app.database.models.data.staging_row import StagingRow
from app.modules.data.imports.excel_processor import ExcelProcessor
from app.modules.data.imports.mapping_engine import CANONICAL_FIELDS, suggest_mappings
from app.modules.data.imports.processor import CSVProcessor
from app.modules.data.imports.repository import DataImportRepository
from app.modules.data.imports.staging_repository import (
    StagingRowRepository,
)
from app.modules.data.source.repository import DataSourceRepository
from app.modules.data.storage.local_storage import LocalStorage


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
        self.excel_processor = ExcelProcessor()

    async def create(
        self,
        data_source_id: UUID,
        file: UploadFile,
        organization_id: UUID,
    ) -> DataImport:
        data_source = await self.data_source_repository.get_by_id(
            data_source_id,
            organization_id,
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
        organization_id: UUID,
    ) -> DataImport:
        data_import = await self.repository.get_by_id(
            import_id
        )

        if not data_import:
            raise ValueError(
                "Data import not found."
            )

        data_source = await self.data_source_repository.get_by_id(
            data_import.data_source_id,
            organization_id,
        )

        if not data_source:
            raise ValueError("Data import not found.")

        return data_import

    async def get_schema(
        self,
        import_id: UUID,
        organization_id: UUID,
    ) -> dict | None:
        data_import = await self.get_by_id(import_id, organization_id)

        if data_import.schema_metadata is None:
            return None

        return {
            "import_id": data_import.id,
            **data_import.schema_metadata,
        }

    async def discover_import_schema(
        self,
        import_id: UUID,
        organization_id: UUID,
    ) -> dict:
        data_import = await self.get_by_id(import_id, organization_id)
        if data_import.status != "PENDING":
            raise ValueError("Only PENDING imports can be discovered.")
        if not data_import.stored_path:
            raise ValueError("Import has no stored file path.")
        if Path(data_import.file_name).suffix.lower() not in {".xlsx", ".xlsm"}:
            raise ValueError("Workbook discovery is available for .xlsx and .xlsm imports.")

        result = self.excel_processor.discover(data_import.stored_path)
        data_import.schema_metadata = result["schema_metadata"]
        await self.repository.update(data_import)
        schema = await self.get_schema(import_id, organization_id)
        assert schema is not None
        return schema

    async def select_import_sheets(
        self,
        import_id: UUID,
        organization_id: UUID,
        sheet_names: list[str],
    ) -> dict:
        data_import = await self.get_by_id(import_id, organization_id)
        if data_import.status != "PENDING":
            raise ValueError("Sheets can only be selected for PENDING imports.")
        metadata = data_import.schema_metadata
        if not metadata or "workbook" not in metadata:
            raise ValueError("Discover the workbook before selecting sheets.")
        if len(sheet_names) != len(set(sheet_names)):
            raise ValueError("A worksheet can only be selected once.")

        sheets = metadata["workbook"]["sheets"]
        available_names = {sheet["name"] for sheet in sheets}
        if set(sheet_names) - available_names:
            raise ValueError("One or more selected worksheets do not exist.")
        invalid_names = {
            sheet["name"]
            for sheet in sheets
            if sheet["name"] in sheet_names and sheet.get("validation_error")
        }
        if invalid_names:
            raise ValueError(
                "Selected worksheets must have a valid header and unique, non-empty columns."
            )

        updated = dict(metadata)
        updated["selected_sheets"] = list(sheet_names)
        data_import.schema_metadata = updated
        await self.repository.update(data_import)
        schema = await self.get_schema(import_id, organization_id)
        assert schema is not None
        return schema

    async def get_mappings(self, import_id: UUID, organization_id: UUID) -> dict:
        schema = await self.get_schema(import_id, organization_id)
        if schema is None:
            raise ValueError("Schema discovery has not completed for this import.")
        mappings = suggest_mappings(schema)
        saved = schema.get("mappings", {})
        for mapping in mappings:
            decision = saved.get(str(mapping["position"]))
            if decision:
                mapping.update(decision)
        return {
            "import_id": schema["import_id"],
            "canonical_fields": CANONICAL_FIELDS,
            "columns": mappings,
        }

    async def decide_mapping(
        self, import_id: UUID, organization_id: UUID, position: int,
        status: str, canonical_field_id: str | None,
    ) -> dict:
        data_import = await self.get_by_id(import_id, organization_id)
        metadata = data_import.schema_metadata
        if metadata is None:
            raise ValueError("Schema discovery has not completed for this import.")
        if not any(column["position"] == position for column in metadata["columns"]):
            raise ValueError("Source column not found.")
        field_ids = {field["id"] for field in CANONICAL_FIELDS}
        if status == "approved" and canonical_field_id not in field_ids:
            raise ValueError("Choose a valid canonical field before approval.")
        if status == "unmapped" and canonical_field_id is not None:
            raise ValueError("Unmapped decisions cannot include a canonical field.")
        updated = dict(metadata)
        decisions = dict(updated.get("mappings", {}))
        decisions[str(position)] = {
            "mapping_status": status,
            "canonical_field_id": canonical_field_id,
        }
        updated["mappings"] = decisions
        data_import.schema_metadata = updated
        await self.repository.update(data_import)
        return await self.get_mappings(import_id, organization_id)

    async def list_by_data_source(
        self,
        data_source_id: UUID,
        organization_id: UUID,
    ) -> list[DataImport]:
        data_source = await self.data_source_repository.get_by_id(
            data_source_id,
            organization_id,
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
        organization_id: UUID,
    ) -> DataImport:
        data_import = await self.get_by_id(import_id, organization_id)

        if data_import.status != "PENDING":
            raise ValueError(
                "Only PENDING imports can be processed."
            )

        if not data_import.stored_path:
            raise ValueError(
                "Import has no stored file path."
            )

        is_excel = Path(data_import.file_name).suffix.lower() in {".xlsx", ".xlsm"}
        if is_excel:
            metadata = data_import.schema_metadata
            if not metadata or "workbook" not in metadata:
                raise ValueError("Discover the workbook before processing it.")
            if not metadata.get("selected_sheets"):
                raise ValueError("Select at least one worksheet before processing.")

        data_import.status = "PROCESSING"
        await self.repository.update(data_import)

        try:
            staged_rows: list[StagingRow] = []
            staging_batch_size = 500
            if is_excel:
                result = await self._stage_excel_import(
                    data_import,
                    staged_rows,
                    staging_batch_size,
                )
            else:
                result = await self._stage_csv_import(
                    data_import,
                    staged_rows,
                    staging_batch_size,
                )
            data_import.total_rows = result["total_rows"]
            data_import.successful_rows = result["successful_rows"]
            data_import.failed_rows = result["failed_rows"]
            data_import.status = "COMPLETED" if result["failed_rows"] == 0 else "FAILED"
            data_import.error_message = None

        except (ValueError, FileNotFoundError) as exc:
            data_import.status = "FAILED"
            data_import.error_message = str(exc)

        await self.repository.update(data_import)

        return data_import

    async def _stage_csv_import(
        self,
        data_import: DataImport,
        staged_rows: list[StagingRow],
        batch_size: int,
    ) -> dict[str, int]:
        result = self.processor.process(data_import.stored_path)
        data_import.schema_metadata = result["schema_metadata"]
        schema_metadata = result["schema_metadata"]

        with open(
            data_import.stored_path,
            encoding=schema_metadata["encoding"],
            newline="",
        ) as csv_file:
            reader = csv.DictReader(
                csv_file,
                delimiter=schema_metadata["delimiter"],
                restkey="__extra_fields__",
                strict=True,
            )
            columns = [column.strip() for column in reader.fieldnames]
            for row_number, row in enumerate(reader, start=1):
                if "__extra_fields__" in row or any(value is None for value in row.values()):
                    continue
                row_data = {
                    column: row[original_column]
                    for column, original_column in zip(
                        columns,
                        reader.fieldnames,
                        strict=True,
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
                if len(staged_rows) >= batch_size:
                    await self.staging_repository.create_many(staged_rows)
                    staged_rows.clear()

        if staged_rows:
            await self.staging_repository.create_many(staged_rows)
            staged_rows.clear()
        return result

    async def _stage_excel_import(
        self,
        data_import: DataImport,
        staged_rows: list[StagingRow],
        batch_size: int,
    ) -> dict[str, int]:
        metadata = data_import.schema_metadata
        selected_names = metadata["selected_sheets"]
        sheets_by_name = {
            sheet["name"]: sheet
            for sheet in metadata["workbook"]["sheets"]
        }
        total_rows = 0
        global_row_number = 0

        for sheet_name in selected_names:
            sheet = sheets_by_name[sheet_name]
            for source_row_number, row_data in self.excel_processor.iter_data_rows(
                data_import.stored_path,
                sheet_name,
                sheet["columns"],
            ):
                global_row_number += 1
                total_rows += 1
                staged_rows.append(
                    StagingRow(
                        data_import_id=data_import.id,
                        data_source_id=data_import.data_source_id,
                        row_number=global_row_number,
                        source_sheet_name=sheet_name,
                        source_row_number=source_row_number,
                        row_data=row_data,
                    )
                )
                if len(staged_rows) >= batch_size:
                    await self.staging_repository.create_many(staged_rows)
                    staged_rows.clear()

        if staged_rows:
            await self.staging_repository.create_many(staged_rows)
            staged_rows.clear()
        return {
            "total_rows": total_rows,
            "successful_rows": total_rows,
            "failed_rows": 0,
        }
