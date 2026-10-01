from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

from app.modules.decision.decision.repository import DecisionRepository
from app.modules.decision.decision.service import DecisionService

def get_decision_repository(
        session: AsyncSession = Depends(get_db)
) -> DecisionRepository:

    return DecisionRepository(session)

def get_decision_service(
        session: AsyncSession = Depends(get_db),
        repository: DecisionRepository = Depends(
            get_decision_repository
        ),
) -> DecisionService:

    return DecisionService(
        repository=repository,
        session=session,
    )