"""Feature representation registry for controlled Phase 3 clustering experiments.

Tracks candidate feature representations, applied scalers, normalization strategies,
and intended research hypotheses.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any, Literal
import pandas as pd

from naval_propulsion.features.correlation import (
    REPRESENTATION_A_FEATURES,
    REPRESENTATION_B_FEATURES,
)
from naval_propulsion.preprocessing.transformers import (
    ColumnFilterTransformer,
    OperatingRegimeNormalizer,
    TelemetryScaler,
)
from naval_propulsion.utils.paths import get_experiments_dir


@dataclass(frozen=True)
class FeatureRepresentationSpec:
    representation_id: str
    description: str
    feature_names: tuple[str, ...]
    scaler_type: str
    normalization: str
    intended_use: str
    status: Literal["candidate", "recommended", "baseline", "deprecated"]


# Registry of candidate representations
CANDIDATE_REPRESENTATIONS: dict[str, FeatureRepresentationSpec] = {
    "R1_ALL_VALID_TELEMETRY": FeatureRepresentationSpec(
        representation_id="R1_ALL_VALID_TELEMETRY",
        description="All non-constant, non-duplicate sensors including commanded speed and lever position.",
        feature_names=REPRESENTATION_A_FEATURES,
        scaler_type="standard",
        normalization="global_standard",
        intended_use="Baseline: evaluates unconditioned clustering recovery of combined speed and plant state.",
        status="baseline",
    ),
    "R2_WITHOUT_OPERATING_DEMAND": FeatureRepresentationSpec(
        representation_id="R2_WITHOUT_OPERATING_DEMAND",
        description="Telemetry features with direct commanded setpoints (lp, v) excluded.",
        feature_names=tuple(c for c in REPRESENTATION_A_FEATURES if c not in ("lp", "v")),
        scaler_type="standard",
        normalization="global_standard",
        intended_use="Tests whether clustering recovers operating regimes indirectly through coupled physics.",
        status="candidate",
    ),
    "R3_REDUCED_CORRELATION": FeatureRepresentationSpec(
        representation_id="R3_REDUCED_CORRELATION",
        description="Pruned collinear feature subset (|r| < 0.985) across distinct thermodynamic subsystems.",
        feature_names=REPRESENTATION_B_FEATURES,
        scaler_type="standard",
        normalization="global_standard",
        intended_use="Evaluates whether removing collinear redundancy sharpens cluster separation in distance metrics.",
        status="candidate",
    ),
    "R4_ROBUST_SCALED_TELEMETRY": FeatureRepresentationSpec(
        representation_id="R4_ROBUST_SCALED_TELEMETRY",
        description="Telemetry scaled via RobustScaler (median centering, IQR scaling) to limit boundary distortion.",
        feature_names=tuple(c for c in REPRESENTATION_A_FEATURES if c not in ("lp", "v")),
        scaler_type="robust",
        normalization="global_robust",
        intended_use="Evaluates sensitivity of distance metrics to operational boundary extremes.",
        status="candidate",
    ),
    "R5_WITHIN_SPEED_NORMALIZED": FeatureRepresentationSpec(
        representation_id="R5_WITHIN_SPEED_NORMALIZED",
        description="Telemetry features conditionally normalized (mean=0, std=1) within each discrete operating speed regime.",
        feature_names=tuple(c for c in REPRESENTATION_A_FEATURES if c not in ("lp", "v")),
        scaler_type="within_regime_standard",
        normalization="conditional_within_speed",
        intended_use="Primary hypothesis: isolates subtle component degradation signatures from dominant speed variance.",
        status="recommended",
    ),
}


def build_representation_data(
    df: pd.DataFrame,
    spec: FeatureRepresentationSpec,
) -> pd.DataFrame:
    """Build transformed DataFrame according to the representation specification.

    Guarantees strict zero-leakage of kMc and kMt.
    """
    if spec.normalization == "conditional_within_speed":
        normalizer = OperatingRegimeNormalizer(regime_column="v")
        # Include 'v' and required telemetry features for fitting
        input_cols = ["v"] + list(spec.feature_names)
        transformed = normalizer.fit_transform(df[input_cols])
        return transformed

    # Global scaling
    X_subset = df[list(spec.feature_names)].copy()
    if spec.scaler_type in ("standard", "robust", "minmax"):
        scaler = TelemetryScaler(scaler_type=spec.scaler_type)  # type: ignore
        return scaler.fit_transform(X_subset)

    return X_subset


def save_representation_registry(
    output_path: Path | None = None,
) -> Path:
    """Serialize representation registry to JSON."""
    target_path = output_path or (get_experiments_dir() / "outputs" / "phase2" / "representation_registry.json")
    target_path.parent.mkdir(parents=True, exist_ok=True)
    registry_dict = {k: asdict(v) for k, v in CANDIDATE_REPRESENTATIONS.items()}
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(registry_dict, f, indent=2)
    return target_path
