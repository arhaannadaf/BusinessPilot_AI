from __future__ import annotations

from decimal import Decimal

from sqlalchemy import Boolean, ForeignKey, String, Integer, Text, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.database.models.base_model import BaseModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.database.models.identity.organization import Organization


class Company(BaseModel):
    __tablename__ = "companies"

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "name",
            name="uq_company_org_name",
        ),
    )

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    legal_name: Mapped[str | None] = mapped_column(String(255))

    website: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
    )

    description: Mapped[str | None] = mapped_column(Text)

    industry_id: Mapped[str | None] = mapped_column(ForeignKey("industries.id"),index=True,)
    company_size_id:Mapped[str | None] = mapped_column(ForeignKey("company_sizes.id"),index=True,)
    company_status_id:Mapped[str | None] = mapped_column(ForeignKey("company_statuses.id"),index=True,)

    country_id: Mapped[str | None] = mapped_column(
        ForeignKey("countries.id"),
        index=True,
    )
    city: Mapped[str | None] = mapped_column(String(100))
    state: Mapped[str | None] = mapped_column(String(100))
    postal_code: Mapped[str | None] = mapped_column(String(30))
    address_line_1: Mapped[str | None] = mapped_column(String(255))
    address_line_2: Mapped[str | None] = mapped_column(String(255))


    employee_count: Mapped[int | None] = mapped_column(Integer)
    annual_revenue: Mapped[Decimal | None] = mapped_column(Numeric(18,2))
    founded_year: Mapped[int | None] = mapped_column(Integer)


    email: Mapped[str | None] = mapped_column(String(255),index=True)
    phone: Mapped[str | None] = mapped_column(String(50))
    linkedin_url: Mapped[str |None] = mapped_column(String(255))


    is_customer : Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    is_partner: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
            Boolean,
            default=True,
            nullable=False,
        )

    organization: Mapped["Organization"] = relationship(
    "Organization",
    back_populates="companies",
)