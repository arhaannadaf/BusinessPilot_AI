from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.modules.reference.country.repository import CountryRepository
from app.modules.reference.country.service import CountryService
def get_country_service(
        db: AsyncSession = Depends(get_db),

) -> CountryService:
    repository = CountryRepository(db)

    return CountryService(repository)