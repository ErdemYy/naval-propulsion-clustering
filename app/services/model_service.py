"""Model loading, validation, and lifecycle management service.

Loads serialized artifacts from models/final/, validates model_manifest.json,
and provides strictly immutable model wrappers. Never retrains models silently.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
import joblib
from sklearn.cluster import KMeans

from naval_propulsion.preprocessing.transformers import OperatingRegimeNormalizer
from naval_propulsion.utils.paths import get_models_dir


class ModelArtifactError(Exception):
    """Raised when model artifacts are missing, corrupt, or inconsistent with manifest."""
    pass


def get_final_models_dir() -> Path:
    """Return path to final models directory."""
    return get_models_dir() / "final"


def load_model_manifest() -> dict[str, Any]:
    """Load and validate final model manifest.

    Raises
    ------
    ModelArtifactError
        If manifest file is missing or has invalid schema.
    """
    manifest_path = get_final_models_dir() / "model_manifest.json"
    if not manifest_path.exists():
        raise ModelArtifactError(
            f"Missing required model manifest at: {manifest_path}. "
            "Ensure Phase 4 validation has been executed."
        )

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception as e:
        raise ModelArtifactError(f"Failed to parse model_manifest.json: {e}")

    # Validate essential schema
    required_sections = ["model_selection", "representation", "data_provenance", "environment"]
    for sec in required_sections:
        if sec not in manifest:
            raise ModelArtifactError(f"Manifest missing required section: '{sec}'")

    if "primary_model" not in manifest["model_selection"]:
        raise ModelArtifactError("Manifest missing 'primary_model' in model_selection")
    if "secondary_model" not in manifest["model_selection"]:
        raise ModelArtifactError("Manifest missing 'secondary_model' in model_selection")

    return manifest


def load_final_models() -> dict[str, Any]:
    """Load all serialized final model artifacts.

    Returns
    -------
    dict[str, Any]
        Dictionary containing:
        - 'normalizer': Fitted OperatingRegimeNormalizer
        - 'primary_model': Fitted KMeans (k=2)
        - 'secondary_model': Fitted KMeans (k=3)
        - 'manifest': Manifest metadata dict

    Raises
    ------
    ModelArtifactError
        If any serialized artifact is missing.
    """
    manifest = load_model_manifest()
    models_dir = get_final_models_dir()

    transformer_file = models_dir / manifest["representation"]["transformer_artifact"]
    primary_file = models_dir / manifest["model_selection"]["primary_model"]["artifact_file"]
    secondary_file = models_dir / manifest["model_selection"]["secondary_model"]["artifact_file"]

    for name, path in [
        ("Normalizer", transformer_file),
        ("Primary model (k=2)", primary_file),
        ("Secondary model (k=3)", secondary_file),
    ]:
        if not path.exists():
            raise ModelArtifactError(
                f"{name} artifact not found at: {path}. "
                "The dashboard requires pre-trained serialized artifacts and will NEVER silently retrain."
            )

    try:
        normalizer: OperatingRegimeNormalizer = joblib.load(transformer_file)
        primary_model: KMeans = joblib.load(primary_file)
        secondary_model: KMeans = joblib.load(secondary_file)
    except Exception as e:
        raise ModelArtifactError(f"Failed to deserialize model artifacts: {e}")

    return {
        "normalizer": normalizer,
        "primary_model": primary_model,
        "secondary_model": secondary_model,
        "manifest": manifest,
    }
