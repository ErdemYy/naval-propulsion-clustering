"""Abstract base classes and contracts for data preprocessing."""

from __future__ import annotations

from abc import ABC, abstractmethod
import numpy as np
import pandas as pd


class BasePreprocessor(ABC):
    """Abstract interface for all preprocessing transformations.

    Ensures consistent fit/transform contracts across raw sensor features.
    """

    @abstractmethod
    def fit(self, X: pd.DataFrame | np.ndarray) -> BasePreprocessor:
        """Fit preprocessor parameters on sensor feature data."""
        pass

    @abstractmethod
    def transform(self, X: pd.DataFrame | np.ndarray) -> np.ndarray:
        """Transform sensor feature data into sanitized/scaled array."""
        pass

    def fit_transform(self, X: pd.DataFrame | np.ndarray) -> np.ndarray:
        """Fit to sensor features, then transform."""
        return self.fit(X).transform(X)
