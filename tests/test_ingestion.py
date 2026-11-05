import pytest
import pandas as pd
from src.ingestion import FAERSDataIngestor


def test_load_safety_dataset_deduplication(tmp_path):
    csv_file = tmp_path / "test_faers.csv"
    csv_file.write_text(
        "case_id,drug_name,preferred_term,report_year,patient_age,patient_sex,serious,outcome\n"
        "101,Lipitor,Rhabdomyolysis,2022,65,M,Y,Hospitalization\n"
        "101,Lipitor,Rhabdomyolysis,2023,65,M,Y,Hospitalization\n"
        "102,Metformin,Nausea,2023,55,F,N,Recovered\n"
    )
    df, meta = FAERSDataIngestor.load_safety_dataset(csv_file, deduplicate_by_case=True)

    assert meta["initial_records"] == 3
    assert meta["deduplicated_records"] == 2
    assert meta["duplicates_removed"] == 1
    # Check that the 2023 version was kept
    case101 = df[df["case_id"] == 101]
    assert case101.iloc[0]["report_year"] == 2023
