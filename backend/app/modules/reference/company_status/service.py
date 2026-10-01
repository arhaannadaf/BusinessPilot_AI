from app.modules.reference.company_status.repository import CompanyStatusRepository
from app.modules.reference.company_status.schemas import CompanyStatusResponse

class CompanyStatusService:

    def __init__(
            self,
            repository: CompanyStatusRepository
    ):
        self.repository = repository

    async def list_company_statuses(
            self,
            *,
            is_active: bool | None = True,
    ) -> list[CompanyStatusResponse]:

        statuses = await self.repository.list(
            is_active=is_active,
        )

        return [
            CompanyStatusResponse.model_validate(status)
            for status in statuses
        ]