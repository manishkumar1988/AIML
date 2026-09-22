from pathlib import Path

import pytest

from aiml.smoke import main


def test_missing_seed_fails(tmp_path: Path) -> None:
    path = tmp_path / "config.toml"
    path.write_text('[paths]\ndata = "data"\ncheckpoints = "checkpoints"\n', encoding="utf-8")
    with pytest.raises(SystemExit, match="seed"):
        main([str(path)])
