"""Scaler comparison and distribution transformation analysis.

Compares StandardScaler, RobustScaler, and MinMaxScaler on telemetry features,
reporting moments, quantiles, extreme value compression, and generating
diagnostic comparative plots.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Sequence
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from naval_propulsion.preprocessing.transformers import TelemetryScaler
from naval_propulsion.utils.paths import get_experiments_dir, get_figures_dir
from naval_propulsion.visualization.plots import configure_plot_style


def compare_scalers(
    df: pd.DataFrame,
    features: Sequence[str],
) -> dict[str, Any]:
    """Compute transformation moments and quantiles across scalers.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset containing features to scale.
    features : Sequence[str]
        List of feature column names to compare.

    Returns
    -------
    dict[str, Any]
        Dictionary with statistical summaries for each scaler.
    """
    X = df[list(features)].copy()
    scaler_types = ["standard", "robust", "minmax"]
    results: dict[str, Any] = {}

    for stype in scaler_types:
        scaler = TelemetryScaler(scaler_type=stype)
        X_scaled = scaler.fit_transform(X)

        feature_summaries: dict[str, dict[str, float]] = {}
        for col in features:
            s = X_scaled[col]
            q05 = float(s.quantile(0.05))
            q25 = float(s.quantile(0.25))
            q50 = float(s.median())
            q75 = float(s.quantile(0.75))
            q95 = float(s.quantile(0.95))
            iqr = q75 - q25

            feature_summaries[col] = {
                "mean": float(s.mean()),
                "std": float(s.std(ddof=1)),
                "min": float(s.min()),
                "max": float(s.max()),
                "median": q50,
                "iqr": iqr,
                "q05": q05,
                "q25": q25,
                "q75": q75,
                "q95": q95,
            }

        results[stype] = {
            "scaler_type": stype,
            "overall_min": float(X_scaled.min().min()),
            "overall_max": float(X_scaled.max().max()),
            "overall_mean": float(X_scaled.mean().mean()),
            "overall_std": float(X_scaled.std().mean()),
            "features": feature_summaries,
        }

    return results


def generate_scaler_comparison_figure(
    df: pd.DataFrame,
    features: Sequence[str] | None = None,
    output_path: Path | None = None,
) -> Path:
    """Generate comparative violin/boxplots showing distribution of features under each scaler."""
    configure_plot_style()
    target_path = output_path or (get_figures_dir() / "phase2" / "scaler_comparison.png")
    target_path.parent.mkdir(parents=True, exist_ok=True)

    test_features = list(features) if features is not None else ["GTT", "GTn", "GGn", "T48", "P2", "mf"]
    X = df[test_features].copy()

    fig, axes = plt.subplots(3, 1, figsize=(13, 12), sharex=True)
    scaler_types = [("standard", "StandardScaler (Z-Score: mean=0, std=1)"),
                    ("robust", "RobustScaler (Median=0, IQR-scaled)"),
                    ("minmax", "MinMaxScaler (Bounded [0, 1])")]

    for idx, (stype, title) in enumerate(scaler_types):
        scaler = TelemetryScaler(scaler_type=stype)
        X_s = scaler.fit_transform(X)
        melted = X_s.melt(var_name="Feature", value_name="Scaled Value")
        sns.boxplot(
            data=melted,
            x="Feature",
            y="Scaled Value",
            ax=axes[idx],
            palette="Blues_d",
        )
        axes[idx].set_title(title)
        axes[idx].set_ylabel("Transformed Value")

    axes[2].set_xlabel("Propulsion Telemetry Feature")
    plt.suptitle("Phase 2: Comparative Distribution Profiles Across Scalers", y=1.01)
    plt.tight_layout()
    fig.savefig(target_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return target_path


def save_scaler_comparison_results(
    comparison_results: dict[str, Any],
    output_path: Path | None = None,
) -> Path:
    """Save scaler comparison moments to JSON."""
    target_path = output_path or (get_experiments_dir() / "outputs" / "phase2" / "scaler_comparison.json")
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(comparison_results, f, indent=2)
    return target_path
