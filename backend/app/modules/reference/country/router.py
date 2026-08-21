from fastapi import APIRouter,Depends

from app.api.dependencies.country import get_country_service
from app.modules.reference.country.schema import CountryResponse
from app.modules.reference.country.service import CountryService

router = APIRouter(
    prefix="/countries",
    tags = ["Reference - Countries"]
)

@router.get(
    "",
    response_model=list[CountryResponse],

) 
async def list_countries(
    is_active: bool | None = True,
    service: CountryService = Depends(
    get_country_service
),
):
    return await service.list_countries(
        is_active=is_active
    )