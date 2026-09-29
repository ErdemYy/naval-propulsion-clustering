"""Centralized logging configuration for reproducible experiment traceability."""

from __future__ import annotations

import logging
import logging.config
from pathlib import Path
import yaml

from naval_propulsion.utils.paths import get_project_root


def setup_logging(
    config_path: Path | str | None = None,
    default_level: int = logging.INFO,
) -> None:
    """Initialize logging configuration from YAML or fallback to basic config.

    Parameters
    ----------
    config_path : Path or str, optional
        Path to the logging YAML configuration file. Defaults to configs/logging.yaml.
    default_level : int, default=logging.INFO
        Fallback log level if config file is not found.
    """
    root_dir = get_project_root()
    if config_path is None:
        config_path = root_dir / "configs" / "logging.yaml"
    else:
        config_path = Path(config_path)

    # Ensure log output directory exists
    log_dir = root_dir / "experiments"
    log_dir.mkdir(parents=True, exist_ok=True)

    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(
            level=default_level,
            format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
