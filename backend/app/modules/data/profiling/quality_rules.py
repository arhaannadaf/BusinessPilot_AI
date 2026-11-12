
from dataclasses import dataclass


@dataclass(frozen=True)
class QualityRules:
    completeness_warning_drop: float = 5.0
    completeness_critical_drop: float = 20.0
    duplicate_rows_warning_increase: int = 1
    duplicate_rows_critical_increase: int = 10

def classify_quality_regression(
    previous_completeness: float,
    current_completeness: float,
    previous_duplicate_rows: int,
    current_duplicate_rows: int,
    rules: QualityRules | None = None,
) -> dict:
    rules = rules or QualityRules()

    completeness_drop = max(
        0.0,
        previous_completeness - current_completeness,
    )

    duplicate_increase = max(
        0,
        current_duplicate_rows - previous_duplicate_rows,
    )

    reasons = []
    severity = "NO_REGRESSION"

    # Completeness regression
    if completeness_drop >= rules.completeness_critical_drop:
        severity = "CRITICAL"
        reasons.append("CRITICAL_COMPLETENESS_DROP")
    elif completeness_drop >= rules.completeness_warning_drop:
        severity = "WARNING"
        reasons.append("COMPLETENESS_DROP")

    # Duplicate-row regression
    if duplicate_increase >= rules.duplicate_rows_critical_increase:
        severity = "CRITICAL"
        reasons.append("CRITICAL_DUPLICATE_INCREASE")
    elif duplicate_increase >= rules.duplicate_rows_warning_increase:
        if severity != "CRITICAL":
            severity = "WARNING"
        reasons.append("DUPLICATE_INCREASE")

    return {
        "severity": severity,
        "completeness_drop": round(completeness_drop, 2),
        "duplicate_rows_increase": duplicate_increase,
        "reasons": reasons,
    }
