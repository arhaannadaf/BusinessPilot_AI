from app.modules.reference.currency.repository import (
    CurrencyRepository,
)
from app.modules.reference.currency.schemas import (
    CurrencyResponse,
)


class CurrencyService:

    def __init__(
        self,
        repository: CurrencyRepository,
    ):
        self.repository = repository

    async def list_currencies(
        self,
        *,
        is_active: bool | None = True,
    ) -> list[CurrencyResponse]:

        currencies = await self.repository.list(
            is_active=is_active,
        )

        return [
            CurrencyResponse.model_validate(currency)
            for currency in currencies
        ]