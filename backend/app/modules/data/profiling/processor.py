
from collections import Counter
from datetime import date, datetime
from decimal import Decimal
from typing import Any


class DataProfilingProcessor:
    """Analyze staged tabular data and generate a quality profile."""

    def profile(self, rows: list[dict[str, Any]]) -> dict[str, Any]:
        if not rows:
            return {
                "row_count": 0,
                "column_count": 0,
                "columns": [],
                "duplicate_rows": 0,
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
            values = [row.get(column) for row in rows]

            missing_count = sum(
                value is None or (
                    isinstance(value, str) and not value.strip()
                )
                for value in values
            )

            non_missing = [
                value for value in values
                if value is not None
                and not (isinstance(value, str) and not value.strip())
            ]

            column_profiles.append({
                "column_name": column,
                "inferred_type": self._infer_type(non_missing),
                "missing_count": missing_count,
                "missing_percentage": round(
                    missing_count / len(rows) * 100, 2
                ),
                "distinct_count": len({
                    str(value) for value in non_missing
                }),
            })

        row_signatures = [
            tuple(
                (column, str(row.get(column)))
                for column in column_names
            )
            for row in rows
        ]

        duplicate_rows = len(row_signatures) - len(
            set(row_signatures)
        )

        return {
            "row_count": len(rows),
            "column_count": len(column_names),
            "columns": column_profiles,
            "duplicate_rows": duplicate_rows,
        }

    @staticmethod
    def _infer_type(values: list[Any]) -> str:
        if not values:
            return "unknown"

        def classify(value: Any) -> str:
            if isinstance(value, bool):
                return "boolean"
            if isinstance(value, (datetime, date)):
                return "date"
            if isinstance(value, int):
                return "integer"
            if isinstance(value, (float, Decimal)):
                return "decimal"

            text = str(value).strip()

            if text.lower() in {"true", "false"}:
                return "boolean"

            try:
                int(text)
                return "integer"
            except ValueError:
                pass

            try:
                float(text)
                return "decimal"
            except ValueError:
                pass

            for fmt in (
                "%Y-%m-%d",
                "%Y/%m/%d",
                "%d-%m-%Y",
                "%m/%d/%Y",
            ):
                try:
                    datetime.strptime(text, fmt)
                    return "date"
                except ValueError:
                    continue

            return "text"

        types = [classify(value) for value in values]
        counts = Counter(types)

        # Report a single type only when all non-missing values agree.
        if len(counts) == 1:
            return types[0]

        return "mixed"
