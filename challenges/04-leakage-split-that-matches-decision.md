# Challenge 4 — Leakage and a split that matches the decision

[Previous: Challenge 3 — Imbalanced classification and a decision metric](03-imbalanced-classification-decision-metric.md) · [Next: Challenge 5 — Regression, heavy tails, and a model memo](05-regression-heavy-tails-model-memo.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 4 — Leakage and a split that matches the decision

- **Goal:** Forecast store sales with a validation design that could have been used in the live competition, and show how a random split lies.
- **Why an engineer needs it:** Random row splits are the default in tutorials and the usual source of silent leakage in production (time, entity, target-derived features).
- **What to build:** A model for [Rossmann Store Sales](https://www.kaggle.com/competitions/rossmann-store-sales). Join `train.csv` and `store.csv`. Metric: RMSPE, ignoring rows with zero sales, matching the competition definition. Before any fit, write a feature inventory: for each column, whether you would know it on the morning you must forecast. Train two ways and put both scores in the log:
  1. A random row split.
  2. A time-based split that holds out a final window of dates, shared across stores.
  Baseline: each store’s recent median sales. One stronger model (linear or gradient-boosted trees). Do not choose features from the public leaderboard.
- **Skills practiced:** Time splits, feature timing, RMSPE, store-level baselines, leakage reviews.
- **Stack and data:** pandas, scikit-learn or LightGBM. Kaggle competition [Rossmann Store Sales](https://www.kaggle.com/competitions/rossmann-store-sales).
- **Difficulty:** core
- **Rough time:** 1 week
- **GPU:** CPU-ok
- **Acceptance criteria:**
  - Both RMSPE numbers are in the log, with the date cutoff written down.
  - The feature inventory exists and was committed before the model scores.
  - The writeup says which score you would trust for a six-week-ahead forecast, and why the other score is the wrong one to quote.
  - The public test file was not used to pick the model.
- **Stretch goal:** Repeat the time-split score with a second cutoff and show whether the ranking of baseline vs model stays the same.
- **Builds on:** Challenges 1–3.
