"""External validation and post-hoc degradation analysis.

Provides external alignment metrics (ARI, NMI against operating speed)
and zero-leakage post-hoc degradation association tests (ANOVA, Kruskal-Wallis,
eta-squared, bootstrap confidence intervals for kMc and kMt).
"""

from __future__ import annotations

from typing import Any, Sequence
import numpy as np
import pandas as pd
from scipy.stats import f_oneway, kruskal
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score


def evaluate_operating_regime_recovery(
    labels: np.ndarray,
    ground_truth_speed: Sequence[float] | np.ndarray,
) -> dict[str, float]:
    """Quantify how strongly cluster assignments align with discrete ship speed setpoints.

    Parameters
    ----------
    labels : np.ndarray
        Cluster labels from unsupervised clustering.
    ground_truth_speed : Sequence[float] or np.ndarray
        Known discrete ship speed setpoints (used solely as external evaluation benchmark).

    Returns
    -------
    dict[str, float]
        Dictionary with ARI and NMI scores.
    """
    speed_arr = np.asarray(ground_truth_speed)
    valid_mask = labels >= 0  # Filter noise if DBSCAN

    if not valid_mask.any():
        return {"ari_vs_speed": 0.0, "nmi_vs_speed": 0.0}

    ari = float(adjusted_rand_score(speed_arr[valid_mask], labels[valid_mask]))
    nmi = float(normalized_mutual_info_score(speed_arr[valid_mask], labels[valid_mask]))
    return {"ari_vs_speed": ari, "nmi_vs_speed": nmi}


def compute_bootstrap_ci(
    values: np.ndarray,
    n_bootstraps: int = 500,
    ci_level: float = 0.95,
    random_state: int = 42,
) -> tuple[float, float]:
    """Compute bootstrap percentile confidence interval for the sample mean."""
    if len(values) < 2:
        val = float(values[0]) if len(values) == 1 else 0.0
        return (val, val)

    rng = np.random.default_rng(random_state)
    boot_means = np.empty(n_bootstraps, dtype=np.float64)
    n = len(values)

    for i in range(n_bootstraps):
        resample = rng.choice(values, size=n, replace=True)
        boot_means[i] = np.mean(resample)

    alpha = (1.0 - ci_level) / 2.0
    lower = float(np.percentile(boot_means, 100.0 * alpha))
    upper = float(np.percentile(boot_means, 100.0 * (1.0 - alpha)))
    return (lower, upper)


def analyze_posthoc_degradation(
    labels: np.ndarray,
    targets_df: pd.DataFrame,
    target_names: tuple[str, ...] = ("kMc", "kMt"),
) -> dict[str, Any]:
    """Perform post-hoc statistical degradation profiling strictly after clustering.

    Parameters
    ----------
    labels : np.ndarray
        Cluster assignments (1D array, length N).
    targets_df : pd.DataFrame
        Ground-truth degradation targets DataFrame (N rows).
    target_names : tuple[str, ...], default=("kMc", "kMt")
        Target column names to analyze.

    Returns
    -------
    dict[str, Any]
        Statistical report containing ANOVA, Kruskal-Wallis, eta-squared,
        and per-cluster summary statistics and bootstrap CIs.
    """
    valid_mask = labels >= 0
    unique_clusters = sorted([int(c) for c in np.unique(labels[valid_mask])])

    if len(unique_clusters) < 2:
        return {
            "status": "insufficient_clusters",
            "message": "Fewer than 2 valid clusters to compute statistical significance.",
        }

    results: dict[str, Any] = {"cluster_counts": {}}
    for c in unique_clusters:
        results["cluster_counts"][str(c)] = int(np.sum(labels == c))

    for target in target_names:
        y = targets_df[target].to_numpy()
        cluster_groups = [y[(labels == c) & valid_mask] for c in unique_clusters]

        # One-way ANOVA
        try:
            f_stat, anova_p = f_oneway(*cluster_groups)
            f_stat = float(f_stat)
            anova_p = float(anova_p)
        except Exception:
            f_stat, anova_p = 0.0, 1.0

        # Kruskal-Wallis H-test
        try:
            h_stat, kw_p = kruskal(*cluster_groups)
            h_stat = float(h_stat)
            kw_p = float(kw_p)
        except Exception:
            h_stat, kw_p = 0.0, 1.0

        # Eta-squared calculation (ANOVA based)
        grand_mean = np.mean(y[valid_mask])
        ss_total = float(np.sum((y[valid_mask] - grand_mean) ** 2))
        ss_between = float(sum(len(g) * (np.mean(g) - grand_mean) ** 2 for g in cluster_groups))
        eta_squared = float(ss_between / ss_total) if ss_total > 0 else 0.0

        # Per-cluster stats
        cluster_profiles: dict[str, dict[str, Any]] = {}
        for c in unique_clusters:
            g = y[labels == c]
            ci_low, ci_high = compute_bootstrap_ci(g)
            cluster_profiles[str(c)] = {
                "count": len(g),
                "mean": float(np.mean(g)),
                "std": float(np.std(g, ddof=1)) if len(g) > 1 else 0.0,
                "median": float(np.median(g)),
                "q25": float(np.percentile(g, 25)),
                "q75": float(np.percentile(g, 75)),
                "min": float(np.min(g)),
                "max": float(np.max(g)),
                "ci_95_lower": ci_low,
                "ci_95_upper": ci_high,
            }

        results[target] = {
            "anova_f_statistic": f_stat,
            "anova_p_value": anova_p,
            "kruskal_h_statistic": h_stat,
            "kruskal_p_value": kw_p,
            "eta_squared": eta_squared,
            "effect_size_interpretation": (
                "Large effect" if eta_squared >= 0.14 else
                ("Moderate effect" if eta_squared >= 0.06 else "Small/negligible effect")
            ),
            "clusters": cluster_profiles,
        }

    return results
