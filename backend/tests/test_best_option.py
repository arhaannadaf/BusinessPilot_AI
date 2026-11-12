# from uuid import uuid4

# from app.modules.decision.engine.engine import DecisionEngine
# from app.modules.decision.engine.schemas import RankedOption


# option_a = uuid4()
# option_b = uuid4()
# option_c = uuid4()


# ranked_options = [
#     RankedOption(
#         option_id=option_b,
#         score=0.80,
#         rank=1,
#     ),
#     RankedOption(
#         option_id=option_c,
#         score=0.60,
#         rank=2,
#     ),
#     RankedOption(
#         option_id=option_a,
#         score=0.40,
#         rank=3,
#     ),
# ]


# engine = DecisionEngine()

# best = engine.select_best_option(
#     []
# )

# print(best)

'''Temporary for now'''
from uuid import uuid4
import pytest

from app.modules.decision.engine.engine import DecisionEngine
from app.modules.decision.engine.schemas import RankedOption

# 1. Global test fixtures are completely fine
option_a = uuid4()
option_b = uuid4()
option_c = uuid4()

mock_ranked_options = [
    RankedOption(option_id=option_b, score=0.80, rank=1),
    RankedOption(option_id=option_c, score=0.60, rank=2),
    RankedOption(option_id=option_a, score=0.40, rank=3),
]


# 2. Wrap operations inside functions prefixed with test_
def test_select_best_option_returns_top_rank():
    engine = DecisionEngine()
    
    # Test with valid mock data
    best = engine.select_best_option(mock_ranked_options)
    
    assert best is not None
    assert best.option_id == option_b
    assert best.score == 0.80


def test_select_best_option_empty_list_raises_value_error():
    engine = DecisionEngine()
    
    # Assert that passing an empty list intentionally triggers the ValueError
    with pytest.raises(ValueError, match="No ranked options provided."):
        engine.select_best_option([])
