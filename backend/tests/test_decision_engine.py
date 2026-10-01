import asyncio

from app.database.session import SessionLocal
from app.modules.decision.engine.service import DecisionEngineService
from app.modules.decision.decision.repository import DecisionRepository
from app.modules.decision.engine.schemas import (
    DecisionEvaluationRequest,
)

DECISION_ID = "681c5609-b456-4e5a-89cd-12f6bd7b472c"
ORGANIZATION_ID = "f98e1fc6-ca56-488e-988d-2fbace1c7640"


async def main():
    async with SessionLocal() as session:

        repository = DecisionRepository(session)

        service = DecisionEngineService(repository)

        request = DecisionEvaluationRequest(
                weights={
                     "Last-Mile Delivery Turnaround Time": 0.4,
                }
            )

        result = await service.evaluate_decision(
            decision_id=DECISION_ID,
            organization_id=ORGANIZATION_ID,
            request=request
        )

        print(result)


if __name__ == "__main__":
    asyncio.run(main())