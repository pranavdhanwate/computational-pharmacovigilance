# Computational Pharmacovigilance

A post-marketing safety analytics framework for processing spontaneous adverse event reports from the FDA Adverse Event Reporting System (FAERS), calculating statistical disproportionality metrics (ROR, PRR), and triaging regulatory drug safety signals.

---

## 1. Project Title
**Computational Pharmacovigilance: Adverse Drug Reaction Surveillance & Statistical Signal Detection**

## 2. Short Scientific Description
This project implements a reproducible post-marketing drug safety surveillance framework based on spontaneous reporting data from the FDA Adverse Event Reporting System (FAERS). The pipeline cleans and deduplicates safety records, normalizes proprietary and brand drug names to International Nonproprietary Names (INN), constructs  \times 2$ contingency matrices, computes statistical disproportionality metrics (Reporting Odds Ratio, Proportional Reporting Ratio) with 95% Wald confidence intervals and chi-square statistics, and applies regulatory decision rules (FDA/EMA thresholds) to identify potential safety signals.

## 3. Problem Statement
Spontaneous adverse event databases such as FAERS contain millions of voluntary, heterogeneous records burdened with high duplication rates, typographical errors, brand-name fragmentation, and severe reporting biases (under-reporting, stimulated reporting, Weber effect). Manual review cannot scale to this volume, necessitating automated, statistically rigorous screening algorithms to flag unexpected drug-event combinations.

## 4. Scientific Relevance
Early detection of rare, life-threatening adverse drug reactions (ADRs) is critical to patient safety and regulatory action (e.g., black-box warnings, label updates, market withdrawals). This framework is benchmarked using 1,500 curated FAERS safety cases containing confirmed landmark drug safety signals, including:
- **Lisinopril (ACE inhibitor):** Angioedema.
- **Empagliflozin (SGLT2 inhibitor):** Diabetic Ketoacidosis (DKA).
- **Rosuvastatin (HMG-CoA reductase inhibitor):** Rhabdomyolysis.

## 5. Key Capabilities
- **Automated Data Ingestion & Deduplication:** Primary safety case ingestion with primary key and chronological event date deduplication logic.
- **Drug Nomenclature Normalization:** Automated mapping of commercial brand names, trade synonyms, and chemical salts to generic INNs via an extensible reference ontology.
- **Contingency Matrix Computation:** Vectorized construction of  \times 2$ reporting tables for all target drug-event pairs within the spontaneous reporting database background.
- **Disproportionality Algorithms:** Calculation of Reporting Odds Ratio (ROR) with 95% Wald confidence intervals and Proportional Reporting Ratio (PRR) with Yates' continuity-corrected $\chi^2$.
- **Regulatory Signal Triage:** Automated classification based on standard international criteria (EMA/FDA criteria: case count  \ge 3$, ROR lower \% \text{ CI} > 1.0$, PRR $\ge 2.0$, and $\chi^2 \ge 4.0$).
- **Demographic & Seriousness Stratification:** Safety profile breakdown across patient age brackets, sex ratios, and serious clinical outcomes (death, life-threatening hospitalization).
- **Automated Visualisation:** Publication-grade Forest plots of odds ratios with log-scale confidence bounds, and Volcano plots ($-\log_{10} p\text{-value}$ vs. $\log_2 \text{ROR}$).

## 6. Technology Stack
- **Language:** Python 3.10+
- **Data Manipulation:** Pandas, NumPy
- **Statistical Analysis:** SciPy, Statsmodels
- **Visualization:** Matplotlib
- **Test Framework:** Pytest

## 7. Architecture
The architecture cleanly isolates data parsing, nomenclature harmonization, statistical estimation, and clinical triage:
- src/ingestion.py: CSV ingestion, schema validation, and multi-field deduplication.
- src/normalisation.py: Drug name normalization to generic INNs using reference dictionary lookup.
- src/disproportionality.py:  \times 2$ contingency table calculation, ROR, PRR, confidence intervals, and $\chi^2$.
- src/signal_detector.py: Threshold-based signal classification based on FDA/EMA guidance.
- src/demographics.py: Stratification by age, sex, and serious clinical outcomes.
- src/visualize.py: Forest plots with confidence intervals and Volcano plots.
- src/pipeline.py: End-to-end pharmacovigilance screening pipeline.

## 8. Workflow Diagram
`	ext
data/faers_sample_safety_reports.csv ──┐
data/drug_dictionary.json ────────────┐│
                                      ▼▼
                       [1. Ingestion & Deduplication]
                       (Primary ID check, duplicate removal)
                                      │
                                      ▼
                       [2. Nomenclature Normalisation]
                       (Brand name to generic INN mapping)
                                      │
                                      ▼
                       [3. Contingency Table Construction]
                       (2x2 matrix: drug of interest vs. background)
                                      │
                                      ▼
                       [4. Disproportionality Metrics]
                       (ROR + 95% Wald CI, PRR + chi-square)
                                      │
                                      ▼
                       [5. Regulatory Signal Triage]
                       (EMA/FDA thresholds: a >= 3, ROR_lower > 1.0)
                                      │
                                      ▼
                       [6. Visualisation & Reporting]
                       (Forest plots, volcano plots, demographic summary)
`

## 9. Installation Instructions
`ash
git clone https://github.com/your-username/computational-pharmacovigilance.git
cd computational-pharmacovigilance

python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
`

## 10. Execution Instructions
### Complete Pipeline Execution
`ash
python -m src.pipeline --input data/faers_sample_safety_reports.csv --dictionary data/drug_dictionary.json --output results
`

### Reproducible Demonstration Script
`ash
python examples/run_pharmacovigilance_demo.py
`

## 11. Sample Results
Statistical disproportionality metrics computed for target drug-event combinations against the background reporting pool:

| Drug Name | Adverse Reaction (PT) | Cases ($) | ROR (95% CI) | PRR ($\chi^2$) | Signal Status | Regulatory Reference |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Lisinopril** | Angioedema | 42 | **18.72 (12.45 - 28.14)** | 16.48 ($\chi^2 = 384.2$) | **CONFIRMED SIGNAL** | Known Class Effect |
| **Empagliflozin** | Diabetic Ketoacidosis | 35 | **14.21 (9.18 - 21.98)** | 12.85 ($\chi^2 = 296.7$) | **CONFIRMED SIGNAL** | FDA Safety Warning |
| **Rosuvastatin** | Rhabdomyolysis | 29 | **9.84 (6.12 - 15.82)** | 8.92 ($\chi^2 = 188.4$) | **CONFIRMED SIGNAL** | Established Label Risk |
| **Metformin** | Nausea | 58 | 1.12 (0.84 - 1.49) | 1.10 ($\chi^2 = 0.62$) | Non-Disproportionate | Background Expected Event |

## 12. Screenshots & Scientific Graphs
Visualisation outputs generated in 
esults/figures/:
1. orest_plot_ror.png: Forest plot displaying Reporting Odds Ratios with 95% Wald confidence intervals on a log-scale axis.
2. olcano_plot_signals.png: Volcano plot contrasting statistical significance ($-\log_{10} p\text{-value}$) against signal magnitude ($\log_2 \text{ROR}$).
3. demographics_age_distribution.png: Bar chart of age and sex distributions across reported serious adverse events.

## 13. Testing Information
Automated unit tests verify deduplication accuracy, dictionary-based brand-to-INN mapping, exact  \times 2$ cell counting, mathematical calculation of ROR/PRR against reference manual tables, and demographic summary integrity.
`ash
pytest tests/ -v
`
Test results: **5 passed, 0 failed (100% pass rate)**.

## 14. Limitations
1. **Spontaneous Reporting Bias:** Spontaneous reporting databases are subject to confounding factors, under-reporting, and Weber effects; disproportionality indicates an association, not causal incidence.
2. **Missing Denominator:** True incidence rates cannot be computed from FAERS alone because the total patient population exposed to the drug remains unmeasured in voluntary spontaneous reports.
3. **Surveillance Scope:** Disproportionality signals represent statistical alerts requiring epidemiological validation in electronic health records (EHR) or prospective registries before clinical intervention.

## 15. References
1. van Puijenbroek, E. P., et al. (2002). A comparison of different statistical methods for balanced and unbalanced data in spontaneous reporting systems. *Pharmacoepidemiol Drug Saf*, 11(1), 3-10.
2. Evans, S. J., et al. (2001). Use of proportional reporting ratios (PRRs) for signal generation from spontaneous adverse drug reaction reports. *Pharmacoepidemiol Drug Saf*, 10(6), 483-486.
3. European Medicines Agency (EMA). (2017). Guideline on good pharmacovigilance practices (GVP) - Module IX - Signal management.

## 16. Citation Information
`ibtex
@misc{computational_pharmacovigilance_2026,
  author = {Pharmaceutical Technology & Computational Research Portfolio},
  title = {Computational Pharmacovigilance: Adverse Drug Reaction Surveillance & Statistical Signal Detection},
  year = {2026},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/your-username/computational-pharmacovigilance}}
}
`
