"""Exploratory Data Analysis (EDA) plotting routines.

Generates publication-quality figures for feature distributions,
correlation heatmaps, operating regimes, and degradation targets.
"""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from naval_propulsion.utils.paths import get_figures_dir
from naval_propulsion.visualization.plots import configure_plot_style


def generate_phase1_figures(
    df: pd.DataFrame,
    output_dir: Path | None = None,
) -> list[Path]:
    """Generate all Phase 1 publication-quality diagnostic figures.

    Parameters
    ----------
    df : pd.DataFrame
        Complete 18-column naval propulsion dataset.
    output_dir : Path, optional
        Target directory for saved figures. Defaults to reports/figures/phase1.

    Returns
    -------
    list[Path]
        List of generated figure file paths.
    """
    configure_plot_style()
    target_dir = output_dir or (get_figures_dir() / "phase1")
    target_dir.mkdir(parents=True, exist_ok=True)
    generated_paths: list[Path] = []

    # Non-constant sensor features
    telemetry_cols = [c for c in df.columns if c not in ("T1", "P1", "kMc", "kMt")]

    # Figure 1: Correlation Heatmap (Pearson)
    fig, ax = plt.subplots(figsize=(12, 10))
    corr_pearson = df[telemetry_cols].corr(method="pearson")
    sns.heatmap(
        corr_pearson,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        vmin=-1,
        vmax=1,
        square=True,
        cbar_kws={"label": "Pearson Correlation Coefficient"},
        ax=ax,
    )
    ax.set_title("Pairwise Pearson Correlation Matrix (Telemetry Features)")
    plt.tight_layout()
    p1 = target_dir / "correlation_matrix_pearson.png"
    fig.savefig(p1, dpi=300)
    plt.close(fig)
    generated_paths.append(p1)

    # Figure 2: Correlation Heatmap (Spearman)
    fig, ax = plt.subplots(figsize=(12, 10))
    corr_spearman = df[telemetry_cols].corr(method="spearman")
    sns.heatmap(
        corr_spearman,
        annot=True,
        fmt=".2f",
        cmap="vlag",
        center=0,
        vmin=-1,
        vmax=1,
        square=True,
        cbar_kws={"label": "Spearman Rank Correlation Coefficient"},
        ax=ax,
    )
    ax.set_title("Pairwise Spearman Rank Correlation Matrix (Telemetry Features)")
    plt.tight_layout()
    p2 = target_dir / "correlation_matrix_spearman.png"
    fig.savefig(p2, dpi=300)
    plt.close(fig)
    generated_paths.append(p2)

    # Figure 3: Operating Conditions (lp and v)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    sns.countplot(
        data=df,
        x="v",
        color="#2b5c8f",
        ax=axes[0],
    )
    axes[0].set_title("Discrete Distribution of Ship Speed (v)")
    axes[0].set_xlabel("Ship Speed v [knots]")
    axes[0].set_ylabel("Sample Count")

    sns.countplot(
        data=df,
        x=df["lp"].round(3),
        color="#3d85c6",
        ax=axes[1],
    )
    axes[1].set_title("Discrete Distribution of Lever Position (lp)")
    axes[1].set_xlabel("Lever Position lp [ ]")
    axes[1].set_ylabel("Sample Count")
    axes[1].tick_params(axis="x", rotation=45)

    plt.suptitle("Factorial Operating Condition Distribution (1,326 samples per discrete setting)", y=1.02)
    plt.tight_layout()
    p3 = target_dir / "operating_conditions_distribution.png"
    fig.savefig(p3, dpi=300, bbox_inches="tight")
    plt.close(fig)
    generated_paths.append(p3)

    # Figure 4: Degradation Targets Distribution (kMc and kMt)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    sns.histplot(
        df["kMc"],
        bins=51,
        kde=True,
        color="#c0392b",
        ax=axes[0],
    )
    axes[0].set_title("Compressor Decay State Coefficient (kMc)")
    axes[0].set_xlabel("kMc [0.95 to 1.00, step 0.001]")
    axes[0].set_ylabel("Sample Count")

    sns.histplot(
        df["kMt"],
        bins=26,
        kde=True,
        color="#8e44ad",
        ax=axes[1],
    )
    axes[1].set_title("Turbine Decay State Coefficient (kMt)")
    axes[1].set_xlabel("kMt [0.975 to 1.00, step 0.001]")
    axes[1].set_ylabel("Sample Count")

    plt.suptitle("Quarantined Degradation Indicators: Ground-Truth Factorial Grid", y=1.02)
    plt.tight_layout()
    p4 = target_dir / "degradation_targets_distribution.png"
    fig.savefig(p4, dpi=300, bbox_inches="tight")
    plt.close(fig)
    generated_paths.append(p4)

    # Figure 5: Feature Scale Disparity (Raw Boxplots on Log Scale)
    fig, ax = plt.subplots(figsize=(13, 6))
    melted_df = df[telemetry_cols].melt(var_name="Sensor", value_name="Raw Value")
    sns.boxplot(
        data=melted_df,
        x="Sensor",
        y="Raw Value",
        color="#70a1ff",
        ax=ax,
    )
    ax.set_yscale("symlog")
    ax.set_title("Unscaled Telemetry Sensor Value Ranges (Symlog Scale)")
    ax.set_xlabel("Propulsion Sensor Telemetry Channels")
    ax.set_ylabel("Recorded Value (Symlog Scale)")
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    p5 = target_dir / "feature_scales_symlog_boxplot.png"
    fig.savefig(p5, dpi=300)
    plt.close(fig)
    generated_paths.append(p5)

    # Figure 6: Operating Demand vs Degradation Signature
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    scatter1 = axes[0].scatter(
        df["v"],
        df["GTT"],
        c=df["kMc"],
        cmap="viridis",
        alpha=0.4,
        s=12,
    )
    fig.colorbar(scatter1, ax=axes[0], label="Compressor Decay State (kMc)")
    axes[0].set_title("Turbine Shaft Torque (GTT) vs Ship Speed (v)")
    axes[0].set_xlabel("Ship Speed v [knots]")
    axes[0].set_ylabel("Shaft Torque GTT [kN m]")

    scatter2 = axes[1].scatter(
        df["v"],
        df["T48"],
        c=df["kMt"],
        cmap="plasma",
        alpha=0.4,
        s=12,
    )
    fig.colorbar(scatter2, ax=axes[1], label="Turbine Decay State (kMt)")
    axes[1].set_title("Turbine Exit Temp (T48) vs Ship Speed (v)")
    axes[1].set_xlabel("Ship Speed v [knots]")
    axes[1].set_ylabel("HP Turbine Exit Temp T48 [C]")

    plt.suptitle("Operating Demand (Speed) Dominance Over Degradation Variance", y=1.02)
    plt.tight_layout()
    p6 = target_dir / "operating_dominance_vs_degradation.png"
    fig.savefig(p6, dpi=300, bbox_inches="tight")
    plt.close(fig)
    generated_paths.append(p6)

    # Figure 7: Key Sensor Distributions (Histograms + KDE)
    plot_sensors = ["GTT", "GTn", "GGn", "T48", "T2", "P2", "P48", "mf"]
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    axes_flat = axes.flatten()
    for idx, sensor in enumerate(plot_sensors):
        sns.histplot(
            df[sensor],
            kde=True,
            ax=axes_flat[idx],
            color="#2e86de",
            stat="density",
            bins=30,
        )
        axes_flat[idx].set_title(f"{sensor} Distribution")
        axes_flat[idx].set_xlabel(sensor)
    plt.suptitle("Distributions of Key Thermodynamic & Rotational Sensors", y=1.02)
    plt.tight_layout()
    p7 = target_dir / "sensor_distributions_multimodal.png"
    fig.savefig(p7, dpi=300, bbox_inches="tight")
    plt.close(fig)
    generated_paths.append(p7)

    return generated_paths
