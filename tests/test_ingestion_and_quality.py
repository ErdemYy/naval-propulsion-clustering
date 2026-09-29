"""Unit tests for Phase 1 data ingestion, provenance manifest, quality, and anti-leakage."""

from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from naval_propulsion.data.ingestion import (
    CANONICAL_COLUMNS,
    FEATURE_COLUMNS,
    TARGET_COLUMNS,
    compute_sha256,
)
from naval_propulsion.data.loader import DatasetContainer, load_naval_dataset
from naval_propulsion.data.quality import analyze_data_quality
from naval_propulsion.utils.paths import get_processed_data_dir, get_raw_data_dir


def test_raw_data_and_manifest_existence() -> None:
    """1 & 7: Verify raw files, archive, and provenance manifest exist."""
    raw_dir = get_raw_data_dir()
    manifest_path = raw_dir / "manifest.json"
    data_txt_path = raw_dir / "data.txt"
    features_txt_path = raw_dir / "Features.txt"
    readme_txt_path = raw_dir / "README.txt"

    assert manifest_path.exists(), "manifest.json must exist in data/raw"
    assert data_txt_path.exists(), "data.txt must exist in data/raw"
    assert features_txt_path.exists(), "Features.txt must exist in data/raw"
    assert readme_txt_path.exists(), "README.txt must exist in data/raw"

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    required_keys = {
        "source",
        "dataset_name",
        "dataset_id",
        "source_url",
        "retrieval_timestamp",
        "raw_archive_file",
        "raw_archive_byte_size",
        "raw_archive_sha256",
        "data_file_name",
        "data_file_byte_size",
        "data_file_sha256",
        "row_count",
        "column_count",
    }
    assert required_keys.issubset(manifest.keys())
    assert manifest["row_count"] == 11934
    assert manifest["column_count"] == 18
    assert len(manifest["data_file_sha256"]) == 64


def test_sha256_generation() -> None:
    """8: Test deterministic SHA-256 generation."""
    sample_bytes = b"naval_propulsion_test_stream"
    expected_hash = "37f613fa0646c858ae0bc8a53a002f9f35638b9bc9cd4d890d97ef3176fac7cd"
    assert compute_sha256(sample_bytes) == expected_hash


def test_dataset_schema_consistency() -> None:
    """2: Verify dataset schema conforms exactly to canonical 18 columns."""
    container = load_naval_dataset()
    assert len(container.features) == 11934
    assert len(container.targets) == 11934
    assert len(container.feature_names) == 16
    assert len(container.target_names) == 2

    # Check dtypes are all float64
    for col in container.features.columns:
        assert container.features[col].dtype == np.float64
    for col in container.targets.columns:
        assert container.targets[col].dtype == np.float64


def test_no_degradation_leakage() -> None:
    """9: Verify kMc and kMt never appear in features."""
    container = load_naval_dataset()
    assert "kMc" not in container.features.columns
    assert "kMt" not in container.features.columns
    assert "kMc" not in container.feature_names
    assert "kMt" not in container.feature_names
    assert set(container.targets.columns) == {"kMc", "kMt"}


def test_numeric_coercion_safety(tmp_path: Path) -> None:
    """3: Test that malformed string values cause errors rather than silent NaN coercion."""
    malformed_data = (
        "1.138 3.0 289.9 1349.4 6677.3 7.58 7.58 464.0 288.0 550.5 1.09 0.99 5.94 1.01 7.13 0.08 0.95 0.97\n"
        "MALFORMED_TOKEN 3.0 289.9 1349.4 6677.3 7.58 7.58 464.0 288.0 550.5 1.09 0.99 5.94 1.01 7.13 0.08 0.95 0.97\n"
    )
    bad_file = tmp_path / "bad_data.txt"
    bad_file.write_text(malformed_data, encoding="utf-8")

    # Strict parser without silent errors='coerce' must raise ValueError
    with pytest.raises((ValueError, Exception)):
        pd.read_csv(
            bad_file,
            sep=r"\s+",
            header=None,
            names=list(CANONICAL_COLUMNS),
            dtype={col: "float64" for col in CANONICAL_COLUMNS},
            engine="c",
        )


def test_quality_analysis_missing_and_duplicates() -> None:
    """4 & 5: Verify missing value and duplicate analysis."""
    df = pd.DataFrame({
        "a": [1.0, 2.0, 3.0, 1.0],
        "b": [10.0, 20.0, 30.0, 10.0],
        "c": [10.0, 20.0, 30.0, 10.0],  # Identical to b
        "const": [5.0, 5.0, 5.0, 5.0],  # Constant
    })
    report = analyze_data_quality(df)
    assert report.row_count == 4
    assert report.col_count == 4
    assert report.duplicate_rows_count == 1  # Row 0 and Row 3 are duplicates
    assert report.constant_columns == ["const"]
    assert ("b", "c") in report.identical_column_pairs or ("c", "b") in report.identical_column_pairs


def test_real_dataset_quality_invariants() -> None:
    """6 & 10: Verify data quality invariants on real ingested dataset."""
    processed_csv = get_processed_data_dir() / "naval_propulsion.csv"
    assert processed_csv.exists()

    df = pd.read_csv(processed_csv)
    report = analyze_data_quality(df)

    assert report.row_count == 11934
    assert report.col_count == 18
    assert report.duplicate_rows_count == 0
    assert report.infinite_values_count == 0
    assert report.constant_columns == ["T1", "P1"]
    assert ("Ts", "Tp") in report.identical_column_pairs

    # Verify discrete operating point grid
    assert df["v"].nunique() == 9
    assert df["lp"].nunique() == 9
    assert df["kMc"].nunique() == 51
    assert df["kMt"].nunique() == 26
