from pathlib import Path
from typing import List, Optional
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_forest_ror(
    signals_df: pd.DataFrame,
    output_path: str | Path,
    top_n: int = 10,
) -> Path:
    """Generates Pharmacovigilance Forest Plot of ROR point estimates and 95% Confidence Intervals."""
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    subset = signals_df.head(top_n).iloc[::-1]

    labels = [f"{row['drug'].capitalize()} - {row['event']}" for _, row in subset.iterrows()]
    ror_vals = subset["ror"].values
    lower_vals = subset["ror_lower_95"].values
    upper_vals = subset["ror_upper_95"].values

    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)
    y_pos = np.arange(len(labels))

    # Error bars (lower to upper)
    xerr = [ror_vals - lower_vals, upper_vals - ror_vals]
    ax.errorbar(ror_vals, y_pos, xerr=xerr, fmt="o", color="#B71C1C", ecolor="#37474F", elinewidth=2.0, capsize=4, markersize=7)

    # Reference null line ROR = 1.0
    ax.axvline(1.0, color="gray", linestyle="--", linewidth=1.0, alpha=0.8, label="Null Line (ROR = 1.0)")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=9, fontweight="bold")
    ax.set_xlabel("Reporting Odds Ratio (ROR) [95% Confidence Interval]", fontsize=10, fontweight="bold")
    ax.set_title(f"Top {top_n} Disproportionality Safety Signals (FAERS)", fontsize=12, fontweight="bold")
    ax.grid(axis="x", linestyle=":", alpha=0.6)
    ax.legend(loc="lower right", fontsize=9)

    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    return out_path


def plot_volcano_signals(
    signals_df: pd.DataFrame,
    output_path: str | Path,
) -> Path:
    """Renders Volcano Plot: Effect Size ln(ROR) vs Statistical Significance -log10(p-value)."""
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    valid_df = signals_df[signals_df["p_value"] > 0].copy()
    log_ror = np.log(np.maximum(valid_df["ror"], 0.01))
    neg_log_p = -np.log10(np.maximum(valid_df["p_value"], 1e-50))

    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)

    # Colors based on signal classification
    colors = ["#C62828" if "Verified" in cat else
              "#F57C00" if "Potential" in cat else
              "#78909C" for cat in valid_df["signal_classification"]]

    ax.scatter(log_ror, neg_log_p, c=colors, s=55, alpha=0.8, edgecolors="black", linewidth=0.5)

    # Threshold guidelines
    ax.axvline(np.log(2.0), color="blue", linestyle=":", linewidth=1.0, label="PRR/ROR Threshold (>= 2.0)")
    ax.axhline(-np.log10(0.05), color="gray", linestyle="--", linewidth=0.8, label="Significance Threshold (p = 0.05)")

    ax.set_xlabel("Effect Size: ln(Reporting Odds Ratio)", fontsize=10, fontweight="bold")
    ax.set_ylabel("-log10(p-value) [Chi-Square Significance]", fontsize=10, fontweight="bold")
    ax.set_title("Pharmacovigilance Volcano Plot: Disproportionality Signal Discovery", fontsize=11, fontweight="bold")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper left", fontsize=8.5)

    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    return out_path
