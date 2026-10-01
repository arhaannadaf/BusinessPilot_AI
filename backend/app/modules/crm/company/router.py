from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query,status

from app.api.dependencies.company import get_company_service

from app.modules.crm.company.schemas import (
    CompanyCreate,
    CompanyUpdate,
    CompanyResponse,
    CompanyListResponse,
)

from app.modules.crm.company.service import CompanyService

from app.modules.crm.company.exceptions import(
    CompanyAlreadyExistsError,
    CompanyNotFoundError,
    InvalidSortFieldError,
    InvalidSortOrderError,
    InvalidSearchError,
)

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)
#POST
@router.post(
    "",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_company(
    company: CompanyCreate,
    service: CompanyService = Depends(get_company_service)
):
    try:
        return await service.create_company(company)

    except CompanyAlreadyExistsError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )
#GET
@router.get(
    "/{company_id}",
    response_model=CompanyResponse,
)
async def get_company(
    company_id: UUID,
    service: CompanyService = Depends(get_company_service),
):
    try:
        return await service.get_company(company_id)

    except CompanyNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
#GET ALL
@router.get(
    "",
    response_model=CompanyListResponse,

)
async def list_companies(
    organization_id: UUID | None = None,
    industry_id: UUID | None = None,
    company_size_id: UUID | None = None,
    company_status_id: UUID | None = None,
    country_id: UUID | None = None,
    is_customer: bool | None = None,
    is_partner: bool | None = None,
    is_active: bool | None = None,
    search: str | None = None,
    sort_by:str = "name",
    sort_order: str = "asc",
    page: int = Query(
        1,
        ge=1,
        description="Page number",
        ),
    page_size: int = Query(
        20,
        ge=1,
        le=100,
        description="Number of companies per page",
    ),
    service: CompanyService = Depends(get_company_service),
):
    skip = (page - 1) * page_size

    try:
        return await service.list_companies(
            organization_id=organization_id,
            industry_id=industry_id,
            company_size_id=company_size_id,
            company_status_id=company_status_id,
            country_id=country_id,
            is_customer=is_customer,
            is_partner=is_partner,
            is_active=is_active,
            search = search,
            sort_by = sort_by,
            sort_order = sort_order,
            skip=skip,
            limit=page_size,
            )
    except InvalidSearchError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except InvalidSortFieldError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except InvalidSortOrderError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
#Patch
@router.patch(
    "/{company_id}",
    response_model=CompanyResponse,
)
async def update_company(
    company_id:UUID,
    data: CompanyUpdate,
    service: CompanyService = Depends(get_company_service)
):
    try:
        return await service.update_company(
            company_id,
            data,
        )

    except CompanyNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

#Delte

@router.delete(
    "/{company_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_company(
    company_id:UUID,
    service: CompanyService= Depends(get_company_service),
):
    try:
        await service.delete_company(company_id)

    except CompanyNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )