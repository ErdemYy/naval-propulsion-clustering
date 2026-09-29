"""Abstract contracts for feature selection and dimensionality reduction."""

from __future__ import annotations

from abc import ABC, abstractmethod
import numpy as np
import pandas as pd


class BaseFeatureSelector(ABC):
    """Abstract base class for feature selection or dimensionality transformation."""

    @abstractmethod
    def fit(self, X: pd.DataFrame | np.ndarray) -> BaseFeatureSelector:
        """Fit selector or transformation mapping on feature data."""
        pass

    @abstractmethod
    def transform(self, X: pd.DataFrame | np.ndarray) -> np.ndarray:
        """Transform feature matrix into selected or reduced representation."""
        pass

    def fit_transform(self, X: pd.DataFrame | np.ndarray) -> np.ndarray:
        """Fit to features, then transform."""
        return self.fit(X).transform(X)

    @property
    @abstractmethod
    def selected_feature_names(self) -> tuple[str, ...]:
        """Return names or indices of retained/projected features."""
        pass
