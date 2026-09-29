"""Metrics evaluation and post-hoc statistical validation contracts."""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score, silhouette_score


@dataclass(frozen=True)
class IntrinsicMetrics:
    """Internal cluster validation metrics (no ground truth required).

    Attributes
    ----------
    silhouette_avg : float
        Mean silhouette coefficient across all points (-1 to 1).
    davies_bouldin : float
        Davies-Bouldin index (lower is better, >= 0).
    calinski_harabasz : float
        Calinski-Harabasz score / Variance ratio criterion (higher is better).
    """

    silhouette_avg: float
    davies_bouldin: float
    calinski_harabasz: float


@dataclass(frozen=True)
class DegradationCorrelationReport:
    """Post-hoc statistical relationship report between clusters and decay states.

    Strictly used after unsupervised clustering to evaluate physical relevance.
    """

    test_method: str
    kmc_statistic: float
    kmc_p_value: float
    kmt_statistic: float
    kmt_p_value: float
    is_kmc_significant: bool
    is_kmt_significant: bool


def compute_intrinsic_metrics(
    X: np.ndarray,
    labels: np.ndarray,
    sample_size_for_silhouette: int | None = None,
    random_state: int = 42,
) -> IntrinsicMetrics:
    """Compute standard internal validation metrics on clustered feature matrix.

    Handles noise labels (-1) by filtering them out for metric calculation.

    Parameters
    ----------
    X : np.ndarray
        Clustered feature matrix.
    labels : np.ndarray
        Cluster labels assigned to points.
    sample_size_for_silhouette : int | None, optional
        Subsample size for silhouette if dataset is very large.
    random_state : int, default=42
        Seed for silhouette subsampling.

    Returns
    -------
    IntrinsicMetrics
        Calculated geometric validation metrics.
    """
    valid_mask = labels >= 0
    unique_labels = np.unique(labels[valid_mask])

    if len(unique_labels) < 2:
        raise ValueError("At least 2 clusters are required to compute validation metrics.")

    X_valid = X[valid_mask]
    labels_valid = labels[valid_mask]

    sil = float(
        silhouette_score(
            X_valid,
            labels_valid,
            sample_size=sample_size_for_silhouette,
            random_state=random_state,
        )
    )
    db = float(davies_bouldin_score(X_valid, labels_valid))
    ch = float(calinski_harabasz_score(X_valid, labels_valid))

    return IntrinsicMetrics(
        silhouette_avg=sil,
        davies_bouldin=db,
        calinski_harabasz=ch,
    )
