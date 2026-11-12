
from typing import Any

from app.shared.column_profile import ColumnProfileAccumulator, value_identity


class DataProfilingProcessor:
    """Analyze staged tabular data and generate a quality profile."""

    def profile(
        self,
        rows: list[dict[str, Any]],
        source_sheet_name: str | None = None,
    ) -> dict[str, Any]:
        if not rows:
            return {
                "row_count": 0,
                "column_count": 0,
                "columns": [],
                "duplicate_rows": 0,
                "duplicate_status": "NO_DUPLICATES",
                "total_cells": 0,
                "completeness_percentage": 0.0,
                "overall_quality_status": "COMPLETE",
            }
                    

        column_names = list(
            dict.fromkeys(
                column
                for row in rows
                for column in row.keys()
            )
        )

        column_profiles = []

        for column in column_names:
            accumulator = ColumnProfileAccumulator()
            for row in rows:
                accumulator.add(row.get(column))
            statistics = accumulator.as_dict(len(rows))
            missing_pct = statistics["missing_percentage"]
            column_profile = {
                "column_name": column,
                **statistics,
                "missing_percentage": missing_pct,
                "quality_status": (
                    "COMPLETE" if missing_pct == 0 
                    else "MINOR_ISSUES" if missing_pct <= 5 
                    else "MODERATE_ISSUES" if missing_pct <= 20 
                    else "MAJOR_ISSUES"
                ), 
            }
            if source_sheet_name is not None:
                column_profile["source_sheet_name"] = source_sheet_name
            column_profiles.append(column_profile)

        quality_statuses = [
            column_profile["quality_status"]
            for column_profile in column_profiles
        ]

        if "MAJOR_ISSUES" in quality_statuses:
                overall_quality_status = "MAJOR_ISSUES"
        elif "MODERATE_ISSUES" in quality_statuses:
                overall_quality_status = "MODERATE_ISSUES"
        elif "MINOR_ISSUES" in quality_statuses:
                overall_quality_status = "MINOR_ISSUES"
        else:
                overall_quality_status = "COMPLETE"
                
        total_cells = len(rows) * len(column_names)

        missing_cells = sum(
            column_profile["missing_count"]
            for column_profile in column_profiles
        )

        completeness_percentage = (
            round(
                ((total_cells - missing_cells) / total_cells) * 100,
                2,
            )
            if total_cells > 0
            else 0.0
        )

        seen_rows: set[tuple[tuple[str, tuple[Any, ...]], ...]] = set()
        duplicate_rows = 0
        for row in rows:
            signature = tuple(
                (column, value_identity(row.get(column)))
                for column in column_names
            )
            if signature in seen_rows:
                duplicate_rows += 1
            else:
                seen_rows.add(signature)

        return {
            "row_count": len(rows),
            "column_count": len(column_names),
            "columns": column_profiles,
            "duplicate_rows": duplicate_rows,
            "duplicate_status": 
               ( "NO_DUPLICATES"
                if duplicate_rows == 0
                else "DUPLICATES_FOUND"
                        ),
            "total_cells": total_cells,
            "completeness_percentage": completeness_percentage,
            "overall_quality_status": overall_quality_status,
            
                }

