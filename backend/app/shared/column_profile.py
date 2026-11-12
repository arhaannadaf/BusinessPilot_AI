"""Reusable, type-aware statistics for source-column profiling."""

import math
import re
from collections import Counter
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any

from app.shared.data_types import classify_data_type, infer_type_from_labels

_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("email", re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", re.IGNORECASE)),
    (
        "uuid",
        re.compile(
            r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
            re.IGNORECASE,
        ),
    ),
    ("date", re.compile(r"^\d{4}[-/]\d{1,2}[-/]\d{1,2}$")),
    ("integer_string", re.compile(r"^[+-]?\d+$")),
    ("decimal_string", re.compile(r"^[+-]?\d+[.,]\d+$")),
    (
        "alphanumeric_identifier",
        re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z0-9_-]+$"),
    ),
)


def value_identity(value: Any) -> tuple[Any, ...]:
    """Return a hashable identity without conflating unlike Python values."""
    value_type = type(value)
    type_name = f"{value_type.__module__}.{value_type.__qualname__}"

    if value is None:
        return ("null",)
    if isinstance(value, dict):
        items = [
            (value_identity(key), value_identity(item))
            for key, item in value.items()
        ]
        return (type_name, tuple(sorted(items, key=repr)))
    if isinstance(value, (list, tuple)):
        return (type_name, tuple(value_identity(item) for item in value))
    if isinstance(value, set):
        return (type_name, tuple(sorted((value_identity(item) for item in value), key=repr)))
    if isinstance(value, float):
        if math.isnan(value):
            return (type_name, "nan")
        return (type_name, value.hex())
    if isinstance(value, (datetime, date)):
        return (type_name, value.isoformat())
    if isinstance(value, Decimal):
        return (type_name, value.as_tuple())

    try:
        hash(value)
    except TypeError:
        return (type_name, repr(value))
    return (type_name, value)


def _pattern_for(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    normalized = value.strip()
    for name, pattern in _PATTERNS:
        if pattern.fullmatch(normalized):
            return name
    return None


def _date_order(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())
    text = str(value).strip()
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        for date_format in ("%Y/%m/%d", "%d-%m-%Y", "%m/%d/%Y"):
            try:
                return datetime.strptime(text, date_format)
            except ValueError:
                continue
    raise ValueError("Value is not a supported date.")


def _json_scalar(value: Any) -> Any:
    if isinstance(value, Decimal):
        return int(value) if value == value.to_integral_value() else float(value)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return value


class ColumnProfileAccumulator:
    """Accumulate bounded-memory profile statistics for one source column."""

    def __init__(self, sample_limit: int = 3) -> None:
        self.sample_limit = sample_limit
        self.missing_count = 0
        self.non_missing_count = 0
        self.type_labels: set[str] = set()
        self.distinct_values: set[tuple[Any, ...]] = set()
        self.samples: list[str] = []
        self.sample_identities: set[tuple[Any, ...]] = set()
        self.pattern_counts: Counter[str] = Counter()
        self._numeric_minimum: Decimal | None = None
        self._numeric_maximum: Decimal | None = None
        self._date_minimum: datetime | None = None
        self._date_maximum: datetime | None = None

    def add(self, value: Any) -> None:
        if value is None or (isinstance(value, str) and not value.strip()):
            self.missing_count += 1
            return

        self.non_missing_count += 1
        value_type = classify_data_type(value)
        self.type_labels.add(value_type)
        identity = value_identity(value)
        self.distinct_values.add(identity)

        if len(self.samples) < self.sample_limit and identity not in self.sample_identities:
            preview = value.isoformat() if isinstance(value, (datetime, date)) else str(value)
            self.samples.append(preview[:200])
            self.sample_identities.add(identity)

        pattern_name = _pattern_for(value)
        if pattern_name:
            self.pattern_counts[pattern_name] += 1

        if value_type in {"integer", "decimal"}:
            try:
                numeric_value = Decimal(str(value))
                if numeric_value.is_finite():
                    self._numeric_minimum = (
                        numeric_value if self._numeric_minimum is None
                        else min(self._numeric_minimum, numeric_value)
                    )
                    self._numeric_maximum = (
                        numeric_value if self._numeric_maximum is None
                        else max(self._numeric_maximum, numeric_value)
                    )
            except InvalidOperation:
                pass
        elif value_type == "date":
            try:
                date_value = _date_order(value)
                self._date_minimum = (
                    date_value if self._date_minimum is None
                    else min(self._date_minimum, date_value)
                )
                self._date_maximum = (
                    date_value if self._date_maximum is None
                    else max(self._date_maximum, date_value)
                )
            except ValueError:
                pass

    def as_dict(self, row_count: int) -> dict[str, Any]:
        inferred_type = infer_type_from_labels(self.type_labels)
        distinct_count = len(self.distinct_values)
        missing_percentage = (
            round(self.missing_count / row_count * 100, 2) if row_count else 0.0
        )
        uniqueness_ratio = (
            round(distinct_count / self.non_missing_count, 4)
            if self.non_missing_count
            else 0.0
        )

        minimum, maximum = self._bounds(inferred_type)
        warnings: list[str] = []
        if self.non_missing_count == 0:
            warnings.append("EMPTY_COLUMN")
        if inferred_type == "mixed":
            warnings.append("MIXED_DATA_TYPES")
        if row_count and missing_percentage > 20:
            warnings.append("HIGH_MISSING_RATE")
        if self.non_missing_count > 1 and distinct_count == 1:
            warnings.append("CONSTANT_VALUE")

        common_patterns = [
            {"pattern": name, "count": count}
            for name, count in self.pattern_counts.most_common(5)
        ]
        return {
            "inferred_type": inferred_type,
            "non_missing_count": self.non_missing_count,
            "missing_count": self.missing_count,
            "missing_percentage": missing_percentage,
            "is_empty": self.non_missing_count == 0,
            "sample_values": self.samples,
            "distinct_count": distinct_count,
            "uniqueness_ratio": uniqueness_ratio,
            "minimum_value": minimum,
            "maximum_value": maximum,
            "common_patterns": common_patterns,
            "validation_warnings": warnings,
        }

    def _bounds(self, inferred_type: str) -> tuple[Any | None, Any | None]:
        if inferred_type in {"integer", "decimal"}:
            if self._numeric_minimum is None or self._numeric_maximum is None:
                return None, None
            return (
                _json_scalar(self._numeric_minimum),
                _json_scalar(self._numeric_maximum),
            )
        if inferred_type == "date":
            if self._date_minimum is None or self._date_maximum is None:
                return None, None
            return _json_scalar(self._date_minimum), _json_scalar(self._date_maximum)
        return None, None
