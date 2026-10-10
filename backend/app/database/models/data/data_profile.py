
from uuid import UUID

from sqlalchemy import ForeignKey, Index, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base_model import BaseModel


class DataProfile(BaseModel):
    __tablename__ = "data_profiles"

    data_import_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("data_imports.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    row_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    column_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    column_profiles: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
    )

    duplicate_rows: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )


Index(
    "ix_data_profiles_import_created",
    DataProfile.data_import_id,
    DataProfile.created_at,
)
