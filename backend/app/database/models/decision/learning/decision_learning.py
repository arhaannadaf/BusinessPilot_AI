from uuid import UUID

from sqlalchemy import ForeignKey, String, Text, Float
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base_model import BaseModel


class DecisionLearning(BaseModel):
    __tablename__ = "decision_learning"

    decision_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(
            "decisions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    learning_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    insight: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    decision_option_id: Mapped[UUID] = mapped_column(
    PGUUID(as_uuid=True),
    ForeignKey(
        "decision_options.id",
        ondelete="CASCADE",
    ),
    nullable=True,
    index=True,
)

    metric_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    performance: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    variance_percentage: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    direction: Mapped[str | None] = mapped_column(
    String(20),
    nullable=True,
)