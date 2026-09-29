"""Authoritative dataset ingestion and provenance pipeline.

Downloads and verifies the UCI Condition Based Maintenance of Naval Propulsion Plants
dataset from official archives, creates cryptographic provenance manifests, and
enforces schema contracts.
"""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import io
from pathlib import Path
import json
from typing import Any
import requests
import zipfile
import pandas as pd

from naval_propulsion.utils.paths import get_processed_data_dir, get_raw_data_dir


OFFICIAL_UCI_ZIP_URL = (
    "https://archive.ics.uci.edu/static/public/316/"
    "condition+based+maintenance+of+naval+propulsion+plants.zip"
)
UCI_DATASET_ID = 316
UCI_DATASET_NAME = "Condition Based Maintenance of Naval Propulsion Plants"

# Authoritative column names as established in Features.txt and README.txt
CANONICAL_COLUMNS: tuple[str, ...] = (
    "lp",    # 1 - Lever position [ ]
    "v",     # 2 - Ship speed [knots]
    "GTT",   # 3 - Gas Turbine shaft torque [kN m]
    "GTn",   # 4 - Gas Turbine rate of revolutions [rpm]
    "GGn",   # 5 - Gas Generator rate of revolutions [rpm]
    "Ts",    # 6 - Starboard Propeller Torque [kN]
    "Tp",    # 7 - Port Propeller Torque [kN]
    "T48",   # 8 - HP Turbine exit temperature [C]
    "T1",    # 9 - GT Compressor inlet air temperature [C]
    "T2",    # 10 - GT Compressor outlet air temperature [C]
    "P48",   # 11 - HP Turbine exit pressure [bar]
    "P1",    # 12 - GT Compressor inlet air pressure [bar]
    "P2",    # 13 - GT Compressor outlet air pressure [bar]
    "Pexh",  # 14 - Gas Turbine exhaust gas pressure [bar]
    "TIC",   # 15 - Turbine Injecton Control [%]
    "mf",    # 16 - Fuel flow [kg/s]
    "kMc",   # 17 - GT Compressor decay state coefficient
    "kMt",   # 18 - GT Turbine decay state coefficient
)

TARGET_COLUMNS: tuple[str, ...] = ("kMc", "kMt")
FEATURE_COLUMNS: tuple[str, ...] = CANONICAL_COLUMNS[:16]


def compute_sha256(data: bytes) -> str:
    """Compute the SHA-256 hexadecimal digest for raw byte sequences."""
    return hashlib.sha256(data).hexdigest()


def ingest_uci_dataset(
    raw_dir: Path | None = None,
    processed_dir: Path | None = None,
    force_download: bool = False,
) -> dict[str, Any]:
    """Download, verify, and store the official UCI Naval Propulsion Plants dataset.

    Parameters
    ----------
    raw_dir : Path, optional
        Target directory for pristine raw artifacts. Defaults to data/raw.
    processed_dir : Path, optional
        Target directory for processed clean dataset copy. Defaults to data/processed.
    force_download : bool, default=False
        If True, re-downloads even if files already exist on disk.

    Returns
    -------
    dict[str, Any]
        Ingestion and provenance metadata summary.
    """
    raw_path = raw_dir or get_raw_data_dir()
    processed_path = processed_dir or get_processed_data_dir()

    raw_path.mkdir(parents=True, exist_ok=True)
    processed_path.mkdir(parents=True, exist_ok=True)

    zip_file_path = raw_path / "condition_based_maintenance_of_naval_propulsion_plants.zip"
    data_txt_path = raw_path / "data.txt"
    features_txt_path = raw_path / "Features.txt"
    readme_txt_path = raw_path / "README.txt"
    manifest_path = raw_path / "manifest.json"
    processed_csv_path = processed_path / "naval_propulsion.csv"

    # Step 1: Download or load existing raw archive
    if not zip_file_path.exists() or force_download:
        try:
            response = requests.get(OFFICIAL_UCI_ZIP_URL, timeout=30)
            response.raise_for_status()
            zip_bytes = response.content
            with open(zip_file_path, "wb") as f:
                f.write(zip_bytes)
            retrieval_timestamp = datetime.now(timezone.utc).isoformat()
        except Exception as exc:
            raise RuntimeError(
                f"Failed to retrieve authoritative UCI dataset from {OFFICIAL_UCI_ZIP_URL}: {exc}"
            ) from exc
    else:
        with open(zip_file_path, "rb") as f:
            zip_bytes = f.read()
        retrieval_timestamp = datetime.now(timezone.utc).isoformat()

    zip_sha256 = compute_sha256(zip_bytes)

    # Step 2: Extract untouched raw files
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        # Extract data.txt
        data_raw_bytes = zf.read("UCI CBM Dataset/data.txt")
        with open(data_txt_path, "wb") as f:
            f.write(data_raw_bytes)

        # Extract Features.txt
        features_raw_bytes = zf.read("UCI CBM Dataset/Features.txt")
        with open(features_txt_path, "wb") as f:
            f.write(features_raw_bytes)

        # Extract README.txt
        readme_raw_bytes = zf.read("UCI CBM Dataset/README.txt")
        with open(readme_txt_path, "wb") as f:
            f.write(readme_raw_bytes)

    data_sha256 = compute_sha256(data_raw_bytes)

    # Step 3: Parse and validate schema strictly (no silent coercion)
    # The file has space-delimited floating point values with no headers
    df = pd.read_csv(
        data_txt_path,
        sep=r"\s+",
        header=None,
        names=list(CANONICAL_COLUMNS),
        dtype={col: "float64" for col in CANONICAL_COLUMNS},
        engine="c",
    )

    row_count, col_count = df.shape

    if col_count != len(CANONICAL_COLUMNS):
        raise ValueError(
            f"Schema violation: expected {len(CANONICAL_COLUMNS)} columns, got {col_count}"
        )
    if row_count == 0:
        raise ValueError("Schema violation: dataset is empty.")

    # Check for any non-finite / NaN values
    missing_count = int(df.isna().sum().sum())
    if missing_count > 0:
        raise ValueError(f"Unexpected missing values found during ingestion: {missing_count}")

    # Step 4: Write processed CSV copy
    df.to_csv(processed_csv_path, index=False)

    # Step 5: Construct provenance manifest
    manifest = {
        "source": "UCI Machine Learning Repository",
        "dataset_name": UCI_DATASET_NAME,
        "dataset_id": UCI_DATASET_ID,
        "source_url": OFFICIAL_UCI_ZIP_URL,
        "retrieval_timestamp": retrieval_timestamp,
        "raw_archive_file": zip_file_path.name,
        "raw_archive_byte_size": len(zip_bytes),
        "raw_archive_sha256": zip_sha256,
        "data_file_name": data_txt_path.name,
        "data_file_byte_size": len(data_raw_bytes),
        "data_file_sha256": data_sha256,
        "row_count": row_count,
        "column_count": col_count,
        "column_names": list(CANONICAL_COLUMNS),
        "feature_columns": list(FEATURE_COLUMNS),
        "target_columns": list(TARGET_COLUMNS),
    }

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    return manifest
