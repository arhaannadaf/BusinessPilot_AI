from __future__ import annotations

from uuid import UUID

from sqlalchemy import select, or_ , func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.crm.company import Company
from app.modules.crm.company.exceptions import (
    InvalidSortFieldError,
    InvalidSortOrderError,
    InvalidSearchError,
)

class CompanyRepository:
    """Repository for Company database operations"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, company: Company) -> Company:
        self.db.add(company)
        await self.db.commit()
        await self.db.refresh(company)
        return company

    async def get_by_id(self, company_id: UUID) -> Company | None:
        result = await self.db.execute(
            select(Company).where(Company.id == company_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(
            self,
            organization_id: UUID,
            name: str,
    ) -> Company | None:
        result = await self.db.execute(
            select(Company).where(
                Company.organization_id == organization_id,
                Company.name == name,
            )
        )
        return result.scalar_one_or_none()

    async def list(
            self,
            *,
            organization_id: UUID | None = None,
            industry_id:UUID | None =None,
            company_size_id: UUID | None = None,
            company_status_id: UUID | None = None,
            country_id: UUID | None = None,
            is_customer:bool|None= None,
            is_partner: bool | None = None,
            is_active: bool | None = None,
            search:str | None =None,
            sort_by: str = "name",
            sort_order: str = "asc",
            skip: int = 0,
            limit: int = 100,
    ) -> tuple[list[Company],int]:

        query = select(Company)

        if organization_id is not None:
            query = query.where(
                Company.organization_id == organization_id
            )
        if industry_id is not None:
            query = query.where(
                Company.industry_id == industry_id
            )

        if company_size_id is not None:
            query = query.where(
                Company.company_size_id == company_size_id
            )
        if company_status_id is not None:
            query = query.where(
                Company.company_status_id == company_status_id
            )
        if country_id is not None:
            query = query.where(
                Company.country_id == country_id
            )

        if is_customer is not None:
            query = query.where(
                Company.is_customer == is_customer
            )
        if is_partner is not None:
            query = query.where(
                Company.is_partner == is_partner
            )
        if is_active is not None:
            query = query.where(
                Company.is_active == is_active
            )
        normalized_search = search.strip() if search else None
        if normalized_search and len(normalized_search) > 100:
            raise InvalidSearchError(
                "Search term cannot exceed 100 characters"
            )
        if normalized_search:
            search_term = f"%{normalized_search}%"
            query = query.where(
                or_(
                    Company.name.ilike(search_term),
                    Company.legal_name.ilike(search_term),
                    Company.email.ilike(search_term),
                    Company.phone.ilike(search_term),
                    Company.website.ilike(search_term),
                )
            )
        
        count_query = select(func.count()).select_from(
            query.subquery()
        )
        count_result = await self.db.execute(count_query)
        total = count_result.scalar_one()
        sortable_fields = {
            "name":Company.name,
            "created_at": Company.created_at,
            "updated_at": Company.updated_at,
            "employee_count": Company.employee_count,
            "annual_revenue":Company.annual_revenue,
            "founded_year":Company.founded_year,
        }
        sort_column = sortable_fields.get(sort_by)
        if sort_column is None:
            raise InvalidSortFieldError(
                f"Invalid sort field:'{sort_by}' ."
            )
        sort_order = sort_order.lower()
        if sort_order not in {"asc","desc"}:
            raise InvalidSortOrderError(
                f"Invalid sort Order: '{sort_order}' ."
                "Expected 'asc' or 'desc'."
            )
        if sort_order == "desc":
            query = query.order_by(sort_column.desc(),Company.id.desc(),)
        else:
            query = query.order_by(sort_column.asc(),Company.id.asc(),)
        query = (
            query
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(query)
        companies = result.scalars().all()

        return list(companies),total

    async def update(self, company:Company) -> Company:
        await self.db.commit()
        await self.db.refresh(company)
        return company

    async def delete(self, company: Company) -> None:
        await self.db.delete(company)
        await self.db.commit()

    async def exists(
            self,
            organization_id: UUID,
            name: str,
    ) -> bool:
        return(
            await self.get_by_name(organization_id,name)

        ) is not None