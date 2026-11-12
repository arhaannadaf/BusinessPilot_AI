# from uuid import uuid4

# from app.modules.decision.engine.engine import DecisionEngine
# from app.modules.decision.engine.schemas import OptionScore


# option_a = uuid4()
# option_b = uuid4()
# option_c = uuid4()


# scores = [
#     OptionScore(
#         option_id=option_a,
#         score=0.40,
#     ),
#     OptionScore(
#         option_id=option_b,
#         score=0.80,
#     ),
#     OptionScore(
#         option_id=option_c,
#         score=0.60,
#     ),
# ]


# engine = DecisionEngine()

# ranked = engine.rank_options([])


# for option in ranked:
#     print(option)

'''Temporary for now'''
from uuid import uuid4
import pytest

from app.modules.decision.engine.engine import DecisionEngine
from app.modules.decision.engine.schemas import OptionScore

# Keep your unique ID configurations here
option_a = uuid4()
option_b = uuid4()
option_c = uuid4()

mock_scores = [
    OptionScore(option_id=option_a, score=0.40),
    OptionScore(option_id=option_b, score=0.80),
    OptionScore(option_id=option_c, score=0.60),
]


def test_rank_options_orders_by_highest_score():
    engine = DecisionEngine()
    
    # Process the active mockup dataset
    ranked = engine.rank_options(mock_scores)
    
    # Assertions to ensure standard operational output integrity
    assert len(ranked) == 3
    assert ranked[0].option_id == option_b  # Highest score (0.80) should be Rank 1
    assert ranked[0].rank == 1
    
    assert ranked[1].option_id == option_c  # Middle score (0.60) should be Rank 2
    assert ranked[1].rank == 2
    
    assert ranked[2].option_id == option_a  # Lowest score (0.40) should be Rank 3
    assert ranked[2].rank == 3


def test_rank_options_empty_list_raises_error():
    engine = DecisionEngine()
    
    # Safely intercept the expected error for the boundary test
    with pytest.raises(ValueError, match="No option scores provided."):
        engine.rank_options([])
