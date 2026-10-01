from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.modules.crm.company.CompanyValidator.CompanyRepository.repository import CompanyRepository
from app.modules.crm.company.service import CompanyService


async def get_company_service(
    db: AsyncSession = Depends(get_db),
) -> CompanyService:
    return CompanyService(
        CompanyRepository(db)
    )