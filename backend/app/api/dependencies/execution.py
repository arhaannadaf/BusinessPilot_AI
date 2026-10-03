from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.modules.decision.execution.repository import ExecutionRepository
from app.modules.decision.execution.service import ExecutionService


def get_execution_service(
    session: AsyncSession = Depends(get_db),
) -> ExecutionService:
    repository = ExecutionRepository(session)

    return ExecutionService(
        repository=repository,
        session=session,
    )