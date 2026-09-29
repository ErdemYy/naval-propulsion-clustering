"""Unit tests for DatasetContainer anti-leakage and structural integrity."""

from __future__ import annotations

import pandas as pd
import pytest
from naval_propulsion.data.loader import DatasetContainer


def test_dataset_container_valid(
    sample_feature_data: pd.DataFrame,
    sample_target_data: pd.DataFrame,
) -> None:
    """Test valid construction of DatasetContainer."""
    container = DatasetContainer(
        features=sample_feature_data,
        targets=sample_target_data,
        feature_names=tuple(sample_feature_data.columns),
        target_names=tuple(sample_target_data.columns),
    )
    assert len(container.features) == 50
    assert len(container.targets) == 50
    assert "kMc" in container.target_names
    assert "sensor_1" in container.feature_names


def test_dataset_container_rejects_leakage(
    sample_feature_data: pd.DataFrame,
    sample_target_data: pd.DataFrame,
) -> None:
    """Verify that an exception is raised if target columns leak into features."""
    leaked_features = sample_feature_data.copy()
    leaked_features["kMc"] = sample_target_data["kMc"]

    with pytest.raises(ValueError, match="Data leakage detected"):
        DatasetContainer(
            features=leaked_features,
            targets=sample_target_data,
            feature_names=tuple(leaked_features.columns),
            target_names=tuple(sample_target_data.columns),
        )


def test_dataset_container_rejects_length_mismatch(
    sample_feature_data: pd.DataFrame,
    sample_target_data: pd.DataFrame,
) -> None:
    """Verify that an exception is raised if feature and target row counts differ."""
    truncated_targets = sample_target_data.iloc[:20]

    with pytest.raises(ValueError, match="Row mismatch"):
        DatasetContainer(
            features=sample_feature_data,
            targets=truncated_targets,
            feature_names=tuple(sample_feature_data.columns),
            target_names=tuple(truncated_targets.columns),
        )
