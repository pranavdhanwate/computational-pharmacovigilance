from typing import Dict, Any, List
import pandas as pd
from .disproportionality import DisproportionalityCalculator


class SignalDetector:
    """Applies international regulatory thresholds (Evans, FDA, EMA, WHO) to flag safety signals."""

    @staticmethod
    def evaluate_signal(metrics: Dict[str, Any]) -> Dict[str, Any]:
        a = metrics["a"]
        ror_lower = metrics["ror_lower_95"]
        prr = metrics["prr"]
        chi2_val = metrics["chi2_yates"]
        ic_lower = metrics["ic_lower_025"]

        # Evans Criteria: PRR >= 2.0, Chi2 >= 4.0, a >= 3
        meets_evans = (prr >= 2.0) and (chi2_val >= 4.0) and (a >= 3)

        # ROR Criterion: Lower 95% CI > 1.0 and a >= 3
        meets_ror = (ror_lower > 1.0) and (a >= 3)

        # WHO-UMC / BCPNN Criterion: IC025 > 0
        meets_bcpnn = (ic_lower > 0.0)

        if meets_evans and meets_ror and meets_bcpnn:
            classification = "Verified Multi-Method Safety Signal"
        elif meets_ror or meets_evans:
            classification = "Potential Safety Signal (Further Audit)"
        else:
            classification = "No Disproportionality Signal"

        result = dict(metrics)
        result["meets_evans"] = meets_evans
        result["meets_ror"] = meets_ror
        result["meets_bcpnn"] = meets_bcpnn
        result["signal_classification"] = classification
        return result

    @classmethod
    def screen_all_pairs(
        cls,
        df: pd.DataFrame,
        min_cases: int = 3,
        drug_col: str = "normalized_drug",
        event_col: str = "preferred_term",
    ) -> pd.DataFrame:
        """Screens all observed drug-event pairs that meet minimum case threshold."""
        pair_counts = df.groupby([drug_col, event_col]).size().reset_index(name="count")
        candidate_pairs = pair_counts[pair_counts["count"] >= min_cases]

        results = []
        for _, row in candidate_pairs.iterrows():
            drug = row[drug_col]
            event = row[event_col]

            ct = DisproportionalityCalculator.build_contingency_table(
                df, target_drug=drug, target_event=event, drug_col=drug_col, event_col=event_col
            )
            raw_metrics = DisproportionalityCalculator.calculate_metrics(ct["a"], ct["b"], ct["c"], ct["d"])
            eval_record = cls.evaluate_signal(raw_metrics)
            eval_record["drug"] = drug
            eval_record["event"] = event
            results.append(eval_record)

        res_df = pd.DataFrame(results)
        return res_df.sort_values(by="ror", ascending=False).reset_index(drop=True)
