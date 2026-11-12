
from uuid import UUID

from sqlalchemy import ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base_model import BaseModel


class DataQualityAlertAudit(BaseModel):
    __tablename__ = "data_quality_alert_audits"

    data_quality_alert_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(
            "data_quality_alerts.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    previous_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    new_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    changed_by: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        nullable=True,
    )

    change_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )


Index(
    "ix_data_quality_alert_audits_alert_created",
    DataQualityAlertAudit.data_quality_alert_id,
    DataQualityAlertAudit.created_at,
)
