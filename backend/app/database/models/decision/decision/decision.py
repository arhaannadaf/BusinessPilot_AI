from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column,relationship

from app.database.models.base_model import BaseModel

class Decision(BaseModel):
    __tablename__ = "decisions"

    scenario_id : Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scenarios.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    organization_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="DRAFT",
    )

    decision_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="DRAFT",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_by: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )

    scenario = relationship(
        "Scenario",
        lazy="select",
    )

    organization = relationship(
        "Organization",
        lazy="select"
    )

    creator = relationship(
        "User",
        lazy="select",
    )