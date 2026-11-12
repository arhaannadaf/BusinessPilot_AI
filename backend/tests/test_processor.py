
from app.modules.data.profiling.processor import DataProfilingProcessor
from app.modules.data.profiling.service import DataProfilingService


def test_profile_empty_rows():
    processor = DataProfilingProcessor()

    report = processor.profile([])

    assert report == {
        "row_count": 0,
        "column_count": 0,
        "columns": [],
        "duplicate_rows": 0,
        "duplicate_status": "NO_DUPLICATES",
        "total_cells": 0,
        "completeness_percentage": 0.0,
        "overall_quality_status": "COMPLETE",
    }

def test_profile_normal_rows():
    processor = DataProfilingProcessor()

    rows = [
        {"Name": "Apple", "Sector": "Technology"},
        {"Name": "Microsoft", "Sector": "Technology"},
    ]

    report = processor.profile(rows)

    assert report["row_count"] == 2
    assert report["column_count"] == 2
    assert report["duplicate_rows"] == 0
    assert report["duplicate_status"] == "NO_DUPLICATES"
    assert report["completeness_percentage"] == 100.0
    assert report["overall_quality_status"] == "COMPLETE"


def test_profile_duplicate_rows():
    processor = DataProfilingProcessor()

    rows = [
        {"Name": "Apple", "Sector": "Technology"},
        {"Name": "Microsoft", "Sector": "Technology"},
        {"Name": "Apple", "Sector": "Technology"},
    ]

    report = processor.profile(rows)

    assert report["row_count"] == 3
    assert report["duplicate_rows"] == 1
    assert report["duplicate_status"] == "DUPLICATES_FOUND"

def test_profile_missing_values():
    processor = DataProfilingProcessor()

    rows = [
        {"Name": "Apple", "Sector": "Technology"},
        {"Name": "Microsoft", "Sector": ""},
        {"Name": "Google", "Sector": "Technology"},
    ]

    report = processor.profile(rows)

    sector = next(
        column
        for column in report["columns"]
        if column["column_name"] == "Sector"
    )

    assert sector["missing_count"] == 1
    assert sector["missing_percentage"] == 33.33
    assert sector["quality_status"] == "MAJOR_ISSUES"
    assert report["overall_quality_status"] == "MAJOR_ISSUES"
    assert report["completeness_percentage"] == 83.33

def test_profile_column_type_inference():
    processor = DataProfilingProcessor()

    rows = [
        {
            "Age": "25",
            "Revenue": "1250.50",
            "JoinDate": "2025-01-15",
            "Active": "true",
            "Name": "Apple",
        },
        {
            "Age": "30",
            "Revenue": "2200.75",
            "JoinDate": "2025-02-20",
            "Active": "false",
            "Name": "Microsoft",
        },
    ]

    report = processor.profile(rows)
    inferred_types = {
        column["column_name"]: column["inferred_type"]
        for column in report["columns"]
    }

    assert inferred_types["Age"] == "integer"
    assert inferred_types["Revenue"] == "decimal"
    assert inferred_types["JoinDate"] == "date"
    assert inferred_types["Active"] == "boolean"
    assert inferred_types["Name"] == "text"


def test_profile_distinct_values_and_duplicate_rows_preserve_value_types():
    processor = DataProfilingProcessor()
    rows = [
        {"Code": 1},
        {"Code": "1"},
        {"Code": 1},
        {"Code": "1"},
    ]

    report = processor.profile(rows)
    code = report["columns"][0]

    assert code["distinct_count"] == 2
    assert code["uniqueness_ratio"] == 0.5
    assert code["inferred_type"] == "integer"
    assert code["validation_warnings"] == []
    assert report["duplicate_rows"] == 2


def test_profile_numeric_bounds_patterns_and_column_warnings():
    report = DataProfilingProcessor().profile(
        [
            {"Amount": "12.50", "Empty": None},
            {"Amount": "18.00", "Empty": ""},
        ]
    )
    amount = next(column for column in report["columns"] if column["column_name"] == "Amount")
    empty = next(column for column in report["columns"] if column["column_name"] == "Empty")

    assert amount["minimum_value"] == 12.5
    assert amount["maximum_value"] == 18
    assert amount["common_patterns"] == [{"pattern": "decimal_string", "count": 2}]
    assert amount["uniqueness_ratio"] == 1.0
    assert empty["distinct_count"] == 0
    assert "EMPTY_COLUMN" in empty["validation_warnings"]


def test_profiles_from_different_sheets_keep_columns_separate():
    processor = DataProfilingProcessor()
    service_reports = [
        processor.profile([{"Amount": 10}, {"Amount": 20}], "Sales"),
        processor.profile([{"Amount": "A-1"}], "Contracts"),
    ]

    combined = DataProfilingService._combine_sheet_reports(service_reports)

    assert combined["row_count"] == 3
    assert combined["column_count"] == 2
    assert [
        (column["source_sheet_name"], column["column_name"])
        for column in combined["columns"]
    ] == [("Sales", "Amount"), ("Contracts", "Amount")]
    assert combined["completeness_percentage"] == 100.0


def test_empty_profile_preserves_discovered_source_columns():
    report = DataProfilingProcessor().profile([])
    metadata = {
        "row_count": 0,
        "columns": [
            {
                "source_name": "EmptyColumn",
                "staging_name": "EmptyColumn",
                "inferred_type": "unknown",
                "is_empty": True,
                "validation_warnings": ["EMPTY_COLUMN"],
            }
        ],
    }

    DataProfilingService._attach_empty_schema_columns(report, metadata)

    assert report["column_count"] == 1
    assert report["columns"][0]["column_name"] == "EmptyColumn"
    assert report["columns"][0]["inferred_type"] == "unknown"
    assert report["columns"][0]["distinct_count"] == 0
