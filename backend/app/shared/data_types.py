from collections.abc import Iterable
from datetime import date, datetime
from decimal import Decimal
from typing import Any


def classify_data_type(value: Any) -> str:
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, (datetime, date)):
        return "date"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, (float, Decimal)):
        return "decimal"

    text = str(value).strip()

    if not text:
        return "unknown"
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

    for date_format in (
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%m/%d/%Y",
    ):
        try:
            datetime.strptime(text, date_format)
            return "date"
        except ValueError:
            continue

    return "text"


def infer_type_from_labels(type_labels: Iterable[str]) -> str:
    unique_labels = set(type_labels)

    if not unique_labels:
        return "unknown"
    if unique_labels <= {"integer", "decimal"}:
        return "decimal" if "decimal" in unique_labels else "integer"
    if len(unique_labels) == 1:
        return next(iter(unique_labels))

    return "mixed"


def infer_column_type(values: Iterable[Any]) -> str:
    return infer_type_from_labels(
        classify_data_type(value)
        for value in values
    )
