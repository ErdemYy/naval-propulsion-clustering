"""Pytest configuration and shared test fixtures."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def sample_feature_data() -> pd.DataFrame:
    """Fixture providing dummy multivariate feature data."""
    rng = np.random.default_rng(42)
    data = rng.standard_normal((50, 4))
    return pd.DataFrame(data, columns=["sensor_1", "sensor_2", "sensor_3", "sensor_4"])


@pytest.fixture
def sample_target_data() -> pd.DataFrame:
    """Fixture providing dummy degradation target data."""
    rng = np.random.default_rng(42)
    kmc = rng.uniform(0.95, 1.0, size=50)
    kmt = rng.uniform(0.975, 1.0, size=50)
    return pd.DataFrame({"kMc": kmc, "kMt": kmt})
