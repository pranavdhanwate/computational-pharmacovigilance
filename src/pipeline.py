import argparse
from pathlib import Path
from typing import Dict, Any, Tuple
import pandas as pd

from .ingestion import FAERSDataIngestor
from .normalisation import DrugNormalizer
from .signal_detector import SignalDetector
from .demographics import DemographicAnalyzer
from .visualize import plot_forest_ror, plot_volcano_signals


def run_pharmacovigilance_pipeline(
    input_csv: str | Path = "data/faers_sample_safety_reports.csv",
    dictionary_json: str | Path = "data/drug_dictionary.json",
    output_dir: str | Path = "results",
    min_cases: int = 3,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Executes the complete pharmacovigilance data cleaning, signal detection, and visualization workflow."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    fig_dir = out_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    # 1. Ingestion & Case Deduplication
    raw_df, meta = FAERSDataIngestor.load_safety_dataset(input_csv, deduplicate_by_case=True)

    # 2. Drug Name Normalization
    normalizer = DrugNormalizer(dictionary_json)
    df_clean = normalizer.standardize_dataframe(raw_df, drug_col="drug_name", out_col="normalized_drug")

    # 3. Disproportionality Signal Detection
    signals_df = SignalDetector.screen_all_pairs(df_clean, min_cases=min_cases)
    signals_df.to_csv(out_dir / "safety_signals_disproportionality.csv", index=False)

    # 4. Demographic & Outcome Profiling
    demographics = DemographicAnalyzer.analyze_demographics(df_clean)
    pd.DataFrame([demographics]).to_csv(out_dir / "demographic_summary.csv", index=False)

    # 5. Scientific Visualizations
    plot_forest_ror(signals_df, fig_dir / "forest_plot_ror.png", top_n=10)
    plot_volcano_signals(signals_df, fig_dir / "volcano_plot_signals.png")

    return signals_df, demographics


def main():
    parser = argparse.ArgumentParser(description="Computational Pharmacovigilance Framework")
    parser.add_argument("--input", "-i", type=str, default="data/faers_sample_safety_reports.csv", help="Input FAERS CSV")
    parser.add_argument("--dict", "-d", type=str, default="data/drug_dictionary.json", help="Drug dictionary JSON")
    parser.add_argument("--output", "-o", type=str, default="results", help="Output directory")
    args = parser.parse_args()

    signals, demo = run_pharmacovigilance_pipeline(args.input, args.dict, output_dir=args.output)
    print("Pharmacovigilance Pipeline Executed! Top 5 Disproportionality Signals:")
    cols = ["drug", "event", "a", "ror", "ror_lower_95", "prr", "chi2_yates", "signal_classification"]
    print(signals[cols].head(5).to_string(index=False))
    print(f"\nDemographics: Total deduplicated cases = {demo['total_reports']}, Mean age = {demo['mean_age']}, Serious = {demo['serious_percentage']}%")


if __name__ == "__main__":
    main()
