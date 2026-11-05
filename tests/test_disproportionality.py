import pytest
from src.disproportionality import DisproportionalityCalculator


def test_calculate_metrics_known_table():
    # Known 2x2 contingency table:
    # Target Drug + Event (a) = 30
    # Target Drug + Other (b) = 70
    # Other Drug + Event (c) = 20
    # Other Drug + Other (d) = 880
    metrics = DisproportionalityCalculator.calculate_metrics(a=30, b=70, c=20, d=880)

    # ROR = (30 * 880) / (70 * 20) = 26400 / 1400 = 18.857
    assert pytest.approx(metrics["ror"], abs=0.01) == 18.86
    assert metrics["ror_lower_95"] > 1.0
    assert metrics["prr"] > 1.0
    assert metrics["chi2_yates"] > 50.0
    assert metrics["p_value"] < 0.001
    assert metrics["ic"] > 0.0
