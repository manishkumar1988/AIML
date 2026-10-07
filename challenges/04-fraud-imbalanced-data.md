# 04 — Fraud detection with imbalanced data

**Phase 1 · Classical ML** · ⏱ 1 week · 💻 Laptop · Level: core

[← 03 Customer churn](03-customer-churn-classification.md) · [Index](../README.md) · [Next: 05 Learning without labels →](05-learning-without-labels.md)

## The problem

A card company wants to flag fraudulent transactions. A missed fraud costs about €100 on average. Each flagged transaction is checked by a person, which costs about €2. Fraud is very rare.

Dataset: **Credit Card Fraud Detection** (ULB), on Kaggle as [mlg-ulb/creditcardfraud](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud). 284,807 transactions over two days, 492 frauds. Features `V1`–`V28` are anonymized (PCA), plus `Time` (seconds since the first transaction) and `Amount`.

## Decide first

1. Fraud is about 0.17% of rows. What accuracy does "never fraud" get? Is that useful?
2. Which mistake is more expensive here, a false alarm or a miss? By how much?
3. The data is ordered in time. Should you split randomly or by time? What's the risk of each?
4. How would you choose the threshold for flagging a transaction?

## Learn

- **Imbalanced data:** when one class is rare, accuracy is useless and ROC-AUC can look great while the model is still poor at finding the rare class.
- **Precision-recall curve:** precision and recall at every possible threshold. **Average precision (PR-AUC)** summarizes it. The baseline PR-AUC equals the positive rate (0.0017), not 0.5.
- **Choosing a threshold with costs:** expected cost = (false positives × cost of a check) + (false negatives × cost of a miss). Choose the threshold that minimizes it **on validation data**, then apply it unchanged to test.
- **Class weights:** `class_weight="balanced"` tells the model to care more about the rare class. It changes the scores, so the predicted "probabilities" are no longer real probabilities.
- **Resampling (SMOTE, undersampling):** popular, but often no better than class weights plus a good threshold. Try it in the stretch, not first.
- **Splitting by time:** a real fraud model is trained on the past and used on the future. A time split tests exactly that.

Read: scikit-learn [precision_recall_curve](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_curve.html) and [Tuning the decision threshold](https://scikit-learn.org/stable/modules/classification_threshold.html).

## Build

Work in `work/04-fraud/`.

1. **Look.** Count rows and frauds. Plot `Amount` for fraud vs normal (log scale). Check for duplicate rows.
   ✅ 492 frauds out of 284,807 (0.172%). Some exact duplicate rows exist; decide what to do with them and write why.

2. **Split by time.** Sort by `Time`. First 60% train, next 20% validation, last 20% test.
   ✅ Each part has some frauds. Write down how many. Validation and test will only have around 60–100 each. Note how few that is.

3. **Baselines.** (a) Always "not fraud." (b) A simple rule: flag if `Amount` > some value. Compute precision, recall and cost on validation.
   ✅ Baseline (a) costs `number_of_frauds × €100`. That's the number to beat.

4. **Logistic regression** with `class_weight="balanced"` (scale features first, in a pipeline). Compute PR-AUC and ROC-AUC on validation.
   ✅ ROC-AUC is very high (above 0.95) while PR-AUC is much lower. Write one sentence on why they differ so much.

5. **Gradient boosting** (`HistGradientBoostingClassifier`). Compare PR-AUC.
   ✅ You have a table of PR-AUC for both models and the baselines.

6. **Pick a threshold by cost.** For your best model, compute the expected cost at many thresholds on validation, and choose the cheapest. Plot cost vs threshold.
   ✅ The chosen threshold is usually *not* 0.5. Your cost at that threshold is far below baseline (a).

7. **Test once.** Apply the chosen model and threshold to test. Report precision, recall, number of flags, and total cost.
   ✅ Test cost is in the same range as validation. If not, write down what changed (remember: very few frauds, so numbers jump around).

8. **Errors.** Look at missed frauds: are they mostly small amounts? Break misses down by `Amount` band.

9. Write `NOTES.md`, ending with the threshold you'd use and the expected monthly cost saving, in plain words.

## Hints

<details><summary>Hint 1 — cost curve code shape</summary>

Loop over `np.linspace(0, 1, 501)` thresholds; for each, `pred = scores >= t`, count FP and FN, and compute `2*FP + 100*FN`. Pick the minimum with `np.argmin`.
</details>

<details><summary>Hint 2 — the numbers change a lot between runs</summary>

With only about 60–100 frauds in validation, catching 3 more or fewer frauds moves recall by several points. That's real uncertainty, not a bug. Mention it in your notes. (In the stretch, you'll measure it.)
</details>

## Common mistakes

- Choosing the threshold on the test set.
- Reporting accuracy or ROC-AUC as the headline for a rare-event problem.
- Applying SMOTE *before* splitting, which leaks synthetic copies of test frauds into training.
- Treating class-weighted scores as true probabilities ("this transaction is 80% likely fraud").

## Done when

- [ ] Time-based split, with fraud counts per part written down.
- [ ] PR-AUC for baselines and two models.
- [ ] A cost-vs-threshold plot and a threshold chosen on validation.
- [ ] One test result: precision, recall, cost.
- [ ] `NOTES.md` explains why accuracy is the wrong headline, in your own words.

## Stretch

- **Bootstrap:** resample the test set with replacement 1,000 times and recompute PR-AUC. Report the 2.5th and 97.5th percentiles. How wide is the range?
- Try SMOTE (inside the training data only, using `imblearn`'s pipeline). Did it beat class weights?

## Reflect

- How would your threshold change if a manual check cost €10 instead of €2?
- Update the **Imbalanced classification** section of your [decision map](../decision-map.md).
