from fastapi import APIRouter, Depends

from app.api.dependencies.currency import get_currency_service
from app.modules.reference.currency.schemas import CurrencyResponse
from app.modules.reference.currency.service import CurrencyService


router = APIRouter(
    prefix="/currencies",
    tags=["Reference - Currencies"],
)


@router.get(
    "",
    response_model=list[CurrencyResponse],
)
async def list_currencies(
    is_active: bool | None = True,
    service: CurrencyService = Depends(
        get_currency_service
    ),
):
    return await service.list_currencies(
        is_active=is_active,
    )