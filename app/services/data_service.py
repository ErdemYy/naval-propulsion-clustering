"""Data access, caching, and demo observation service.

Provides cached access to the naval propulsion dataset, validation summaries,
and pre-selected sample observations for live university demonstrations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
import pandas as pd
import streamlit as st

from naval_propulsion.data.loader import DatasetContainer, load_naval_dataset
from naval_propulsion.utils.paths import get_experiments_dir, get_reports_dir


@st.cache_data
def load_cached_dataset() -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
    """Load and cache the authoritative naval propulsion dataset.

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame, list[str]]
        (features_df, targets_df, telemetry_columns)
    """
    container = load_naval_dataset()
    features = container.features.copy()
    targets = container.targets.copy()
    telemetry_cols = [c for c in features.columns if c not in ("lp", "v")]
    return features, targets, telemetry_cols


@st.cache_data
def load_phase4_validation_results() -> dict[str, Any]:
    """Load Phase 4 scientific validation results JSON."""
    results_path = get_experiments_dir() / "outputs" / "phase4" / "phase4_validation_results.json"
    if not results_path.exists():
        return {}
    with open(results_path, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def load_phase3_summary_results() -> dict[str, Any]:
    """Load Phase 3 clustering sweep results JSON."""
    summary_path = get_experiments_dir() / "outputs" / "phase3" / "phase3_summary.json"
    if not summary_path.exists():
        return {}
    with open(summary_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_demo_observations() -> dict[str, dict[str, Any]]:
    """Return pre-selected demonstration observations from the authoritative dataset.

    Contains 3 distinct physical cases:
    1. 'Nominal Baseline': Low degradation (high kMc, high kMt).
    2. 'Compressor Decay Profile': Noticeable compressor decay (low kMc, high kMt).
    3. 'Turbine Decay Profile': Noticeable turbine decay (high kMc, low kMt).

    Guarantees anti-leakage: The inputs only expose speed 'v' and the 11 telemetry features.
    Ground-truth kMc and kMt are isolated under 'ground_truth_reference' for post-hoc display only.
    """
    features_df, targets_df, _ = load_cached_dataset()
    full_df = pd.concat([features_df, targets_df], axis=1)

    # Filter at standard cruise speed v=18.0 knots
    v18 = full_df[full_df["v"] == 18.0]

    # 1. Nominal: max kMc (1.0), max kMt (1.0)
    nominal_row = v18[(v18["kMc"] == 1.0) & (v18["kMt"] == 1.0)].iloc[0]

    # 2. Compressor Decay: min kMc (0.95), high kMt (1.0)
    comp_decay_row = v18[(v18["kMc"] == 0.95) & (v18["kMt"] == 1.0)].iloc[0]

    # 3. Turbine Decay: high kMc (1.0), min kMt (0.975)
    turb_decay_row = v18[(v18["kMc"] == 1.0) & (v18["kMt"] == 0.975)].iloc[0]

    telemetry_cols = ["GTT", "GTn", "GGn", "Ts", "T48", "T2", "P48", "P2", "Pexh", "TIC", "mf"]

    def extract_demo(row: pd.Series, label: str, desc: str) -> dict[str, Any]:
        inputs = {"v": float(row["v"])}
        for c in telemetry_cols:
            inputs[c] = float(row[c])
        return {
            "label": label,
            "description": desc,
            "inputs": inputs,
            "ground_truth_reference": {
                "kMc": float(row["kMc"]),
                "kMt": float(row["kMt"]),
            },
        }

    return {
        "nominal": extract_demo(
            nominal_row,
            "Case 1: Nominal Baseline Reference (18 kts)",
            "Observed state with reference indicators at highest nominal health (kMc = 1.000, kMt = 1.000).",
        ),
        "compressor_decay": extract_demo(
            comp_decay_row,
            "Case 2: Severe Compressor Degradation (18 kts)",
            "Observed state with pronounced compressor decay (kMc = 0.950) and nominal turbine (kMt = 1.000).",
        ),
        "turbine_decay": extract_demo(
            turb_decay_row,
            "Case 3: Severe Turbine Degradation (18 kts)",
            "Observed state with nominal compressor (kMc = 1.000) and pronounced turbine decay (kMt = 0.975).",
        ),
    }


def get_figure_path(phase: str, filename: str) -> Path:
    """Return absolute path to a generated publication figure."""
    return get_reports_dir() / "figures" / phase / filename
