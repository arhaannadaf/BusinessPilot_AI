from datetime import datetime

from sqlalchemy import String,Boolean,Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped,mapped_column, relationship

from app.database.models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    organization_id : Mapped[str] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False
    )

    role_id: Mapped[str] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    Last_name:Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    username: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )
    email:Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    phone:Mapped[str | None] = mapped_column(
        String(20),
        nullable=True

    )

    is_active:Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    last_login: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    organization = relationship("Organization")
    role = relationship("Role")