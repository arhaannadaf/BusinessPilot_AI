# from app.modules.decision.engine.engine import DecisionEngine


# engine = DecisionEngine()


# score = engine.calculate_final_score(
#     weighted_score=1.0,
#     total_weight=0.0,
# )

# print("Final score:", score)

'''Temporary for now'''
import pytest
from app.modules.decision.engine.engine import DecisionEngine


def test_calculate_final_score_success():
    engine = DecisionEngine()
    
    # Pass valid, positive parameters to verify regular calculation paths
    score = engine.calculate_final_score(
        weighted_score=4.0,
        total_weight=2.0,
    )
    
    # Adjust this assertion value to match whatever formula your engine uses 
    # (e.g., if it divides weighted_score by total_weight, the result should be 2.0)
    assert score == 2.0


def test_calculate_final_score_zero_weight_raises_error():
    engine = DecisionEngine()
    
    # Intercept and validate the expected initialization error
    with pytest.raises(ValueError, match="Total Weight must be greater than zero."):
        engine.calculate_final_score(
            weighted_score=1.0,
            total_weight=0.0,
        )
