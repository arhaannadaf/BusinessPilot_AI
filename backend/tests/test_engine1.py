from uuid import uuid4

from app.modules.decision.scenario.engine.engine import ScenarioEngine
from app.modules.decision.scenario.engine.schemas import ScenarioChange


def test_percentage_change():
    engine = ScenarioEngine()

    change = ScenarioChange(
        metric_name="Annualized Revenue",
        change_type="percentage",
        change_value=10,
    )

    result = engine.evaluate_metric(
        original_value=1_000_000,
        change=change,
    )

    assert result.original_value == 1_000_000
    assert result.adjusted_value == 1_100_000


def test_negative_percentage_change():
    engine = ScenarioEngine()

    change = ScenarioChange(
        metric_name="Operational Cost",
        change_type="percentage",
        change_value=-5,
    )

    result = engine.evaluate_metric(
        original_value=400_000,
        change=change,
    )

    assert result.adjusted_value == 380_000


def test_absolute_change():
    engine = ScenarioEngine()

    change = ScenarioChange(
        metric_name="Annualized Revenue",
        change_type="absolute",
        change_value=50_000,
    )

    result = engine.evaluate_metric(
        original_value=1_000_000,
        change=change,
    )

    assert result.adjusted_value == 1_050_000


def test_invalid_change_type():
    engine = ScenarioEngine()

    change = ScenarioChange(
        metric_name="Annualized Revenue",
        change_type="invalid",
        change_value=10,
    )

    try:
        engine.evaluate_metric(
            original_value=1_000_000,
            change=change,
        )
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "Unsupported change type" in str(exc)