from app.modules.reference.industry.repository import IndustryRepository
from app.modules.reference.industry.schemas import IndustryResponse

class IndustryService:

    def __init__(
            self,
            repository: IndustryRepository
    ):
        self.repository = repository

    async def list_industries(
            self,
            *,
            is_active: bool | None = True,
    ) -> list[IndustryResponse]:

        industries = await self.repository.list(
            is_active=is_active,
        )

        return [
            IndustryResponse.model_validate(industry)
            for industry in industries
        ]