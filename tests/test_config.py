"""Unit tests for configuration schemas and loading routines."""

from __future__ import annotations

from pathlib import Path
from naval_propulsion.config.settings import SystemConfig, load_config


def test_default_config_loading() -> None:
    """Test loading default configuration."""
    config = load_config()
    assert isinstance(config, SystemConfig)
    assert config.project.name == "naval-propulsion-clustering"
    assert config.project.random_seed == 42
    assert "kMc" in config.data.degradation_targets
    assert "kMt" in config.data.degradation_targets


def test_nonexistent_config_falls_back() -> None:
    """Test that a non-existent config path falls back to default SystemConfig."""
    config = load_config(Path("non_existent_config_file.yaml"))
    assert isinstance(config, SystemConfig)
    assert config.project.random_seed == 42
