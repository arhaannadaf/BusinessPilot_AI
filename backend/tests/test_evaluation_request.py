from pydantic import ValidationError

from app.modules.decision.engine.schemas import (
    DecisionEvaluationRequest,
)


# Valid
request = DecisionEvaluationRequest(
    weights={
        "profit": 0.6,
        "risk": 0.4,
    }
)

print("Valid request:")
print(request)


# Test zero weight
try:
    DecisionEvaluationRequest(
        weights={
            "profit": 0,
            "risk": 0.4,
        }
    )

except ValidationError as e:
    print("\nZero weight rejected:")
    print(e)


# Test negative weight
try:
    DecisionEvaluationRequest(
        weights={
            "profit": -0.5,
            "risk": 0.4,
        }
    )

except ValidationError as e:
    print("\nNegative weight rejected:")
    print(e)


# Test empty weights
try:
    DecisionEvaluationRequest(
        weights={}
    )

except ValidationError as e:
    print("\nEmpty weights rejected:")
    print(e)