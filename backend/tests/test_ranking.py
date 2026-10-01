from uuid import uuid4

from app.modules.decision.engine.engine import DecisionEngine
from app.modules.decision.engine.schemas import OptionScore


option_a = uuid4()
option_b = uuid4()
option_c = uuid4()


scores = [
    OptionScore(
        option_id=option_a,
        score=0.40,
    ),
    OptionScore(
        option_id=option_b,
        score=0.80,
    ),
    OptionScore(
        option_id=option_c,
        score=0.60,
    ),
]


engine = DecisionEngine()

ranked = engine.rank_options([])


for option in ranked:
    print(option)