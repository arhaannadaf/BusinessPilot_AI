from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.modules.decision.execution.repository import ExecutionRepository
from app.modules.decision.outcome.repository import OutcomeRepository
from app.modules.decision.outcome.service import OutcomeService


def get_outcome_service(
    session: AsyncSession = Depends(get_db),
) -> OutcomeService:
    outcome_repository = OutcomeRepository(session)
    execution_repository = ExecutionRepository(session)

    return OutcomeService(
        outcome_repository=outcome_repository,
        execution_repository=execution_repository,
    )