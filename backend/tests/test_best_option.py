from uuid import uuid4

from app.modules.decision.engine.engine import DecisionEngine
from app.modules.decision.engine.schemas import RankedOption


option_a = uuid4()
option_b = uuid4()
option_c = uuid4()


ranked_options = [
    RankedOption(
        option_id=option_b,
        score=0.80,
        rank=1,
    ),
    RankedOption(
        option_id=option_c,
        score=0.60,
        rank=2,
    ),
    RankedOption(
        option_id=option_a,
        score=0.40,
        rank=3,
    ),
]


engine = DecisionEngine()

best = engine.select_best_option(
    []
)

print(best)