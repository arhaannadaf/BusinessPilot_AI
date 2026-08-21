from app.database.models.reference.reference_base import ReferenceBase

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class Currency(ReferenceBase):
    __tablename__ = "currencies"

    symbol: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )