"""Deterministic seed management for reproducible scientific computation."""

from __future__ import annotations

import os
import random
import numpy as np


def set_seed(seed: int = 42) -> int:
    """Set random seeds across Python random, NumPy, and environment variables.

    Parameters
    ----------
    seed : int, default=42
        Integer seed value to ensure deterministic executions.

    Returns
    -------
    int
        The seed value that was applied.
    """
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    return seed
