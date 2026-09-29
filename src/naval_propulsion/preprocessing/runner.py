"""Centralized Phase 2 diagnostic pipeline runner.

Executes all Phase 2 preprocessing diagnostics, saves machine-readable
experiment outputs, generates publication figures, and records reproducible metadata.
"""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
from typing import Any
import pandas as pd
import sklearn

from naval_propulsion.data.loader import load_naval_dataset
from naval_propulsion.features.correlation import (
    REPRESENTATION_A_FEATURES,
    generate_correlation_figures,
)
from naval_propulsion.features.pca_analysis import (
    analyze_pca,
    generate_pca_figures,
    save_pca_report,
)
from naval_propulsion.features.registry import (
    save_representation_registry,
)
from naval_propulsion.features.screening import (
    save_feature_screening_table,
    screen_features,
)
from naval_propulsion.preprocessing.outliers import (
    analyze_outliers,
    save_outlier_report,
)
from naval_propulsion.preprocessing.regime import (
    analyze_operating_regimes,
    generate_regime_profile_figures,
    save_regime_report,
)
from naval_propulsion.preprocessing.scalers import (
    compare_scalers,
    generate_scaler_comparison_figure,
    save_scaler_comparison_results,
)
from naval_propulsion.utils.paths import get_experiments_dir, get_processed_data_dir


def run_phase2_diagnostics() -> dict[str, Any]:
    """Execute complete Phase 2 preprocessing and feature engineering diagnostics."""
    output_dir = get_experiments_dir() / "outputs" / "phase2"
    output_dir.mkdir(parents=True, exist_ok=True)

    container = load_naval_dataset()
    full_df = pd.concat([container.features, container.targets], axis=1)

    # 1. Feature Screening
    screening_df = screen_features(full_df)
    save_feature_screening_table(screening_df)

    # 2. Correlation Analysis
    corr_figs = generate_correlation_figures(full_df, features=REPRESENTATION_A_FEATURES)

    # 3. Scaler Comparison
    scaler_results = compare_scalers(full_df, features=REPRESENTATION_A_FEATURES)
    save_scaler_comparison_results(scaler_results)
    generate_scaler_comparison_figure(full_df, features=["GTT", "GTn", "GGn", "T48", "P2", "mf"])

    # 4. Outlier Analysis
    outlier_results = analyze_outliers(full_df, features=REPRESENTATION_A_FEATURES)
    save_outlier_report(outlier_results)

    # 5. Operating Regime Analysis
    regime_results = analyze_operating_regimes(full_df, regime_col="v")
    save_regime_report(regime_results)
    generate_regime_profile_figures(full_df)

    # 6. PCA Analysis
    pca_results = analyze_pca(full_df, features=REPRESENTATION_A_FEATURES)
    save_pca_report(pca_results)
    generate_pca_figures(full_df, features=REPRESENTATION_A_FEATURES)

    # 7. Representation Registry
    save_representation_registry()

    # 8. Provenance & Reproducibility Metadata
    processed_csv = get_processed_data_dir() / "naval_propulsion.csv"
    with open(processed_csv, "rb") as f:
        csv_sha256 = hashlib.sha256(f.read()).hexdigest()

    metadata = {
        "phase": "Phase 2 — Preprocessing, Feature Engineering & Operating-Condition Analysis",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "input_dataset": processed_csv.name,
        "input_sha256": csv_sha256,
        "row_count": len(full_df),
        "quarantined_targets": list(container.target_names),
        "clean_telemetry_features": list(REPRESENTATION_A_FEATURES),
        "library_versions": {
            "python": sys.version,
            "pandas": pd.__version__,
            "numpy": pd.np.__name__ if hasattr(pd, "np") else "numpy",
            "scikit-learn": sklearn.__version__,
        },
        "artifacts_generated": {
            "feature_screening": "experiments/outputs/phase2/feature_screening.csv",
            "scaler_comparison_json": "experiments/outputs/phase2/scaler_comparison.json",
            "outlier_report_json": "experiments/outputs/phase2/outlier_report.json",
            "operating_regime_report_json": "experiments/outputs/phase2/operating_regime_report.json",
            "pca_analysis_json": "experiments/outputs/phase2/pca_analysis.json",
            "representation_registry_json": "experiments/outputs/phase2/representation_registry.json",
            "pearson_correlation_png": "reports/figures/phase2/pearson_correlation.png",
            "spearman_correlation_png": "reports/figures/phase2/spearman_correlation.png",
            "scaler_comparison_png": "reports/figures/phase2/scaler_comparison.png",
            "operating_speed_profiles_png": "reports/figures/phase2/operating_speed_profiles.png",
            "pca_explained_variance_png": "reports/figures/phase2/pca_explained_variance.png",
            "pca_loadings_png": "reports/figures/phase2/pca_loadings.png",
        },
    }

    metadata_path = output_dir / "preprocessing_metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    return metadata


if __name__ == "__main__":
    meta = run_phase2_diagnostics()
    print("Phase 2 diagnostics executed successfully!")
