# 08 — Your first Kaggle competition

**Phase 2 · Kaggle I** · ⏱ 1–2 weeks · 💻 Laptop · Level: core

[← 07 Tune, validate, explain](07-tune-validate-explain.md) · [Index](../README.md) · [Next: 09 Neural net in NumPy →](09-neural-net-from-scratch.md)

## The problem

Kaggle is where many people practise and get noticed. It also teaches a trap that every ML engineer meets at work: **overfitting to a leaderboard**. You'll join a live competition, build a solid local validation setup, and learn to trust it more than the public leaderboard.

Competition: the current [Kaggle Playground Series](https://www.kaggle.com/competitions?searchQuery=playground+series) episode. A new tabular competition starts most months. Pick one that's open and **tabular** (classification or regression). If none is open, use [Titanic](https://www.kaggle.com/competitions/titanic) for mechanics, then the most recent finished Playground episode with late submission.

## Decide first

1. Read the competition's **Overview → Evaluation** page. What's the metric? Does it reward probabilities or hard labels?
2. The public leaderboard is scored on part of the test set. Why might the model that's #1 on the public leaderboard fall on the private one?
3. What would you use as a baseline?

## Learn

- **How a competition works:** `train.csv` (with labels), `test.csv` (no labels), `sample_submission.csv` (the format). You submit predictions; Kaggle scores them on hidden labels.
- **Public vs private leaderboard:** the public score uses a slice of test; the final ranking uses the rest. Choosing models by public score overfits to that slice. This is called "leaderboard probing" or a "shake-up" when it backfires.
- **Local CV is your real compass.** Build a K-fold CV that matches the metric. If your CV and the public leaderboard move together, good. If they disagree, trust CV (especially with a small public slice).
- **Out-of-fold (OOF) predictions:** each training row gets a prediction from the fold model that didn't see it. Useful for checking the metric and for blending.
- **Playground data is synthetic**, generated from a real dataset. Sometimes adding the original dataset helps. Check the discussion forum.
- **Gradient boosting libraries:** LightGBM, XGBoost and CatBoost dominate tabular Kaggle. Start with one.

Read: the competition's Overview, Data and Evaluation pages, and the top-voted "getting started" notebook in its Code tab. Read for ideas, but write your own code.

## Build

Work in `work/08-kaggle-playground/`. Set up the [Kaggle API](https://github.com/Kaggle/kaggle-api) to download data (`uv add kaggle`; your API token lives in `~/.kaggle/`, never in the repo).

1. **Rules and data.** Accept the rules, download the data, read the metric definition.
   ✅ You can state the metric and the submission format in one line each.

2. **EDA.** Target distribution, missing values, number of categorical vs numeric columns. Do train and test features look alike? (Plot one or two feature distributions for both.)

3. **Metric function.** Implement the competition metric yourself (or use the matching scikit-learn function) and test it on a tiny hand-made example.
   ✅ Your function gives the value you expect on the toy example.

4. **CV setup.** 5-fold (stratified for classification), fixed seed. Write a function `run_cv(model, X, y) -> (mean, std, oof_preds)`.

5. **Baseline.** A trivial or linear model. CV score. Submit it.
   ✅ Your first submission appears on the leaderboard. Record CV and public score side by side in a log table.

6. **LightGBM** (`uv add lightgbm`) with default-ish parameters. CV, submit.
   ✅ CV improves over baseline; the public score improves similarly.

7. **Improve, with discipline.** Try at most 5 ideas (feature engineering, encoding categoricals, tuning, adding the original dataset, a second model). For each: CV score first, and **submit only if CV improves**. Log every idea, including failures.

8. **Blend.** Average the predictions of your two best models. Check the OOF score of the blend before submitting.

9. **Pick final submissions** using CV, not public score. Write down why.

10. **After the competition closes** (or if it already has): compare your CV, public and private scores. Did trusting CV pay off?

## Hints

<details><summary>Hint 1 — categorical columns in LightGBM</summary>

Convert them to pandas `category` dtype. LightGBM can then handle them natively. For other models, use one-hot or target encoding *inside* the CV folds.
</details>

<details><summary>Hint 2 — CV and leaderboard disagree</summary>

Check that your CV uses the same metric, the same kind of prediction (probability vs label), and stratification. A small public leaderboard slice is noisy. A difference in the 3rd decimal place means little.
</details>

## Common mistakes

- Submitting 30 times a day and keeping whatever scores best publicly.
- Target encoding using the full training set (it leaks the target into the features). Do it inside each fold.
- Copying a public notebook and calling it your result.

## Done when

- [ ] A metric function tested on a toy example.
- [ ] A CV function, and a log table: idea, CV mean ± std, public score, kept or not.
- [ ] At least 3 submissions, each justified by CV.
- [ ] A final choice made by CV, with the reason written down.
- [ ] `NOTES.md` with your CV vs leaderboard story.

## Stretch

Read the top 3 solution write-ups after the competition ends (Discussion tab). Write down one idea you'd never have thought of.

## Reflect

- Write the milestone entry in `work/milestones.md`: what you learned about classical ML in Challenges 02–08.
- Add a "Kaggle workflow" note to your [decision map](../decision-map.md), under Step 3.
