
from uuid import UUID

from sqlalchemy import ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base_model import BaseModel


class StagingRow(BaseModel):
    __tablename__ = "staging_rows"

    data_import_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("data_imports.id", ondelete="CASCADE"),
        nullable=False,
    )

    data_source_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("data_sources.id", ondelete="CASCADE"),
        nullable=False,
    )

    row_number: Mapped[int] = mapped_column(
        nullable=False,
    )

    row_data: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )


Index(
    "ix_staging_rows_import_row",
    StagingRow.data_import_id,
    StagingRow.row_number,
    unique=True,
)
