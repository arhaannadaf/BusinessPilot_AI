"""Streaming discovery and row iteration for Excel workbooks."""

import hashlib
import json
from collections.abc import Iterator
from datetime import date, datetime, time
from pathlib import Path
from typing import Any

from openpyxl import load_workbook

from app.shared.column_profile import ColumnProfileAccumulator


def _as_json_value(value: Any) -> Any:
    if isinstance(value, (datetime, date, time)):
        return value.isoformat()
    return value


class ExcelProcessor:
    """Inspect XLSX workbook schemas and stream selected sheet rows."""

    def discover(self, file_path: str) -> dict[str, Any]:
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError("Stored Excel workbook not found.")

        try:
            workbook = load_workbook(
                path,
                read_only=True,
                data_only=True,
                keep_links=False,
            )
        except Exception as exc:
            raise ValueError("Excel workbook is invalid or malformed.") from exc

        try:
            sheets: list[dict[str, Any]] = []
            fingerprint_payload: list[dict[str, Any]] = []
            total_rows = 0

            try:
                for worksheet in workbook.worksheets:
                    sheet, fingerprint = self._discover_sheet(worksheet)
                    sheets.append(sheet)
                    fingerprint_payload.append(fingerprint)
                    total_rows += sheet["row_count"]
            except Exception as exc:
                raise ValueError("Excel workbook is invalid or malformed.") from exc

            fingerprint = hashlib.sha256(
                json.dumps(
                    fingerprint_payload,
                    ensure_ascii=False,
                    separators=(",", ":"),
                ).encode("utf-8")
            ).hexdigest()

            return {
                "total_rows": total_rows,
                "schema_metadata": {
                    "schema_version": 1,
                    "fingerprint": fingerprint,
                    "row_count": total_rows,
                    "columns": [],
                    "format": path.suffix.lower().lstrip("."),
                    "workbook": {
                        "sheet_count": len(sheets),
                        "sheets": sheets,
                    },
                    "selected_sheets": [],
                },
            }
        finally:
            workbook.close()

    def _discover_sheet(self, worksheet: Any) -> tuple[dict[str, Any], dict[str, Any]]:
        iterator = worksheet.iter_rows(values_only=True)
        first_row = next(iterator, None)
        sheet_name = worksheet.title
        state = worksheet.sheet_state

        if first_row is None or not any(value is not None for value in first_row):
            return (
                {
                    "name": sheet_name,
                    "state": state,
                    "has_header": False,
                    "row_count": 0,
                    "columns": [],
                    "validation_error": "Worksheet is empty or has no header row.",
                },
                {"name": sheet_name, "state": state, "columns": []},
            )

        headers = list(first_row)
        while headers and headers[-1] is None:
            headers.pop()

        raw_names = ["" if value is None else str(value) for value in headers]
        staging_names = [name.strip() for name in raw_names]
        validation_error: str | None = None
        if any(not name for name in staging_names):
            validation_error = "Worksheet contains an empty column name."
        elif len(staging_names) != len(set(staging_names)):
            validation_error = "Worksheet contains duplicate column names."

        column_count = len(headers)
        column_profiles = [ColumnProfileAccumulator() for _ in headers]
        row_count = 0

        for row in iterator:
            values = list(row[:column_count])
            if len(values) < column_count:
                values.extend([None] * (column_count - len(values)))
            if not any(value is not None and str(value).strip() for value in values):
                continue
            row_count += 1
            for index, value in enumerate(values):
                column_profiles[index].add(value)

        columns: list[dict[str, Any]] = []
        for index, (source_name, staging_name, profile) in enumerate(
            zip(raw_names, staging_names, column_profiles, strict=True)
        ):
            columns.append(
                {
                    "position": index + 1,
                    "source_name": source_name,
                    "staging_name": staging_name,
                    **profile.as_dict(row_count),
                }
            )

        schema_signature = [
            {
                "position": column["position"],
                "source_name": column["source_name"],
                "staging_name": column["staging_name"],
                "inferred_type": column["inferred_type"],
            }
            for column in columns
        ]
        return (
            {
                "name": sheet_name,
                "state": state,
                "has_header": True,
                "row_count": row_count,
                "columns": columns,
                "validation_error": validation_error,
            },
            {"name": sheet_name, "state": state, "columns": schema_signature},
        )

    def iter_data_rows(
        self,
        file_path: str,
        sheet_name: str,
        columns: list[dict[str, Any]],
    ) -> Iterator[tuple[int, dict[str, Any]]]:
        """Yield source row number and JSON-compatible row data for one sheet."""
        try:
            workbook = load_workbook(
                file_path,
                read_only=True,
                data_only=True,
                keep_links=False,
            )
        except Exception as exc:
            raise ValueError("Excel workbook is invalid or malformed.") from exc
        try:
            if sheet_name not in workbook.sheetnames:
                raise ValueError(f"Worksheet '{sheet_name}' no longer exists.")
            worksheet = workbook[sheet_name]
            if not columns:
                raise ValueError(f"Worksheet '{sheet_name}' has no usable columns.")
            if any(not column["staging_name"] for column in columns):
                raise ValueError(f"Worksheet '{sheet_name}' has an empty column name.")
            names = [column["staging_name"] for column in columns]
            if len(names) != len(set(names)):
                raise ValueError(f"Worksheet '{sheet_name}' has duplicate column names.")

            try:
                for source_row_number, row in enumerate(
                    worksheet.iter_rows(min_row=2, values_only=True),
                    start=2,
                ):
                    if not any(value is not None and str(value).strip() for value in row):
                        continue
                    values = list(row[:len(columns)])
                    values.extend([None] * (len(columns) - len(values)))
                    yield source_row_number, {
                        column_name: _as_json_value(value)
                        for column_name, value in zip(names, values, strict=True)
                    }
            except Exception as exc:
                raise ValueError("Excel workbook is invalid or malformed.") from exc
        finally:
            workbook.close()
