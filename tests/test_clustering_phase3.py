"""Unit tests for Phase 3 clustering models, stability, metrics, and post-hoc validation."""

from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from naval_propulsion.clustering.models import (
    AgglomerativeClustererWrapper,
    DBSCANClustererWrapper,
    GMMClustererWrapper,
    KMeansClusterer,
)
from naval_propulsion.data.loader import load_naval_dataset
from naval_propulsion.evaluation.external import (
    analyze_posthoc_degradation,
    evaluate_operating_regime_recovery,
)
from naval_propulsion.evaluation.metrics import compute_intrinsic_metrics
from naval_propulsion.evaluation.stability import evaluate_cluster_stability
from naval_propulsion.features.registry import (
    CANDIDATE_REPRESENTATIONS,
    build_representation_data,
)
from naval_propulsion.utils.paths import get_experiments_dir


def test_no_kmc_kmt_leakage_in_models() -> None:
    """1: Verify that kMc and kMt never enter clustering inputs."""
    container = load_naval_dataset()
    full_df = pd.concat([container.features, container.targets], axis=1)

    for rep_id, spec in CANDIDATE_REPRESENTATIONS.items():
        transformed = build_representation_data(full_df, spec)
        assert "kMc" not in transformed.columns
        assert "kMt" not in transformed.columns


def test_deterministic_kmeans() -> None:
    """2: Verify K-Means produces bitwise identical cluster assignments with fixed seed."""
    rng = np.random.default_rng(42)
    X = rng.normal(size=(100, 5))

    km1 = KMeansClusterer(n_clusters=3, random_state=42)
    km2 = KMeansClusterer(n_clusters=3, random_state=42)

    res1 = km1.fit_predict(X)
    res2 = km2.fit_predict(X)

    np.testing.assert_array_equal(res1.labels, res2.labels)
    assert res1.additional_metadata["inertia"] == pytest.approx(res2.additional_metadata["inertia"])


def test_deterministic_preprocessing() -> None:
    """3: Verify candidate representation transformations are strictly deterministic."""
    container = load_naval_dataset()
    full_df = pd.concat([container.features, container.targets], axis=1)

    spec = CANDIDATE_REPRESENTATIONS["R5_WITHIN_SPEED_NORMALIZED"]
    df1 = build_representation_data(full_df, spec)
    df2 = build_representation_data(full_df, spec)

    pd.testing.assert_frame_equal(df1, df2)


def test_stable_experiment_metadata() -> None:
    """4 & 9: Verify Phase 3 experiment outputs and summary exist and have valid structure."""
    phase3_dir = get_experiments_dir() / "outputs" / "phase3"
    summary_file = phase3_dir / "phase3_summary.json"

    assert summary_file.exists(), "phase3_summary.json must exist"
    with open(summary_file, "r", encoding="utf-8") as f:
        summary = json.load(f)

    assert "representation_sweeps" in summary
    assert "stability_analysis" in summary
    assert "degradation_validation" in summary


def test_ari_nmi_calculations() -> None:
    """5: Verify ARI and NMI calculations against known ground truth."""
    labels = np.array([0, 0, 1, 1, 2, 2])
    speeds = np.array([3.0, 3.0, 6.0, 6.0, 9.0, 9.0])

    metrics = evaluate_operating_regime_recovery(labels, speeds)
    assert metrics["ari_vs_speed"] == pytest.approx(1.0)
    assert metrics["nmi_vs_speed"] == pytest.approx(1.0)


def test_cluster_metric_calculations() -> None:
    """6: Verify intrinsic metric computation on known separated clusters."""
    rng = np.random.default_rng(42)
    c1 = rng.normal(loc=0.0, scale=0.1, size=(20, 3))
    c2 = rng.normal(loc=10.0, scale=0.1, size=(20, 3))
    X = np.vstack([c1, c2])
    labels = np.array([0] * 20 + [1] * 20)

    m = compute_intrinsic_metrics(X, labels)
    assert m.silhouette_avg > 0.8
    assert m.davies_bouldin < 0.2
    assert m.calinski_harabasz > 50.0


def test_posthoc_degradation_analysis() -> None:
    """7: Verify post-hoc degradation ANOVA and Kruskal-Wallis calculation."""
    labels = np.array([0] * 50 + [1] * 50)
    rng = np.random.default_rng(42)
    kmc = np.concatenate([rng.uniform(0.95, 0.97, 50), rng.uniform(0.98, 1.00, 50)])
    kmt = rng.uniform(0.975, 1.00, 100)
    targets_df = pd.DataFrame({"kMc": kmc, "kMt": kmt})

    rep = analyze_posthoc_degradation(labels, targets_df)
    assert "kMc" in rep
    assert "kMt" in rep
    assert rep["kMc"]["eta_squared"] > 0.5  # Strongly separated kMc
    assert rep["kMc"]["kruskal_p_value"] < 1e-5


def test_dbscan_single_cluster_or_noise_handling() -> None:
    """8: Verify DBSCAN wrapper handles cases where only noise or 1 cluster is produced."""
    X = np.array([[1.0, 1.0], [10.0, 10.0]])
    db = DBSCANClustererWrapper(eps=0.1, min_samples=5)
    res = db.fit_predict(X)

    assert res.n_clusters == 0  # Both classified as noise
    assert res.additional_metadata["noise_count"] == 2
    assert res.additional_metadata["noise_ratio"] == 1.0


def test_consistent_feature_matrices() -> None:
    """10: Verify sample counts remain identical (11,934) across all representations."""
    container = load_naval_dataset()
    full_df = pd.concat([container.features, container.targets], axis=1)

    for rep_id, spec in CANDIDATE_REPRESENTATIONS.items():
        transformed = build_representation_data(full_df, spec)
        assert len(transformed) == 11934
        assert not transformed.isna().any().any()
