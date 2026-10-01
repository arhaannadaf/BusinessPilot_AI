from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base_model import BaseModel

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.database.models.crm.company import Company

class Organization(BaseModel):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    domain : Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    ) 

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    companies: Mapped[list["Company"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan",
    )