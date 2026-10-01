from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB,UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base_model import BaseModel

class Recommendation(BaseModel):
    __tablename__ = "recommendations"

    decision_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "decisions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    recommended_option_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "decision_options.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="PROPOSED",
    )

    rationale: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    confidence: Mapped[float | None] = mapped_column(
        nullable=True,
    )

    supporting_metrics: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    source: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )