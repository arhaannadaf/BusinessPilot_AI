
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

from app.api.dependencies.auth import get_current_actor
from app.modules.data.imports.dependency import (
    get_data_import_service,
)
from app.modules.data.imports.schemas import (
    DataImportResponse,
    DataImportSchemaResponse,
    MappingDecisionRequest,
    SheetSelectionRequest,
)
from app.modules.data.imports.service import DataImportService
from app.modules.identity.schemas import CurrentActor

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
    actor: CurrentActor = Depends(get_current_actor),
):
    try:
        return await service.create(
            data_source_id=data_source_id,
            file=file,
            organization_id=actor.organization_id,
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
    actor: CurrentActor = Depends(get_current_actor),
):
    try:
        return await service.get_by_id(import_id, actor.organization_id)

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
    actor: CurrentActor = Depends(get_current_actor),
):
    try:
        return await service.list_by_data_source(
            data_source_id,
            actor.organization_id,
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
    actor: CurrentActor = Depends(get_current_actor),
):
    try:
        return await service.process_import(
            import_id,
            actor.organization_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.post(
    "/{import_id}/discover",
    response_model=DataImportSchemaResponse,
)
async def discover_data_import_schema(
    import_id: UUID,
    service: DataImportService = Depends(get_data_import_service),
    actor: CurrentActor = Depends(get_current_actor),
) -> DataImportSchemaResponse:
    try:
        schema = await service.discover_import_schema(
            import_id,
            actor.organization_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    return schema


@router.patch(
    "/{import_id}/sheets",
    response_model=DataImportSchemaResponse,
)
async def select_import_sheets(
    import_id: UUID,
    selection: SheetSelectionRequest,
    service: DataImportService = Depends(get_data_import_service),
    actor: CurrentActor = Depends(get_current_actor),
) -> DataImportSchemaResponse:
    try:
        return await service.select_import_sheets(
            import_id,
            actor.organization_id,
            selection.sheet_names,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

@router.get(
    "/{import_id}/schema",
    response_model=DataImportSchemaResponse,
)
async def get_import_schema(
    import_id: UUID,
    service: DataImportService = Depends(
        get_data_import_service
    ),
    actor: CurrentActor = Depends(get_current_actor),
) -> DataImportSchemaResponse:
    try:
        schema = await service.get_schema(
            import_id,
            actor.organization_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    if schema is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Schema discovery has not completed for this import.",
        )

    return schema


@router.get("/{import_id}/mappings")
async def get_import_mappings(
    import_id: UUID,
    service: DataImportService = Depends(get_data_import_service),
    actor: CurrentActor = Depends(get_current_actor),
):
    try:
        return await service.get_mappings(import_id, actor.organization_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.patch("/{import_id}/mappings/{position}")
async def decide_import_mapping(
    import_id: UUID,
    position: int,
    decision: MappingDecisionRequest,
    service: DataImportService = Depends(get_data_import_service),
    actor: CurrentActor = Depends(get_current_actor),
):
    try:
        return await service.decide_mapping(
            import_id, actor.organization_id, position,
            decision.status, decision.canonical_field_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
