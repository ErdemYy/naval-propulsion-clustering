"""Tests for Phase 4 scientific validation, statistical testing, and final model serialization."""

from __future__ import annotations

import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import pytest

from naval_propulsion.data.loader import load_naval_dataset
from naval_propulsion.evaluation.phase4_runner import reload_and_verify_final_model
from naval_propulsion.evaluation.validation import (
    analyze_degradation_grid_occupancy,
    analyze_operating_speed_invariance,
    compute_cliffs_delta,
    interpret_cliffs_delta,
    run_bootstrap_cluster_validation,
    run_pairwise_degradation_tests,
)
from naval_propulsion.features.registry import (
    CANDIDATE_REPRESENTATIONS,
    build_representation_data,
)
from naval_propulsion.utils.paths import get_models_dir


def test_cliffs_delta_calculation() -> None:
    """Verify that Cliff's delta correctly measures effect size and handles extreme separations."""
    # Complete separation: all x1 > x2 -> delta = 1.0
    x1 = np.array([10.0, 11.0, 12.0, 13.0])
    x2 = np.array([1.0, 2.0, 3.0, 4.0])
    d = compute_cliffs_delta(x1, x2)
    assert np.isclose(d, 1.0)
    assert interpret_cliffs_delta(d) == "Large"

    # Opposite separation -> delta = -1.0
    d_neg = compute_cliffs_delta(x2, x1)
    assert np.isclose(d_neg, -1.0)
    assert interpret_cliffs_delta(d_neg) == "Large"

    # Identical distributions -> delta = 0.0
    d_zero = compute_cliffs_delta(x1, x1)
    assert np.isclose(d_zero, 0.0)
    assert interpret_cliffs_delta(d_zero) == "Negligible"


def test_pairwise_degradation_tests_and_fdr_correction() -> None:
    """Verify that pairwise Mann-Whitney tests compute valid p-values and FDR corrections."""
    np.random.seed(42)
    # Synthetic 3 clusters
    n_per = 100
    labels = np.array([0] * n_per + [1] * n_per + [2] * n_per)
    target = np.concatenate([
        np.random.normal(10.0, 1.0, n_per),
        np.random.normal(10.0, 1.0, n_per),
        np.random.normal(5.0, 1.0, n_per),
    ])

    results = run_pairwise_degradation_tests(labels, target, "synthetic_target")
    assert len(results) == 3  # (0 vs 1), (0 vs 2), (1 vs 2)

    for res in results:
        assert 0.0 <= res.raw_p_value <= 1.0
        assert 0.0 <= res.adjusted_p_value <= 1.0
        assert res.adjusted_p_value >= res.raw_p_value - 1e-9  # FDR adjusted >= raw
        assert -1.0 <= res.cliffs_delta <= 1.0
        assert res.effect_size_interpretation in {"Negligible", "Small", "Medium", "Large"}


def test_bootstrap_determinism_and_bounds() -> None:
    """Verify that bootstrap stability validation is deterministic given random_state."""
    np.random.seed(42)
    X = np.random.randn(200, 5)

    boot1 = run_bootstrap_cluster_validation(X, n_clusters=2, n_bootstraps=10, random_state=42)
    boot2 = run_bootstrap_cluster_validation(X, n_clusters=2, n_bootstraps=10, random_state=42)

    assert boot1["mean_ari"] == pytest.approx(boot2["mean_ari"])
    assert boot1["std_ari"] == pytest.approx(boot2["std_ari"])
    assert 0.0 <= boot1["mean_ari"] <= 1.0
    assert boot1["ci_2_5_percentile"] <= boot1["ci_97_5_percentile"]


def test_speed_wise_cluster_proportion_calculation() -> None:
    """Verify operating speed invariance calculations."""
    speeds = np.array([3.0] * 50 + [6.0] * 50)
    labels = np.array([0] * 25 + [1] * 25 + [0] * 25 + [1] * 25)

    res = analyze_operating_speed_invariance(labels, speeds)
    records = res["speed_records"]
    assert len(records) == 2
    assert records[0]["speed"] == 3.0
    assert records[0]["cluster_0_proportion"] == pytest.approx(0.5)
    assert records[0]["cluster_1_proportion"] == pytest.approx(0.5)
    assert records[1]["speed"] == 6.0
    assert records[1]["cluster_0_proportion"] == pytest.approx(0.5)
    assert records[1]["cluster_1_proportion"] == pytest.approx(0.5)
    assert res["cramers_v"] == pytest.approx(0.0)


def test_degradation_grid_generation() -> None:
    """Verify degradation grid occupancy mapping."""
    kmc = np.array([0.95, 0.95, 1.0, 1.0])
    kmt = np.array([0.98, 0.99, 0.98, 0.99])
    labels = np.array([1, 1, 0, 0])

    res = analyze_degradation_grid_occupancy(labels, kmc, kmt)
    assert res["n_kmc_values"] == 2
    assert res["n_kmt_values"] == 2
    assert res["total_grid_cells"] == 4
    assert res["mean_speed_consistency"] == pytest.approx(1.0)


def test_final_model_manifest_integrity_and_serialization() -> None:
    """Verify that models/final/ contains valid serialized artifacts and complete manifest."""
    models_dir = get_models_dir() / "final"
    manifest_path = models_dir / "model_manifest.json"

    assert manifest_path.exists(), f"Manifest file missing at {manifest_path}"

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # Check manifest required fields
    assert "model_selection" in manifest
    assert "primary_model" in manifest["model_selection"]
    assert "secondary_model" in manifest["model_selection"]
    assert "representation" in manifest
    assert "data_provenance" in manifest
    assert "environment" in manifest

    primary_file = models_dir / manifest["model_selection"]["primary_model"]["artifact_file"]
    secondary_file = models_dir / manifest["model_selection"]["secondary_model"]["artifact_file"]
    transformer_file = models_dir / manifest["representation"]["transformer_artifact"]

    assert primary_file.exists(), f"Primary model artifact missing: {primary_file}"
    assert secondary_file.exists(), f"Secondary model artifact missing: {secondary_file}"
    assert transformer_file.exists(), f"Transformer artifact missing: {transformer_file}"


def test_model_reload_and_predictive_consistency() -> None:
    """Verify that final models reload seamlessly on Windows and generate valid cluster labels."""
    ok = reload_and_verify_final_model()
    assert ok is True


def test_kmc_kmt_anti_leakage_invariance() -> None:
    """Verify that kMc and kMt are never used in representation construction or model inputs."""
    container = load_naval_dataset()
    full_df = pd.concat([container.features, container.targets], axis=1)

    r5_spec = CANDIDATE_REPRESENTATIONS["R5_WITHIN_SPEED_NORMALIZED"]
    r5_df = build_representation_data(full_df, r5_spec)

    assert "kMc" not in r5_df.columns, "Data leakage: kMc found in R5 feature columns!"
    assert "kMt" not in r5_df.columns, "Data leakage: kMt found in R5 feature columns!"
    assert "lp" not in r5_df.columns, "Operating demand lp should be excluded from R5!"
    assert "v" not in r5_df.columns, "Regime variable v should be excluded from R5 output!"

    # Ensure 11 valid telemetry features are retained
    expected_features = {"GTT", "GTn", "GGn", "Ts", "T48", "T2", "P48", "P2", "Pexh", "TIC", "mf"}
    assert set(r5_df.columns) == expected_features
