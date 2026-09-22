# AI/ML challenges workspace

Practice repo for the sequenced challenges in [aiml-engineer-challenges.md](aiml-engineer-challenges.md). Challenge 1 is a reproducible local workspace: pinned dependencies, a fixed seed, and a smoke check. The smoke check does not train a model.

**Environment used:** Python 3.13.7 on macOS 27.0 (Darwin arm64, Apple Silicon).

## Setup

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --extra dev
```

This creates `.venv` from the lockfile and installs the package in editable mode, including pytest.

## Smoke check

From the repo root:

```bash
uv run aiml-smoke
```

A good run prints `seed=42` and exits 0. A second run prints the same seed. The value comes from `seed` in `config.toml`.

If a required key is missing (`seed`, `paths.data`, or `paths.checkpoints`), the command prints `smoke check failed: ...` to stderr and exits 1.

```bash
uv run pytest
```

## Layout

| Path | Role |
| --- | --- |
| `config.toml` | Seed and the `data/` and `checkpoints/` paths |
| `src/aiml/seed.py` | Sets the Python seed from that config |
| `src/aiml/smoke.py` | Loads config, prints the seed, exits |
| `data/` | Later datasets. Gitignored. Challenge 2 reads `data/creditcard.csv`. |
| `checkpoints/` | Later model weights. Gitignored. |
| `notes/creditcard-audit.md` | Challenge 2 data note and the Challenge 3 split rule |
| `experiments/log.csv` | Experiment log. Challenge 2 has the first row. |

## Challenge 2 — fraud table audit

The CSV is not in git. Place the ULB credit-card file at `data/creditcard.csv` (Kaggle `mlg-ulb/creditcardfraud`). The copy used here is the Zenodo file with MD5 `e90efcb83d69faf99fcab8b0255024de`.

```bash
uv run python -m aiml.creditcard
```

A good run prints `row_count=284807` and exits 0. It checks that `Class` is present and that the row count still matches `row_count:` in `notes/creditcard-audit.md`. It does not fit a classifier.
