# 40 — Kaggle NLP competition

**Phase 13 · Kaggle II** · ⏱ 1–2 weeks · 💻 Laptop or Kaggle GPU · Level: core

[← 39 Demo and monitoring](39-demo-and-monitoring.md) · [Index](../README.md) · [Next: 41 Capstone →](41-capstone.md)

## The problem

Time to run the whole workflow **on your own**, with less guidance. This challenge has no Build steps, only requirements. You decide the approach.

Competition: [Natural Language Processing with Disaster Tweets](https://www.kaggle.com/competitions/nlp-getting-started), a permanent "getting started" competition. Predict whether a tweet is about a real disaster. About 7,600 labelled training tweets; metric: **F1**.

If you prefer, choose any other open Kaggle text or image competition with a clear metric. The requirements are the same.

## Decide first

Write a one-page plan in `NOTES.md` **before any code**:

1. Problem type, metric, and what the metric rewards.
2. Your validation strategy, and how you'll avoid overfitting to the public leaderboard.
3. Baseline, and at least two stronger approaches you'll try, in order. Use your decision map.
4. Risks you expect in this dataset. (Read the Data tab carefully and look at 50 tweets first.)
5. A time budget.

## Learn

You already have what you need. Useful reminders:

- Challenge 08: the competition workflow, CV vs leaderboard.
- Challenges 15, 19, 20: text baselines and fine-tuning transformers.
- Challenge 28: comparing an LLM against a fine-tuned model.
- **F1 needs a threshold.** Choose it on out-of-fold predictions.
- Kaggle Notebooks give you free GPU hours per week. Useful for fine-tuning larger models.

## Requirements

1. **Data check:** duplicates and near-duplicates in train (including duplicates with *different* labels), the `keyword` and `location` columns, and the label balance. Write what you found and what you did about it.
2. **Validation:** stratified K-fold CV, with duplicate tweets kept in the same fold. The metric function is tested.
3. **Baseline:** TF-IDF + linear model, with CV F1. Submitted.
4. **At least two stronger approaches**, chosen by you, e.g. a fine-tuned DistilBERT/DeBERTa-small, an embedding + classifier model, or an LLM zero-/few-shot classifier (on a sample, if slow). CV F1 for each.
5. **Threshold** chosen on out-of-fold predictions.
6. **An experiment log:** every idea, its CV score, whether you submitted, and its public score. Submit only when CV improves.
7. **Error analysis:** 30 out-of-fold errors read and grouped.
8. **Final selection** by CV, with a written reason.
9. **Write-up** in `NOTES.md`, as if publishing it on Kaggle: approach, what worked, what didn't, CV vs leaderboard, and what you'd try next.

## Hints

<details><summary>Hint 1 — duplicate tweets with different labels</summary>

Some tweets appear several times with conflicting labels. Decide a rule (majority label, drop them, or keep them) and apply it only to training folds, never in a way that uses validation labels. Keep duplicates in the same fold, using `GroupKFold` on the normalized text, so CV isn't inflated.
</details>

<details><summary>Hint 2 — public leaderboard scores near 1.0</summary>

This competition's test labels have leaked publicly over the years, so some leaderboard entries are not real results. Ignore the top of the leaderboard; compare yourself with your own CV and with well-documented public notebooks.
</details>

## Common mistakes

- Starting to code before writing the plan.
- Choosing your final model by public leaderboard.
- Fine-tuning a big model before you have a baseline.

## Done when

- [ ] A plan written before code.
- [ ] Data issues found and handled.
- [ ] A duplicate-aware CV setup.
- [ ] A baseline and two stronger approaches with CV scores.
- [ ] An experiment log and an error analysis.
- [ ] A Kaggle-style write-up. (Publish it as a Kaggle notebook if you're comfortable; it's good for your profile.)

## Stretch

Enter a currently *active* Kaggle competition with your workflow, and finish it.

## Reflect

- Compare your plan with what you actually did. What did you get right up front? What did you only learn by doing?
- Update **Step 3** of your [decision map](../decision-map.md) with your competition checklist.
