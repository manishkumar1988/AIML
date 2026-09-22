# Challenge 3 — Imbalanced classification and a decision metric

[Previous: Challenge 2 — Data audit and an experiment log](02-data-audit-experiment-log.md) · [Next: Challenge 4 — Leakage and a split that matches the decision](04-leakage-split-that-matches-decision.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 3 — Imbalanced classification and a decision metric

- **Goal:** Detect fraudulent transactions with a metric and an operating point, not a leaderboard accuracy.
- **Why an engineer needs it:** Fraud, medical flags, and abuse queues are imbalanced. Accuracy hides a model that never fires.
- **What to build:** A classical classifier on the ULB fraud table, using the split rule from Challenge 2. Headline metric: average precision (area under the precision-recall curve). Also record precision at two recalls you choose in advance (for example 0.50 and 0.80), and a calibration check (reliability curve or binned predicted vs empirical rate). Baselines: always-negative, and a logistic regression on `Amount` plus `Time` only.
- **Skills practiced:** PR curves, operating points, calibration, simple vs full feature sets.
- **Stack and data:** scikit-learn. Same Kaggle file as Challenge 2, [Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud).
- **Difficulty:** revision
- **Rough time:** 4–6 days
- **GPU:** CPU-ok
- **Acceptance criteria:**
  - The experiment log has the baseline and the full model on the same test indices.
  - Average precision and the two precision-at-recall numbers are in the log.
  - Accuracy is present only as a footnote that says why it is the wrong headline.
  - A short error note lists false positives and false negatives at the chosen operating point, with `Amount` bands.
  - The test split was not used to pick the model class or the threshold. The threshold comes from the train/dev portion.
- **Stretch goal:** A cost table: if a false positive costs 1 and a missed fraud costs a number you declare, show the operating point that minimizes expected cost.
- **Builds on:** Challenges 1–2.
