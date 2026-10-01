import asyncio
from uuid import UUID

from app.database.session import SessionLocal
from app.modules.decision.engine.schemas import (
    DecisionEvaluationRequest,
)
from app.modules.decision.engine.service import (
    DecisionEngineService,
)


async def main():

    decision_id = UUID("a78dae3b-1b1d-4091-8712-1e2a79e06ec2")
    organization_id = UUID("f98e1fc6-ca56-488e-988d-2fbace1c7640")

    request = DecisionEvaluationRequest(
        weights={
             "Last-Mile Delivery Turnaround Time": 0.4,
        }
    )

    async with SessionLocal() as session:

        service = DecisionEngineService(session)

        result = await service.evaluate_decision(
            decision_id=decision_id,
            organization_id=organization_id,
            request=request,
        )

        print(result)


if __name__ == "__main__":
    asyncio.run(main())