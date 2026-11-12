
from app.modules.data.profiling.quality_rules import (
    classify_quality_regression,
)


def test_no_quality_regression():
    result = classify_quality_regression(
        previous_completeness=100.0,
        current_completeness=98.0,
        previous_duplicate_rows=5,
        current_duplicate_rows=3,
    )

    assert result["severity"] == "NO_REGRESSION"
    assert result["completeness_drop"] == 2.0
    assert result["duplicate_rows_increase"] == 0
    assert result["reasons"] == []


def test_completeness_warning():
    result = classify_quality_regression(
        previous_completeness=100.0,
        current_completeness=95.0,
        previous_duplicate_rows=0,
        current_duplicate_rows=0,
    )

    assert result["severity"] == "WARNING"
    assert result["completeness_drop"] == 5.0
    assert "COMPLETENESS_DROP" in result["reasons"]


def test_completeness_critical():
    result = classify_quality_regression(
        previous_completeness=100.0,
        current_completeness=75.0,
        previous_duplicate_rows=0,
        current_duplicate_rows=0,
    )

    assert result["severity"] == "CRITICAL"
    assert result["completeness_drop"] == 25.0
    assert "CRITICAL_COMPLETENESS_DROP" in result["reasons"]


def test_duplicate_increase_warning():
    result = classify_quality_regression(
        previous_completeness=100.0,
        current_completeness=100.0,
        previous_duplicate_rows=0,
        current_duplicate_rows=2,
    )

    assert result["severity"] == "WARNING"
    assert result["duplicate_rows_increase"] == 2
    assert "DUPLICATE_INCREASE" in result["reasons"]


def test_critical_severity_takes_precedence():
    result = classify_quality_regression(
        previous_completeness=100.0,
        current_completeness=95.0,
        previous_duplicate_rows=0,
        current_duplicate_rows=10,
    )

    assert result["severity"] == "CRITICAL"
    assert "COMPLETENESS_DROP" in result["reasons"]
    assert "CRITICAL_DUPLICATE_INCREASE" in result["reasons"]
