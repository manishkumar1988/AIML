# Project rules for AI coding tools

This repo is a learning path (see `README.md`). The human makes the decisions; the AI implements them.

## Environment
- Use `uv run` and `uv add`. Never `pip install`. Python 3.12.
- Shared helpers live in `work/common/` and import as `common` (e.g. `from common.seed import set_seed`).
- Each challenge's code lives in `work/NN-name/` (e.g. `work/03-churn/`).

## Reproducibility
- Call `set_seed()` from `common.seed` at the start of every script, and also pass `random_state=42` explicitly to scikit-learn splits and models.
- Every script prints the numbers it produces and saves results to files, not only to a notebook.

## Data and models
- Datasets go in `data/`, trained models and checkpoints in `models/`. Never commit them.
- Never put API keys or tokens in code. Read them from `.env`.

## Evaluation discipline
- Split the data before any preprocessing. Fit scalers, encoders, imputers, vectorizers and tokenizers on the training split only.
- Never use the test split to choose anything (model, features, threshold, prompt, epoch, hyperparameters). Use it once, at the end, when asked.

## Working with the human
- If the split, metric, or approach is ambiguous, ask instead of choosing.
- Do not write or edit `NOTES.md` files or `decision-map.md`. The human writes those.
