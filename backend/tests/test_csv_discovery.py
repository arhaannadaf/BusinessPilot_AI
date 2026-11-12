import pytest

from app.modules.data.imports.processor import CSVProcessor


def test_discovers_semicolon_csv_and_windows_1252(tmp_path):
    path = tmp_path / "clients.csv"
    path.write_bytes(
        "ClientCode;Client_Name;YearlyValue\r\n"
        "A-1;Caf\u00e9;1250.50\r\n"
        "A-2;;900\r\n".encode("cp1252")
    )

    result = CSVProcessor().process(str(path))
    metadata = result["schema_metadata"]

    assert result["columns"] == ["ClientCode", "Client_Name", "YearlyValue"]
    assert result["successful_rows"] == 2
    assert metadata["delimiter"] == ";"
    assert metadata["encoding"] == "cp1252"
    assert metadata["columns"][0]["inferred_type"] == "text"
    assert metadata["columns"][1]["missing_count"] == 1
    assert metadata["columns"][1]["missing_percentage"] == 50.0
    assert metadata["columns"][2]["inferred_type"] == "decimal"
    assert metadata["columns"][2]["distinct_count"] == 2
    assert metadata["columns"][2]["uniqueness_ratio"] == 1.0
    assert metadata["columns"][2]["minimum_value"] == 900
    assert metadata["columns"][2]["maximum_value"] == 1250.5


def test_empty_file_requires_header(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_bytes(b"")

    with pytest.raises(ValueError, match="header row"):
        CSVProcessor().process(str(path))


def test_rejects_empty_and_duplicate_headers(tmp_path):
    processor = CSVProcessor()
    empty_header = tmp_path / "empty-header.csv"
    duplicate_header = tmp_path / "duplicate-header.csv"
    empty_header.write_text(",Value\n1,2\n", encoding="utf-8")
    duplicate_header.write_text("Name, Name \nA,B\n", encoding="utf-8")

    with pytest.raises(ValueError, match="empty column names"):
        processor.process(str(empty_header))
    with pytest.raises(ValueError, match="duplicate column names"):
        processor.process(str(duplicate_header))


def test_zero_row_csv_discovers_empty_columns(tmp_path):
    path = tmp_path / "headers-only.csv"
    path.write_text("Name,Amount\n", encoding="utf-8")

    result = CSVProcessor().process(str(path))
    columns = result["schema_metadata"]["columns"]

    assert result["total_rows"] == 0
    assert [column["inferred_type"] for column in columns] == ["unknown", "unknown"]
    assert [column["missing_percentage"] for column in columns] == [0.0, 0.0]
    assert all(column["is_empty"] for column in columns)


def test_malformed_quoting_returns_validation_error(tmp_path):
    path = tmp_path / "malformed.csv"
    path.write_text('Name,Value\n"unfinished,1\n', encoding="utf-8")

    with pytest.raises(ValueError, match="malformed"):
        CSVProcessor().process(str(path))


def test_extra_fields_are_counted_as_failed_rows(tmp_path):
    path = tmp_path / "extra-fields.csv"
    path.write_text("Name,Value\nA,1,unexpected\n", encoding="utf-8")

    result = CSVProcessor().process(str(path))

    assert result["total_rows"] == 1
    assert result["successful_rows"] == 0
    assert result["failed_rows"] == 1
