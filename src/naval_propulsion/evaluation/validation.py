"""Phase 4 Scientific Validation and Statistical Testing.

Implements pairwise degradation validation (Mann-Whitney U, Cliff's delta,
Benjamini-Hochberg FDR correction), bootstrap cluster stability validation,
operating-speed invariance profiling, degradation grid mapping, and
robust telemetry profiling.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Sequence
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, false_discovery_control, mannwhitneyu
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score


@dataclass(frozen=True)
class PairwiseComparisonResult:
    cluster_i: int
    cluster_j: int
    target_name: str
    n_i: int
    n_j: int
    median_i: float
    median_j: float
    mean_i: float
    mean_j: float
    mwu_statistic: float
    raw_p_value: float
    adjusted_p_value: float
    cliffs_delta: float
    rank_biserial: float
    effect_size_interpretation: str
    ci_lower: float
    ci_upper: float


def compute_cliffs_delta(x1: np.ndarray, x2: np.ndarray) -> float:
    """Compute Cliff's delta effect size between two independent groups.

    Formula:
        d = (2 * U / (n1 * n2)) - 1
    where U is the Mann-Whitney statistic counting pairs where x1 > x2.
    """
    n1, n2 = len(x1), len(x2)
    if n1 == 0 or n2 == 0:
        return 0.0
    res = mannwhitneyu(x1, x2, alternative="two-sided")
    # In scipy, mannwhitneyu returns U1 (number of times x1 > x2 + 0.5 * ties)
    d = (2.0 * float(res.statistic) / (n1 * n2)) - 1.0
    return float(np.clip(d, -1.0, 1.0))


def interpret_cliffs_delta(delta: float) -> str:
    """Interpret Cliff's delta magnitude according to Romano et al. (2006)."""
    abs_d = abs(delta)
    if abs_d < 0.147:
        return "Negligible"
    elif abs_d < 0.33:
        return "Small"
    elif abs_d < 0.474:
        return "Medium"
    else:
        return "Large"


def compute_median_diff_bootstrap_ci(
    x1: np.ndarray,
    x2: np.ndarray,
    n_bootstraps: int = 500,
    ci_level: float = 0.95,
    random_state: int = 42,
) -> tuple[float, float]:
    """Compute bootstrap percentile confidence interval for difference in medians (median_i - median_j)."""
    if len(x1) < 2 or len(x2) < 2:
        diff = float(np.median(x1) - np.median(x2)) if len(x1) and len(x2) else 0.0
        return (diff, diff)

    rng = np.random.default_rng(random_state)
    boot_diffs = np.empty(n_bootstraps, dtype=np.float64)
    n1, n2 = len(x1), len(x2)

    for b in range(n_bootstraps):
        b1 = rng.choice(x1, size=n1, replace=True)
        b2 = rng.choice(x2, size=n2, replace=True)
        boot_diffs[b] = np.median(b1) - np.median(b2)

    alpha = (1.0 - ci_level) / 2.0
    lower = float(np.percentile(boot_diffs, 100.0 * alpha))
    upper = float(np.percentile(boot_diffs, 100.0 * (1.0 - alpha)))
    return (lower, upper)


def run_pairwise_degradation_tests(
    labels: np.ndarray,
    target_series: pd.Series | np.ndarray,
    target_name: str,
    random_state: int = 42,
) -> list[PairwiseComparisonResult]:
    """Run all pairwise Mann-Whitney U tests for a given degradation target with FDR correction.

    Guarantees strict zero-leakage by operating post-hoc on fitted cluster labels.
    """
    y = np.asarray(target_series)
    unique_clusters = sorted([int(c) for c in np.unique(labels) if c >= 0])
    k = len(unique_clusters)

    if k < 2:
        return []

    comparisons_raw = []
    p_values = []

    for i_idx in range(k):
        for j_idx in range(i_idx + 1, k):
            c_i = unique_clusters[i_idx]
            c_j = unique_clusters[j_idx]
            x_i = y[labels == c_i]
            x_j = y[labels == c_j]

            res = mannwhitneyu(x_i, x_j, alternative="two-sided")
            d = compute_cliffs_delta(x_i, x_j)
            ci_low, ci_high = compute_median_diff_bootstrap_ci(
                x_i, x_j, random_state=random_state + (c_i * 10 + c_j)
            )

            p_val = float(res.pvalue)
            p_values.append(p_val)
            comparisons_raw.append({
                "cluster_i": c_i,
                "cluster_j": c_j,
                "target_name": target_name,
                "n_i": len(x_i),
                "n_j": len(x_j),
                "median_i": float(np.median(x_i)),
                "median_j": float(np.median(x_j)),
                "mean_i": float(np.mean(x_i)),
                "mean_j": float(np.mean(x_j)),
                "mwu_statistic": float(res.statistic),
                "raw_p_value": p_val,
                "cliffs_delta": d,
                "rank_biserial": -d,
                "effect_size_interpretation": interpret_cliffs_delta(d),
                "ci_lower": ci_low,
                "ci_upper": ci_high,
            })

    # Benjamini-Hochberg FDR correction
    if len(p_values) > 1:
        try:
            adj_p_values = false_discovery_control(p_values, method="bh")
        except Exception:
            # Fallback manual BH procedure
            m = len(p_values)
            sorted_idx = np.argsort(p_values)
            sorted_p = np.array(p_values)[sorted_idx]
            adj = np.empty(m, dtype=np.float64)
            cummin = 1.0
            for rank_down in range(m, 0, -1):
                p_adj = min(1.0, (m / rank_down) * sorted_p[rank_down - 1])
                cummin = min(cummin, p_adj)
                adj[rank_down - 1] = cummin
            adj_p_values = np.empty(m, dtype=np.float64)
            adj_p_values[sorted_idx] = adj
    else:
        adj_p_values = np.array(p_values, dtype=np.float64)

    results: list[PairwiseComparisonResult] = []
    for comp, adj_p in zip(comparisons_raw, adj_p_values):
        comp["adjusted_p_value"] = float(adj_p)
        results.append(PairwiseComparisonResult(**comp))

    return results


def run_bootstrap_cluster_validation(
    X: np.ndarray,
    n_clusters: int,
    n_bootstraps: int = 100,
    random_state: int = 42,
    n_init: int = 5,
) -> dict[str, Any]:
    """Run bootstrap resampling validation on clustering stability.

    For each bootstrap repetition:
    1. Sample N observations with replacement.
    2. Fit K-Means on bootstrap sample.
    3. Predict labels across the entire reference dataset.
    4. Compute Adjusted Rand Index (ARI) against the reference solution.

    Reports:
    - Mean ARI, Median ARI, Std, 2.5th and 97.5th percentiles.
    """
    n_samples = len(X)
    ref_km = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    ref_labels = ref_km.fit_predict(X)

    rng = np.random.default_rng(random_state)
    ari_scores = np.empty(n_bootstraps, dtype=np.float64)

    for b in range(n_bootstraps):
        boot_idx = rng.choice(n_samples, size=n_samples, replace=True)
        X_boot = X[boot_idx]

        boot_km = KMeans(n_clusters=n_clusters, random_state=random_state + b, n_init=n_init)
        boot_km.fit(X_boot)

        # Predict reference dataset to evaluate partition preservation
        pred_full = boot_km.predict(X)
        ari = adjusted_rand_score(ref_labels, pred_full)
        ari_scores[b] = float(ari)

    return {
        "n_clusters": n_clusters,
        "n_bootstraps": n_bootstraps,
        "mean_ari": float(np.mean(ari_scores)),
        "median_ari": float(np.median(ari_scores)),
        "std_ari": float(np.std(ari_scores, ddof=1)),
        "ci_2_5_percentile": float(np.percentile(ari_scores, 2.5)),
        "ci_97_5_percentile": float(np.percentile(ari_scores, 97.5)),
        "min_ari": float(np.min(ari_scores)),
        "max_ari": float(np.max(ari_scores)),
        "bootstrap_ari_samples": [float(x) for x in ari_scores],
    }


def analyze_operating_speed_invariance(
    labels: np.ndarray,
    speed_series: pd.Series | np.ndarray,
) -> dict[str, Any]:
    """Calculate cluster proportions across discrete operating speed regimes.

    Evaluates whether discovered clusters are invariant to commanded speed or
    systematically skewed across ship speed setpoints.
    """
    speeds = np.asarray(speed_series)
    unique_speeds = sorted([float(s) for s in np.unique(speeds)])
    unique_clusters = sorted([int(c) for c in np.unique(labels) if c >= 0])

    records = []
    contingency_matrix = []

    for spd in unique_speeds:
        mask = speeds == spd
        spd_labels = labels[mask]
        total_in_speed = len(spd_labels)

        row_counts = []
        rec: dict[str, Any] = {"speed": spd, "total": total_in_speed}

        for c in unique_clusters:
            cnt = int(np.sum(spd_labels == c))
            prop = float(cnt / total_in_speed) if total_in_speed > 0 else 0.0
            rec[f"cluster_{c}_count"] = cnt
            rec[f"cluster_{c}_proportion"] = prop
            row_counts.append(cnt)

        records.append(rec)
        contingency_matrix.append(row_counts)

    # Contingency test for independence
    try:
        chi2, p_val, dof, _ = chi2_contingency(contingency_matrix)
        n_total = len(labels)
        min_dim = min(len(unique_speeds) - 1, len(unique_clusters) - 1)
        cramers_v = float(np.sqrt(chi2 / (n_total * min_dim))) if (min_dim > 0 and n_total > 0) else 0.0
    except Exception:
        chi2, p_val, dof, cramers_v = 0.0, 1.0, 0, 0.0

    # Summary statistics of proportions across speeds
    df_props = pd.DataFrame(records)
    prop_stats: dict[str, dict[str, float]] = {}
    for c in unique_clusters:
        p_col = f"cluster_{c}_proportion"
        prop_stats[str(c)] = {
            "mean": float(df_props[p_col].mean()),
            "std": float(df_props[p_col].std(ddof=1)),
            "min": float(df_props[p_col].min()),
            "max": float(df_props[p_col].max()),
            "range": float(df_props[p_col].max() - df_props[p_col].min()),
        }

    return {
        "speed_records": records,
        "contingency_chi2": float(chi2),
        "contingency_p_value": float(p_val),
        "contingency_dof": int(dof),
        "cramers_v": float(cramers_v),
        "proportion_stats": prop_stats,
    }


def analyze_degradation_grid_occupancy(
    labels: np.ndarray,
    kmc_series: pd.Series | np.ndarray,
    kmt_series: pd.Series | np.ndarray,
) -> dict[str, Any]:
    """Analyze cluster assignments across the 2D factorial degradation grid (kMc x kMt).

    Determines whether clusters represent spatially contiguous regions of degradation
    space and quantifies assignment consistency across the 9 speed setpoints for every cell.
    """
    df_grid = pd.DataFrame({
        "kMc": np.asarray(kmc_series),
        "kMt": np.asarray(kmt_series),
        "cluster": labels,
    })

    unique_kmc = sorted([float(x) for x in df_grid["kMc"].unique()])
    unique_kmt = sorted([float(x) for x in df_grid["kMt"].unique()])

    grid_cells = []
    consistency_scores = []

    for kmc in unique_kmc:
        for kmt in unique_kmt:
            sub = df_grid[(df_grid["kMc"] == kmc) & (df_grid["kMt"] == kmt)]["cluster"]
            if len(sub) == 0:
                continue
            counts = sub.value_counts()
            majority_cluster = int(counts.index[0])
            consistency = float(counts.iloc[0] / len(sub))  # Max proportion out of 9
            consistency_scores.append(consistency)

            cell_record = {
                "kMc": kmc,
                "kMt": kmt,
                "majority_cluster": majority_cluster,
                "consistency": consistency,
                "counts": {int(k): int(v) for k, v in counts.items()},
            }
            grid_cells.append(cell_record)

    return {
        "n_kmc_values": len(unique_kmc),
        "n_kmt_values": len(unique_kmt),
        "total_grid_cells": len(grid_cells),
        "mean_speed_consistency": float(np.mean(consistency_scores)),
        "min_speed_consistency": float(np.min(consistency_scores)),
        "median_speed_consistency": float(np.median(consistency_scores)),
        "grid_cells": grid_cells,
    }


def compute_standardized_cluster_profiles(
    X_df: pd.DataFrame,
    labels: np.ndarray,
    n_bootstraps: int = 500,
    random_state: int = 42,
) -> dict[str, Any]:
    """Calculate standardized cluster profiles with bootstrap 95% CIs for telemetry means."""
    unique_clusters = sorted([int(c) for c in np.unique(labels) if c >= 0])
    rng = np.random.default_rng(random_state)
    profiles: dict[str, dict[str, Any]] = {}

    for c in unique_clusters:
        sub_df = X_df[labels == c]
        n_c = len(sub_df)
        feat_dict: dict[str, Any] = {}

        for col in X_df.columns:
            vals = sub_df[col].to_numpy()
            mean_val = float(np.mean(vals))
            std_val = float(np.std(vals, ddof=1)) if n_c > 1 else 0.0

            # Bootstrap CI for mean
            boot_means = np.empty(n_bootstraps, dtype=np.float64)
            for b in range(n_bootstraps):
                resample = rng.choice(vals, size=n_c, replace=True)
                boot_means[b] = np.mean(resample)

            ci_low = float(np.percentile(boot_means, 2.5))
            ci_high = float(np.percentile(boot_means, 97.5))

            feat_dict[col] = {
                "mean": mean_val,
                "std": std_val,
                "ci_95_lower": ci_low,
                "ci_95_upper": ci_high,
                "direction": "positive" if ci_low > 0 else ("negative" if ci_high < 0 else "neutral"),
            }

        profiles[str(c)] = feat_dict

    return profiles
