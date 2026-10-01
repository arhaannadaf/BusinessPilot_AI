from sqlalchemy import Boolean,String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base_model import BaseModel

class Role(BaseModel):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    is_active : Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )