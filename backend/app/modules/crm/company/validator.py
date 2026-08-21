from uuid import UUID
from decimal import Decimal
from datetime import datetime



from app.modules.crm.company.exceptions import (
    CompanyAlreadyExistsError,
    OrganizationNotFoundError,
    InvalidEmployeeCountError,
    InvalidAnnualRevenueError,
    InvalidFoundedYearError,
    InvalidPhoneNumber,
)
from app.database.models.reference.industry import Industry
from app.database.models.reference.company_size import CompanySize
from app.database.models.reference.company_status import CompanyStatus
from app.database.models.reference.country import Country

from app.modules.crm.company.CompanyValidator.reference.exceptions import (
CompanySizeNotFoundError,
CompanyStatusNotFoundError,
CountryNotFoundError,
IndustryNotFoundError
)

from app.modules.crm.company.CompanyValidator.CompanyRepository.repository import CompanyRepository
from app.modules.crm.company.CompanyValidator.organization.repository import OrganizationRepository
from app.modules.crm.company.CompanyValidator.reference.repository import ReferenceRepository

from app.modules.crm.company.schemas import (CompanyCreate,CompanyUpdate)
from app.database.models.crm.company import Company


class CompanyValidator:
    """
    Business validator layer for security
    """

    def __init__(
            self,
            company_repository:CompanyRepository,
            organization_repository:OrganizationRepository,
            reference_repository:ReferenceRepository
                 ):
        self.organization_repository = organization_repository
        self.company_repository = company_repository
        self.reference_repository = reference_repository

    async def validate_company_name(
            self,
            organization_id: UUID,
            name:str,
    ) -> None:
        """
        Ensure a company is unique within an organization
        """

        exists = await self.company_repository.exists(
            organization_id=organization_id,
            name=name
        )

        if exists:
            raise CompanyAlreadyExistsError(
                f"Company '{name}' already exists."
            )

    async def validate_organization(
            self,
            organization_id: UUID,

    ) -> None:
        """
        Ensure Organization Exists.
        """

        exists = await self.organization_repository.exists(
            organization_id
        )

        if not exists:
            raise OrganizationNotFoundError(
                f"Organization '{organization_id}' does not exists."
            )

    async def validate_industry(
            self,
            industry_id:UUID | None,
    ) -> None:
        if industry_id is None:
            return
        exists = await self.reference_repository.exists(
            Industry,
            industry_id,
        )

        if not exists:
            raise IndustryNotFoundError(
                f"Industry '{industry_id}' does not exists."
            )
    async def validate_company_size(
            self,
            company_size_id:UUID | None,
    ) -> None:
        if company_size_id is None:
            return

        exists = await self.reference_repository.exists(
            CompanySize,
            company_size_id,
        )

        if not exists:
            raise CompanySizeNotFoundError(
                f"Company Size does not exists."
            )

    async def validate_company_status(
            self,
            company_status_id: UUID |None
    ) -> None:
        if company_status_id is None:
            return

        exists = await self.reference_repository.exists(
            CompanyStatus,
            company_status_id,
        )

        if not exists:
            raise CompanyStatusNotFoundError(
                f"Company Status does not exist."
            )

    async def validate_country(
            self,
            country_id:UUID|None
    ) -> None:

        if country_id is None:
            return

        exists = await self.reference_repository.exists(
            Country,
            country_id,
        )

        if not exists:
            raise CountryNotFoundError(
                f"Country is not found"
            )


    def validate_business_rules(
            self,
            data: CompanyCreate,

    )-> None:

        self.validate_employee_count(data.employee_count)
        self.validate_annual_revenue(data.annual_revenue)
        self.validate_founded_year(data.founded_year)
        self.validate_phone(data.phone)

    def validate_employee_count(
            self,
            employee_count: int | None,
    ) -> None:

        if employee_count is None:
            return
        if employee_count < 0 :
            raise InvalidEmployeeCountError(
                "Employee count cannot be negative"
            )

    def validate_annual_revenue(
            self,
            revenue: Decimal | None,

    ) -> None:

        if revenue is None:
            return

        if revenue < 0 :
            raise InvalidAnnualRevenueError(
                "Annual revenue cannot be negative"
            )

    def validate_founded_year(
            self,
            year: int | None,
    ) -> None:
        if year is None:
            return

        current_year = datetime.now().year

        if year < 1800 or year > current_year:
            raise InvalidFoundedYearError(
                "Invalid founded year."
            )

    def validate_phone(
                self,
                phone: str | None,
        ) -> None:

            if phone is None:
                return

            if len(phone) > 50:
                raise InvalidPhoneNumber(
                    "Phone Number is Invalid"
                )

    async def validate_update(
            self,
            company: Company,
            data: CompanyUpdate,
    ) -> None:
        if data.name is not None and data.name != company.name:
            await self.validate_company_name(
                company.organization_id,
                data.name
            )
        if data.industry_id is not None:
            await self.validate_industry(
                data.industry_id
            )
        if data.company_size_id is not None:
            await self.validate_company_size(
                data.company_size_id
            )
        if data.company_status_id is not None:
            await self.validate_company_status(
                data.company_status_id
            )
        if data.country_id is not None:
            await self.validate_country(
                data.country_id
            )
        # Business Rules update
        if data.employee_count is not None:
            self.validate_employee_count(
                data.employee_count
            )
        if data.annual_revenue is not None:
            self.validate_annual_revenue(
                data.annual_revenue
            )
        if data.founded_year is not None:
            self.validate_founded_year(
                data.founded_year
            )
        if data.phone is not None:
            self.validate_phone(
                data.phone
            )
