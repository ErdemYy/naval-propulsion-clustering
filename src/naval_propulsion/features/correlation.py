"""Correlation analysis and correlation-reduced feature representation generator.

Computes Pearson and Spearman correlation matrices, exports publication figures,
and constructs both Minimal-Cleaning (Representation A) and Reduced-Correlation
(Representation B) feature sets.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from naval_propulsion.utils.paths import get_figures_dir
from naval_propulsion.visualization.plots import configure_plot_style


# Canonical representation definitions
REPRESENTATION_A_FEATURES: tuple[str, ...] = (
    "lp", "v", "GTT", "GTn", "GGn", "Ts", "T48", "T2", "P48", "P2", "Pexh", "TIC", "mf"
)

# Representation B: Pruning exact duplicates and collinear features (|r| > 0.985)
# Retaining distinct thermodynamic subsystems:
# - v: ship speed (retained as operating condition, dropping redundant lp)
# - GTT: gas turbine torque (retained, dropping redundant propeller torque Ts and redundant pressures P48, Pexh)
# - GTn: power turbine rotational speed
# - GGn: gas generator rotational speed
# - T48: turbine exit temperature
# - T2: compressor outlet temperature
# - P2: compressor outlet pressure
# - TIC: turbine injection control
# - mf: fuel flow
REPRESENTATION_B_FEATURES: tuple[str, ...] = (
    "v", "GTT", "GTn", "GGn", "T48", "T2", "P2", "TIC", "mf"
)


def compute_correlations(df: pd.DataFrame, features: Sequence[str] | None = None) -> dict[str, pd.DataFrame]:
    """Compute Pearson and Spearman correlation matrices for specified features."""
    cols = list(features) if features is not None else [
        c for c in df.columns if c not in ("T1", "P1", "Tp", "kMc", "kMt")
    ]
    pearson_corr = df[cols].corr(method="pearson")
    spearman_corr = df[cols].corr(method="spearman")
    return {"pearson": pearson_corr, "spearman": spearman_corr}


def generate_correlation_figures(
    df: pd.DataFrame,
    output_dir: Path | None = None,
    features: Sequence[str] | None = None,
) -> dict[str, Path]:
    """Generate Pearson and Spearman correlation heatmaps for Phase 2.

    Saves figures with non-blocking headless rendering to avoid UI halts.
    """
    configure_plot_style()
    target_dir = output_dir or (get_figures_dir() / "phase2")
    target_dir.mkdir(parents=True, exist_ok=True)

    corrs = compute_correlations(df, features)
    paths: dict[str, Path] = {}

    # 1. Pearson heatmap
    fig, ax = plt.subplots(figsize=(11, 9))
    sns.heatmap(
        corrs["pearson"],
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        vmin=-1,
        vmax=1,
        square=True,
        cbar_kws={"label": "Pearson Correlation (r)"},
        ax=ax,
    )
    ax.set_title("Phase 2: Pearson Correlation Matrix (Filtered Telemetry Features)")
    plt.tight_layout()
    p_path = target_dir / "pearson_correlation.png"
    fig.savefig(p_path, dpi=300)
    plt.close(fig)
    paths["pearson"] = p_path

    # 2. Spearman heatmap
    fig, ax = plt.subplots(figsize=(11, 9))
    sns.heatmap(
        corrs["spearman"],
        annot=True,
        fmt=".2f",
        cmap="vlag",
        center=0,
        vmin=-1,
        vmax=1,
        square=True,
        cbar_kws={"label": "Spearman Rank Correlation (rho)"},
        ax=ax,
    )
    ax.set_title("Phase 2: Spearman Rank Correlation Matrix (Filtered Telemetry Features)")
    plt.tight_layout()
    s_path = target_dir / "spearman_correlation.png"
    fig.savefig(s_path, dpi=300)
    plt.close(fig)
    paths["spearman"] = s_path

    return paths
