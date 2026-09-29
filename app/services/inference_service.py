"""Inference service for observation analysis and profile assignment.

Processes user or demo observations:
1. Validates input telemetry schema.
2. Rejects any leakage of kMc or kMt.
3. Applies conditional within-speed normalization using the serialized normalizer.
4. Computes Euclidean distances to cluster centroids.
5. Returns nearest cluster assignment and non-causal academic profile characterization.
"""

from __future__ import annotations

from typing import Any, Literal
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from app.services.model_service import load_final_models
from naval_propulsion.preprocessing.transformers import OperatingRegimeNormalizer


VALID_SPEEDS: tuple[float, ...] = (3.0, 6.0, 9.0, 12.0, 15.0, 18.0, 21.0, 24.0, 27.0)
REQUIRED_TELEMETRY: tuple[str, ...] = (
    "GTT", "GTn", "GGn", "Ts", "T48", "T2", "P48", "P2", "Pexh", "TIC", "mf"
)


class InputValidationError(Exception):
    """Raised when user input violates schema, includes leaked targets, or has invalid values."""
    pass


def validate_observation_input(input_data: dict[str, float]) -> None:
    """Validate input dictionary against strict zero-leakage and schema rules.

    Raises
    ------
    InputValidationError
        If kMc/kMt are present, required telemetry features are missing, or speed is unobserved.
    """
    # Strict anti-leakage check
    if "kMc" in input_data or "kMt" in input_data:
        raise InputValidationError(
            "CRITICAL INVARIANT VIOLATION: kMc and kMt are reference degradation indicators "
            "and MUST NEVER be supplied as model inputs!"
        )

    # Operating speed conditioning requirement
    if "v" not in input_data:
        raise InputValidationError("Missing required conditioning variable 'v' (ship speed).")

    v_val = float(input_data["v"])
    if v_val not in VALID_SPEEDS:
        raise InputValidationError(
            f"Observed speed {v_val} knots not recognized. "
            f"Must be one of the discrete simulated speeds: {list(VALID_SPEEDS)}"
        )

    # Required telemetry features
    missing_feats = [f for f in REQUIRED_TELEMETRY if f not in input_data]
    if missing_feats:
        raise InputValidationError(f"Missing required telemetry features: {missing_feats}")


def assign_observation_profile(
    input_data: dict[str, float],
    model_choice: Literal["k2", "k3"] = "k2",
) -> dict[str, Any]:
    """Assign an observation to its closest learned cluster profile.

    Parameters
    ----------
    input_data : dict[str, float]
        Dictionary with 'v' and the 11 clustering telemetry features.
    model_choice : Literal["k2", "k3"], default="k2"
        Whether to evaluate using the Primary Model (k=2) or Secondary Model (k=3).

    Returns
    -------
    dict[str, Any]
        Dictionary containing:
        - 'assigned_cluster': int
        - 'closest_profile_name': str
        - 'centroid_distance': float
        - 'all_distances': dict[int, float]
        - 'normalized_features': dict[str, float]
        - 'profile_description': str
        - 'model_used': str
    """
    validate_observation_input(input_data)

    models_bundle = load_final_models()
    normalizer: OperatingRegimeNormalizer = models_bundle["normalizer"]
    model: KMeans = models_bundle["primary_model"] if model_choice == "k2" else models_bundle["secondary_model"]

    # Build 1-row DataFrame preserving exact column order
    cols = ["v"] + list(REQUIRED_TELEMETRY)
    row_df = pd.DataFrame([{c: float(input_data[c]) for c in cols}])

    # Transform through within-speed normalizer
    norm_df = normalizer.transform(row_df)
    z_vector = norm_df[list(REQUIRED_TELEMETRY)].to_numpy()  # shape (1, 11)

    # Compute Euclidean distance to all centroids
    centroids = model.cluster_centers_  # shape (k, 11)
    diffs = centroids - z_vector
    distances = np.linalg.norm(diffs, axis=1)  # shape (k,)

    assigned_cluster = int(np.argmin(distances))
    min_dist = float(distances[assigned_cluster])
    all_dists = {int(i): float(distances[i]) for i in range(len(distances))}

    # Academic non-causal descriptions
    if model_choice == "k2":
        if assigned_cluster == 0:
            profile_name = "Cluster 0: Compressor Nominal Association"
            desc = (
                "Characterized by below-baseline temperatures (T2, T48) and fuel flow (mf) relative to "
                "the operating speed baseline. Post-hoc analysis associates this profile with higher "
                "compressor health (kMc ≈ 0.985)."
            )
        else:
            profile_name = "Cluster 1: Compressor Degradation Association"
            desc = (
                "Characterized by above-baseline temperatures (T2, T48) and fuel flow (mf) relative to "
                "the operating speed baseline. Post-hoc analysis associates this profile with elevated "
                "compressor decay (kMc ≈ 0.965)."
            )
        model_name = "Primary Scientific Model (KMeans k=2)"
    else:
        if assigned_cluster == 0:
            profile_name = "Cluster 0: Turbine Degradation Association"
            desc = (
                "Characterized by elevated turbine exit pressure (P48) and compressor outlet pressure (P2), "
                "with lower shaft speeds (GTn, GGn). Post-hoc analysis associates this profile with degraded turbine "
                "decay states (kMt ≈ 0.982) and nominal compressor."
            )
        elif assigned_cluster == 1:
            profile_name = "Cluster 1: Nominal Baseline Reference Profile"
            desc = (
                "Characterized by lowest fuel flow (mf) and low turbine inlet temperatures (T48, TIC). "
                "Post-hoc analysis associates this profile with high compressor and high turbine health (kMt ≈ 0.992, kMc ≈ 0.983)."
            )
        else:
            profile_name = "Cluster 2: Compressor Degradation Association"
            desc = (
                "Characterized by elevated compressor outlet temperature (T2), gas generator speed (GGn), "
                "and turbine inlet temperature (T48). Post-hoc analysis associates this profile with pronounced "
                "compressor decay (kMc ≈ 0.961)."
            )
        model_name = "Secondary Multi-Component Diagnostic Model (KMeans k=3)"

    return {
        "assigned_cluster": assigned_cluster,
        "closest_profile_name": profile_name,
        "centroid_distance": min_dist,
        "all_distances": all_dists,
        "normalized_features": {col: float(z_vector[0, idx]) for idx, col in enumerate(REQUIRED_TELEMETRY)},
        "profile_description": desc,
        "model_used": model_name,
    }
