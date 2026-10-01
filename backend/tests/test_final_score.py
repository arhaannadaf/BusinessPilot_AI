from app.modules.decision.engine.engine import DecisionEngine


engine = DecisionEngine()


score = engine.calculate_final_score(
    weighted_score=1.0,
    total_weight=0.0,
)

print("Final score:", score)