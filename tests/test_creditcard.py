from pathlib import Path

import pandas as pd
import pytest

from aiml.creditcard import COLUMNS, SchemaError, main, row_count_from_note, time_ordered_split


def _write_note(path: Path, row_count: int) -> None:
    path.write_text(f"row_count: {row_count}\n", encoding="utf-8")


def _write_table(path: Path, rows: list[dict[str, object]]) -> None:
    pd.DataFrame(rows).to_csv(path, index=False)


def test_missing_class_fails(tmp_path: Path) -> None:
    csv_path = tmp_path / "creditcard.csv"
    note_path = tmp_path / "note.md"
    csv_path.write_text("Time,Amount\n1,2\n", encoding="utf-8")
    _write_note(note_path, 1)
    with pytest.raises(SystemExit, match="Class"):
        main([str(csv_path), str(note_path)])


def test_row_count_drift_fails(tmp_path: Path) -> None:
    csv_path = tmp_path / "creditcard.csv"
    note_path = tmp_path / "note.md"
    row = {name: 0 for name in COLUMNS}
    _write_table(csv_path, [row])
    _write_note(note_path, 99)
    with pytest.raises(SystemExit, match="drifted"):
        main([str(csv_path), str(note_path)])


def test_note_requires_one_row_count() -> None:
    with pytest.raises(SchemaError):
        row_count_from_note("no count here\n")


def test_time_does_not_cross_the_split() -> None:
    frame = pd.DataFrame({"Time": [1, 2, 3, 4, 5, 5, 5, 6, 7, 8]})
    split = time_ordered_split(frame)
    train_time = frame.loc[split.train, "Time"]
    dev_time = frame.loc[split.dev, "Time"]
    test_time = frame.loc[split.test, "Time"]
    assert train_time.max() < dev_time.min()
    assert dev_time.max() < test_time.min()
    assert split.dev_cut == 4
    assert split.test_cut == 8
