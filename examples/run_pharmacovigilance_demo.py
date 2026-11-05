import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.pipeline import run_pharmacovigilance_pipeline

if __name__ == "__main__":
    data_csv = project_root / "data" / "faers_sample_safety_reports.csv"
    dict_json = project_root / "data" / "drug_dictionary.json"
    out_dir = project_root / "results"

    print("Running Computational Pharmacovigilance Safety Screening Demo...")
    signals_df, demo = run_pharmacovigilance_pipeline(data_csv, dict_json, output_dir=out_dir)

    print("\nVerified Disproportionality Signals (Top 6):")
    cols = ["drug", "event", "a", "ror", "ror_lower_95", "prr", "chi2_yates", "signal_classification"]
    print(signals_df[cols].head(6).to_string(index=False))
    print(f"\nCohort Overview: Mean Age = {demo['mean_age']}, Serious = {demo['serious_percentage']}%")
