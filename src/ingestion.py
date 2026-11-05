from pathlib import Path
from typing import Dict, Any, Tuple
import pandas as pd


class FAERSDataIngestor:
    """Ingests, cleans, and deduplicates FDA FAERS spontaneous adverse event reports."""

    @staticmethod
    def load_safety_dataset(
        filepath: str | Path,
        deduplicate_by_case: bool = True,
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"FAERS dataset not found at: {path}")

        raw_df = pd.read_csv(path)
        initial_count = len(raw_df)

        # Standardize missing strings
        clean_df = raw_df.copy()
        clean_df["patient_sex"] = clean_df["patient_sex"].fillna("UNK").astype(str).str.upper()
        clean_df["patient_age"] = pd.to_numeric(clean_df["patient_age"], errors="coerce")
        clean_df["serious"] = clean_df["serious"].fillna("N").astype(str).str.upper()

        duplicates_removed = 0
        if deduplicate_by_case and "case_id" in clean_df.columns:
            # Sort by report_year descending to retain the latest follow-up version of the case
            clean_df = clean_df.sort_values(by="report_year", ascending=False)
            before_dedup = len(clean_df)
            clean_df = clean_df.drop_duplicates(subset=["case_id", "drug_name", "preferred_term"], keep="first")
            duplicates_removed = before_dedup - len(clean_df)

        metadata = {
            "initial_records": initial_count,
            "deduplicated_records": len(clean_df),
            "duplicates_removed": duplicates_removed,
            "unique_cases": clean_df["case_id"].nunique() if "case_id" in clean_df.columns else len(clean_df),
            "reporting_years": sorted(clean_df["report_year"].dropna().unique().astype(int).tolist()),
        }
        return clean_df.reset_index(drop=True), metadata
