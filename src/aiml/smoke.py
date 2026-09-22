"""Smoke check: load config, print the seed, exit. Does not train a model."""

from __future__ import annotations

import sys
from pathlib import Path

from aiml.config import ConfigError, load_config
from aiml.seed import set_seed


def main(argv: list[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)
    path = Path(args[0]) if args else Path("config.toml")
    try:
        config = load_config(path)
    except ConfigError as exc:
        raise SystemExit(f"smoke check failed: {exc}") from exc
    print(f"seed={set_seed(config.seed)}")


if __name__ == "__main__":
    main()
