"""Feature engineering, selection, and representation registry module."""

from naval_propulsion.features.correlation import (
    REPRESENTATION_A_FEATURES,
    REPRESENTATION_B_FEATURES,
    compute_correlations,
    generate_correlation_figures,
)
from naval_propulsion.features.pca_analysis import (
    analyze_pca,
    generate_pca_figures,
    save_pca_report,
)
from naval_propulsion.features.registry import (
    CANDIDATE_REPRESENTATIONS,
    FeatureRepresentationSpec,
    build_representation_data,
    save_representation_registry,
)
from naval_propulsion.features.screening import (
    save_feature_screening_table,
    screen_features,
)
from naval_propulsion.features.selection import BaseFeatureSelector

__all__ = [
    "BaseFeatureSelector",
    "CANDIDATE_REPRESENTATIONS",
    "FeatureRepresentationSpec",
    "REPRESENTATION_A_FEATURES",
    "REPRESENTATION_B_FEATURES",
    "analyze_pca",
    "build_representation_data",
    "compute_correlations",
    "generate_correlation_figures",
    "generate_pca_figures",
    "save_feature_screening_table",
    "save_pca_report",
    "save_representation_registry",
    "screen_features",
]
