# Challenge 26 — Porto Seguro, local Gini, no leaderboard tuning

[Previous: Challenge 25 — Train and evaluate an 8M–33M model](25-train-evaluate-8m-33m-model.md) · [Next: Challenge 27 — PII detection, competition metric](27-pii-detection-competition-metric.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 26 — Porto Seguro, local Gini, no leaderboard tuning

- **Goal:** Reproduce [Porto Seguro’s Safe Driver Prediction](https://www.kaggle.com/competitions/porto-seguro-safe-driver-prediction) with a local normalized Gini score you trust.
- **Why an engineer needs it:** Competition work is the pressure test of Phase 2: a fixed metric, a messy table, and a rule that the public test file does not choose the model.
- **What to build:** A claims model on the Porto Seguro training file. Headline: normalized Gini, the competition metric. Implement the metric and check it on a toy vector where you know the answer. Stratified local CV, pre-registered. Baselines: a constant prediction, and a linear model. Then one gradient-boosted tree model. Missing values are the competition’s `-1` codes; handle them inside the folds. Write a rules file: no model choice from the public leaderboard. Generate one submission file at the end if you want a late submission, after the model is frozen.
- **Skills practiced:** Competition metrics, stratified CV, missing-value codes, submission hygiene.
- **Stack and data:** pandas, scikit-learn or LightGBM. [Porto Seguro’s Safe Driver Prediction](https://www.kaggle.com/competitions/porto-seguro-safe-driver-prediction).
- **Difficulty:** core
- **Rough time:** 1–2 weeks
- **GPU:** CPU-ok
- **Acceptance criteria:**
  - The metric unit check passes.
  - The log has constant, linear, and tree Gini on the same CV protocol.
  - The rules file exists and the README says you did not pick the model from the public leaderboard.
  - A short note explains what would have leaked if you had tuned on the test file.
- **Stretch goal:** A feature-group ablation (`ind`, `reg`, `car`, `calc`) that says which group you could drop.
- **Builds on:** Challenges 3–5.
