import json
from pathlib import Path
from typing import Dict, Optional
import pandas as pd


class DrugNormalizer:
    """Normalizes proprietary brand names and salt variants to standardized generic active substances."""

    def __init__(self, mapping_dict_path: Optional[str | Path] = None):
        self.dictionary: Dict[str, str] = {}
        if mapping_dict_path:
            dict_path = Path(mapping_dict_path)
            if dict_path.exists():
                with open(dict_path, "r", encoding="utf-8") as f:
                    self.dictionary = {k.lower(): v.lower() for k, v in json.load(f).items()}

    def normalize_name(self, raw_drug_name: str) -> str:
        if not raw_drug_name or pd.isna(raw_drug_name):
            return "unknown"

        clean = str(raw_drug_name).strip().lower()

        # Remove common salt extensions
        salts = [" hydrochloride", " hcl", " sodium", " potassium", " maleate", " tartrate", " mesylate"]
        for s in salts:
            if clean.endswith(s):
                clean = clean[:-len(s)].strip()

        # Check lookup dictionary
        return self.dictionary.get(clean, clean)

    def standardize_dataframe(
        self,
        df: pd.DataFrame,
        drug_col: str = "drug_name",
        out_col: str = "normalized_drug",
    ) -> pd.DataFrame:
        result_df = df.copy()
        result_df[out_col] = result_df[drug_col].apply(self.normalize_name)
        return result_df
