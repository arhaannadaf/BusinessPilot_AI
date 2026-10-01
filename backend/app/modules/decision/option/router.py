from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)

from app.api.dependencies.option import get_decision_option_service

from app.modules.decision.option.schemas import (
    DecisionOptionCreate,
    DecisionOptionResponse,
    DecisionOptionUpdate,
)

from app.modules.decision.option.service import DecisionOptionService

router = APIRouter(
    prefix="/decision-options",
    tags=["Decision Options"],
)

@router.post(
    "",
    response_model=DecisionOptionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_decision_option(
    data: DecisionOptionCreate,
    service: DecisionOptionService = Depends(
        get_decision_option_service
    ),
):
    organization_id = UUID(
"f98e1fc6-ca56-488e-988d-2fbace1c7640"
    )

    try:
        return await service.create_option(
            data=data,
            organization_id=organization_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        )

@router.get(
    "/decision/{decision_id}",
    response_model=list[DecisionOptionResponse],
)
async def list_decision_option(
    decision_id: UUID,
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    service: DecisionOptionService = Depends(
        get_decision_option_service
    ),
):
    organization_id = UUID(
        "f98e1fc6-ca56-488e-988d-2fbace1c7640"
    )
    skip = (page - 1) * page_size

    return await service.list_options(
        decision_id=decision_id,
        organization_id=organization_id,
        skip=skip,
        limit=page_size,
    )
@router.get(
    "/{decision_id}/{option_id}",
    response_model=DecisionOptionResponse,
)

async def get_decision_option(
    decision_id:UUID,
    option_id:UUID,
    service:DecisionOptionService=Depends(
        get_decision_option_service
    ),
):
    organization_id =UUID(
        "f98e1fc6-ca56-488e-988d-2fbace1c7640"
    )

    option = await service.get_option(
        option_id=option_id,
        decision_id=decision_id,
        organization_id=organization_id,
    )

    if option is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Decision option not found",
        )
    return option

@router.patch(
    "/{decision_id}/{option_id}",
    response_model=DecisionOptionResponse
)
async def update_decision_option(
    decision_id:UUID,
    option_id:UUID,
    data : DecisionOptionUpdate,
    service: DecisionOptionService= Depends(
        get_decision_option_service
    ),
):
    organization_id = UUID(
        "f98e1fc6-ca56-488e-988d-2fbace1c7640"
    )
    option = await service.update_option(
        option_id=option_id,
        decision_id=decision_id,
        data=data,
        organization_id=organization_id,
    )

    if option is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Decision option not found",
        )

    return option

@router.delete(
    "/{decision_id}/{option_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)

async def delete_decision_option(
    decision_id: UUID,
    option_id: UUID,
    service: DecisionOptionService = Depends(
        get_decision_option_service
    ),
):
    organization_id = UUID(
        "f98e1fc6-ca56-488e-988d-2fbace1c7640"
    )

    deleted = await service.delete_option(
        option_id=option_id,
        decision_id=decision_id,
        organization_id=organization_id
    )
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Decision option not found",
        )

    return None