"""Multi-seed cluster stability evaluation.

Assesses cluster solution determinism and convergence consistency across
different random initialization seeds via pairwise Adjusted Rand Index (ARI).
"""

from __future__ import annotations

from typing import Any, Sequence
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_mutual_info_score, adjusted_rand_score


DEFAULT_STABILITY_SEEDS: tuple[int, ...] = (0, 1, 2, 3, 4, 5, 10, 21, 42, 100)


def evaluate_cluster_stability(
    X: np.ndarray,
    n_clusters: int,
    seeds: Sequence[int] = DEFAULT_STABILITY_SEEDS,
    n_init: int = 10,
) -> dict[str, Any]:
    """Run K-Means across multiple random seeds and compute pairwise stability metrics.

    Parameters
    ----------
    X : np.ndarray
        Transformed feature matrix.
    n_clusters : int
        Number of clusters to evaluate.
    seeds : Sequence[int], default=(0, 1, 2, 3, 4, 5, 10, 21, 42, 100)
        Random seeds to test.
    n_init : int, default=10
        Number of centroid initializations per K-Means fit.

    Returns
    -------
    dict[str, Any]
        Stability statistics including mean, median, std, min, and max pairwise ARI/AMI.
    """
    labels_by_seed: dict[int, np.ndarray] = {}

    for seed in seeds:
        km = KMeans(n_clusters=n_clusters, random_state=seed, n_init=n_init)
        labels_by_seed[seed] = km.fit_predict(X)

    seed_list = list(seeds)
    pairwise_ari: list[float] = []
    pairwise_ami: list[float] = []

    for i in range(len(seed_list)):
        for j in range(i + 1, len(seed_list)):
            s1, s2 = seed_list[i], seed_list[j]
            ari = float(adjusted_rand_score(labels_by_seed[s1], labels_by_seed[s2]))
            ami = float(adjusted_mutual_info_score(labels_by_seed[s1], labels_by_seed[s2]))
            pairwise_ari.append(ari)
            pairwise_ami.append(ami)

    return {
        "n_clusters": n_clusters,
        "n_seeds_tested": len(seeds),
        "n_pairwise_comparisons": len(pairwise_ari),
        "ari_mean": float(np.mean(pairwise_ari)),
        "ari_median": float(np.median(pairwise_ari)),
        "ari_std": float(np.std(pairwise_ari, ddof=1)) if len(pairwise_ari) > 1 else 0.0,
        "ari_min": float(np.min(pairwise_ari)),
        "ari_max": float(np.max(pairwise_ari)),
        "ami_mean": float(np.mean(pairwise_ami)),
        "ami_median": float(np.median(pairwise_ami)),
        "stability_rating": (
            "Highly Stable" if np.mean(pairwise_ari) >= 0.95 else
            ("Moderately Stable" if np.mean(pairwise_ari) >= 0.80 else "Unstable / Seed Dependent")
        ),
    }
