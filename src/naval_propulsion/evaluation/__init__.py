"""Evaluation module for unsupervised metrics and post-hoc degradation validation."""

from naval_propulsion.evaluation.metrics import (
    DegradationCorrelationReport,
    IntrinsicMetrics,
    compute_intrinsic_metrics,
)

__all__ = [
    "DegradationCorrelationReport",
    "IntrinsicMetrics",
    "compute_intrinsic_metrics",
]
