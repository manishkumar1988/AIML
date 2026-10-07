# 07 — Tune, validate, explain

**Phase 1 · Classical ML** · ⏱ 1 week · 💻 Laptop · Level: core

[← 06 Forecasting demand](06-time-series-forecasting.md) · [Index](../README.md) · [Next: 08 Kaggle playground →](08-kaggle-playground.md)

## The problem

Your churn model from Challenge 03 goes to a review meeting. Three questions come up:

1. "Is it really better than logistic regression, or did you get lucky with the split?"
2. "Did you tune it properly?"
3. "Why does it say *this* customer will leave?"

This challenge answers all three. It also includes a "spot the leak" exercise.

Dataset: the Telco churn data from Challenge 03.

## Decide first

1. If model A scores 0.84 and model B 0.85 on one validation split, is B better?
2. You try 200 hyperparameter combinations and pick the best validation score. Is that score an honest estimate?
3. What's the difference between "which features matter overall" and "why this one prediction"?

## Learn

- **Cross-validation (CV):** split training data into k folds (5 is common); train k times, each time validating on a different fold. You get k scores, so you can see the **mean and the spread**. If two models' ranges overlap a lot, you can't call a winner.
- **Stratified K-fold** keeps the class ratio the same in each fold.
- **Hyperparameter tuning:** `GridSearchCV` tries every combination; `RandomizedSearchCV` samples. Random search is usually enough and much faster. Tuning happens *inside* cross-validation on training data. The test set stays untouched.
- **Optimistic bias:** the best score out of 200 tries is a bit lucky. That's why the test set exists.
- **Global explanation:** permutation importance ("how much worse does the model get if I shuffle this column?").
- **Local explanation:** SHAP values ("for this customer, tenure pushed the risk up by this much"). Explanations describe the *model*, not the real world. They are not proof of cause.

Read: scikit-learn [Cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html) (sections 3.1.1–3.1.2), [Tuning hyperparameters](https://scikit-learn.org/stable/modules/grid_search.html), and the SHAP [intro notebook](https://shap.readthedocs.io/en/latest/example_notebooks/overviews/An%20introduction%20to%20explainable%20AI%20with%20Shapley%20values.html).

## Build

Work in `work/07-tune-explain/`. Reuse your Challenge 03 split: CV happens on train+validation combined (80%), and the test set stays aside.

1. **CV comparison.** 5-fold stratified CV (seed 42) for: logistic regression, random forest, gradient boosting. Metric: ROC-AUC and average precision. Report mean ± standard deviation.
   ✅ A table with mean and std for each. Write one sentence: is there a clear winner?

2. **Tuning.** `RandomizedSearchCV` on gradient boosting (`learning_rate`, `max_depth` or `max_leaf_nodes`, `min_samples_leaf`, `l2_regularization`), 40 iterations, 5-fold CV.
   ✅ The best CV score and its parameters are saved. Compare with the untuned score. Is the gain bigger than the fold-to-fold spread?

3. **Learning curve.** `learning_curve` for your best model with 10%…100% of training data.
   ✅ A plot. Write: would more data help?

4. **Global importance.** Permutation importance on the held-out fold or validation part.
   ✅ Top 5 features, in plain words.

5. **Local explanations.** `uv add shap`. Compute SHAP values for the tuned tree model. Plot a summary (beeswarm) plot, and a waterfall plot for one high-risk and one low-risk customer.
   ✅ You can explain one individual prediction in a sentence a retention agent would understand.

6. **Spot the leak.** Make a copy of the training data and add a column `retention_call_made`: set it to 1 for 80% of churners and 5% of non-churners at random (imagine a CRM field filled in *after* customers called to cancel). Retrain.
   ✅ The score jumps, and SHAP ranks this column #1. Write: how would you have caught this in a real project, without being told?

7. **Test once** with your tuned model. Compare with Challenge 03's test number.

8. Write `NOTES.md`.

## Hints

<details><summary>Hint 1 — SHAP and pipelines</summary>

SHAP needs the transformed features. Fit the pipeline, then `X_t = pipe[:-1].transform(X)`, and use `shap.TreeExplainer(pipe[-1])` on `X_t`, with `feature_names=pipe[:-1].get_feature_names_out()`.
</details>

<details><summary>Hint 2 — tuning made almost no difference</summary>

That's a normal and useful result. On small tabular data, default gradient boosting is often near its best. Write it down. Knowing when tuning isn't worth the time is a skill.
</details>

## Common mistakes

- Comparing models on a single split and declaring a winner by 0.005.
- Tuning with the test set, or doing feature selection on all data before CV.
- Saying "SHAP shows that month-to-month contracts *cause* churn." It shows the model *uses* that feature.

## Done when

- [ ] CV table with mean ± std for three models.
- [ ] Tuned vs untuned comparison, with a judgment on whether tuning mattered.
- [ ] A learning curve and a sentence on whether more data would help.
- [ ] Global and local explanations, in plain words.
- [ ] The leakage experiment, and how you'd catch it in real life.

## Stretch

Try [Optuna](https://optuna.org/) instead of random search. Was it better, for the same number of trials?

## Reflect

- Fill in **Choosing between classical models** in your [decision map](../decision-map.md).
- Write a half-page `work/milestones.md` entry after Challenge 08: what you now know about classical ML.
