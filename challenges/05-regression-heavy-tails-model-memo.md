# Challenge 5 — Regression, heavy tails, and a model memo

[Previous: Challenge 4 — Leakage and a split that matches the decision](04-leakage-split-that-matches-decision.md) · [Next: Challenge 6 — Fine-grained intent classification](06-fine-grained-intent-classification.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 5 — Regression, heavy tails, and a model memo

- **Goal:** Predict claim severity and say where the model fails, in a memo a teammate can act on.
- **Why an engineer needs it:** Many business targets are skewed money amounts. A good average error can still be useless in the tail, which is where the money is.
- **What to build:** A regression model for [Allstate Claims Severity](https://www.kaggle.com/competitions/allstate-claims-severity). Headline metric: MAE on the original `loss` scale. Baselines: global median, and a linear model. Then one tree model. Slice absolute error by loss decile. If you transform the target, the number you compare is still MAE after you invert the transform. Dev split from the training file only.
- **Skills practiced:** MAE vs a transformed training loss, residual slices, model memos.
- **Stack and data:** pandas, scikit-learn or LightGBM. Kaggle competition [Allstate Claims Severity](https://www.kaggle.com/competitions/allstate-claims-severity).
- **Difficulty:** core
- **Rough time:** 4–6 days
- **GPU:** CPU-ok
- **Acceptance criteria:**
  - The log contains median baseline, linear model, and tree model, same split, MAE on the original scale.
  - A decile table shows where absolute error concentrates.
  - A one-page memo states which model you would ship and which loss range you would not trust it on.
  - The competition test file was not used for model choice.
- **Stretch goal:** A calibration-style plot of predicted vs actual in each decile, plus one change that improves the worst decile without worsening overall MAE by more than a margin you set first.
- **Builds on:** Challenges 3–4.
