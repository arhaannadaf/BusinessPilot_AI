from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
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