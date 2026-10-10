
import csv
from pathlib import Path
from typing import Any


class CSVProcessor:
    def process(self, file_path: str) -> dict[str, Any]:
        path = Path(file_path)

        if not path.is_file():
            raise FileNotFoundError("Stored CSV file not found.")

        total_rows = 0
        successful_rows = 0
        failed_rows = 0
        columns: list[str] = []

        try:
            with path.open(
                "r",
                encoding="utf-8-sig",
                newline="",
            ) as csv_file:
                reader = csv.DictReader(csv_file)

                if not reader.fieldnames:
                    raise ValueError(
                        "CSV file must contain a header row."
                    )

                columns = [
                    column.strip()
                    for column in reader.fieldnames
                    if column and column.strip()
                ]

                if not columns:
                    raise ValueError(
                        "CSV file contains no valid column names."
                    )

                if len(columns) != len(reader.fieldnames):
                    raise ValueError(
                        "CSV file contains empty column names."
                    )

                if len(set(columns)) != len(columns):
                    raise ValueError(
                        "CSV file contains duplicate column names."
                    )

                for row in reader:
                    total_rows += 1

                    if None in row:
                        failed_rows += 1
                        continue

                    if any(
                        value is None
                        for value in row.values()
                    ):
                        failed_rows += 1
                        continue

                    successful_rows += 1

        except UnicodeDecodeError as exc:
            raise ValueError(
                "CSV file must use UTF-8 encoding."
            ) from exc

        return {
            "columns": columns,
            "total_rows": total_rows,
            "successful_rows": successful_rows,
            "failed_rows": failed_rows,
        }
