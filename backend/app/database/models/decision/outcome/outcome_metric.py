from uuid import UUID

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base_model import BaseModel


class OutcomeMetric(BaseModel):
    __tablename__ = "outcome_metrics"

    outcome_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(
            "outcomes.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    metric_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    expected_value: Mapped[float] = mapped_column(
        Numeric,
        nullable=False,
    )

    actual_value: Mapped[float] = mapped_column(
        Numeric,
        nullable=False,
    )

    unit: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    variance: Mapped[float] = mapped_column(
        Numeric,
        nullable=False,
    )

    variance_percentage: Mapped[float | None] = mapped_column(
        Numeric,
        nullable=True,
    )