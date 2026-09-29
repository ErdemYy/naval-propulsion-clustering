"""Phase 4 Publication Visualizations.

Generates high-resolution publication figures for Phase 4:
- Degradation grid maps (kMc x kMt) for Candidate A (k=2) and Candidate B (k=3)
- Speed invariance cluster proportion charts across operating speed regimes
- Bootstrap stability ARI distribution plots
- Robust telemetry profile comparison with 95% bootstrap confidence intervals
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
import matplotlib
matplotlib.use("Agg")  # Headless execution
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from naval_propulsion.utils.paths import get_reports_dir


def setup_figure_style() -> None:
    """Set academic figure style."""
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 10,
        "axes.labelsize": 11,
        "axes.titlesize": 12,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "figure.titlesize": 13,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
    })


def plot_degradation_grid(
    full_df: pd.DataFrame,
    cluster_labels: np.ndarray,
    n_clusters: int,
    output_path: Path,
) -> Path:
    """Plot 2D degradation map (x = kMc, y = kMt) colored by cluster assignment."""
    setup_figure_style()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df_plot = full_df[["kMc", "kMt"]].copy()
    df_plot["cluster"] = cluster_labels

    # Aggregate majority cluster per (kMc, kMt) grid coordinate
    piv = df_plot.pivot_table(
        index="kMt",
        columns="kMc",
        values="cluster",
        aggfunc=lambda s: s.mode()[0],
    )

    fig, ax = plt.subplots(figsize=(9, 6.5))

    # Distinct discrete colormap
    if n_clusters == 2:
        colors = ["#2b5c8f", "#d95f02"]
        cmap = matplotlib.colors.ListedColormap(colors)
        bounds = [-0.5, 0.5, 1.5]
        norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
        labels = ["Cluster 0: Compressor Nominal (kMc ≈ 0.985)", "Cluster 1: Compressor Degraded (kMc ≈ 0.965)"]
    else:
        colors = ["#2b5c8f", "#7570b3", "#d95f02"]
        cmap = matplotlib.colors.ListedColormap(colors)
        bounds = [-0.5, 0.5, 1.5, 2.5]
        norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
        labels = [
            "Cluster 0: Degraded Turbine (kMt ≈ 0.982, kMc ≈ 0.984)",
            "Cluster 1: Nominal Baseline (kMt ≈ 0.992, kMc ≈ 0.983)",
            "Cluster 2: Degraded Compressor (kMc ≈ 0.961, kMt ≈ 0.988)",
        ]

    # Convert coordinates for pcolormesh
    kmc_vals = np.array(piv.columns, dtype=float)
    kmt_vals = np.array(piv.index, dtype=float)
    mesh = ax.pcolormesh(
        kmc_vals,
        kmt_vals,
        piv.values,
        cmap=cmap,
        norm=norm,
        shading="nearest",
        edgecolors="none",
    )

    cbar = fig.colorbar(mesh, ax=ax, ticks=range(n_clusters), orientation="horizontal", pad=0.12, shrink=0.85)
    cbar.ax.set_xticklabels(labels, fontsize=8.5)
    cbar.set_label("Assigned Cluster Profile (Post-hoc Validation Only — Zero Training Leakage)", fontsize=9.5)

    ax.set_xlabel("Compressor Decay State Coefficient (kMc) [Decreasing = Degraded]", fontsize=10.5, fontweight="bold")
    ax.set_ylabel("Turbine Decay State Coefficient (kMt) [Decreasing = Degraded]", fontsize=10.5, fontweight="bold")
    ax.set_title(
        f"Degradation Grid Coherence Map: Candidate {'A (k=2)' if n_clusters == 2 else 'B (k=3)'}\n"
        f"Spatial Partitioning in Factorial Degradation Space (kMc × kMt, N=11,934)",
        fontsize=11.5,
        pad=12,
    )

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close(fig)
    return output_path


def plot_speed_invariance(
    speed_records: list[dict[str, Any]],
    n_clusters: int,
    output_path: Path,
) -> Path:
    """Plot cluster proportions independently across the 9 operating speed regimes."""
    setup_figure_style()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df_speed = pd.DataFrame(speed_records)
    speeds = df_speed["speed"].to_numpy()
    n_speeds = len(speeds)

    fig, ax = plt.subplots(figsize=(8.5, 5))

    width = 0.8 / n_clusters
    x = np.arange(n_speeds)

    palette = ["#2b5c8f", "#d95f02", "#7570b3"]

    for c in range(n_clusters):
        prop_col = f"cluster_{c}_proportion"
        props = df_speed[prop_col].to_numpy()
        offset = (c - (n_clusters - 1) / 2) * width
        ax.bar(
            x + offset,
            props * 100.0,
            width=width,
            label=f"Cluster {c} ({'Nominal' if c == 0 and n_clusters == 2 else 'Degraded' if c == 1 and n_clusters == 2 else f'Profile {c}'})",
            color=palette[c],
            alpha=0.9,
            edgecolor="white",
            linewidth=0.8,
        )

        # Reference dashed line at overall mean proportion
        mean_p = np.mean(props) * 100.0
        ax.axhline(mean_p, color=palette[c], linestyle="--", linewidth=1.0, alpha=0.6)

    ax.set_xticks(x)
    ax.set_xticklabels([f"{int(s)} kts" for s in speeds], fontweight="bold")
    ax.set_xlabel("Ship Commanded Speed Regime (knots)", fontsize=10.5, fontweight="bold")
    ax.set_ylabel("Cluster Proportion within Speed Regime (%)", fontsize=10.5, fontweight="bold")
    ax.set_ylim(0, max(60, (df_speed[[f'cluster_{c}_proportion' for c in range(n_clusters)]].values.max() * 100) + 10))
    ax.set_title(
        f"Operating-Speed Invariance: Candidate {'A (k=2)' if n_clusters == 2 else 'B (k=3)'}\n"
        f"Stability of Cluster Proportions Across Commanded Speeds (v = 3..27 knots)",
        fontsize=11.5,
        pad=10,
    )
    ax.legend(frameon=True, facecolor="white", edgecolor="none", loc="upper right")

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close(fig)
    return output_path


def plot_bootstrap_stability_comparison(
    boot_k2: dict[str, Any],
    boot_k3: dict[str, Any],
    output_path: Path,
) -> Path:
    """Plot bootstrap stability Adjusted Rand Index distributions for Candidates A and B."""
    setup_figure_style()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 4.5))

    sns.kdeplot(
        boot_k2["bootstrap_ari_samples"],
        ax=ax,
        label=f"Candidate A (k=2): Mean ARI = {boot_k2['mean_ari']:.4f} [95% CI: {boot_k2['ci_2_5_percentile']:.3f}–{boot_k2['ci_97_5_percentile']:.3f}]",
        color="#2b5c8f",
        fill=True,
        alpha=0.4,
        linewidth=2.0,
    )
    sns.kdeplot(
        boot_k3["bootstrap_ari_samples"],
        ax=ax,
        label=f"Candidate B (k=3): Mean ARI = {boot_k3['mean_ari']:.4f} [95% CI: {boot_k3['ci_2_5_percentile']:.3f}–{boot_k3['ci_97_5_percentile']:.3f}]",
        color="#d95f02",
        fill=True,
        alpha=0.4,
        linewidth=2.0,
    )

    ax.set_xlabel("Adjusted Rand Index (ARI) against Full Reference Solution", fontsize=10.5, fontweight="bold")
    ax.set_ylabel("Kernel Density Estimate", fontsize=10.5, fontweight="bold")
    ax.set_title(
        "Bootstrap Clustering Stability Distributions (B=100 Repetitions with Replacement)\n"
        "Comparison of Candidate A (k=2) vs Candidate B (k=3) on Representation R5",
        fontsize=11.5,
        pad=10,
    )
    ax.legend(frameon=True, facecolor="white", loc="upper left")

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close(fig)
    return output_path


def plot_telemetry_profiles(
    profiles_k2: dict[str, dict[str, Any]],
    profiles_k3: dict[str, dict[str, Any]],
    output_path: Path,
) -> Path:
    """Plot standardized telemetry feature deviation profiles with 95% bootstrap CIs."""
    setup_figure_style()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    features = list(profiles_k2["0"].keys())
    n_feats = len(features)
    x = np.arange(n_feats)

    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Top: Candidate A (k=2)
    ax0 = axes[0]
    width = 0.35
    for c_idx, c_name in enumerate(["0", "1"]):
        means = [profiles_k2[c_name][f]["mean"] for f in features]
        err_low = [profiles_k2[c_name][f]["mean"] - profiles_k2[c_name][f]["ci_95_lower"] for f in features]
        err_high = [profiles_k2[c_name][f]["ci_95_upper"] - profiles_k2[c_name][f]["mean"] for f in features]
        offset = (c_idx - 0.5) * width
        color = "#2b5c8f" if c_idx == 0 else "#d95f02"
        label = "Cluster 0 (Compressor Nominal)" if c_idx == 0 else "Cluster 1 (Compressor Degraded)"
        ax0.bar(
            x + offset,
            means,
            width=width,
            yerr=[err_low, err_high],
            capsize=3,
            label=label,
            color=color,
            alpha=0.85,
        )

    ax0.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    ax0.set_ylabel("Standardized Deviation (z-score)", fontsize=10)
    ax0.set_title("Candidate A (k=2) Telemetry Deviation Profiles with 95% Bootstrap CIs", fontsize=11)
    ax0.legend(loc="upper right", frameon=True)

    # Bottom: Candidate B (k=3)
    ax1 = axes[1]
    width_b = 0.25
    colors_b = ["#2b5c8f", "#7570b3", "#d95f02"]
    labels_b = [
        "Cluster 0: Degraded Turbine",
        "Cluster 1: Nominal Baseline",
        "Cluster 2: Degraded Compressor",
    ]
    for c_idx, c_name in enumerate(["0", "1", "2"]):
        means = [profiles_k3[c_name][f]["mean"] for f in features]
        err_low = [profiles_k3[c_name][f]["mean"] - profiles_k3[c_name][f]["ci_95_lower"] for f in features]
        err_high = [profiles_k3[c_name][f]["ci_95_upper"] - profiles_k3[c_name][f]["mean"] for f in features]
        offset = (c_idx - 1.0) * width_b
        ax1.bar(
            x + offset,
            means,
            width=width_b,
            yerr=[err_low, err_high],
            capsize=2,
            label=labels_b[c_idx],
            color=colors_b[c_idx],
            alpha=0.85,
        )

    ax1.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    ax1.set_xticks(x)
    ax1.set_xticklabels(features, fontsize=9.5, fontweight="bold")
    ax1.set_xlabel("Clustering-Eligible Telemetry Channels", fontsize=10.5, fontweight="bold")
    ax1.set_ylabel("Standardized Deviation (z-score)", fontsize=10)
    ax1.set_title("Candidate B (k=3) Telemetry Deviation Profiles with 95% Bootstrap CIs", fontsize=11)
    ax1.legend(loc="upper right", frameon=True)

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close(fig)
    return output_path
