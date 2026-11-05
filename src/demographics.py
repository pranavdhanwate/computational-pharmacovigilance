from typing import Dict, Any
import numpy as np
import pandas as pd


class DemographicAnalyzer:
    """Analyzes patient age, sex distribution, outcomes, and seriousness patterns."""

    @staticmethod
    def analyze_demographics(df: pd.DataFrame) -> Dict[str, Any]:
        total = len(df)
        if total == 0:
            return {}

        # Age profiling
        valid_ages = df["patient_age"].dropna()
        mean_age = float(valid_ages.mean()) if len(valid_ages) > 0 else 0.0
        median_age = float(valid_ages.median()) if len(valid_ages) > 0 else 0.0

        pediatric = int(np.sum(valid_ages < 18))
        adult = int(np.sum((valid_ages >= 18) & (valid_ages < 65)))
        elderly = int(np.sum(valid_ages >= 65))

        # Sex breakdown
        sex_counts = df["patient_sex"].value_counts().to_dict()

        # Seriousness & Outcomes
        serious_count = int(np.sum(df["serious"] == "Y"))
        serious_pct = round((serious_count / total) * 100.0, 2)
        outcome_counts = df["outcome"].value_counts().to_dict()

        # Reporting by year
        year_counts = df["report_year"].value_counts().sort_index().to_dict()

        return {
            "total_reports": total,
            "mean_age": round(mean_age, 1),
            "median_age": round(median_age, 1),
            "age_strata": {
                "pediatric_under_18": pediatric,
                "adult_18_to_64": adult,
                "elderly_65_plus": elderly,
            },
            "sex_distribution": sex_counts,
            "serious_reports": serious_count,
            "serious_percentage": serious_pct,
            "clinical_outcomes": outcome_counts,
            "longitudinal_reporting_years": year_counts,
        }
