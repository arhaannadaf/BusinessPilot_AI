from datetime import datetime, timezone
from uuid import UUID

from app.database.models.decision.execution.execution import Execution
from app.database.models.decision.outcome.outcome import Outcome
from app.modules.decision.execution.repository import ExecutionRepository
from app.modules.decision.outcome.repository import OutcomeRepository


class OutcomeService:

    def __init__(
        self,
        outcome_repository: OutcomeRepository,
        execution_repository: ExecutionRepository,
    ):
        self.outcome_repository = outcome_repository
        self.execution_repository = execution_repository

    async def create_outcome(
        self,
        execution_id: UUID,
        summary: str | None = None,
        meta_data: dict | None = None,
    ) -> Outcome:

        execution = await self.execution_repository.get_by_id(
            execution_id
        )

        if not execution:
            raise ValueError("Execution not found")

        if execution.status != "COMPLETED":
            raise ValueError(
                "Outcome can only be created for a completed execution"
            )

        existing_outcome = (
            await self.outcome_repository.get_by_execution(
                execution_id
            )
        )

        if existing_outcome:
            raise ValueError(
                "Outcome already exists for this execution"
            )

        outcome = Outcome(
            execution_id=execution_id,
            status="RECORDED",
            observed_at=datetime.now(timezone.utc),
            summary=summary,
            meta_data=meta_data or {},
        )

        return await self.outcome_repository.create(outcome)

    async def get_outcome(
        self,
        outcome_id: UUID,
    ) -> Outcome:

        outcome = await self.outcome_repository.get_by_id(
            outcome_id
        )

        if not outcome:
            raise ValueError("Outcome not found")

        return outcome

    async def get_outcome_by_execution(
        self,
        execution_id: UUID,
    ) -> Outcome:

        outcome = await self.outcome_repository.get_by_execution(
            execution_id
        )

        if not outcome:
            raise ValueError("Outcome not found")

        return outcome