from pydantic import ValidationError

from app.modules.decision.engine.schemas import MetricInput

metric = MetricInput(
    metric_name="profit",
    value=100,
    direction="maximize",
    weight=0.5,
)

print("Valid metric:")
print(metric)

# Invalid
try:
    MetricInput(
        metric_name="risk",
        value=20,
        direction="random",
        weight=0.5,
    )

except ValidationError as e:
    print("\nInvalid metric correctly rejected:")
    print(e)