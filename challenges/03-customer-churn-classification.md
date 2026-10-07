# 03 — Customer churn

**Phase 1 · Classical ML** · ⏱ 1 week · 💻 Laptop · Level: core

[← 02 First end-to-end model](02-first-end-to-end-model.md) · [Index](../README.md) · [Next: 04 Fraud detection →](04-fraud-imbalanced-data.md)

## The problem

A telecom company loses customers every month. The retention team can call 500 customers a month with a discount offer. They want a list of who to call: the customers most likely to leave (churn).

Dataset: **Telco Customer Churn** (IBM sample data), on Kaggle as [blastchar/telco-customer-churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn). About 7,000 customers, a mix of numeric and text columns, target `Churn` (Yes/No).

## Decide first

1. Problem type? Input and output?
2. Roughly a quarter of customers churn. What accuracy does "predict nobody churns" get?
3. The team can only call 500 people. Which matters more here: precision or recall? Why?
4. Columns like `Contract` are text ("Month-to-month", "One year"…). How would you feed them to a model?

## Learn

- **Classification** predicts a category. Most models output a **probability**; you choose a **threshold** to turn it into yes/no.
- **Confusion matrix:** true positives, false positives, true negatives, false negatives. Every classification metric comes from these four numbers.
- **Precision:** of the people we called, how many were really going to leave? **Recall:** of everyone who left, how many did we call?
- **Preprocessing:** categorical columns need **one-hot encoding**; numeric columns sometimes need **scaling** (important for logistic regression, not for trees).
- **`Pipeline` + `ColumnTransformer`:** bundle preprocessing and model so preprocessing *learns only from training data* and runs the same way on new data. This prevents a subtle kind of leakage.
- **Logistic regression** is the standard classification baseline. Its coefficients tell you which features push towards churn.

Read: scikit-learn [Column Transformer with Mixed Types](https://scikit-learn.org/stable/auto_examples/compose/plot_column_transformer_mixed_types.html) and [Precision-Recall](https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html) (just the first part).

## Build

Work in `work/03-churn/`. Download the CSV into `data/`.

1. **Load and clean.** Check dtypes. `TotalCharges` looks numeric but isn't. Find out why and fix it.
   ✅ `TotalCharges` is a float column; you've decided what to do with the rows that were blank, and written why.

2. **Split.** Stratified split (`stratify=y`): 60/20/20 train/val/test, seed 42. Drop `customerID` from the features (why?).
   ✅ The churn rate is about the same (~26%) in all three parts.

3. **Baseline.** "Predict no one churns." Compute accuracy, precision and recall on validation.
   ✅ Accuracy is about 73–74%, and recall is 0. That's why accuracy alone is misleading.

4. **Pipeline.** `ColumnTransformer` with `OneHotEncoder(handle_unknown="ignore")` for categoricals and `StandardScaler` for numerics, then `LogisticRegression`. Fit on train only.
   ✅ ROC-AUC on validation of about 0.83–0.85.

5. **Stronger model.** Swap in `HistGradientBoostingClassifier` or `RandomForestClassifier`.
   ✅ Similar to, or slightly better than, logistic regression. (Surprised? Write it down. On small tabular data, simple models often hold their own.)

6. **The business view.** The team can call 500 customers. Sort the validation customers by predicted probability, take the top 20% (≈ the same share 500 is of the monthly base, for this exercise). What's the precision in that group? What fraction of all churners does it catch?
   ✅ Precision in the top group is well above 26% (roughly 50–65%). That's the lift the model gives the retention team.

7. **Explain.** Print the 10 largest logistic-regression coefficients (positive and negative). Which features push towards churn?
   ✅ You can explain in plain words why month-to-month contracts and short tenure appear.

8. **Errors.** Look at 10 false negatives (churners with low predicted probability). What do they have in common?

9. **Test once** with your chosen model and threshold. Write `NOTES.md`.

## Hints

<details><summary>Hint 1 — <code>TotalCharges</code></summary>

`pd.to_numeric(df["TotalCharges"], errors="coerce")` turns blanks into NaN. Look at those rows' `tenure`. They're brand-new customers who haven't been billed yet. Filling with 0 is defensible. Write down your reasoning.
</details>

<details><summary>Hint 2 — getting feature names out of a pipeline</summary>

`pipeline[:-1].get_feature_names_out()` gives the transformed column names; pair them with `pipeline[-1].coef_[0]`.
</details>

## Common mistakes

- Calling `fit_transform` on the whole dataset before splitting. The scaler then "sees" the test set.
- Leaving `customerID` in as a feature. It's a unique id; the model can memorize it.
- Using the default 0.5 threshold without asking whether it fits the business.

## Done when

- [ ] A table with baseline, logistic regression and one tree model: accuracy, precision, recall, F1, ROC-AUC on validation.
- [ ] The "top 500 calls" precision and recall number.
- [ ] A plain-language list of the top churn drivers.
- [ ] One test score for the chosen model.
- [ ] `NOTES.md` ends with: what you'd tell the retention team.

## Stretch

Plot a **gain chart**: x = % of customers called (sorted by score), y = % of churners caught. Compare with the diagonal (random calling).

## Reflect

- Why did the simple model compete with the complex one here?
- Update the **Classification** section of your [decision map](../decision-map.md).
