from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.modules.reference.company_status.repository import CompanyStatusRepository
from app.modules.reference.company_status.service import CompanyStatusService

def get_company_status_service(
        db: AsyncSession = Depends(get_db),

) -> CompanyStatusService:
    repository = CompanyStatusRepository(db)

    return CompanyStatusService(repository)