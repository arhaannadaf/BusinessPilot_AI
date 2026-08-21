from app.modules.reference.company_size.repository import CompanySizeRepository
from app.modules.reference.company_size.schemas import CompanySizeResponse

class CompanySizeService:

    def __init__(
            self,
            repository: CompanySizeRepository
    ):
        self.repository = repository

    async def list_company_size(
            self,
            *,
            is_active: bool | None = True,
    ) -> list[CompanySizeResponse]:

        company_sizes = await self.repository.list(
            is_active=is_active,
        )

        return [
            CompanySizeResponse.model_validate(company_sizes)
            for company_sizes in company_sizes
        ]