"""Audit the ULB credit-card table and build the Challenge 3 split.

This module does not fit a classifier.
"""

from __future__ import annotations

import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

COLUMNS = ["Time", *[f"V{i}" for i in range(1, 29)], "Amount", "Class"]
ROW_COUNT_LINE = re.compile(r"^row_count:\s*(\d+)\s*$", re.MULTILINE)


class SchemaError(Exception):
    """Raised when the table does not match the data note."""


@dataclass(frozen=True)
class Split:
    """Original-file row ids for train, dev, and test."""

    train: np.ndarray
    dev: np.ndarray
    test: np.ndarray

    @property
    def dev_cut(self) -> int:
        return int(len(self.train))

    @property
    def test_cut(self) -> int:
        return int(len(self.train) + len(self.dev))


def load_creditcard(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def row_count_from_note(text: str) -> int:
    found = ROW_COUNT_LINE.findall(text)
    if len(found) != 1:
        raise SchemaError("data note must contain exactly one 'row_count:' line")
    return int(found[0])


def check_schema(frame: pd.DataFrame, expected_row_count: int) -> None:
    if "Class" not in frame.columns:
        raise SchemaError("column 'Class' is absent")
    missing = [name for name in COLUMNS if name not in frame.columns]
    if missing:
        raise SchemaError("missing columns: " + ", ".join(missing))
    actual = len(frame)
    if actual != expected_row_count:
        raise SchemaError(
            f"row count {actual} drifted from the note ({expected_row_count})"
        )


def time_ordered_split(frame: pd.DataFrame) -> Split:
    """60/20/20 split sorted by Time, then by original row id.

    An equal-Time run is never cut. The cut moves earlier so the whole run
    sits on the later side. Time therefore does not appear on both sides of
    a boundary.
    """
    if "Time" not in frame.columns:
        raise SchemaError("column 'Time' is absent")
    row_count = len(frame)
    time = frame["Time"].to_numpy()
    order = np.lexsort((np.arange(row_count, dtype=np.int64), time))
    dev_cut = _snap_time_boundary(order, time, (row_count * 60) // 100)
    test_cut = _snap_time_boundary(order, time, (row_count * 80) // 100)
    if not (0 < dev_cut < test_cut < row_count):
        raise SchemaError("time boundary snap collapsed a split")
    train_time = time[order[:dev_cut]]
    dev_time = time[order[dev_cut:test_cut]]
    test_time = time[order[test_cut:]]
    if train_time.max() >= dev_time.min() or dev_time.max() >= test_time.min():
        raise SchemaError("Time crosses a split boundary")
    return Split(
        train=order[:dev_cut].copy(),
        dev=order[dev_cut:test_cut].copy(),
        test=order[test_cut:].copy(),
    )


def _snap_time_boundary(order: np.ndarray, time: np.ndarray, cut: int) -> int:
    boundary = time[order[cut]]
    while cut > 0 and time[order[cut - 1]] == boundary:
        cut -= 1
    return int(cut)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def describe(frame: pd.DataFrame, split: Split) -> dict[str, object]:
    class_values = frame["Class"]
    positives = int((class_values == 1).sum())
    row_count = len(frame)
    amount = frame["Amount"]
    quantiles = amount.quantile([0.5, 0.9, 0.99]).tolist()
    return {
        "row_count": row_count,
        "positives": positives,
        "positive_rate": positives / row_count,
        "missing_cells": int(frame.isna().sum().sum()),
        "duplicate_rows": int(frame.duplicated().sum()),
        "rows_in_duplicate_groups": int(frame.duplicated(keep=False).sum()),
        "time_min": frame["Time"].min(),
        "time_max": frame["Time"].max(),
        "amount_min": amount.min(),
        "amount_p50": quantiles[0],
        "amount_p90": quantiles[1],
        "amount_p99": quantiles[2],
        "amount_max": amount.max(),
        "amount_mean": amount.mean(),
        "amount_skew": amount.skew(),
        "train_rows": len(split.train),
        "dev_rows": len(split.dev),
        "test_rows": len(split.test),
        "dev_cut": split.dev_cut,
        "test_cut": split.test_cut,
        "dev_time_min": frame.loc[split.dev, "Time"].min(),
        "test_time_min": frame.loc[split.test, "Time"].min(),
        "train_time_max": frame.loc[split.train, "Time"].max(),
        "dev_time_max": frame.loc[split.dev, "Time"].max(),
    }


def main(argv: list[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)
    csv_path = Path(args[0]) if args else Path("data/creditcard.csv")
    note_path = Path(args[1]) if len(args) > 1 else Path("notes/creditcard-audit.md")
    try:
        note_text = note_path.read_text(encoding="utf-8")
        frame = load_creditcard(csv_path)
        check_schema(frame, row_count_from_note(note_text))
        split = time_ordered_split(frame)
    except (SchemaError, OSError) as exc:
        raise SystemExit(f"audit failed: {exc}") from exc
    facts = describe(frame, split)
    print(f"sha256={file_sha256(csv_path)}")
    for key, value in facts.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
