import asyncio
from uuid import UUID

from app.database.session import SessionLocal
from app.modules.decision.scenario.engine.service import (
    ScenarioEngineService,
)
from app.modules.decision.scenario.engine.schemas import (
    ScenarioChange,
    ScenarioEvaluationRequest,
)


DECISION_ID = UUID(
    "681c5609-b456-4e5a-89cd-12f6bd7b472c"
)

SCENARIO_ID = UUID(
    "a5d7acef-59c9-4ebe-8efe-e83c63b00d32"
)


async def main():

    async with SessionLocal() as session:

        service = ScenarioEngineService(session)

        request = ScenarioEvaluationRequest(
            scenario_id=SCENARIO_ID,
            changes=[
                ScenarioChange(
                    metric_name="Annualized Revenue",
                    change_type="percentage",
                    change_value=10,
                ),
                ScenarioChange(
                    metric_name="Operational Cost",
                    change_type="percentage",
                    change_value=-5,
                ),
            ],
             weights={
        "Annualized Revenue": 1.0,
        "Operational Cost": 1.0,
    },
        )

        result = await service.evaluate_scenario(
            scenario_id=SCENARIO_ID,
            decision_id=DECISION_ID,
            request=request,
        )

        print(result)

        weights = {
            "Annualized Revenue": 1.0,
            "Operational Cost": 1.0,
        }

        decision_inputs = service.build_decision_inputs(
            results=result.metrics,
            weights=weights,
        )

        for option_input in decision_inputs:
            print(f"\nOption: {option_input.option_id}")

            for metric in option_input.metrics:
                print(
                    f"  {metric.metric_name}: "
                    f"value={metric.value}, "
                    f"direction={metric.direction}, "
                    f"weight={metric.weight}"
                )
        best_option = service.evaluate_with_decision_engine(
        results=result.metrics,
        weights={
            "Annualized Revenue": 1.0,
            "Operational Cost": 1.0,
        },
    )

        print("\nScenario Decision Result:")
        print(best_option)

if __name__ == "__main__":
    asyncio.run(main())