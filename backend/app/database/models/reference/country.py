from app.database.models.reference.reference_base import ReferenceBase

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Country(ReferenceBase):
    __tablename__ = "countries"

    code_3: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        unique=True,
    )

