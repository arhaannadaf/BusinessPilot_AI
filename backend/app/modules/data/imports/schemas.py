from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DataImportCreate(BaseModel):
    data_source_id: UUID
    file_name: str


class DataImportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    data_source_id: UUID
    file_name: str
    status: str
    total_rows: int
    successful_rows: int
    failed_rows: int
    error_message: str | None
    stored_path: str | None
    file_size_bytes: int
    created_at: datetime
    updated_at: datetime


class DiscoveredColumnResponse(BaseModel):
    position: int
    source_name: str
    staging_name: str
    inferred_type: str
    non_missing_count: int
    missing_count: int
    missing_percentage: float
    is_empty: bool
    sample_values: list[str] = Field(
        description="Up to three source value previews, truncated at 200 characters."
    )
    distinct_count: int = 0
    uniqueness_ratio: float = 0.0
    minimum_value: Any | None = None
    maximum_value: Any | None = None
    common_patterns: list[dict[str, Any]] = Field(default_factory=list)
    validation_warnings: list[str] = Field(default_factory=list)


class WorkbookSheetResponse(BaseModel):
    name: str
    state: str
    has_header: bool
    row_count: int
    columns: list[DiscoveredColumnResponse]
    validation_error: str | None = None


class WorkbookDiscoveryResponse(BaseModel):
    sheet_count: int
    sheets: list[WorkbookSheetResponse]


class SheetSelectionRequest(BaseModel):
    sheet_names: list[str] = Field(min_length=1)


class DataImportSchemaResponse(BaseModel):
    import_id: UUID
    schema_version: int
    fingerprint: str
    row_count: int
    columns: list[DiscoveredColumnResponse]
    format: str | None = None
    workbook: WorkbookDiscoveryResponse | None = None
    selected_sheets: list[str] = Field(default_factory=list)


class MappingDecisionRequest(BaseModel):
    status: Literal["approved", "unmapped"]
    canonical_field_id: str | None = None
