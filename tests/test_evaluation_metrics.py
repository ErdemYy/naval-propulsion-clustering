"""Unit tests for intrinsic clustering metrics."""

from __future__ import annotations

import numpy as np
import pytest
from naval_propulsion.evaluation.metrics import (
    IntrinsicMetrics,
    compute_intrinsic_metrics,
)


def test_compute_intrinsic_metrics() -> None:
    """Test calculation of silhouette, Davies-Bouldin, and Calinski-Harabasz."""
    # Synthetic 2-cluster data
    rng = np.random.default_rng(42)
    c1 = rng.normal(loc=-5.0, scale=0.5, size=(30, 2))
    c2 = rng.normal(loc=5.0, scale=0.5, size=(30, 2))
    X = np.vstack([c1, c2])
    labels = np.array([0] * 30 + [1] * 30)

    metrics = compute_intrinsic_metrics(X, labels)
    assert isinstance(metrics, IntrinsicMetrics)
    assert metrics.silhouette_avg > 0.8  # Well separated clusters
    assert metrics.davies_bouldin < 0.5   # Small within-cluster scatter relative to separation
    assert metrics.calinski_harabasz > 100.0


def test_compute_intrinsic_metrics_rejects_single_cluster() -> None:
    """Verify that an error is raised when fewer than 2 clusters exist."""
    X = np.ones((20, 2))
    labels = np.zeros(20, dtype=int)

    with pytest.raises(ValueError, match="At least 2 clusters"):
        compute_intrinsic_metrics(X, labels)
