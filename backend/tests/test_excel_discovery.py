from datetime import date
from io import BytesIO
from types import SimpleNamespace
from uuid import uuid4

import pytest
from fastapi import UploadFile
from openpyxl import Workbook

from app.modules.data.imports.excel_processor import ExcelProcessor
from app.modules.data.imports.schemas import DataImportSchemaResponse
from app.modules.data.imports.service import DataImportService
from app.modules.data.storage.local_storage import LocalStorage


def _write_workbook(path):
    workbook = Workbook()
    clients = workbook.active
    clients.title = "Clients"
    clients.append(["ClientCode", "Client_Name", "YearlyValue"])
    clients.append(["C-01", "Acme", 1200.5])
    clients.append(["C-02", None, 950])

    contracts = workbook.create_sheet("Contracts")
    contracts.append(["Contract_No", "ContractDate"])
    contracts.append(["K-01", date(2025, 1, 2)])

    workbook.create_sheet("Empty")
    workbook.save(path)
    return path


def test_discovers_each_sheet_independently_and_keeps_order(tmp_path):
    path = _write_workbook(tmp_path / "clients.xlsx")

    result = ExcelProcessor().discover(str(path))
    metadata = result["schema_metadata"]
    sheets = metadata["workbook"]["sheets"]

    assert [sheet["name"] for sheet in sheets] == ["Clients", "Contracts", "Empty"]
    assert [column["source_name"] for column in sheets[0]["columns"]] == [
        "ClientCode",
        "Client_Name",
        "YearlyValue",
    ]
    assert sheets[0]["columns"][0]["inferred_type"] == "text"
    assert sheets[0]["columns"][2]["inferred_type"] == "decimal"
    assert sheets[0]["columns"][2]["distinct_count"] == 2
    assert sheets[0]["columns"][2]["minimum_value"] == 950
    assert sheets[0]["columns"][2]["maximum_value"] == 1200.5
    assert sheets[0]["columns"][1]["missing_count"] == 1
    assert sheets[1]["columns"][1]["inferred_type"] == "date"
    assert sheets[2]["has_header"] is False
    assert metadata["selected_sheets"] == []
    assert metadata["fingerprint"]


def test_streams_rows_with_source_sheet_and_original_row_number(tmp_path):
    path = _write_workbook(tmp_path / "clients.xlsx")
    processor = ExcelProcessor()
    sheets = processor.discover(str(path))["schema_metadata"]["workbook"]["sheets"]
    clients = sheets[0]

    rows = list(processor.iter_data_rows(str(path), "Clients", clients["columns"]))

    assert rows == [
        (2, {"ClientCode": "C-01", "Client_Name": "Acme", "YearlyValue": 1200.5}),
        (3, {"ClientCode": "C-02", "Client_Name": None, "YearlyValue": 950}),
    ]


def test_duplicate_headers_are_reported_and_cannot_be_processed(tmp_path):
    path = tmp_path / "duplicate.xlsx"
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(["Name", "Name"])
    worksheet.append(["Ada", "A"])
    workbook.save(path)

    processor = ExcelProcessor()
    sheet = processor.discover(str(path))["schema_metadata"]["workbook"]["sheets"][0]

    assert sheet["validation_error"] == "Worksheet contains duplicate column names."
    with pytest.raises(ValueError, match="duplicate column names"):
        list(processor.iter_data_rows(str(path), "Sheet", sheet["columns"]))


def test_malformed_workbook_returns_validation_error(tmp_path):
    path = tmp_path / "broken.xlsx"
    path.write_bytes(b"not an xlsx workbook")

    with pytest.raises(ValueError, match="invalid or malformed"):
        ExcelProcessor().discover(str(path))


@pytest.mark.asyncio
async def test_storage_accepts_xlsx_without_using_user_filename_as_path(tmp_path):
    storage = LocalStorage(storage_dir=str(tmp_path))
    upload = UploadFile(filename="../clients.xlsx", file=BytesIO(b"workbook"))

    stored_path, stored_size = await storage.save_upload(upload)

    assert stored_path.endswith(".xlsx")
    assert "clients" not in stored_path
    assert stored_size == len(b"workbook")


def test_discovers_macro_enabled_workbooks_without_executing_macros(tmp_path):
    path = _write_workbook(tmp_path / "clients.xlsm")

    metadata = ExcelProcessor().discover(str(path))["schema_metadata"]

    assert metadata["format"] == "xlsm"
    assert metadata["workbook"]["sheet_count"] == 3


class _ImportRepository:
    def __init__(self, data_import):
        self.data_import = data_import

    async def get_by_id(self, _import_id):
        return self.data_import

    async def update(self, data_import):
        return data_import


class _DataSourceRepository:
    async def get_by_id(self, _data_source_id, _organization_id):
        return object()


@pytest.mark.asyncio
async def test_sheet_selection_is_validated_and_persisted():
    import_id = uuid4()
    org_id = uuid4()
    data_import = SimpleNamespace(
        id=import_id,
        data_source_id=uuid4(),
        status="PENDING",
        file_name="book.xlsx",
        schema_metadata={
            "columns": [],
            "schema_version": 1,
            "fingerprint": "test-fingerprint",
            "row_count": 0,
            "workbook": {
                "sheet_count": 2,
                "sheets": [
                    {
                        "name": "Clients",
                        "state": "visible",
                        "has_header": True,
                        "row_count": 0,
                        "columns": [],
                        "validation_error": None,
                    },
                    {
                        "name": "Empty",
                        "state": "visible",
                        "has_header": False,
                        "row_count": 0,
                        "columns": [],
                        "validation_error": "No header",
                    },
                ]
            },
            "selected_sheets": [],
        },
    )
    service = DataImportService(
        _ImportRepository(data_import),
        _DataSourceRepository(),
        LocalStorage(),
        SimpleNamespace(),
    )

    response = await service.select_import_sheets(import_id, org_id, ["Clients"])
    assert response["selected_sheets"] == ["Clients"]
    validated = DataImportSchemaResponse.model_validate(response)
    assert validated.workbook.sheets[0].name == "Clients"

    with pytest.raises(ValueError, match="do not exist"):
        await service.select_import_sheets(import_id, org_id, ["Unknown"])
    with pytest.raises(ValueError, match="valid header"):
        await service.select_import_sheets(import_id, org_id, ["Empty"])


class _StagingRepository:
    def __init__(self):
        self.rows = []

    async def create_many(self, rows):
        self.rows.extend(rows)


@pytest.mark.asyncio
async def test_selected_sheets_stage_with_source_provenance(tmp_path):
    path = _write_workbook(tmp_path / "clients.xlsx")
    discovered = ExcelProcessor().discover(str(path))["schema_metadata"]
    discovered["selected_sheets"] = ["Clients", "Contracts"]
    staging = _StagingRepository()
    service = DataImportService(
        _ImportRepository(None),
        _DataSourceRepository(),
        LocalStorage(),
        staging,
    )
    data_import = SimpleNamespace(
        id=uuid4(),
        data_source_id=uuid4(),
        stored_path=str(path),
        schema_metadata=discovered,
    )

    result = await service._stage_excel_import(data_import, [], 500)

    assert result == {"total_rows": 3, "successful_rows": 3, "failed_rows": 0}
    assert [(row.source_sheet_name, row.source_row_number) for row in staging.rows] == [
        ("Clients", 2),
        ("Clients", 3),
        ("Contracts", 2),
    ]
    assert staging.rows[2].row_data["ContractDate"] == "2025-01-02T00:00:00"
