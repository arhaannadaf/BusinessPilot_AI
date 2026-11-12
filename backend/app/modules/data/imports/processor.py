
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

from app.shared.column_profile import ColumnProfileAccumulator


def _detect_encoding(path: Path) -> str:
    with path.open("rb") as source:
        sample = source.read(65536)

    if sample.startswith((b"\xff\xfe", b"\xfe\xff")):
        return "utf-16"
    if sample.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"

    try:
        sample.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError:
        return "cp1252"


def _detect_delimiter(path: Path, encoding: str) -> str:
    with path.open("r", encoding=encoding, newline="") as source:
        sample = source.read(65536)

    try:
        return csv.Sniffer().sniff(sample, delimiters=",;\t|").delimiter
    except csv.Error:
        return ","


class CSVProcessor:
    def process(self, file_path: str) -> dict[str, Any]:
        path = Path(file_path)

        if not path.is_file():
            raise FileNotFoundError("Stored CSV file not found.")

        total_rows = 0
        successful_rows = 0
        failed_rows = 0
        raw_columns: list[str] = []
        columns: list[str] = []

        encoding = _detect_encoding(path)
        delimiter = _detect_delimiter(path, encoding)

        try:
            with path.open(
                "r",
                encoding=encoding,
                newline="",
            ) as csv_file:
                reader = csv.DictReader(
                    csv_file,
                    delimiter=delimiter,
                    restkey="__extra_fields__",
                    strict=True,
                )

                if not reader.fieldnames:
                    raise ValueError(
                        "CSV file must contain a header row."
                    )

                raw_columns = list(reader.fieldnames)
                columns = [
                    column.strip()
                    for column in raw_columns
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

                column_profiles = [ColumnProfileAccumulator() for _ in columns]

                for row in reader:
                    total_rows += 1

                    for position, source_name in enumerate(raw_columns):
                        value = row.get(source_name)
                        column_profiles[position].add(value)

                    if "__extra_fields__" in row:
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
                "CSV encoding could not be decoded. Use UTF-8, UTF-8 with BOM, "
                "UTF-16, or Windows-1252."
            ) from exc
        except csv.Error as exc:
            raise ValueError("CSV file is malformed or uses inconsistent quoting.") from exc

        discovered_columns = []
        fingerprint_columns = []

        for position, (source_name, staging_name, profile) in enumerate(
            zip(raw_columns, columns, column_profiles, strict=True),
            start=1,
        ):
            column_profile = profile.as_dict(total_rows)
            inferred_type = column_profile["inferred_type"]
            discovered_columns.append(
                {
                    "position": position,
                    "source_name": source_name,
                    "staging_name": staging_name,
                    **column_profile,
                }
            )
            fingerprint_columns.append({
                "position": position,
                "source_name": source_name,
                "staging_name": staging_name,
                "inferred_type": inferred_type,
            })

        fingerprint_payload = json.dumps(
            fingerprint_columns,
            ensure_ascii=False,
            separators=(",", ":"),
        )
        fingerprint = hashlib.sha256(
            fingerprint_payload.encode("utf-8")
        ).hexdigest()

        return {
            "columns": columns,
            "total_rows": total_rows,
            "successful_rows": successful_rows,
            "failed_rows": failed_rows,
            "schema_metadata": {
                "schema_version": 1,
                "fingerprint": fingerprint,
                "row_count": total_rows,
                "encoding": encoding,
                "delimiter": delimiter,
                "columns": discovered_columns,
            },
        }
