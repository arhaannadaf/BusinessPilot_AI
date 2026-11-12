
from uuid import UUID

from sqlalchemy import ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base_model import BaseModel


class DataQualityAlert(BaseModel):
    __tablename__ = "data_quality_alerts"

    data_import_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("data_imports.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    data_profile_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("data_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    severity: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    alert_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    details: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="OPEN",
    )


Index(
    "ix_data_quality_alerts_import_created",
    DataQualityAlert.data_import_id,
    DataQualityAlert.created_at,
)
