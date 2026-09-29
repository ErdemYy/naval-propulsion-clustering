"""Configuration schemas and loading routines for reproducible execution."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import yaml

from naval_propulsion.utils.paths import get_project_root


@dataclass(frozen=True)
class ProjectConfig:
    name: str = "naval-propulsion-clustering"
    random_seed: int = 42
    environment: str = "local"


@dataclass(frozen=True)
class PathsConfig:
    raw_data_dir: Path = Path("data/raw")
    processed_data_dir: Path = Path("data/processed")
    models_dir: Path = Path("models")
    experiments_dir: Path = Path("experiments")
    reports_dir: Path = Path("reports")
    figures_dir: Path = Path("reports/figures")


@dataclass(frozen=True)
class DataConfig:
    degradation_targets: tuple[str, ...] = ("kMc", "kMt")
    sample_size: int | None = None


@dataclass(frozen=True)
class ClusteringConfig:
    algorithms: tuple[str, ...] = ("kmeans", "hierarchical", "dbscan", "gmm")
    default_random_seed: int = 42


@dataclass(frozen=True)
class SystemConfig:
    project: ProjectConfig = field(default_factory=ProjectConfig)
    paths: PathsConfig = field(default_factory=PathsConfig)
    data: DataConfig = field(default_factory=DataConfig)
    clustering: ClusteringConfig = field(default_factory=ClusteringConfig)


def load_config(config_path: Path | str | None = None) -> SystemConfig:
    """Load system configuration from a YAML file or return defaults.

    Parameters
    ----------
    config_path : Path or str, optional
        Path to the configuration YAML file. Defaults to configs/default.yaml.

    Returns
    -------
    SystemConfig
        Validated, immutable configuration instance.
    """
    if config_path is None:
        config_path = get_project_root() / "configs" / "default.yaml"
    else:
        config_path = Path(config_path)

    if not config_path.exists():
        return SystemConfig()

    with open(config_path, "r", encoding="utf-8") as f:
        raw_dict: dict[str, Any] = yaml.safe_load(f) or {}

    project_data = raw_dict.get("project", {})
    paths_data = raw_dict.get("paths", {})
    data_data = raw_dict.get("data", {})
    clustering_data = raw_dict.get("clustering", {})

    return SystemConfig(
        project=ProjectConfig(
            name=project_data.get("name", "naval-propulsion-clustering"),
            random_seed=project_data.get("random_seed", 42),
            environment=project_data.get("environment", "local"),
        ),
        paths=PathsConfig(
            raw_data_dir=Path(paths_data.get("raw_data_dir", "data/raw")),
            processed_data_dir=Path(paths_data.get("processed_data_dir", "data/processed")),
            models_dir=Path(paths_data.get("models_dir", "models")),
            experiments_dir=Path(paths_data.get("experiments_dir", "experiments")),
            reports_dir=Path(paths_data.get("reports_dir", "reports")),
            figures_dir=Path(paths_data.get("figures_dir", "reports/figures")),
        ),
        data=DataConfig(
            degradation_targets=tuple(data_data.get("degradation_targets", ["kMc", "kMt"])),
            sample_size=data_data.get("sample_size"),
        ),
        clustering=ClusteringConfig(
            algorithms=tuple(clustering_data.get("algorithms", ["kmeans", "hierarchical", "dbscan", "gmm"])),
            default_random_seed=clustering_data.get("default_random_seed", 42),
        ),
    )
