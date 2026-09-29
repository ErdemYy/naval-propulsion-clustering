"""Phase 3 publication figures generation.

Generates 10 publication-quality diagnostic plots for clustering validation,
operating regime recovery, degradation post-hoc profiling, and algorithm comparisons.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA

from naval_propulsion.utils.paths import get_figures_dir
from naval_propulsion.visualization.plots import configure_plot_style


def generate_all_phase3_figures(
    experiment_results: dict[str, Any],
    r1_df: pd.DataFrame,
    r1_labels_k9: np.ndarray,
    r5_df: pd.DataFrame,
    r5_labels_best: np.ndarray,
    targets_df: pd.DataFrame,
    speeds: np.ndarray,
    output_dir: Path | None = None,
) -> dict[str, Path]:
    """Generate all 10 required publication figures for Phase 3.

    Parameters
    ----------
    experiment_results : dict[str, Any]
        Aggregated results dictionary containing sweep metrics across representations.
    r1_df : pd.DataFrame
        Transformed features for Representation R1.
    r1_labels_k9 : np.ndarray
        Cluster labels for R1 at k=9.
    r5_df : pd.DataFrame
        Transformed features for Representation R5.
    r5_labels_best : np.ndarray
        Cluster labels for best R5 candidate.
    targets_df : pd.DataFrame
        Ground-truth degradation targets (kMc, kMt).
    speeds : np.ndarray
        Operating speeds (v) for each observation.
    output_dir : Path, optional
        Target directory for figures. Defaults to reports/figures/phase3.

    Returns
    -------
    dict[str, Path]
        Dictionary mapping figure names to saved file paths.
    """
    configure_plot_style()
    target_dir = output_dir or (get_figures_dir() / "phase3")
    target_dir.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}

    rep_sweeps = experiment_results.get("representation_sweeps", {})

    # 1. K vs Silhouette for all representations
    fig, ax = plt.subplots(figsize=(10, 6))
    for rep_id, data in rep_sweeps.items():
        ks = [item["k"] for item in data]
        sils = [item["silhouette"] for item in data]
        ax.plot(ks, sils, marker="o", linewidth=2, label=rep_id)
    ax.set_title("Intrinsic Clustering Quality: Silhouette Score vs Cluster Count (k)")
    ax.set_xlabel("Number of Clusters (k)")
    ax.set_ylabel("Silhouette Score (Higher is Better)")
    ax.set_xticks(range(2, 13))
    ax.legend(loc="best", frameon=True)
    fig.tight_layout()
    p1 = target_dir / "k_vs_silhouette_all_representations.png"
    fig.savefig(p1, dpi=300)
    plt.close(fig)
    paths["k_vs_silhouette"] = p1

    # 2. K vs Davies-Bouldin
    fig, ax = plt.subplots(figsize=(10, 6))
    for rep_id, data in rep_sweeps.items():
        ks = [item["k"] for item in data]
        dbs = [item["davies_bouldin"] for item in data]
        ax.plot(ks, dbs, marker="s", linewidth=2, label=rep_id)
    ax.set_title("Intrinsic Clustering Quality: Davies-Bouldin Index vs Cluster Count (k)")
    ax.set_xlabel("Number of Clusters (k)")
    ax.set_ylabel("Davies-Bouldin Index (Lower is Better)")
    ax.set_xticks(range(2, 13))
    ax.legend(loc="best", frameon=True)
    fig.tight_layout()
    p2 = target_dir / "k_vs_davies_bouldin.png"
    fig.savefig(p2, dpi=300)
    plt.close(fig)
    paths["k_vs_davies_bouldin"] = p2

    # 3. K vs Calinski-Harabasz
    fig, ax = plt.subplots(figsize=(10, 6))
    for rep_id, data in rep_sweeps.items():
        ks = [item["k"] for item in data]
        chs = [item["calinski_harabasz"] for item in data]
        ax.plot(ks, chs, marker="^", linewidth=2, label=rep_id)
    ax.set_title("Intrinsic Clustering Quality: Calinski-Harabasz Index vs Cluster Count (k)")
    ax.set_xlabel("Number of Clusters (k)")
    ax.set_ylabel("Calinski-Harabasz Score (Higher is Better)")
    ax.set_xticks(range(2, 13))
    ax.legend(loc="best", frameon=True)
    fig.tight_layout()
    p3 = target_dir / "k_vs_calinski_harabasz.png"
    fig.savefig(p3, dpi=300)
    plt.close(fig)
    paths["k_vs_calinski_harabasz"] = p3

    # 4. Speed Regime vs Cluster Heatmap (R1 at k=9)
    fig, ax = plt.subplots(figsize=(9, 7))
    crosstab_speed = pd.crosstab(
        pd.Series(r1_labels_k9, name="K-Means Cluster (k=9)"),
        pd.Series(speeds, name="Ship Speed v [knots]"),
    )
    sns.heatmap(crosstab_speed, annot=True, fmt="d", cmap="Blues", cbar=True, ax=ax)
    ax.set_title("Operating Regime Recovery: K-Means (k=9) on R1 vs Commanded Speed (v)")
    fig.tight_layout()
    p4 = target_dir / "speed_regime_vs_cluster_heatmap.png"
    fig.savefig(p4, dpi=300)
    plt.close(fig)
    paths["speed_vs_cluster_heatmap"] = p4

    # 5. Cluster Stability Distribution across seeds
    stability_data = experiment_results.get("stability_analysis", {})
    fig, ax = plt.subplots(figsize=(9, 5))
    rep_names = list(stability_data.keys())
    means = [stability_data[r]["ari_mean"] for r in rep_names]
    stds = [stability_data[r]["ari_std"] for r in rep_names]
    x_pos = np.arange(len(rep_names))
    ax.bar(x_pos, means, yerr=stds, capsize=6, color="#2ecc71", alpha=0.8)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(rep_names, rotation=25, ha="right")
    ax.set_ylabel("Mean Pairwise ARI Across 10 Seeds")
    ax.set_ylim(0.0, 1.05)
    ax.set_title("Cluster Stability Evaluation Across Multi-Seed Initializations")
    fig.tight_layout()
    p5 = target_dir / "cluster_stability_distribution.png"
    fig.savefig(p5, dpi=300)
    plt.close(fig)
    paths["cluster_stability"] = p5

    # 6. R5 Clustering Visualization (2D PCA projection for visualization only)
    fig, ax = plt.subplots(figsize=(9, 7))
    pca_2d = PCA(n_components=2, random_state=42)
    coords_2d = pca_2d.fit_transform(r5_df)
    scatter = ax.scatter(
        coords_2d[:, 0],
        coords_2d[:, 1],
        c=r5_labels_best,
        cmap="tab10",
        alpha=0.6,
        s=10,
    )
    fig.colorbar(scatter, ax=ax, label="Cluster Assignment")
    ax.set_title("R5 Cluster Space Projection (2D visualization only — not clustering feature space)")
    ax.set_xlabel(f"PC1 ({pca_2d.explained_variance_ratio_[0]*100:.1f}% var)")
    ax.set_ylabel(f"PC2 ({pca_2d.explained_variance_ratio_[1]*100:.1f}% var)")
    fig.tight_layout()
    p6 = target_dir / "r5_clustering_visualization.png"
    fig.savefig(p6, dpi=300)
    plt.close(fig)
    paths["r5_clustering_vis"] = p6

    # 7. Cluster vs kMc distribution
    fig, ax = plt.subplots(figsize=(9, 6))
    df_plot_kmc = pd.DataFrame({"Cluster": r5_labels_best, "kMc": targets_df["kMc"]})
    sns.boxplot(data=df_plot_kmc, x="Cluster", y="kMc", palette="Set2", ax=ax)
    ax.set_title("Post-Hoc Degradation Profiling: Compressor Decay State (kMc) by Cluster")
    ax.set_xlabel("Discovered Cluster Index (R5 Within-Speed Normalized)")
    ax.set_ylabel("Compressor Decay State Coefficient (kMc)")
    fig.tight_layout()
    p7 = target_dir / "cluster_vs_kmc_distribution.png"
    fig.savefig(p7, dpi=300)
    plt.close(fig)
    paths["cluster_vs_kmc"] = p7

    # 8. Cluster vs kMt distribution
    fig, ax = plt.subplots(figsize=(9, 6))
    df_plot_kmt = pd.DataFrame({"Cluster": r5_labels_best, "kMt": targets_df["kMt"]})
    sns.boxplot(data=df_plot_kmt, x="Cluster", y="kMt", palette="Set2", ax=ax)
    ax.set_title("Post-Hoc Degradation Profiling: Turbine Decay State (kMt) by Cluster")
    ax.set_xlabel("Discovered Cluster Index (R5 Within-Speed Normalized)")
    ax.set_ylabel("Turbine Decay State Coefficient (kMt)")
    fig.tight_layout()
    p8 = target_dir / "cluster_vs_kmt_distribution.png"
    fig.savefig(p8, dpi=300)
    plt.close(fig)
    paths["cluster_vs_kmt"] = p8

    # 9. Cluster Telemetry Profiles (mean standardized effect per cluster)
    fig, ax = plt.subplots(figsize=(12, 6))
    profile_df = r5_df.copy()
    profile_df["Cluster"] = r5_labels_best
    profile_means = profile_df.groupby("Cluster").mean()
    profile_means.T.plot(kind="bar", ax=ax, width=0.8)
    ax.set_title("Standardized Telemetry Sensor Profiles Across Clusters (R5 Space)")
    ax.set_xlabel("Telemetry Sensor Feature")
    ax.set_ylabel("Standardized Deviation from Operating Mean (Z-score)")
    ax.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    ax.legend(title="Cluster", loc="best")
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    p9 = target_dir / "cluster_telemetry_profiles.png"
    fig.savefig(p9, dpi=300)
    plt.close(fig)
    paths["cluster_telemetry_profiles"] = p9

    # 10. Algorithm comparison metrics on R5
    algo_comp = experiment_results.get("algorithm_comparison", {})
    fig, ax = plt.subplots(figsize=(9, 5))
    algos = list(algo_comp.keys())
    sils = [algo_comp[a].get("silhouette", 0.0) for a in algos]
    bars = ax.bar(algos, sils, color=["#3498db", "#9b59b6", "#e67e22", "#1abc9c"])
    ax.set_ylabel("Silhouette Score")
    ax.set_ylim(0.0, max(sils) * 1.2 if sils and max(sils) > 0 else 1.0)
    ax.set_title("Algorithm Performance Comparison on Representation R5")
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.01, f"{h:.3f}", ha="center", va="bottom")
    fig.tight_layout()
    p10 = target_dir / "algorithm_comparison_metrics.png"
    fig.savefig(p10, dpi=300)
    plt.close(fig)
    paths["algo_comparison"] = p10

    return paths
