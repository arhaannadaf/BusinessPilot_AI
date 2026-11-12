from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator


class DataProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    data_import_id: UUID
    row_count: int
    column_count: int
    column_profiles: list[dict]
    duplicate_rows: int
    total_cells: int
    completeness_percentage: float
    overall_quality_status: str
    duplicate_status: str
    created_at: datetime
    updated_at: datetime

class MetricComparison(BaseModel):
    previous: int | float
    current: int | float
    delta: int | float


class StatusComparison(BaseModel):
    previous: str
    current: str


class ColumnChange(BaseModel):
    column_name: str
    change: str
    source_sheet_name: str | None = None
    changed_fields: list[str] | None = None
    previous: dict[str, Any] | None = None
    current: dict[str, Any] | None = None


class DataQualityChanges(BaseModel):
    row_count: MetricComparison
    column_count: MetricComparison
    completeness_percentage: MetricComparison
    duplicate_rows: MetricComparison
    overall_quality_status: StatusComparison
    duplicate_status: StatusComparison
    columns: list[ColumnChange]

class QualityRegressionResponse(BaseModel):
    severity: str
    completeness_drop: float
    duplicate_rows_increase: int
    reasons: list[str]
    
class DataQualityComparisonResponse(BaseModel):
    import_id: str
    previous_profile_id: str
    current_profile_id: str
    changes: DataQualityChanges
    quality_regression: QualityRegressionResponse


class DataQualityAlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    data_import_id: UUID
    data_profile_id: UUID
    severity: str
    alert_type: str
    message: str
    details: dict[str, Any]
    status: str
    created_at: datetime
    updated_at: datetime


class DataQualityAlertStatusUpdate(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        allowed_statuses = {
            "OPEN",
            "ACKNOWLEDGED",
            "RESOLVED",
        }

        normalized_status = value.strip().upper()

        if normalized_status not in allowed_statuses:
            raise ValueError(
                "Status must be OPEN, ACKNOWLEDGED, or RESOLVED."
            )

        return normalized_status

class DataQualityAlertAuditResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    data_quality_alert_id: UUID
    previous_status: str
    new_status: str
    changed_by: UUID | None
    change_reason: str | None
    created_at: datetime
    updated_at: datetime


