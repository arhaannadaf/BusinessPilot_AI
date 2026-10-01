from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.modules.reference.industry.repository import IndustryRepository
from app.modules.reference.industry.service import IndustryService

def get_industry_service(
        db: AsyncSession = Depends(get_db),

) -> IndustryService:
    repository = IndustryRepository(db)

    return IndustryService(repository)