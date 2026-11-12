
from uuid import UUID

from app.modules.data.imports.repository import DataImportRepository
from app.modules.data.imports.staging_repository import StagingRowRepository
from app.modules.data.profiling.alert_repository import (
    DataQualityAlertRepository,
)
from app.modules.data.profiling.processor import DataProfilingProcessor
from app.modules.data.profiling.quality_rules import (
    classify_quality_regression,
)
from app.modules.data.profiling.repository import DataProfileRepository


class DataProfilingService:
    """Coordinate profiling and persist every profiling run."""

    def __init__(
        self,
        data_import_repository: DataImportRepository,
        staging_repository: StagingRowRepository,
        profile_repository: DataProfileRepository,
        alert_repository: DataQualityAlertRepository | None = None,
    ):
        self.data_import_repository = data_import_repository
        self.staging_repository = staging_repository
        self.profile_repository = profile_repository
        self.alert_repository = alert_repository
        self.processor = DataProfilingProcessor()

    async def _create_quality_alert_if_needed(
        self,
        *,
        import_id: UUID,
        profile_id: UUID,
        regression: dict,
    ) -> dict | None:
        """Persist an alert when a quality regression is detected."""

        severity = regression["severity"]

        if severity not in {"WARNING", "CRITICAL"}:
            return None

        if self.alert_repository is None:
            raise RuntimeError(
                "Data quality alert repository is not configured."
            )

        reasons = regression["reasons"]

        alert_type = (
            reasons[0]
            if reasons
            else "QUALITY_REGRESSION"
        )

        message = (
            f"Data quality regression detected: {severity}. "
            f"Reasons: {', '.join(reasons) or 'Unspecified'}."
        )

        alert = await self.alert_repository.create(
            data_import_id=import_id,
            data_profile_id=profile_id,
            severity=severity,
            alert_type=alert_type,
            message=message,
            details=regression,
        )

        return {
            "alert_id": str(alert.id),
            "severity": alert.severity,
            "alert_type": alert.alert_type,
            "message": alert.message,
            "status": alert.status,
        }

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
        rows_by_sheet: dict[str | None, list[dict]] = {}
        for staged_row in staged_rows:
            source_sheet_name = getattr(staged_row, "source_sheet_name", None)
            rows_by_sheet.setdefault(source_sheet_name, []).append(staged_row.row_data)

        if not rows_by_sheet:
            report = self.processor.profile([])
            schema_metadata = getattr(data_import, "schema_metadata", None) or {}
            if schema_metadata.get("row_count", 0) == 0:
                self._attach_empty_schema_columns(report, schema_metadata)
        else:
            sheet_reports = []
            for sheet_name, rows in rows_by_sheet.items():
                if sheet_name is None:
                    sheet_reports.append(self.processor.profile(rows))
                else:
                    sheet_reports.append(
                        self.processor.profile(rows, source_sheet_name=sheet_name)
                    )
            report = self._combine_sheet_reports(sheet_reports)

        # 4. Add import metadata.
        report["import_id"] = str(data_import.id)
        report["data_source_id"] = str(data_import.data_source_id)
        report["file_name"] = data_import.file_name

        # 5. Persist the new profiling run.
        profile = await self.profile_repository.create(
            data_import_id=data_import.id,
            report=report,
        )

        report["profile_id"] = str(profile.id)
        report["profiled_at"] = profile.created_at.isoformat()

        # 6. Compare profiles if a previous run exists.
        profiles = await self.profile_repository.list_by_import(
            import_id
        )

        
        if len(profiles) >= 2:
            comparison = await self.compare_latest_profiles(import_id)
            report["comparison"] = comparison

            regression = comparison["quality_regression"]

            alert = await self._create_quality_alert_if_needed(
                import_id=data_import.id,
                profile_id=profile.id,
                regression=regression,
            )

            report["alert"] = alert
        else:
            report["comparison"] = None
            report["alert"] = None


        return report

    @staticmethod
    def _combine_sheet_reports(reports: list[dict]) -> dict:
        """Combine per-sheet statistics without treating other sheets' columns as nulls."""
        if len(reports) == 1:
            return reports[0]

        row_count = sum(report["row_count"] for report in reports)
        column_profiles = [
            column
            for report in reports
            for column in report["columns"]
        ]
        total_cells = sum(report["total_cells"] for report in reports)
        missing_cells = sum(
            column["missing_count"]
            for report in reports
            for column in report["columns"]
        )
        complete_cells = total_cells - missing_cells
        completeness = (
            round(complete_cells / total_cells * 100, 2)
            if total_cells
            else 0.0
        )
        duplicate_rows = sum(report["duplicate_rows"] for report in reports)
        status_rank = {
            "COMPLETE": 0,
            "MINOR_ISSUES": 1,
            "MODERATE_ISSUES": 2,
            "MAJOR_ISSUES": 3,
        }
        overall_quality_status = max(
            (report["overall_quality_status"] for report in reports),
            key=lambda status: status_rank.get(status, 0),
            default="COMPLETE",
        )

        return {
            "row_count": row_count,
            "column_count": len(column_profiles),
            "columns": column_profiles,
            "duplicate_rows": duplicate_rows,
            "duplicate_status": "DUPLICATES_FOUND" if duplicate_rows else "NO_DUPLICATES",
            "total_cells": total_cells,
            "completeness_percentage": completeness,
            "overall_quality_status": overall_quality_status,
        }

    @staticmethod
    def _attach_empty_schema_columns(report: dict, schema_metadata: dict) -> None:
        """Keep discovered headers visible in profiles for header-only uploads."""
        discovered: list[tuple[str | None, dict]] = []
        workbook = schema_metadata.get("workbook")
        if workbook:
            selected_names = schema_metadata.get("selected_sheets")
            selected_sheets = set(selected_names or [])
            for sheet in workbook.get("sheets", []):
                if selected_names is not None and sheet["name"] not in selected_sheets:
                    continue
                discovered.extend(
                    (sheet["name"], column)
                    for column in sheet.get("columns", [])
                )
        else:
            discovered.extend((None, column) for column in schema_metadata.get("columns", []))

        for sheet_name, column in discovered:
            missing_percentage = column.get("missing_percentage", 0.0)
            quality_status = (
                "COMPLETE" if missing_percentage == 0
                else "MINOR_ISSUES" if missing_percentage <= 5
                else "MODERATE_ISSUES" if missing_percentage <= 20
                else "MAJOR_ISSUES"
            )
            column_profile = {
                "column_name": column.get("staging_name", column["source_name"]),
                "source_name": column["source_name"],
                "inferred_type": column.get("inferred_type", "unknown"),
                "missing_count": column.get("missing_count", 0),
                "missing_percentage": missing_percentage,
                "non_missing_count": column.get("non_missing_count", 0),
                "is_empty": column.get("is_empty", True),
                "sample_values": column.get("sample_values", []),
                "quality_status": quality_status,
                "distinct_count": column.get("distinct_count", 0),
                "uniqueness_ratio": column.get("uniqueness_ratio", 0.0),
                "minimum_value": column.get("minimum_value"),
                "maximum_value": column.get("maximum_value"),
                "common_patterns": column.get("common_patterns", []),
                "validation_warnings": column.get("validation_warnings", []),
            }
            if sheet_name is not None:
                column_profile["source_sheet_name"] = sheet_name
            report["columns"].append(column_profile)

        report["column_count"] = len(report["columns"])


    async def compare_latest_profiles(self, import_id: UUID) -> dict:
        # Verify that the import exists.
        data_import = await self.data_import_repository.get_by_id(
            import_id
        )

        if data_import is None:
            raise ValueError("Data import not found.")

        # Repository returns profiles newest first.
        profiles = await self.profile_repository.list_by_import(
            import_id
        )

        if len(profiles) < 2:
            raise ValueError(
                "At least two profiling runs are required for comparison."
            )

        latest = profiles[0]
        previous = profiles[1]

        def column_map(profile):
            return {
                (column.get("source_sheet_name"), column["column_name"]): column
                for column in profile.column_profiles
            }

        latest_columns = column_map(latest)
        previous_columns = column_map(previous)

        latest_names = set(latest_columns)
        previous_names = set(previous_columns)

        column_changes = []

        column_identities = sorted(
            latest_names | previous_names,
            key=lambda identity: (identity[0] or "", identity[1]),
        )
        for source_sheet_name, name in column_identities:
            old = previous_columns.get((source_sheet_name, name))
            new = latest_columns.get((source_sheet_name, name))
            column_change = {"column_name": name}
            if source_sheet_name is not None:
                column_change["source_sheet_name"] = source_sheet_name

            if old is None:
                column_changes.append({
                    **column_change,
                    "change": "ADDED",
                    "previous": None,
                    "current": new,
                })
            elif new is None:
                column_changes.append({
                    **column_change,
                    "change": "REMOVED",
                    "previous": old,
                    "current": None,
                })
            else:
                changed_fields = [
                    field
                    for field in (
                        "inferred_type",
                        "missing_count",
                        "missing_percentage",
                        "quality_status",
                        "distinct_count",
                        "uniqueness_ratio",
                        "minimum_value",
                        "maximum_value",
                        "common_patterns",
                        "validation_warnings",
                    )
                    if old.get(field) != new.get(field)
                ]

                if changed_fields:
                    column_changes.append({
                        **column_change,
                        "change": "MODIFIED",
                        "changed_fields": changed_fields,
                        "previous": old,
                        "current": new,
                    })

        regression = classify_quality_regression(
            previous_completeness=previous.completeness_percentage,
            current_completeness=latest.completeness_percentage,
            previous_duplicate_rows=previous.duplicate_rows,
            current_duplicate_rows=latest.duplicate_rows,
        )           
        return {
            "import_id": str(import_id),
            "previous_profile_id": str(previous.id),
            "current_profile_id": str(latest.id),
            "quality_regression": regression,
            "changes": {
                "row_count": {
                    "previous": previous.row_count,
                    "current": latest.row_count,
                    "delta": latest.row_count - previous.row_count,
                },
                "column_count": {
                    "previous": previous.column_count,
                    "current": latest.column_count,
                    "delta": latest.column_count - previous.column_count,
                },
                "completeness_percentage": {
                    "previous": previous.completeness_percentage,
                    "current": latest.completeness_percentage,
                    "delta": round(
                        latest.completeness_percentage
                        - previous.completeness_percentage,
                        2,
                    ),
                },
                "duplicate_rows": {
                    "previous": previous.duplicate_rows,
                    "current": latest.duplicate_rows,
                    "delta": latest.duplicate_rows - previous.duplicate_rows,
                },
                "overall_quality_status": {
                    "previous": previous.overall_quality_status,
                    "current": latest.overall_quality_status,
                },
                "duplicate_status": {
                    "previous": previous.duplicate_status,
                    "current": latest.duplicate_status,
                },
               
                "columns": column_changes,
            },
            
        }
