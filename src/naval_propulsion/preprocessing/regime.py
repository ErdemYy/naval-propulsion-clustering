"""Operating condition and regime decomposition analysis.

Analyzes the dominance of operating speed (v) and throttle (lp) over telemetry
features, computing between-speed vs within-speed variance, eta-squared,
and generating comparative operating regime profiles.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Sequence
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from naval_propulsion.utils.paths import get_experiments_dir, get_figures_dir
from naval_propulsion.visualization.plots import configure_plot_style


def analyze_operating_regimes(
    df: pd.DataFrame,
    telemetry_features: Sequence[str] | None = None,
    regime_col: str = "v",
) -> dict[str, Any]:
    """Compute within-speed vs between-speed variance decomposition and eta-squared.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset containing telemetry and operating regime columns.
    telemetry_features : Sequence[str], optional
        List of telemetry features to analyze.
    regime_col : str, default="v"
        Column denoting the operating regime.

    Returns
    -------
    dict[str, Any]
        Decomposition report containing variance ratios, eta-squared, and profile tables.
    """
    if telemetry_features is None:
        telemetry_features = [
            c for c in df.columns
            if c not in ("T1", "P1", "Tp", "kMc", "kMt", "lp", "v")
        ]
    cols = list(telemetry_features)

    grand_mean = df[cols].mean()
    ss_total = ((df[cols] - grand_mean) ** 2).sum()

    speeds = sorted(df[regime_col].unique())
    n_total = len(df)
    k_groups = len(speeds)

    ss_between = pd.Series(0.0, index=cols)
    within_var_by_speed: dict[str, dict[str, float]] = {str(s): {} for s in speeds}

    for s in speeds:
        sub = df[df[regime_col] == s][cols]
        n_k = len(sub)
        mean_k = sub.mean()
        ss_between += n_k * ((mean_k - grand_mean) ** 2)

        for c in cols:
            within_var_by_speed[str(s)][c] = float(sub[c].var(ddof=1))

    ss_within = ss_total - ss_between
    eta_squared = ss_between / ss_total

    # Compute F-statistic
    df_between = k_groups - 1
    df_within = n_total - k_groups
    ms_between = ss_between / df_between
    ms_within = ss_within / df_within
    f_stat = ms_between / ms_within

    feature_metrics: dict[str, dict[str, float]] = {}
    for c in cols:
        feature_metrics[c] = {
            "eta_squared": float(eta_squared[c]),
            "percent_variance_explained_by_speed": float(eta_squared[c] * 100.0),
            "ss_total": float(ss_total[c]),
            "ss_between_speeds": float(ss_between[c]),
            "ss_within_speeds": float(ss_within[c]),
            "f_statistic": float(f_stat[c]),
        }

    report = {
        "regime_column": regime_col,
        "unique_regimes": [float(s) for s in speeds],
        "n_samples_per_regime": int(n_total / k_groups),
        "feature_metrics": feature_metrics,
        "mean_variance_explained_by_speed": float(eta_squared.mean() * 100.0),
        "scientific_conclusion": (
            f"Operating speed '{regime_col}' explains an average of {eta_squared.mean() * 100.0:.2f}% "
            "of total feature variance across telemetry channels. Unconditioned clustering on "
            "standardized telemetry will inevitably reconstruct the discrete operating speed setpoints "
            "rather than subtle degradation profiles."
        ),
    }

    return report


def generate_regime_profile_figures(
    df: pd.DataFrame,
    features: Sequence[str] | None = None,
    output_path: Path | None = None,
) -> Path:
    """Generate multi-panel plot showing telemetry profiles across operating speeds."""
    configure_plot_style()
    target_path = output_path or (get_figures_dir() / "phase2" / "operating_speed_profiles.png")
    target_path.parent.mkdir(parents=True, exist_ok=True)

    plot_features = list(features) if features is not None else ["GTT", "GTn", "GGn", "T48", "P2", "mf"]
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    axes_flat = axes.flatten()

    for idx, feat in enumerate(plot_features):
        ax = axes_flat[idx]
        sns.boxplot(
            data=df,
            x="v",
            y=feat,
            color="#3498db",
            ax=ax,
        )
        ax.set_title(f"{feat} across Ship Speed (v)")
        ax.set_xlabel("Ship Speed v [knots]")
        ax.set_ylabel(feat)

    plt.suptitle("Phase 2: Sensor Telemetry Profiles Across Commanded Ship Speeds", y=1.02)
    plt.tight_layout()
    fig.savefig(target_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return target_path


def save_regime_report(
    report: dict[str, Any],
    output_path: Path | None = None,
) -> Path:
    """Save operating regime analysis report to JSON."""
    target_path = output_path or (get_experiments_dir() / "outputs" / "phase2" / "operating_regime_report.json")
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    return target_path
