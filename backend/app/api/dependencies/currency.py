from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.modules.reference.currency.repository import (
    CurrencyRepository,
)
from app.modules.reference.currency.service import (
    CurrencyService,
)


def get_currency_service(
    db: AsyncSession = Depends(get_db),
) -> CurrencyService:

    repository = CurrencyRepository(db)

    return CurrencyService(repository)