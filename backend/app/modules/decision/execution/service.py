from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.decision.execution import Execution
from app.database.models.decision.recommendation import Recommendation
from app.modules.decision.execution.repository import ExecutionRepository


class ExecutionService:

    def __init__(
        self,
        repository: ExecutionRepository,
        session: AsyncSession,
    ):
        self.repository = repository
        self.session = session

    async def create_execution(
        self,
        recommendation_id: UUID,
        executed_by: UUID | None = None,
        execution_details: dict | None = None,
    ) -> Execution:

        result = await self.session.execute(
            select(Recommendation).where(
                Recommendation.id == recommendation_id,
            )
        )

        recommendation = result.scalar_one_or_none()

        if recommendation is None:
            raise ValueError(
                "Recommendation not found."
            )

        if recommendation.status != "APPROVED":
            raise ValueError(
                "Only an APPROVED recommendation can be executed."
            )

        execution = Execution(
            recommendation_id=recommendation_id,
            status="PENDING",
            executed_by=executed_by,
            execution_details=execution_details or {},
        )

        return await self.repository.create(execution)


    async def update_execution(
        self,
        execution_id: UUID,
        status_value: str | None = None,
        result: str | None = None,
        error_message: str | None = None,
        execution_details: dict | None = None,
        started_at=None,
        completed_at=None,
    ) -> Execution | None:

        execution = await self.repository.get_by_id(
            execution_id=execution_id,
        )

        if execution is None:
            return None

        if status_value is not None:
            allowed_transitions = {
                "PENDING": {"IN_PROGRESS", "FAILED"},
                "IN_PROGRESS": {"COMPLETED", "FAILED"},
                "COMPLETED": set(),
                "FAILED": set(),
            }

            if status_value != execution.status:
                allowed_statuses = allowed_transitions.get(
                    execution.status,
                    set(),
                )

                if status_value not in allowed_statuses:
                    raise ValueError(
                        f"Invalid execution status transition: "
                        f"{execution.status} -> {status_value}"
                    )

        if status_value is not None:
            execution.status = status_value

        if result is not None:
            execution.result = result

        if error_message is not None:
            execution.error_message = error_message

        if execution_details is not None:
            execution.execution_details = execution_details

        if started_at is not None:
            execution.started_at = started_at

        if completed_at is not None:
            execution.completed_at = completed_at

        return await self.repository.update(execution)