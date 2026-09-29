"""Unit tests for utility modules (seed, paths)."""

from __future__ import annotations

import numpy as np
from naval_propulsion.utils.paths import get_data_dir, get_project_root
from naval_propulsion.utils.seed import set_seed


def test_project_root_exists() -> None:
    """Verify that project root directory is correctly resolved and exists."""
    root = get_project_root()
    assert root.exists()
    assert (root / "pyproject.toml").exists()
    assert get_data_dir().exists()


def test_seed_determinism() -> None:
    """Verify that setting the seed produces reproducible pseudo-random numbers."""
    set_seed(1234)
    val_1 = np.random.uniform(0, 1, 5)

    set_seed(1234)
    val_2 = np.random.uniform(0, 1, 5)

    np.testing.assert_allclose(val_1, val_2)
