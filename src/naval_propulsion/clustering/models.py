"""Clustering algorithm wrappers adhering to the BaseClusterer interface.

Provides standardized implementations for K-Means, Agglomerative Clustering,
DBSCAN, and Gaussian Mixture Models with deterministic seed controls.
"""

from __future__ import annotations

from typing import Any, Literal
import numpy as np
from sklearn.cluster import AgglomerativeClustering, DBSCAN, KMeans
from sklearn.mixture import GaussianMixture

from naval_propulsion.clustering.base import BaseClusterer, ClusterResult


class KMeansClusterer(BaseClusterer):
    """K-Means clustering wrapper with deterministic initialization."""

    def __init__(
        self,
        n_clusters: int = 4,
        random_state: int = 42,
        n_init: int = 10,
        max_iter: int = 300,
    ) -> None:
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.n_init = n_init
        self.max_iter = max_iter
        self.model_ = KMeans(
            n_clusters=self.n_clusters,
            random_state=self.random_state,
            n_init=self.n_init,
            max_iter=self.max_iter,
        )

    def fit_predict(self, X: np.ndarray) -> ClusterResult:
        labels = self.model_.fit_predict(X)
        return ClusterResult(
            labels=labels,
            n_clusters=self.n_clusters,
            algorithm_name="KMeans",
            hyperparameters={
                "n_clusters": self.n_clusters,
                "random_state": self.random_state,
                "n_init": self.n_init,
                "max_iter": self.max_iter,
            },
            cluster_centers=self.model_.cluster_centers_,
            additional_metadata={"inertia": float(self.model_.inertia_)},
        )


class AgglomerativeClustererWrapper(BaseClusterer):
    """Agglomerative Hierarchical Clustering wrapper."""

    def __init__(
        self,
        n_clusters: int = 4,
        linkage: Literal["ward", "complete", "average", "single"] = "ward",
        metric: str = "euclidean",
    ) -> None:
        self.n_clusters = n_clusters
        self.linkage = linkage
        self.metric = metric
        self.model_ = AgglomerativeClustering(
            n_clusters=self.n_clusters,
            linkage=self.linkage,
            metric=self.metric if self.linkage != "ward" else "euclidean",
        )

    def fit_predict(self, X: np.ndarray) -> ClusterResult:
        labels = self.model_.fit_predict(X)
        return ClusterResult(
            labels=labels,
            n_clusters=self.n_clusters,
            algorithm_name="AgglomerativeClustering",
            hyperparameters={
                "n_clusters": self.n_clusters,
                "linkage": self.linkage,
                "metric": self.metric,
            },
            cluster_centers=None,
            additional_metadata={"n_leaves": int(self.model_.n_leaves_)},
        )


class DBSCANClustererWrapper(BaseClusterer):
    """Density-Based Spatial Clustering of Applications with Noise (DBSCAN) wrapper."""

    def __init__(
        self,
        eps: float = 0.5,
        min_samples: int = 5,
        metric: str = "euclidean",
    ) -> None:
        self.eps = eps
        self.min_samples = min_samples
        self.metric = metric
        self.model_ = DBSCAN(
            eps=self.eps,
            min_samples=self.min_samples,
            metric=self.metric,
        )

    def fit_predict(self, X: np.ndarray) -> ClusterResult:
        labels = self.model_.fit_predict(X)
        unique_labels = set(labels)
        n_clusters = len(unique_labels - {-1})
        noise_count = int(np.sum(labels == -1))
        noise_ratio = float(noise_count / len(labels)) if len(labels) > 0 else 0.0

        return ClusterResult(
            labels=labels,
            n_clusters=n_clusters,
            algorithm_name="DBSCAN",
            hyperparameters={
                "eps": self.eps,
                "min_samples": self.min_samples,
                "metric": self.metric,
            },
            cluster_centers=None,
            additional_metadata={
                "noise_count": noise_count,
                "noise_ratio": noise_ratio,
            },
        )


class GMMClustererWrapper(BaseClusterer):
    """Gaussian Mixture Model (GMM) clustering wrapper."""

    def __init__(
        self,
        n_components: int = 4,
        covariance_type: Literal["full", "tied", "diag", "spherical"] = "full",
        random_state: int = 42,
        max_iter: int = 150,
    ) -> None:
        self.n_components = n_components
        self.covariance_type = covariance_type
        self.random_state = random_state
        self.max_iter = max_iter
        self.model_ = GaussianMixture(
            n_components=self.n_components,
            covariance_type=self.covariance_type,
            random_state=self.random_state,
            max_iter=self.max_iter,
        )

    def fit_predict(self, X: np.ndarray) -> ClusterResult:
        labels = self.model_.fit_predict(X)
        bic = float(self.model_.bic(X))
        aic = float(self.model_.aic(X))
        converged = bool(self.model_.converged_)

        return ClusterResult(
            labels=labels,
            n_clusters=self.n_components,
            algorithm_name="GaussianMixture",
            hyperparameters={
                "n_components": self.n_components,
                "covariance_type": self.covariance_type,
                "random_state": self.random_state,
                "max_iter": self.max_iter,
            },
            cluster_centers=self.model_.means_,
            additional_metadata={
                "bic": bic,
                "aic": aic,
                "converged": converged,
            },
        )
