# Challenge 00 — Workspace setup

## Decide first (my answers)

1. Why might a notebook that ran fine last month fail today?
   - Packages were not pinned, so a newer version changed or removed an API. The data file changed or moved. Cells were run out of order, so the notebook depended on hidden state that a fresh run doesn't recreate. Different Python version on another machine.
   - Fix: pinned versions (`uv.lock`), fixed paths, and final code in scripts that run top to bottom.

2. What should never go into git for an ML project?
   - Datasets and model checkpoints (too big, and sometimes licensed or private).
   - Secrets: API keys, tokens, `.env` files.
   - Generated stuff: virtual environments (`.venv/`), `__pycache__/`, notebook checkpoints, OS files like `.DS_Store`.

3. Why does a fixed random seed matter when comparing two models?
   - Shuffling, splits and weight initialization are random. Without a fixed seed, two runs of the *same* model give different scores, so I can't tell whether model B beat model A because it's better or because it got lucky.
   - A fixed seed makes runs repeatable. It doesn't remove luck completely (one seed can still be lucky), so for close results I should compare across several seeds or folds.

## What I set up

| Item | Result |
| --- | --- |
| Python | 3.12, pinned in `.python-version` (committed) |
| Packages | numpy 2.5.3, pandas 3.0.6, scikit-learn 1.9.1, matplotlib, jupyter. Exact versions locked in `uv.lock` |
| Folders | `work/` (code per challenge), `data/` and `models/` (ignored by git) |
| Seed helper | `work/common/seed.py`: `set_seed(42)` seeds Python `random` and NumPy |
| Smoke check | `uv run python work/00-setup/check.py` prints versions and `first_draw=0.374540` on every run |
| AI rules | `AGENTS.md` (single source), used by `CLAUDE.md` and `.cursor/rules/project.mdc` |

## Decisions I made

- **Commit `uv.lock`:** it locks the exact version of every package, so `uv sync` rebuilds the same environment anywhere.
- **Commit `.python-version`:** it pins Python 3.12 for anyone who clones the repo.
- **Seed value 42:** arbitrary. What matters is that it's fixed and never tuned to get a better score.
- **Shared code is an installable package:** `common` is installed by `uv sync`, so `from common.seed import set_seed` works from any script without path hacks.
- **One rules file for all AI tools:** `AGENTS.md`, so conventions only live in one place.

## What confused me

- Why the seed is 42. Answer: it's arbitrary (a *Hitchhiker's Guide to the Galaxy* joke). Any fixed number works.
- The difference between the seed *value* and *which generators* get seeded (Python `random`, NumPy global). NumPy's `default_rng()` and scikit-learn's `random_state` need the seed passed explicitly.
- How scripts in `work/NN-*/` import shared code: solved by installing `common` as a package.
