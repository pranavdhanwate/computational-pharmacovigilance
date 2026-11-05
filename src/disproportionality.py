import math
from typing import Dict, Any, List
import numpy as np
import pandas as pd
from scipy.stats import chi2


class DisproportionalityCalculator:
    """Calculates statistical disproportionality metrics (ROR, PRR, IC) from 2x2 contingency tables."""

    @staticmethod
    def build_contingency_table(
        df: pd.DataFrame,
        target_drug: str,
        target_event: str,
        drug_col: str = "normalized_drug",
        event_col: str = "preferred_term",
    ) -> Dict[str, int]:
        d_lower = target_drug.lower()
        e_lower = target_event.lower()

        is_drug = df[drug_col].str.lower() == d_lower
        is_event = df[event_col].str.lower() == e_lower

        a = int(np.sum(is_drug & is_event))
        b = int(np.sum(is_drug & ~is_event))
        c = int(np.sum(~is_drug & is_event))
        d = int(np.sum(~is_drug & ~is_event))

        return {"a": a, "b": b, "c": c, "d": d, "total": a + b + c + d}

    @classmethod
    def calculate_metrics(cls, a: int, b: int, c: int, d: int) -> Dict[str, Any]:
        """Calculates ROR, PRR, Chi-square (with Yates correction), and Bayesian Information Component (IC)."""
        n = a + b + c + d
        if a == 0 or b == 0 or c == 0 or d == 0 or n == 0:
            return {
                "a": a, "b": b, "c": c, "d": d,
                "ror": 0.0, "ror_lower_95": 0.0, "ror_upper_95": 0.0,
                "prr": 0.0, "prr_lower_95": 0.0, "prr_upper_95": 0.0,
                "chi2_yates": 0.0, "p_value": 1.0,
                "ic": 0.0, "ic_lower_025": 0.0,
            }

        # 1. Reporting Odds Ratio (ROR)
        ror = (a * d) / (b * c)
        se_ln_ror = math.sqrt((1.0 / a) + (1.0 / b) + (1.0 / c) + (1.0 / d))
        ror_lower = math.exp(math.log(ror) - (1.96 * se_ln_ror))
        ror_upper = math.exp(math.log(ror) + (1.96 * se_ln_ror))

        # 2. Proportional Reporting Ratio (PRR)
        p_drug = a / (a + b)
        p_other = c / (c + d)
        prr = p_drug / p_other if p_other > 0 else 0.0

        var_ln_prr = (1.0 / a) - (1.0 / (a + b)) + (1.0 / c) - (1.0 / (c + d))
        se_ln_prr = math.sqrt(max(0.0, var_ln_prr))
        prr_lower = math.exp(math.log(prr) - (1.96 * se_ln_prr)) if prr > 0 else 0.0
        prr_upper = math.exp(math.log(prr) + (1.96 * se_ln_prr)) if prr > 0 else 0.0

        # 3. Chi-square with Yates continuity correction
        numerator = max(0.0, abs(a * d - b * c) - (n / 2.0)) ** 2 * n
        denominator = float((a + b) * (c + d) * (a + c) * (b + d))
        chi2_val = numerator / denominator if denominator > 0 else 0.0
        p_val = float(chi2.sf(chi2_val, df=1))

        # 4. Bayesian Information Component (BCPNN / IC)
        expected_a = ((a + b) * (a + c)) / n
        ic = math.log2((a + 0.5) / (expected_a + 0.5))
        ic_lower = ic - (3.3 / math.sqrt(a + 0.5))

        return {
            "a": a, "b": b, "c": c, "d": d,
            "ror": round(float(ror), 3),
            "ror_lower_95": round(float(ror_lower), 3),
            "ror_upper_95": round(float(ror_upper), 3),
            "prr": round(float(prr), 3),
            "prr_lower_95": round(float(prr_lower), 3),
            "prr_upper_95": round(float(prr_upper), 3),
            "chi2_yates": round(float(chi2_val), 3),
            "p_value": float(f"{p_val:.2e}"),
            "ic": round(float(ic), 3),
            "ic_lower_025": round(float(ic_lower), 3),
        }
