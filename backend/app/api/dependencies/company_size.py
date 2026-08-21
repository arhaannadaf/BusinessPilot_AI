from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.modules.reference.company_size.repository import CompanySizeRepository
from app.modules.reference.company_size.service import CompanySizeService

def get_company_size_service(
        db: AsyncSession = Depends(get_db),
) -> CompanySizeService:

    repository = CompanySizeRepository(db)

    return CompanySizeService(repository)