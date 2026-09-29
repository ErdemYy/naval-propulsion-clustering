"""Clustering abstractions and standardized result containers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any
import numpy as np


@dataclass(frozen=True)
class ClusterResult:
    """Standardized output container for clustering algorithm executions.

    Attributes
    ----------
    labels : np.ndarray
        1D array of assigned cluster labels (integers, with -1 denoting noise if applicable).
    n_clusters : int
        Number of clusters detected (excluding noise).
    algorithm_name : str
        Name of the clustering algorithm.
    hyperparameters : dict[str, Any]
        Dictionary of hyperparameters passed to the model.
    cluster_centers : np.ndarray | None
        Centroids in feature space if supported by algorithm, otherwise None.
    additional_metadata : dict[str, Any]
        Additional algorithm-specific diagnostics (e.g. inertia, probabilities).
    """

    labels: np.ndarray
    n_clusters: int
    algorithm_name: str
    hyperparameters: dict[str, Any] = field(default_factory=dict)
    cluster_centers: np.ndarray | None = None
    additional_metadata: dict[str, Any] = field(default_factory=dict)


class BaseClusterer(ABC):
    """Abstract base class for all clustering implementations.

    Follows scikit-learn conventions while returning structured ClusterResult.
    """

    @abstractmethod
    def fit_predict(self, X: np.ndarray) -> ClusterResult:
        """Fit clustering estimator and return structured clustering results."""
        pass
