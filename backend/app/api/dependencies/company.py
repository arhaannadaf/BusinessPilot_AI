from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

from app.modules.crm.company.CompanyValidator.CompanyRepository.repository import CompanyRepository
from app.modules.crm.company.CompanyValidator.organization.repository import OrganizationRepository
from app.modules.crm.company.CompanyValidator.reference.repository import ReferenceRepository
from app.modules.crm.company.service import CompanyService
from app.modules.crm.company.validator import CompanyValidator
async def get_company_service(
        db: AsyncSession = Depends(get_db)

) -> CompanyService:
    company_repository = CompanyRepository(db)
    organization_repository= OrganizationRepository(db)
    reference_repository= ReferenceRepository(db)
    validator = CompanyValidator(

        company_repository=company_repository,
        organization_repository=organization_repository,
        reference_repository=reference_repository,
    )

    return CompanyService(
        repository = company_repository,
        validator = validator,
        )