
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.modules.data.profiling.dependencies import (
    get_data_profiling_service,
)
from app.modules.data.profiling.service import DataProfilingService


router = APIRouter(
    prefix="/data-profiling",
    tags=["Data Profiling"],
)


@router.get("/imports/{import_id}")
async def profile_import(
    import_id: UUID,
    service: DataProfilingService = Depends(
        get_data_profiling_service
    ),
):
    try:
        return await service.profile_import(import_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
