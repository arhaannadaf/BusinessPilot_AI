from uuid import uuid4

from app.modules.decision.engine.engine import DecisionEngine
from app.modules.decision.engine.schemas import (
    MetricInput,
    OptionInput,
)


option_a = OptionInput(
    option_id=uuid4(),
    metrics=[
        MetricInput(
            metric_name="profit",
            value=80,
            direction="maximize",
            weight=1.5,
        ),
        MetricInput(
            metric_name="risk",
            value=20,
            direction="minimize",
            weight=0.2,
        ),
    ],
)


option_b = OptionInput(
    option_id=uuid4(),
    metrics=[
        MetricInput(
            metric_name="profit",
            value=120,
            direction="maximize",
            weight=0.8,
        ),
        MetricInput(
            metric_name="risk",
            value=50,
            direction="minimize",
            weight=0.2,
        ),
    ],
)


engine = DecisionEngine()

results = engine.calculate_option_scores(
    [
        option_a,
        option_b,
    ]
)

for result in results:
    print(result)