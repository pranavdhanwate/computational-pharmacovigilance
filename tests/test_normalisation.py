import pytest
import json
from src.normalisation import DrugNormalizer


def test_drug_normalizer(tmp_path):
    dict_file = tmp_path / "dict.json"
    dict_file.write_text(json.dumps({"lipitor": "atorvastatin", "glucophage": "metformin"}))

    normalizer = DrugNormalizer(dict_file)

    assert normalizer.normalize_name("Lipitor") == "atorvastatin"
    assert normalizer.normalize_name("GLUCOPHAGE HCL") == "metformin"
    assert normalizer.normalize_name("Ciprofloxacin Hydrochloride") == "ciprofloxacin"
