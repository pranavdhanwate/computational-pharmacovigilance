import pytest
from src.signal_detector import SignalDetector


def test_evaluate_signal_classification():
    # Strong signal table metrics
    strong_metrics = {
        "a": 25, "b": 75, "c": 10, "d": 890,
        "ror": 29.67, "ror_lower_95": 13.8, "ror_upper_95": 63.7,
        "prr": 22.5, "prr_lower_95": 11.2, "prr_upper_95": 45.1,
        "chi2_yates": 140.2, "ic": 3.8, "ic_lower_025": 3.1,
    }
    eval_res = SignalDetector.evaluate_signal(strong_metrics)

    assert eval_res["meets_evans"] is True
    assert eval_res["meets_ror"] is True
    assert eval_res["meets_bcpnn"] is True
    assert "Verified" in eval_res["signal_classification"]
