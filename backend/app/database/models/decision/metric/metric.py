from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped,mapped_column

from app.database.models.base_model import BaseModel

class DecisionMetric(BaseModel):
    __tablename__ = "decision_metrics"

    decision_option_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "decision_options.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    metric_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    value: Mapped[float] = mapped_column(
        nullable=False,
    )

    unit: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )
    direction: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    source: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    meta_data: Mapped[dict] =mapped_column(
        JSONB,
        nullable=False,
        default=dict
    )