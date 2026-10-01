from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

from app.modules.decision.option.repository import DecisionOptionRepository

from app.modules.decision.option.service import DecisionOptionService

def get_decision_option_repository(
        session: AsyncSession = Depends(get_db)
) -> DecisionOptionRepository:

    return DecisionOptionRepository(session)

def get_decision_option_service(
    session: AsyncSession =Depends(get_db),
    repository: DecisionOptionRepository = Depends(
        get_decision_option_repository
    )
) -> DecisionOptionService:

    return DecisionOptionService(
        repository=repository,
        session=session
        )

