"""Load the workspace config."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path


class ConfigError(Exception):
    """Raised when config.toml is missing a required key or has a bad value."""


@dataclass(frozen=True)
class Paths:
    data: Path
    checkpoints: Path


@dataclass(frozen=True)
class Config:
    seed: int
    paths: Paths


def load_config(path: Path) -> Config:
    if not path.is_file():
        raise ConfigError(f"config file not found: {path}")

    with path.open("rb") as handle:
        raw = tomllib.load(handle)

    missing: list[str] = []
    if "seed" not in raw:
        missing.append("seed")

    paths = raw.get("paths")
    if not isinstance(paths, dict):
        missing.append("paths")
    else:
        for key in ("data", "checkpoints"):
            if key not in paths:
                missing.append(f"paths.{key}")

    if missing:
        raise ConfigError("missing required config key(s): " + ", ".join(missing))

    seed = raw["seed"]
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ConfigError("config key 'seed' must be an integer")

    assert isinstance(paths, dict)
    return Config(
        seed=seed,
        paths=Paths(data=Path(paths["data"]), checkpoints=Path(paths["checkpoints"])),
    )
