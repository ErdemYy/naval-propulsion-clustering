"""Controlled clustering experiments engine for Phase 3.

Executes Experiment Groups A through L:
- Group A: Operating Regime Baseline (R1, k=2..12)
- Group B: Operating-Condition-Excluded Baseline (R2, k=2..12)
- Group C: Correlation-Reduced Representation (R3, k=2..12)
- Group D: Robust Scaling (R4, k=2..12)
- Group E: Primary Degradation Experiment (R5, k=2..12)
- Group F: Multi-seed Stability Analysis
- Group G: Hierarchical Clustering (Ward & Average linkage)
- Group H: DBSCAN parameter search
- Group I: Gaussian Mixture Models (BIC/AIC)
- Group J & K: Post-hoc Degradation Validation (kMc, kMt)
- Group L: Cluster Telemetry Profiles
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any
import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score

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
from naval_propulsion.visualization.phase3 import generate_all_phase3_figures


def run_representation_kmeans_sweep(
    X_df: pd.DataFrame,
    speeds: np.ndarray,
    rep_id: str,
    k_range: range = range(2, 13),
    random_state: int = 42,
) -> list[dict[str, Any]]:
    """Run K-Means sweep from k_min to k_max on a given representation."""
    X_arr = X_df.to_numpy()
    results = []

    for k in k_range:
        clusterer = KMeansClusterer(n_clusters=k, random_state=random_state)
        res = clusterer.fit_predict(X_arr)

        # Intrinsic metrics
        int_metrics = compute_intrinsic_metrics(X_arr, res.labels)

        # External recovery of speed regimes
        ext_metrics = evaluate_operating_regime_recovery(res.labels, speeds)

        results.append({
            "k": k,
            "inertia": res.additional_metadata.get("inertia", 0.0),
            "silhouette": int_metrics.silhouette_avg,
            "davies_bouldin": int_metrics.davies_bouldin,
            "calinski_harabasz": int_metrics.calinski_harabasz,
            "ari_vs_speed": ext_metrics["ari_vs_speed"],
            "nmi_vs_speed": ext_metrics["nmi_vs_speed"],
        })

    return results


def run_all_phase3_experiments() -> dict[str, Any]:
    """Execute complete Phase 3 experimental matrix."""
    base_output_dir = get_experiments_dir() / "outputs" / "phase3"
    base_output_dir.mkdir(parents=True, exist_ok=True)

    container = load_naval_dataset()
    full_df = pd.concat([container.features, container.targets], axis=1)
    speeds = full_df["v"].to_numpy()

    # Pre-build transformed representations
    built_representations: dict[str, pd.DataFrame] = {}
    for rep_id, spec in CANDIDATE_REPRESENTATIONS.items():
        built_representations[rep_id] = build_representation_data(full_df, spec)

    summary: dict[str, Any] = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "representation_sweeps": {},
        "stability_analysis": {},
        "algorithm_comparison": {},
        "degradation_validation": {},
        "cluster_profiles": {},
    }

    # ==========================================
    # EXPERIMENT GROUPS A, B, C, D, E: K-Means Sweeps
    # ==========================================
    for rep_id in [
        "R1_ALL_VALID_TELEMETRY",
        "R2_WITHOUT_OPERATING_DEMAND",
        "R3_REDUCED_CORRELATION",
        "R4_ROBUST_SCALED_TELEMETRY",
        "R5_WITHIN_SPEED_NORMALIZED",
    ]:
        sweep = run_representation_kmeans_sweep(
            built_representations[rep_id],
            speeds=speeds,
            rep_id=rep_id,
        )
        summary["representation_sweeps"][rep_id] = sweep

        # Save individual experiment record
        exp_dir = base_output_dir / rep_id
        exp_dir.mkdir(parents=True, exist_ok=True)
        with open(exp_dir / "sweep_metrics.json", "w", encoding="utf-8") as f:
            json.dump(sweep, f, indent=2)

    # Save fitted model and labels for R1 at k=9 (baseline speed recovery)
    r1_clusterer = KMeansClusterer(n_clusters=9, random_state=42)
    r1_res_k9 = r1_clusterer.fit_predict(built_representations["R1_ALL_VALID_TELEMETRY"].to_numpy())

    # ==========================================
    # EXPERIMENT GROUP E & J: Primary Degradation Analysis on R5
    # ==========================================
    # Evaluate R5 K-Means across k=2, 3, 4
    r5_df = built_representations["R5_WITHIN_SPEED_NORMALIZED"]
    r5_arr = r5_df.to_numpy()

    for k_cand in [2, 3, 4]:
        km_r5 = KMeansClusterer(n_clusters=k_cand, random_state=42)
        r5_res = km_r5.fit_predict(r5_arr)

        deg_report = analyze_posthoc_degradation(
            r5_res.labels,
            targets_df=container.targets,
        )
        summary["degradation_validation"][f"R5_KMeans_k{k_cand}"] = deg_report

        # Save individual record
        cand_dir = base_output_dir / f"R5_KMeans_k{k_cand}"
        cand_dir.mkdir(parents=True, exist_ok=True)
        with open(cand_dir / "degradation_validation.json", "w", encoding="utf-8") as f:
            json.dump(deg_report, f, indent=2)

    # Best R5 model for visual profiling (e.g. k=2 or k=3)
    best_k = 2  # k=2 achieves highest silhouette in R5
    best_r5_clusterer = KMeansClusterer(n_clusters=best_k, random_state=42)
    best_r5_res = best_r5_clusterer.fit_predict(r5_arr)

    # ==========================================
    # EXPERIMENT GROUP F: Multi-Seed Stability
    # ==========================================
    summary["stability_analysis"]["R1_k9_SpeedRegimes"] = evaluate_cluster_stability(
        built_representations["R1_ALL_VALID_TELEMETRY"].to_numpy(),
        n_clusters=9,
    )
    summary["stability_analysis"]["R5_k2_Degradation"] = evaluate_cluster_stability(
        r5_arr,
        n_clusters=2,
    )
    summary["stability_analysis"]["R5_k3_Degradation"] = evaluate_cluster_stability(
        r5_arr,
        n_clusters=3,
    )

    # ==========================================
    # EXPERIMENT GROUP G: Hierarchical Clustering on R5
    # ==========================================
    # Ward Linkage
    agg_ward = AgglomerativeClustererWrapper(n_clusters=2, linkage="ward")
    agg_ward_res = agg_ward.fit_predict(r5_arr)
    ward_metrics = compute_intrinsic_metrics(r5_arr, agg_ward_res.labels)

    # Average Linkage
    agg_avg = AgglomerativeClustererWrapper(n_clusters=2, linkage="average")
    agg_avg_res = agg_avg.fit_predict(r5_arr)
    avg_metrics = compute_intrinsic_metrics(r5_arr, agg_avg_res.labels)

    # ==========================================
    # EXPERIMENT GROUP H: DBSCAN Parameter Search on R5
    # ==========================================
    # In standardized R5 space (11 dimensions), test eps from 0.8 to 2.2
    dbscan_sweep = []
    for eps in [0.8, 1.2, 1.6, 2.0, 2.4]:
        for min_samples in [10, 25, 50]:
            db_wrapper = DBSCANClustererWrapper(eps=eps, min_samples=min_samples)
            db_res = db_wrapper.fit_predict(r5_arr)
            sil = float(silhouette_score(r5_arr, db_res.labels)) if db_res.n_clusters >= 2 else 0.0
            dbscan_sweep.append({
                "eps": eps,
                "min_samples": min_samples,
                "n_clusters": db_res.n_clusters,
                "noise_ratio": db_res.additional_metadata.get("noise_ratio", 0.0),
                "silhouette": sil,
            })

    # Pick representative DBSCAN
    db_best = DBSCANClustererWrapper(eps=1.6, min_samples=25)
    db_best_res = db_best.fit_predict(r5_arr)

    # ==========================================
    # EXPERIMENT GROUP I: Gaussian Mixture Model on R5
    # ==========================================
    gmm_wrapper = GMMClustererWrapper(n_components=2, random_state=42)
    gmm_res = gmm_wrapper.fit_predict(r5_arr)
    gmm_metrics = compute_intrinsic_metrics(r5_arr, gmm_res.labels)

    summary["algorithm_comparison"] = {
        "KMeans_k2": {
            "silhouette": float(summary["representation_sweeps"]["R5_WITHIN_SPEED_NORMALIZED"][0]["silhouette"]),
            "davies_bouldin": float(summary["representation_sweeps"]["R5_WITHIN_SPEED_NORMALIZED"][0]["davies_bouldin"]),
            "calinski_harabasz": float(summary["representation_sweeps"]["R5_WITHIN_SPEED_NORMALIZED"][0]["calinski_harabasz"]),
        },
        "Agglomerative_Ward_k2": {
            "silhouette": ward_metrics.silhouette_avg,
            "davies_bouldin": ward_metrics.davies_bouldin,
            "calinski_harabasz": ward_metrics.calinski_harabasz,
        },
        "Agglomerative_Average_k2": {
            "silhouette": avg_metrics.silhouette_avg,
            "davies_bouldin": avg_metrics.davies_bouldin,
            "calinski_harabasz": avg_metrics.calinski_harabasz,
        },
        "GMM_k2": {
            "silhouette": gmm_metrics.silhouette_avg,
            "davies_bouldin": gmm_metrics.davies_bouldin,
            "calinski_harabasz": gmm_metrics.calinski_harabasz,
            "bic": gmm_res.additional_metadata.get("bic"),
            "aic": gmm_res.additional_metadata.get("aic"),
        },
    }

    # ==========================================
    # EXPERIMENT GROUP L: Cluster Profiles on R5
    # ==========================================
    profile_df = r5_df.copy()
    profile_df["Cluster"] = best_r5_res.labels
    cluster_means = profile_df.groupby("Cluster").mean().to_dict(orient="index")
    cluster_stds = profile_df.groupby("Cluster").std().to_dict(orient="index")
    summary["cluster_profiles"]["R5_k2"] = {
        "means": cluster_means,
        "stds": cluster_stds,
    }

    # ==========================================
    # GENERATE PUBLICATION FIGURES
    # ==========================================
    fig_paths = generate_all_phase3_figures(
        experiment_results=summary,
        r1_df=built_representations["R1_ALL_VALID_TELEMETRY"],
        r1_labels_k9=r1_res_k9.labels,
        r5_df=r5_df,
        r5_labels_best=best_r5_res.labels,
        targets_df=container.targets,
        speeds=speeds,
    )

    summary["figures_generated"] = {k: str(v.name) for k, v in fig_paths.items()}

    # Save summary report
    summary_path = base_output_dir / "phase3_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return summary


if __name__ == "__main__":
    res = run_all_phase3_experiments()
    print("Phase 3 experiments completed successfully!")
