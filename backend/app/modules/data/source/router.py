from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.modules.data.source.dependency import (
    get_data_source_service,
)
from app.modules.data.source.schemas import (
    DataSourceCreate,
    DataSourceResponse,
)
from app.modules.data.source.service import DataSourceService


router = APIRouter(
    prefix="/data-sources",
    tags=["Data Sources"],
)


@router.post(
    "",
    response_model=DataSourceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_data_source(
    data: DataSourceCreate,
    service: DataSourceService = Depends(
        get_data_source_service
    ),
):
    try:
        return await service.create(data)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "/{data_source_id}",
    response_model=DataSourceResponse,
)
async def get_data_source(
    data_source_id: UUID,
    service: DataSourceService = Depends(
        get_data_source_service
    ),
):
    try:
        return await service.get_by_id(
            data_source_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.get(
    "/organization/{organization_id}",
    response_model=list[DataSourceResponse],
)
async def list_data_sources(
    organization_id: UUID,
    service: DataSourceService = Depends(
        get_data_source_service
    ),
):
    return await service.list_by_organization(
        organization_id
    )