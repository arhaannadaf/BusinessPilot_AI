from fastapi import APIRouter,Depends

from app.api.dependencies.company_status import get_company_status_service
from app.modules.reference.company_status.schemas import CompanyStatusResponse
from app.modules.reference.company_status.service import CompanyStatusService

router = APIRouter(
    prefix="/company-statuses",
    tags=["Reference - Company Statuses"]
)
@router.get(
        "",
        response_model=list[CompanyStatusResponse]
)
async def list_company_sizes(
    is_active: bool | None = True,
    service: CompanyStatusService = Depends(get_company_status_service),
):
    return await service.list_company_statuses(
        is_active=is_active,
    )