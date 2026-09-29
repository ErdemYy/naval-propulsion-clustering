"""Path resolution utilities for local and reproducible project access."""

from __future__ import annotations

from pathlib import Path


def get_project_root() -> Path:
    """Return the absolute path to the project root directory.

    Assumes this file is located at <project_root>/src/naval_propulsion/utils/paths.py.
    """
    return Path(__file__).resolve().parent.parent.parent.parent


def get_data_dir() -> Path:
    """Return absolute path to the data directory."""
    return get_project_root() / "data"


def get_raw_data_dir() -> Path:
    """Return absolute path to the raw data directory."""
    return get_data_dir() / "raw"


def get_processed_data_dir() -> Path:
    """Return absolute path to the processed data directory."""
    return get_data_dir() / "processed"


def get_models_dir() -> Path:
    """Return absolute path to the serialized models directory."""
    return get_project_root() / "models"


def get_reports_dir() -> Path:
    """Return absolute path to reports directory."""
    return get_project_root() / "reports"


def get_figures_dir() -> Path:
    """Return absolute path to figures directory."""
    return get_reports_dir() / "figures"


def get_experiments_dir() -> Path:
    """Return absolute path to experiments directory."""
    return get_project_root() / "experiments"
