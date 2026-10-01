from fastapi import APIRouter,Depends

from app.api.dependencies.company_size import get_company_size_service
from app.modules.reference.company_size.schemas import CompanySizeResponse
from app.modules.reference.company_size.service import CompanySizeService

router = APIRouter(
    prefix="/company-sizes",
    tags=["Reference - Company Sizes"]
)
@router.get(
        "",
        response_model=list[CompanySizeResponse]
)
async def list_company_sizes(
    is_active: bool | None = True,
    service: CompanySizeService = Depends(get_company_size_service),
):
    return await service.list_company_size(
        is_active=is_active,
    )