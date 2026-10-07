# 02 — Your first end-to-end model

**Phase 1 · Classical ML** · ⏱ 1 week · 💻 Laptop · Level: core

[← 01 Problem framing](01-problem-framing.md) · [Index](../README.md) · [Next: 03 Customer churn →](03-customer-churn-classification.md)

## The problem

A real-estate startup wants to estimate the median house value of a California neighborhood from census data: income, house age, rooms, location. They want to know how far off the estimates usually are.

Dataset: **California Housing**, built into scikit-learn (`sklearn.datasets.fetch_california_housing`). 20,640 rows, 8 numeric features. Target: median house value in units of $100,000. No download needed.

## Decide first

1. What problem type is this? What's the input, what's the output?
2. What's the dumbest possible prediction you could make? How bad do you think it would be?
3. Which metric would the startup understand best: RMSE, MAE, or R²? Why?
4. Why must the test set be set aside *before* you look closely at the data?

## Learn

- **The workflow** you'll repeat in every challenge: split → baseline → simple model → stronger model → look at errors → decide.
- **Train / validation / test.** Train to learn, validation to choose, test once to report. If you pick the model using test scores, the test score is no longer an honest estimate.
- **Baselines.** Predicting the training median for every row is a real model. If your fancy model can't beat it by a lot, something's wrong.
- **Linear regression** fits a weighted sum of features. Fast, easy to explain, misses non-linear patterns.
- **Random forest / gradient boosting** combine many decision trees. Usually the strongest choice on tables.
- **MAE vs RMSE.** MAE = average absolute error ("off by $40k on average"). RMSE punishes large errors more. Report MAE to humans; know what RMSE tells you.

Read: scikit-learn's [Getting Started](https://scikit-learn.org/stable/getting_started.html) and the [`train_test_split`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html) page.

## Build

Work in `work/02-first-model/`. Explore in a notebook, then put the final pipeline in `train.py`.

1. **Load and look.** Load the data as a DataFrame (`as_frame=True`). Print shape, `describe()`, and plot a histogram of the target.
   ✅ 20,640 rows, 8 features. The target histogram has a strange spike at the far right (5.0).

2. **Split first.** 60% train, 20% validation, 20% test, with `random_state=42`. From now on, the test set stays untouched until step 8.
   ✅ About 12,384 / 4,128 / 4,128 rows.

3. **Explore (train only).** Plot the target against `MedInc` (median income). Plot `Latitude` vs `Longitude` coloured by target.
   ✅ You can see income is strongly related to value, and the coastline appears in the map.

4. **Baseline.** Predict the training median for every validation row. Compute MAE and RMSE.
   ✅ MAE is roughly 0.9 (about $90k). Write it down. This is the number to beat.

5. **Linear regression.** Fit on train, score on validation.
   ✅ Clearly better than the baseline. MAE roughly 0.5–0.55.

6. **A tree ensemble.** Try `RandomForestRegressor` and `HistGradientBoostingRegressor`.
   ✅ MAE drops further, roughly 0.3–0.35.

7. **Look at errors.** For your best model, add the absolute error to the validation frame. Which rows have the biggest errors? Group the error by income bands (`pd.qcut(MedInc, 5)`). Where is the model worst?
   ✅ You can name one segment where the model is clearly worse, and guess why (hint: the spike at 5.0).

8. **Test once.** Retrain your chosen model on train+validation, score on test, and record the number.
   ✅ The test MAE is close to the validation MAE. If it's much worse, write down why you think that is.

9. **Write `NOTES.md`:** a results table (baseline, linear, forest, boosting; validation MAE and RMSE), the final test MAE, the error-by-segment finding, and a 3-sentence recommendation to the startup.

## Hints

<details><summary>Hint 1 — what is the spike at 5.0?</summary>

The values were capped at 5.0 ($500k) when the dataset was made. Any house worth more is recorded as 5.0. The model can't learn what's above the cap, so errors are large there. In a real project you'd ask whether to drop those rows, keep them, or flag that the model can't price expensive homes.
</details>

<details><summary>Hint 2 — tree models aren't much better than linear</summary>

Check that you didn't pass the target as a feature or scale the target by accident. Also check `random_state`. Tree ensembles should clearly win here because location matters in non-linear ways.
</details>

## Common mistakes

- Exploring the full dataset before splitting. Patterns you see in the test set influence your choices.
- Reporting the test score of every model and picking the best. That turns test into validation.
- Reporting only R². "R² = 0.8" means nothing to a business person. "Off by $33k on average" does.

## Done when

- [ ] Results table with a baseline and at least three models, on the same validation set.
- [ ] One test score, for one chosen model.
- [ ] An error breakdown by at least one segment.
- [ ] `train.py` reproduces your final numbers with one command.
- [ ] `NOTES.md` includes a recommendation a non-technical person could read.

## Stretch

Plot predicted vs actual for the test set. Add a feature (rooms per household, bedrooms per room) and see whether linear regression improves. Does the tree model care?

## Reflect

- Why do tree ensembles beat linear regression here? When might linear regression still be the better choice?
- Update the **Regression** section of your [decision map](../decision-map.md).
