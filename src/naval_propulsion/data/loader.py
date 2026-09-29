"""Data loading and structural integrity verification.

Enforces strict separation between unsupervised sensor features (X)
and degradation validation targets (y: kMc, kMt).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence
import pandas as pd

from naval_propulsion.data.ingestion import CANONICAL_COLUMNS, TARGET_COLUMNS
from naval_propulsion.utils.paths import get_processed_data_dir, get_raw_data_dir


@dataclass(frozen=True)
class DatasetContainer:
    """Container holding strictly partitioned features and post-hoc targets.

    Attributes
    ----------
    features : pd.DataFrame
        Multivariate sensor measurements to be used for unsupervised clustering.
    targets : pd.DataFrame
        Ground-truth degradation coefficients (kMc, kMt) reserved solely for
        post-hoc validation and statistical profiling.
    feature_names : tuple[str, ...]
        Tuple of feature column names.
    target_names : tuple[str, ...]
        Tuple of target column names.
    """

    features: pd.DataFrame
    targets: pd.DataFrame
    feature_names: tuple[str, ...]
    target_names: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate strict separation between features and targets."""
        overlap = set(self.features.columns).intersection(set(self.targets.columns))
        if overlap:
            raise ValueError(
                f"Data leakage detected! Columns present in both features and targets: {overlap}"
            )
        if len(self.features) != len(self.targets):
            raise ValueError(
                f"Row mismatch: features has {len(self.features)} rows, "
                f"targets has {len(self.targets)} rows."
            )


def load_naval_dataset(
    filepath: Path | str | None = None,
    target_columns: Sequence[str] = TARGET_COLUMNS,
) -> DatasetContainer:
    """Load dataset from path and return verified DatasetContainer.

    If filepath is not provided, defaults to processed CSV (data/processed/naval_propulsion.csv),
    or falls back to raw data (data/raw/data.txt).

    Parameters
    ----------
    filepath : Path or str, optional
        Path to the dataset file.
    target_columns : Sequence[str], default=("kMc", "kMt")
        Column names to be extracted as post-hoc validation targets.

    Returns
    -------
    DatasetContainer
        Container with verified separation of features and targets.
    """
    if filepath is None:
        processed_file = get_processed_data_dir() / "naval_propulsion.csv"
        raw_file = get_raw_data_dir() / "data.txt"
        if processed_file.exists():
            filepath = processed_file
        elif raw_file.exists():
            filepath = raw_file
        else:
            raise FileNotFoundError(
                f"Neither processed ({processed_file}) nor raw ({raw_file}) dataset exists. "
                "Please run data ingestion first."
            )
    else:
        filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"Dataset file not found at: {filepath}")

    # Determine file format by suffix
    if filepath.suffix == ".csv":
        df = pd.read_csv(filepath)
    else:
        # Space-separated raw file
        df = pd.read_csv(
            filepath,
            sep=r"\s+",
            header=None,
            names=list(CANONICAL_COLUMNS),
            dtype={col: "float64" for col in CANONICAL_COLUMNS},
            engine="c",
        )

    targets_set = set(target_columns)
    available_cols = set(df.columns)

    missing_targets = targets_set - available_cols
    if missing_targets:
        raise ValueError(f"Requested target columns not present in dataset: {missing_targets}")

    feature_cols = [c for c in df.columns if c not in targets_set]
    target_cols = [c for c in df.columns if c in targets_set]

    features_df = df[feature_cols].copy()
    targets_df = df[target_cols].copy()

    return DatasetContainer(
        features=features_df,
        targets=targets_df,
        feature_names=tuple(feature_cols),
        target_names=tuple(target_cols),
    )
