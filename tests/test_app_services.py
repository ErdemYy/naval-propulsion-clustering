"""Unit tests for Streamlit application services and zero-leakage inference."""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from app.services.data_service import get_demo_observations, load_cached_dataset
from app.services.inference_service import (
    InputValidationError,
    assign_observation_profile,
    validate_observation_input,
)
from app.services.model_service import (
    ModelArtifactError,
    load_final_models,
    load_model_manifest,
)


def test_manifest_validation() -> None:
    """Verify that model_manifest.json is present, valid, and contains required sections."""
    manifest = load_model_manifest()
    assert "model_selection" in manifest
    assert "primary_model" in manifest["model_selection"]
    assert "secondary_model" in manifest["model_selection"]
    assert "representation" in manifest
    assert manifest["representation"]["representation_id"] == "R5_WITHIN_SPEED_NORMALIZED"


def test_model_loading() -> None:
    """Verify that all serialized artifacts deserialize into valid scikit-learn models."""
    bundle = load_final_models()
    assert "normalizer" in bundle
    assert "primary_model" in bundle
    assert "secondary_model" in bundle
    assert bundle["primary_model"].n_clusters == 2
    assert bundle["secondary_model"].n_clusters == 3


def test_missing_artifact_handling(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify that model_service raises a descriptive ModelArtifactError when an artifact is missing."""
    import app.services.model_service as ms

    # Point models dir to an empty temporary directory
    monkeypatch.setattr(ms, "get_final_models_dir", lambda: tmp_path)

    with pytest.raises(ModelArtifactError) as exc_info:
        ms.load_model_manifest()
    assert "Missing required model manifest" in str(exc_info.value)


def test_input_schema_validation_speed_required() -> None:
    """Verify that input validation requires the operating speed conditioning variable."""
    bad_input = {"GTT": 1000.0}
    with pytest.raises(InputValidationError) as exc_info:
        validate_observation_input(bad_input)
    assert "Missing required conditioning variable 'v'" in str(exc_info.value)


def test_input_schema_validation_unobserved_speed() -> None:
    """Verify that input validation rejects unobserved or out-of-range operating speeds."""
    bad_input = {"v": 99.0}
    with pytest.raises(InputValidationError) as exc_info:
        validate_observation_input(bad_input)
    assert "not recognized" in str(exc_info.value)


def test_input_schema_validation_missing_telemetry() -> None:
    """Verify that input validation detects missing telemetry features."""
    bad_input = {"v": 18.0, "GTT": 1000.0}
    with pytest.raises(InputValidationError) as exc_info:
        validate_observation_input(bad_input)
    assert "Missing required telemetry features" in str(exc_info.value)


def test_anti_leakage_rejection_of_kmc_kmt() -> None:
    """Verify that any attempt to supply kMc or kMt as inputs raises a critical validation error."""
    demos = get_demo_observations()
    leaked_input = demos["nominal"]["inputs"].copy()
    leaked_input["kMc"] = 0.98

    with pytest.raises(InputValidationError) as exc_info:
        validate_observation_input(leaked_input)
    assert "CRITICAL INVARIANT VIOLATION: kMc and kMt" in str(exc_info.value)

    leaked_input_2 = demos["nominal"]["inputs"].copy()
    leaked_input_2["kMt"] = 0.99
    with pytest.raises(InputValidationError) as exc_info:
        validate_observation_input(leaked_input_2)
    assert "CRITICAL INVARIANT VIOLATION: kMc and kMt" in str(exc_info.value)


def test_observation_profile_assignment_determinism() -> None:
    """Verify that observation inference produces deterministic, non-empty profile assignments."""
    demos = get_demo_observations()
    input_data = demos["nominal"]["inputs"]

    res_k2 = assign_observation_profile(input_data, model_choice="k2")
    assert res_k2["assigned_cluster"] in {0, 1}
    assert res_k2["centroid_distance"] >= 0.0
    assert len(res_k2["all_distances"]) == 2
    assert "closest_profile_name" in res_k2
    assert "profile_description" in res_k2

    res_k3 = assign_observation_profile(input_data, model_choice="k3")
    assert res_k3["assigned_cluster"] in {0, 1, 2}
    assert res_k3["centroid_distance"] >= 0.0
    assert len(res_k3["all_distances"]) == 3


def test_demo_observations_integrity() -> None:
    """Verify that demonstration presets are properly formatted and maintain zero-leakage."""
    demos = get_demo_observations()
    assert set(demos.keys()) == {"nominal", "compressor_decay", "turbine_decay"}

    for case_name, case_data in demos.items():
        assert "inputs" in case_data
        assert "v" in case_data["inputs"]
        assert "kMc" not in case_data["inputs"], f"Leaked kMc in demo {case_name} inputs!"
        assert "kMt" not in case_data["inputs"], f"Leaked kMt in demo {case_name} inputs!"
        assert "ground_truth_reference" in case_data
        assert "kMc" in case_data["ground_truth_reference"]
        assert "kMt" in case_data["ground_truth_reference"]
