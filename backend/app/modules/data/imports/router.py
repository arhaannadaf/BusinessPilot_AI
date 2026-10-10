
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)

from app.modules.data.imports.dependency import (
    get_data_import_service,
)
from app.modules.data.imports.schemas import DataImportResponse
from app.modules.data.imports.service import DataImportService


router = APIRouter(
    prefix="/data-imports",
    tags=["Data Imports"],
)


@router.post(
    "",
    response_model=DataImportResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_data_import(
    data_source_id: UUID = Form(...),
    file: UploadFile = File(...),
    service: DataImportService = Depends(
        get_data_import_service
    ),
):
    try:
        return await service.create(
            data_source_id=data_source_id,
            file=file,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "/{import_id}",
    response_model=DataImportResponse,
)
async def get_data_import(
    import_id: UUID,
    service: DataImportService = Depends(
        get_data_import_service
    ),
):
    try:
        return await service.get_by_id(import_id)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.get(
    "/source/{data_source_id}",
    response_model=list[DataImportResponse],
)
async def list_data_imports(
    data_source_id: UUID,
    service: DataImportService = Depends(
        get_data_import_service
    ),
):
    try:
        return await service.list_by_data_source(
            data_source_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

@router.post(
    "/{import_id}/process",
    response_model=DataImportResponse,
)
async def process_data_import(
    import_id: UUID,
    service: DataImportService = Depends(
        get_data_import_service
    ),
):
    try:
        return await service.process_import(import_id)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
