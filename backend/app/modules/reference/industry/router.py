from fastapi import APIRouter,Depends

from app.api.dependencies.industry import get_industry_service
from app.modules.reference.industry.schemas import IndustryResponse
from app.modules.reference.industry.service import IndustryService

router = APIRouter(
    prefix="/industries",
    tags=["Reference - Industries"]
)
@router.get(
        "",
        response_model=list[IndustryResponse]
)
async def list_industries(
    is_active: bool | None = True,
    service: IndustryService = Depends(get_industry_service),
):
    return await service.list_industries(
        is_active=is_active,
    )