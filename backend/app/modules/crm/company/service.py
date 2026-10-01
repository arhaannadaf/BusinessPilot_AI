from __future__ import annotations

from uuid import UUID

from app.database.models.crm.company import Company
from app.modules.crm.company.CompanyValidator.CompanyRepository.repository import CompanyRepository
from app.modules.crm.company.schemas import (
    CompanyCreate,
    CompanyUpdate,
    CompanyListResponse,
)
from app.modules.crm.company.exceptions import (
    CompanyNotFoundError,
    
)
from app.modules.crm.company.validator import CompanyValidator
class CompanyService:

    def __init__(
            self, 
            repository: CompanyRepository,
            validator: CompanyValidator,

            ):
        self.repository = repository
        self.validator =  validator

    async def create_company(
            self,
            data: CompanyCreate,
    ) -> Company:

        await self.validator.validate_company_name(
                data.organization_id,
                data.name
            )
        await self.validator.validate_organization(
        data.organization_id,
        )

        await self.validator.validate_industry(
            data.industry_id,
        )

        await self.validator.validate_company_size(
            data.company_size_id
        )

        await self.validator.validate_company_status(
            data.company_status_id
        )

        await self.validator.validate_country(
            data.country_id
        )
        self.validator.validate_business_rules(data)

        company = Company(**data.model_dump(mode="json"))

        return await self.repository.create(company)

    async def get_company(
            self,
            company_id : UUID,

    ) -> Company:

        company = await self.repository.get_by_id(
            company_id
        )

        if company is None:
            raise CompanyNotFoundError()
        

        return company

    async def list_companies(
            self,
            organization_id: UUID |None =None,
            industry_id: UUID | None = None,
            company_size_id: UUID | None = None,
            company_status_id : UUID | None = None,
            country_id : UUID | None = None,
            is_customer: bool | None= None,
            is_partner: bool | None = None,
            is_active: bool| None = None,
            search: str | None = None,
            sort_by:str = "name",
            sort_order:str = "asc",
            skip: int = 0,
            limit: int = 100,

    ) -> CompanyListResponse:

        companies, total = await self.repository.list(
            organization_id=organization_id,
            industry_id=industry_id,
            company_size_id=company_size_id,
            company_status_id=company_status_id,
            country_id=country_id,
            is_customer=is_customer,
            is_partner=is_partner,
            is_active=is_active,
            search=search,
            sort_by = sort_by,
            sort_order=sort_order,
            skip=skip,
            limit=limit,
        )

        page = (skip//limit) + 1

        pages = (total + limit -1) // limit

        return CompanyListResponse(
            items=companies,
            page=page,
            page_size=limit,
            total=total,
            pages=pages,
            has_next=page < pages,
            has_previous=page > 1,
        )

    async def update_company(
            self,
            company_id: UUID,
            data: CompanyUpdate,

    ) -> Company:

        company = await self.get_company(company_id)

        await self.validator.validate_update(
            company,
            data,
        )

        update_data = data.model_dump(
            exclude_unset=True,
            mode="json",
        )

        for key, value in update_data.items():
            setattr(company, key, value)

        return await self.repository.update(company)

    async def delete_company(
            self,
            company_id:UUID,
    ) -> None:

        company = await self.get_company(company_id)

        await self.repository.delete(company)
