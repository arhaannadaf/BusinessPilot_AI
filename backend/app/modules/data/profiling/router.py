
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.modules.data.profiling.dependencies import (
    get_data_profiling_service,
)
from app.modules.data.profiling.service import DataProfilingService
from app.modules.data.profiling.schemas import DataProfileResponse
from app.modules.data.profiling.schemas import (
    DataQualityComparisonResponse,
    DataQualityAlertResponse,
    DataQualityAlertStatusUpdate,
    )
from app.modules.data.profiling.schemas import (
    DataQualityAlertAuditResponse,
)


router = APIRouter(
    prefix="/data-profiling",
    tags=["Data Profiling"],
)


@router.post("/imports/{import_id}")
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
@router.get(
    "/imports/{import_id}/history",
    response_model=list[DataProfileResponse],
)
async def get_profile_history(
    import_id: UUID,
    service: DataProfilingService = Depends(
        get_data_profiling_service
    ),
):
    data_import = await service.data_import_repository.get_by_id(
        import_id
    )

    if data_import is None:
        raise HTTPException(
            status_code=404,
            detail="Data import not found.",
        )

    profiles = await service.profile_repository.list_by_import(
        import_id
    )

    return profiles

@router.get(
    "/profiles/{profile_id}",
    response_model=DataProfileResponse,
)
async def get_profile(
    profile_id: UUID,
    service: DataProfilingService = Depends(
        get_data_profiling_service
    ),
):
    profile = await service.profile_repository.get_by_id(
        profile_id
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Data profile not found.",
        )

    return profile


@router.get(
        "/imports/{import_id}/comparison",
        response_model=DataQualityComparisonResponse,
        )
async def compare_import_profiles(
    import_id: UUID,
    service: DataProfilingService = Depends(get_data_profiling_service),
):
    try:
        return await service.compare_latest_profiles(import_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

@router.get(
    "/alerts/{alert_id}",
    response_model=DataQualityAlertResponse,
)
async def get_quality_alert(
    alert_id: UUID,
    service: DataProfilingService = Depends(
        get_data_profiling_service
    ),
):
    alert = await service.alert_repository.get_by_id(alert_id)

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Data quality alert not found.",
        )

    return alert


@router.get(
    "/imports/{import_id}/alerts",
    response_model=list[DataQualityAlertResponse],
)
async def get_import_quality_alerts(
    import_id: UUID,
    service: DataProfilingService = Depends(
        get_data_profiling_service
    ),
):
    data_import = await service.data_import_repository.get_by_id(
        import_id
    )

    if data_import is None:
        raise HTTPException(
            status_code=404,
            detail="Data import not found.",
        )

    return await service.alert_repository.list_by_import(import_id)


@router.patch(
    "/alerts/{alert_id}/status",
    response_model=DataQualityAlertResponse,
)
async def update_quality_alert_status(
    alert_id: UUID,
    payload: DataQualityAlertStatusUpdate,
    service: DataProfilingService = Depends(
        get_data_profiling_service
    ),
):
    alert = await service.alert_repository.get_by_id(alert_id)

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Data quality alert not found.",
        )

    current_status = alert.status
    new_status = payload.status

    allowed_transitions = {
        "OPEN": {"ACKNOWLEDGED"},
        "ACKNOWLEDGED": {"RESOLVED"},
        "RESOLVED": set(),
    }

    if new_status == current_status:
        return alert

    if new_status not in allowed_transitions.get(
        current_status, set()
    ):
        raise HTTPException(
            status_code=409,
            detail=(
                f"Cannot transition alert from "
                f"{current_status} to {new_status}."
            ),
        )

    return await service.alert_repository.update_status(
        alert,
        new_status,
    )


@router.get(
    "/alerts/{alert_id}/history",
    response_model=list[DataQualityAlertAuditResponse],
)
async def get_alert_history(
    alert_id: UUID,
    service: DataProfilingService = Depends(
        get_data_profiling_service
    ),
):
    alert = await service.alert_repository.get_by_id(alert_id)

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Data quality alert not found.",
        )

    return await service.alert_repository.list_audit_history(
        alert_id
    )


