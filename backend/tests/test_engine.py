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
            weight=0.6,
        ),
        MetricInput(
            metric_name="risk",
            value=20,
            direction="minimize",
            weight=0.4,
        ),
    ],
)


option_b = OptionInput(
    option_id=uuid4(),
    metrics=[
        MetricInput(
            metric_name="profit",
            value=100,
            direction="maximize",
            weight=0.6,
        ),
        MetricInput(
            metric_name="risk",
            value=30,
            direction="minimize",
            weight=0.4,
        ),
    ],
)


option_c = OptionInput(
    option_id=uuid4(),
    metrics=[
        MetricInput(
            metric_name="profit",
            value=120,
            direction="maximize",
            weight=0.6,
        ),
        MetricInput(
            metric_name="risk",
            value=50,
            direction="minimize",
            weight=0.4,
        ),
    ],
)


engine = DecisionEngine()

results = engine.calculate_option_scores(
    [
        option_a,
        option_b,
        option_c,
    ]
)

for result in results:
    print(result)