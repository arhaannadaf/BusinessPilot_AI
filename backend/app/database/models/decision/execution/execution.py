from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base_model import BaseModel


class Execution(BaseModel):
    __tablename__ = "executions"

    recommendation_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(
            "recommendations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="PENDING",
        index=True,
    )

    executed_by: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="RESTRICT",
        ),
        nullable=True,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    execution_details: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    result: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )