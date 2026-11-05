import pytest
import pandas as pd
from src.demographics import DemographicAnalyzer


def test_analyze_demographics():
    data = {
        "patient_age": [70, 68, 25, 45, 80],
        "patient_sex": ["M", "F", "M", "F", "M"],
        "serious": ["Y", "Y", "N", "N", "Y"],
        "outcome": ["Hospitalization", "Life-threatening", "Recovered", "Recovered", "Hospitalization"],
        "report_year": [2022, 2022, 2023, 2023, 2024],
    }
    df = pd.DataFrame(data)
    res = DemographicAnalyzer.analyze_demographics(df)

    assert res["total_reports"] == 5
    assert res["serious_reports"] == 3
    assert res["serious_percentage"] == 60.0
    assert res["age_strata"]["elderly_65_plus"] == 3
    assert res["age_strata"]["adult_18_to_64"] == 2
