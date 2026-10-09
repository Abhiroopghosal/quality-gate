import pytest
from qualitygate.core.grading import grade_soft

def test_grade_score_zero_risk_at_zero():
    assert grade_soft(0.0, threshold=0.1, kink=0.2) == pytest.approx(0.0)

def test_grade_soft_reaches_kink_at_threshold():
    assert grade_soft(0.1, threshold=0.1, kink=0.2) == pytest.approx(0.2)

def test_grade_soft_reaches_full_risk_at_one():
    assert grade_soft(1.0, threshold=0.1, kink=0.2) == pytest.approx(1.0)

def test_grade_soft_rejects_invalid_threshold():
    with pytest.raises(ValueError):
        grade_soft(0.5, threshold=1.0, kink=0.2)
