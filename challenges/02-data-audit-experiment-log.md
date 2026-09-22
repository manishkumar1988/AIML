# Challenge 2 — Data audit and an experiment log

[Previous: Challenge 1 — Reproducible local workspace](01-reproducible-local-workspace.md) · [Next: Challenge 3 — Imbalanced classification and a decision metric](03-imbalanced-classification-decision-metric.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 2 — Data audit and an experiment log

- **Goal:** A written audit of the fraud table you will model next, and a log you will append to for the rest of the curriculum.
- **Why an engineer needs it:** Most bad models are bad data decisions made before `fit`. A log is how you defend a number a month later.
- **What to build:**
  - Download [Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) (ULB). Columns include `Time`, `V1`–`V28`, `Amount`, `Class`.
  - A data note: row count, positive rate, missingness, duplicate rows, `Time` range, and the shape of `Amount`.
  - The split rule for Challenge 3, written before any model: what is held out, and whether `Time` is allowed to cross the split.
  - An experiment log (markdown or CSV) with columns: date, question, data version, split rule, metric, result, decision. One completed row for this audit.
- **Skills practiced:** Data contracts, class balance, time as a leakage risk, lab notes.
- **Stack and data:** pandas. Kaggle dataset `mlg-ulb/creditcardfraud`.
- **Difficulty:** revision
- **Rough time:** 2–3 days
- **GPU:** CPU-ok
- **Acceptance criteria:**
  - The data note states the positive rate and whether duplicate rows exist.
  - The split rule is specific enough that another person could build the same indices.
  - The log has one row, and that row is not a model score.
  - No classifier has been fit on this file yet.
- **Stretch goal:** Add a short schema check that fails if `Class` is absent or the row count drifts from the note.
- **Builds on:** Challenge 1.
