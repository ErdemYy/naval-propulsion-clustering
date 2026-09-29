"""Unit tests for Phase 2 preprocessing, feature screening, scalers, and within-regime normalizer."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from naval_propulsion.data.loader import load_naval_dataset
from naval_propulsion.features.correlation import (
    REPRESENTATION_A_FEATURES,
    REPRESENTATION_B_FEATURES,
    compute_correlations,
)
from naval_propulsion.features.registry import (
    CANDIDATE_REPRESENTATIONS,
    build_representation_data,
)
from naval_propulsion.features.screening import screen_features
from naval_propulsion.preprocessing.outliers import analyze_outliers
from naval_propulsion.preprocessing.regime import analyze_operating_regimes
from naval_propulsion.preprocessing.transformers import (
    ColumnFilterTransformer,
    OperatingRegimeNormalizer,
    TelemetryScaler,
)


def test_zero_variance_feature_detection() -> None:
    """1: Verify zero-variance columns (T1, P1) are flagged for mandatory removal."""
    container = load_naval_dataset()
    full_df = pd.concat([container.features, container.targets], axis=1)
    screening = screen_features(full_df)

    t1_action = screening.loc[screening["feature"] == "T1", "proposed_action"].values[0]
    p1_action = screening.loc[screening["feature"] == "P1", "proposed_action"].values[0]

    assert t1_action == "mandatory removal"
    assert p1_action == "mandatory removal"


def test_duplicate_feature_detection() -> None:
    """2: Verify exact duplicate Tp is identified and flagged for mandatory removal."""
    container = load_naval_dataset()
    full_df = pd.concat([container.features, container.targets], axis=1)
    screening = screen_features(full_df)

    tp_action = screening.loc[screening["feature"] == "Tp", "proposed_action"].values[0]
    assert tp_action == "mandatory removal"
    assert "Ts/Tp" in screening.loc[screening["feature"] == "Tp", "duplicate_group"].values[0]


def test_scaler_reproducibility() -> None:
    """3: Verify scalers produce identical outputs on repeated fits."""
    container = load_naval_dataset()
    X = container.features[list(REPRESENTATION_B_FEATURES)]

    scaler1 = TelemetryScaler(scaler_type="standard")
    scaler2 = TelemetryScaler(scaler_type="standard")

    out1 = scaler1.fit_transform(X)
    out2 = scaler2.fit_transform(X)

    pd.testing.assert_frame_equal(out1, out2)


def test_transformation_shape_consistency() -> None:
    """4: Verify transformation shape consistency across all candidate representations."""
    container = load_naval_dataset()
    full_df = pd.concat([container.features, container.targets], axis=1)

    for rep_id, spec in CANDIDATE_REPRESENTATIONS.items():
        transformed = build_representation_data(full_df, spec)
        assert len(transformed) == len(full_df)
        assert len(transformed.columns) == len(spec.feature_names)


def test_no_nan_or_infinite_values() -> None:
    """5 & 6: Verify no NaNs or infinite values are introduced by preprocessing."""
    container = load_naval_dataset()
    full_df = pd.concat([container.features, container.targets], axis=1)

    for rep_id, spec in CANDIDATE_REPRESENTATIONS.items():
        transformed = build_representation_data(full_df, spec)
        assert not transformed.isna().any().any(), f"{rep_id} produced NaN values"
        assert np.isfinite(transformed.to_numpy()).all(), f"{rep_id} produced non-finite values"


def test_preservation_of_metadata() -> None:
    """7: Verify column names and original DataFrame indices are preserved."""
    container = load_naval_dataset()
    full_df = pd.concat([container.features, container.targets], axis=1)

    normalizer = OperatingRegimeNormalizer(regime_column="v")
    cols = ["v", "GTT", "GTn", "T48"]
    transformed = normalizer.fit_transform(full_df[cols])

    assert list(transformed.columns) == ["GTT", "GTn", "T48"]
    pd.testing.assert_index_equal(transformed.index, full_df.index)


def test_within_speed_normalization_determinism() -> None:
    """8: Verify within-speed normalization produces mean ~0 and std ~1 within each speed."""
    container = load_naval_dataset()
    full_df = pd.concat([container.features, container.targets], axis=1)

    normalizer = OperatingRegimeNormalizer(regime_column="v")
    cols = ["v", "GTT", "GTn", "T48", "P2"]
    transformed = normalizer.fit_transform(full_df[cols])

    # For each speed, compute transformed mean and std
    for s in full_df["v"].unique():
        mask = full_df["v"] == s
        sub = transformed[mask]
        means = sub.mean()
        stds = sub.std(ddof=1)
        np.testing.assert_allclose(means.to_numpy(), 0.0, atol=1e-7)
        np.testing.assert_allclose(stds.to_numpy(), 1.0, atol=1e-7)


def test_kmc_kmt_leakage_protection() -> None:
    """9: Verify degradation targets kMc and kMt never leak into candidate feature sets."""
    for rep_id, spec in CANDIDATE_REPRESENTATIONS.items():
        assert "kMc" not in spec.feature_names
        assert "kMt" not in spec.feature_names


def test_determinism_same_input_same_output() -> None:
    """10: Same input + same config = exact bitwise identical output."""
    container = load_naval_dataset()
    full_df = pd.concat([container.features, container.targets], axis=1)

    spec = CANDIDATE_REPRESENTATIONS["R5_WITHIN_SPEED_NORMALIZED"]
    res1 = build_representation_data(full_df, spec)
    res2 = build_representation_data(full_df, spec)

    pd.testing.assert_frame_equal(res1, res2)
