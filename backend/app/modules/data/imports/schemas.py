from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


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
