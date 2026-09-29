"""Data ingestion and validation module."""

from naval_propulsion.data.ingestion import (
    CANONICAL_COLUMNS,
    FEATURE_COLUMNS,
    OFFICIAL_UCI_ZIP_URL,
    TARGET_COLUMNS,
    UCI_DATASET_ID,
    UCI_DATASET_NAME,
    compute_sha256,
    ingest_uci_dataset,
)
from naval_propulsion.data.loader import DatasetContainer, load_naval_dataset
from naval_propulsion.data.quality import (
    ColumnQualityProfile,
    DataQualityReport,
    analyze_data_quality,
    save_data_quality_report,
)

__all__ = [
    "CANONICAL_COLUMNS",
    "ColumnQualityProfile",
    "DataQualityReport",
    "DatasetContainer",
    "FEATURE_COLUMNS",
    "OFFICIAL_UCI_ZIP_URL",
    "TARGET_COLUMNS",
    "UCI_DATASET_ID",
    "UCI_DATASET_NAME",
    "analyze_data_quality",
    "compute_sha256",
    "ingest_uci_dataset",
    "load_naval_dataset",
    "save_data_quality_report",
]
