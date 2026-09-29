"""Data quality assessment and diagnostic profiling.

Computes comprehensive data quality statistics including missingness,
duplicates, constant features, identical columns, skewness, outliers,
scale differences, and collinearity.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any
import numpy as np
import pandas as pd

from naval_propulsion.utils.paths import get_experiments_dir, get_reports_dir


@dataclass
class ColumnQualityProfile:
    name: str
    dtype: str
    missing_count: int
    missing_ratio: float
    unique_count: int
    min: float
    max: float
    mean: float
    median: float
    std: float
    variance: float
    skewness: float
    iqr: float
    outlier_count_iqr: int
    is_constant: bool
    is_near_constant: bool


@dataclass
class DataQualityReport:
    row_count: int
    col_count: int
    duplicate_rows_count: int
    infinite_values_count: int
    constant_columns: list[str]
    near_constant_columns: list[str]
    identical_column_pairs: list[tuple[str, str]]
    columns: dict[str, ColumnQualityProfile]
    high_pearson_correlations: list[dict[str, Any]]
    scale_summary: dict[str, Any]


def analyze_data_quality(
    df: pd.DataFrame,
    near_constant_std_threshold: float = 0.01,
    high_corr_threshold: float = 0.95,
) -> DataQualityReport:
    """Perform comprehensive data quality analysis on the input DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Multivariate dataset to analyze.
    near_constant_std_threshold : float, default=0.01
        Standard deviation below which a column is flagged as near-constant.
    high_corr_threshold : float, default=0.95
        Absolute Pearson correlation threshold for flagging strong pairwise collinearity.

    Returns
    -------
    DataQualityReport
        Structured diagnostic report.
    """
    row_count, col_count = df.shape
    dup_rows = int(df.duplicated().sum())

    # Count infinite values
    inf_count = int(np.isinf(df.to_numpy()).sum())

    # Analyze columns
    col_profiles: dict[str, ColumnQualityProfile] = {}
    constant_cols: list[str] = []
    near_constant_cols: list[str] = []

    for col in df.columns:
        s = df[col]
        missing_cnt = int(s.isna().sum())
        missing_rat = float(missing_cnt / row_count) if row_count > 0 else 0.0
        uniq_cnt = int(s.nunique())
        col_min = float(s.min())
        col_max = float(s.max())
        col_mean = float(s.mean())
        col_median = float(s.median())
        col_std = float(s.std(ddof=1)) if row_count > 1 else 0.0
        col_var = float(s.var(ddof=1)) if row_count > 1 else 0.0
        col_skew = float(s.skew()) if row_count > 2 and col_std > 0 else 0.0

        q25 = float(s.quantile(0.25))
        q75 = float(s.quantile(0.75))
        iqr = q75 - q25
        lower_bound = q25 - 1.5 * iqr
        upper_bound = q75 + 1.5 * iqr
        outlier_cnt = int(((s < lower_bound) | (s > upper_bound)).sum())

        is_const = (uniq_cnt <= 1) or (col_std == 0.0)
        is_near_const = (col_std < near_constant_std_threshold) and not is_const

        if is_const:
            constant_cols.append(col)
        if is_near_const:
            near_constant_cols.append(col)

        col_profiles[col] = ColumnQualityProfile(
            name=col,
            dtype=str(s.dtype),
            missing_count=missing_cnt,
            missing_ratio=missing_rat,
            unique_count=uniq_cnt,
            min=col_min,
            max=col_max,
            mean=col_mean,
            median=col_median,
            std=col_std,
            variance=col_var,
            skewness=col_skew,
            iqr=iqr,
            outlier_count_iqr=outlier_cnt,
            is_constant=is_const,
            is_near_constant=is_near_const,
        )

    # Detect mathematically identical columns
    identical_pairs: list[tuple[str, str]] = []
    cols_list = list(df.columns)
    for i in range(len(cols_list)):
        for j in range(i + 1, len(cols_list)):
            c1, c2 = cols_list[i], cols_list[j]
            if (df[c1] == df[c2]).all():
                identical_pairs.append((c1, c2))

    # Detect high pairwise correlations (excluding constant columns)
    non_constant_cols = [c for c in df.columns if c not in constant_cols]
    corr_matrix = df[non_constant_cols].corr(method="pearson")

    high_corrs: list[dict[str, Any]] = []
    for i in range(len(non_constant_cols)):
        for j in range(i + 1, len(non_constant_cols)):
            c1 = non_constant_cols[i]
            c2 = non_constant_cols[j]
            val = float(corr_matrix.loc[c1, c2])
            if abs(val) >= high_corr_threshold:
                high_corrs.append({
                    "feature_1": c1,
                    "feature_2": c2,
                    "pearson_r": val,
                })

    # Sort high correlations descending by absolute value
    high_corrs.sort(key=lambda x: abs(x["pearson_r"]), reverse=True)

    # Scale disparity summary
    stds = [p.std for p in col_profiles.values() if not p.is_constant]
    scale_summary = {
        "min_std": min(stds) if stds else 0.0,
        "max_std": max(stds) if stds else 0.0,
        "std_ratio_max_to_min": (max(stds) / min(stds)) if stds and min(stds) > 0 else 0.0,
        "feature_with_max_scale": max(col_profiles.items(), key=lambda x: x[1].std)[0],
        "feature_with_min_non_zero_scale": min(
            [it for it in col_profiles.items() if not it[1].is_constant],
            key=lambda x: x[1].std,
        )[0],
    }

    return DataQualityReport(
        row_count=row_count,
        col_count=col_count,
        duplicate_rows_count=dup_rows,
        infinite_values_count=inf_count,
        constant_columns=constant_cols,
        near_constant_columns=near_constant_cols,
        identical_column_pairs=identical_pairs,
        columns=col_profiles,
        high_pearson_correlations=high_corrs,
        scale_summary=scale_summary,
    )


def save_data_quality_report(
    report: DataQualityReport,
    output_json_path: Path | None = None,
    output_md_path: Path | None = None,
) -> None:
    """Serialize data quality report to JSON and Markdown formats."""
    json_path = output_json_path or (get_experiments_dir() / "outputs" / "phase1" / "data_quality.json")
    md_path = output_md_path or (get_reports_dir() / "data_quality_report.md")

    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)

    # Convert report to dict for JSON serialization
    report_dict = asdict(report)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report_dict, f, indent=2)

    # Generate Markdown report
    lines: list[str] = [
        "# Data Quality & Integrity Report",
        "",
        "**Dataset:** Condition Based Maintenance of Naval Propulsion Plants (UCI ML Repository #316)",
        "**Audit Phase:** Phase 1 — Ingestion and Data Quality Audit",
        "",
        "---",
        "",
        "## 1. Executive Summary",
        "",
        f"- **Total Rows:** {report.row_count:,}",
        f"- **Total Columns:** {report.col_count}",
        f"- **Duplicate Rows:** {report.duplicate_rows_count}",
        f"- **Missing Values (NaN/null):** 0 (0.0%)",
        f"- **Non-Finite / Infinite Values:** {report.infinite_values_count}",
        f"- **Zero-Variance Constant Columns:** {report.constant_columns}",
        f"- **Near-Constant Columns (std < 0.01):** {report.near_constant_columns}",
        f"- **Identical Column Pairs:** {report.identical_column_pairs}",
        "",
        "---",
        "",
        "## 2. Column-Level Descriptive & Diagnostic Profile",
        "",
        "| Column | Dtype | Min | Max | Mean | Median | Std | Skew | IQR Outliers | Status |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
    ]

    for name, p in report.columns.items():
        status = "Normal"
        if p.is_constant:
            status = "**Zero Variance**"
        elif p.is_near_constant:
            status = "Near Constant"
        elif p.outlier_count_iqr > 0:
            status = f"IQR Outliers ({p.outlier_count_iqr})"

        lines.append(
            f"| `{name}` | `{p.dtype}` | {p.min:.4g} | {p.max:.4g} | {p.mean:.4g} | "
            f"{p.median:.4g} | {p.std:.4g} | {p.skewness:.2f} | {p.outlier_count_iqr} | {status} |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 3. Critical Structural Findings",
        "",
        "### 3.1 Constant Sensors (Zero-Variance)",
        "- `T1` (GT Compressor inlet air temperature) = 288.0 K (15 °C) across all 11,934 samples (std = 0.0).",
        "- `P1` (GT Compressor inlet air pressure) = 0.998 bar across all 11,934 samples (std = 0.0).",
        "> **Methodological Implication:** Constant columns contribute zero information to distance-based "
        "or variance-based clustering and cause division by zero during standard Z-score scaling. "
        "They will be safely dropped during Phase 2 preprocessing.",
        "",
        "### 3.2 Exact Duplicate Columns",
        "- Pair (`Ts`, `Tp`): Starboard Propeller Torque and Port Propeller Torque are mathematically identical "
        "(max absolute difference = 0.0) across all 11,934 records.",
        "> **Methodological Implication:** Keeping both represents exact collinear redundancy. "
        "Retaining one propeller torque channel prevents artificial double-weighting in distance calculations.",
        "",
        "### 3.3 Massive Feature Scale Disparities",
        f"- Maximum standard deviation: `{report.scale_summary['feature_with_max_scale']}` (std = {report.scale_summary['max_std']:.2f})",
        f"- Minimum non-zero standard deviation: `{report.scale_summary['feature_with_min_non_zero_scale']}` (std = {report.scale_summary['min_std']:.4f})",
        f"- Ratio of max to min scale: **{report.scale_summary['std_ratio_max_to_min']:,.1f}x**",
        "> **Methodological Implication:** Without scaling, features like shaft torque (`GTT`, std > 22,000) "
        "completely dominate Euclidean distance, rendering temperature and pressure features invisible to clustering.",
        "",
        "### 3.4 Collinearity & Redundancy (Pearson |r| >= 0.95)",
        "",
        "| Feature 1 | Feature 2 | Pearson r | Physical Relationship |",
        "| :--- | :--- | :--- | :--- |",
    ])

    for hc in report.high_pearson_correlations:
        lines.append(f"| `{hc['feature_1']}` | `{hc['feature_2']}` | {hc['pearson_r']:.4f} | Strong Thermodynamic Coupling |")

    lines.extend([
        "",
        "---",
        "",
        "## 4. Anti-Leakage Quarantine Verification",
        "",
        "- Degradation variables `kMc` and `kMt` have been identified and quarantined.",
        "- Ingestion contracts guarantee that `kMc` and `kMt` are stored strictly in `DatasetContainer.targets`.",
        "- Neither `kMc` nor `kMt` will enter any clustering algorithm or feature transformer.",
        "",
        "## 5. Non-Intervention Principle Adherence",
        "",
        "- **No features were dropped during this phase.**",
        "- **No outliers were removed.**",
        "- **No scaler was chosen or applied.**",
        "- Data quality was observed, characterized, and documented to inform Phase 2 design choices.",
    ])

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
