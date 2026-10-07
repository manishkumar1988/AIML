# 01 — Problem framing

**Phase 0** · ⏱ 3–5 hours · 💻 Laptop (no code) · Level: core — the most important challenge

[← 00 Workspace setup](00-workspace-setup.md) · [Index](../README.md) · [Next: 02 First end-to-end model →](02-first-end-to-end-model.md)

## The problem

At work, nobody says "train a gradient-boosted classifier with PR-AUC as the metric." They say "can we use AI to catch bad orders?" Your first job is turning that sentence into a problem you can solve and measure. You get this wrong more often than you get the model wrong.

You'll do this challenge three times: now, after Challenge 18, and after Challenge 37. Keep this first attempt. Watching your answers improve is part of the point.

## Decide first

There's no "decide first" here. The whole challenge is deciding.

## Learn

For any request, answer these six questions:

1. **Input → output.** What exactly goes in, and what comes out? Be concrete: "one transaction row → yes/no fraud", not "data → insights".
2. **Problem type.** Regression, classification, imbalanced classification, clustering, anomaly detection, forecasting, ranking/search, image classification, detection, segmentation, text classification, extraction, generation, RAG, agent. See [Step 1 of the decision map](../decision-map.md).
3. **Labels.** Do examples of the right answer exist? How many? Who made them? If none exist, how could you get some?
4. **Baseline.** The dumbest thing that could work: predict the average, the most common class, a keyword rule, "same as last week", a plain search box.
5. **Metric.** How would the *business* judge success? Which mistake is worse: a false alarm, or a miss?
6. **Is ML even needed?** Sometimes a rule, a SQL query, or a search engine is the right answer.

Read: Google's [Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml), Rules #1–#4 only. Rule #1 is "don't be afraid to launch a product without machine learning."

## Build

Create `work/01-framing/NOTES.md`. For each of the 25 requests below, fill in a block like this:

```
### 7. Spotting cracked parts on a production line
- Input → output:
- Problem type:
- Labels:
- Baseline:
- Metric (and which mistake is worse):
- Is ML needed? Why?
```

**The 25 requests**

1. An online store wants to predict how many units of each product will sell next week.
2. A bank wants to flag credit-card transactions that might be fraud, for a team that can review 200 a day.
3. A real-estate site wants to suggest a listing price for a house from its details.
4. A telecom company wants to know which customers are likely to cancel next month, to offer them a discount.
5. A marketing team wants to "understand our different types of customers." They have purchase history but no customer categories.
6. A support team receives 5,000 emails a day and wants each one routed to one of 30 departments.
7. A factory wants to spot cracked parts from photos on a production line. Cracks are rare.
8. A hospital wants to outline tumors in MRI scans, pixel by pixel, to help radiologists.
9. A warehouse wants to count and locate boxes on shelves from camera images.
10. A legal team wants to ask questions about 3,000 internal contracts and get answers with the clause cited.
11. An HR team wants to pull name, email, years of experience, and skills out of PDF résumés into a spreadsheet.
12. A news site wants to show "related articles" under each article.
13. A server team wants to be alerted when a machine "behaves strangely." They have metrics but no history of labeled incidents.
14. A company wants a chatbot that answers questions about its HR policies.
15. A travel company wants an assistant that can search flights, check the user's calendar, and book a trip after the user confirms.
16. An app wants to block toxic comments. Some comments are toxic in several ways at once (insult *and* threat).
17. A bank wants product descriptions rewritten in its brand voice. It has 2,000 examples of approved rewrites.
18. A retailer wants to know whether a product review is positive or negative.
19. A city wants to predict hourly bike-rental demand to plan bike redistribution.
20. A company wants to know which of its 50 support macros to suggest to an agent while they type a reply.
21. A school wants to detect whether essays were copied from each other.
22. A game company wants to generate new background art in the style of its existing game.
23. A company wants to translate its help center into Spanish.
24. A manager wants a weekly report of "how many tickets were opened per category." Tickets already have a category field.
25. A clinic wants to predict a patient's risk of readmission within 30 days, for use in care planning.

✅ Checkpoint: every request has all six lines filled in. Leaving "not sure" is allowed, but write *why* you're not sure.

**Then** open the reference answers below and compare. For each request where yours differed, write one line on what you missed. Don't erase your answer. Write the correction next to it.

## Hints

<details><summary>Hint — I don't know the problem types yet</summary>

That's expected. Use the table in [the decision map](../decision-map.md) and guess. The point is to notice what you don't know yet, so you recognize it when a later challenge teaches it.
</details>

<details><summary>Reference answers (open only after you've written all 25)</summary>

Short versions. Yours can differ and still be reasonable. Focus on the *reasoning*.

1. Time series forecasting (product × week → units). Labels: past sales. Baseline: same week last year, or last 4-week average. Metric: MAE or WAPE. Overstock vs stockout cost decides which direction of error is worse.
2. Imbalanced classification. Labels: confirmed fraud cases. Baseline: rules (amount > X, new country). Metric: precision in the top 200 per day (capacity!). Missing fraud costs money; false alarms waste reviewer time.
3. Regression. Baseline: median price per neighborhood. Metric: MAE in currency, or percentage error.
4. Classification (often imbalanced). Baseline: "customers with a complaint last month." Metric: precision/recall at the number of discounts you can afford. Note it's really about *who would respond to the discount*, which is harder (uplift modeling).
5. Clustering. No labels. Baseline: simple segments by spend and frequency (RFM). Success: segments the team can act on. Hard to measure with a single number.
6. Text classification (30 classes). Labels: past routed emails. Baseline: keyword rules or TF-IDF + logistic regression. Metric: macro-F1 plus accuracy; check which departments get confused.
7. Image classification or anomaly detection, imbalanced. If there are few crack photos, consider anomaly detection trained on good parts only. Metric: recall on cracks at an acceptable false-alarm rate. A miss is worse.
8. Segmentation. Labels: radiologist outlines (expensive). Metric: Dice/IoU. Human in the loop. Not a fully automatic decision.
9. Object detection. Metric: mAP; for counting, count error. Baseline: a pretrained detector.
10. RAG. Labels: you'll need to write test questions with known answers. Metric: retrieval recall@k, plus answer correctness and citation correctness.
11. Extraction (structured output) from documents. Baseline: regex for email; an LLM with a schema for the rest. Metric: field-level accuracy on a hand-labeled set.
12. Similarity search / recommendation with embeddings. Baseline: same category + recent. Metric: click-through in an A/B test; offline, judged relevance.
13. Anomaly detection, unsupervised. Baseline: thresholds on each metric (mean ± 3 std). Metric: hard without labels. Have engineers review alerts and track precision.
14. RAG over the policy documents (not fine-tuning: the policies change). Metric: answer correctness and "I don't know" rate on a test set you write.
15. Agent with tools (search, calendar, booking) and a **human confirmation step** before booking. Metric: task success rate; never book without confirmation.
16. Multi-label text classification. Metric: per-label precision/recall with a threshold per label.
17. Fine-tuning (style transfer with plenty of examples), or few-shot prompting first as the baseline. Metric: human ratings, plus checks that facts weren't changed.
18. Text classification (sentiment). Baseline: TF-IDF + logistic regression, or a pretrained sentiment pipeline. Metric: accuracy or F1.
19. Time series forecasting. Baseline: same hour last week. Metric: MAE. Weather and holidays are features you'd know in advance (or as a forecast).
20. Ranking / retrieval (or classification over 50 macros). Embeddings of the draft vs the macros. Metric: was the used macro in the top 3?
21. Similarity / near-duplicate detection. Embeddings or n-gram overlap (MinHash). No training needed for a baseline.
22. Image generation (diffusion fine-tuning, e.g. LoRA). Metric: human review. Also licensing questions.
23. Use an existing translation model or LLM. Don't train one. Metric: human review on a sample; glossary of fixed terms.
24. **Not ML.** It's a SQL `GROUP BY`.
25. Classification with probability calibration. High stakes: fairness checks, explanations, a human decides. Metric: calibrated risk + recall at a chosen risk level.
</details>

## Common mistakes

- Jumping straight to "use an LLM" or "use deep learning." Ask what the baseline is first.
- Using accuracy for rare events (2, 7, 13).
- Treating time series as normal regression with a random split (1, 19).
- Missing that the answer is "not ML" (24) or "use an existing model" (23).
- Choosing fine-tuning when the information changes often (14). RAG handles changing facts; fine-tuning teaches style and skills.

## Done when

- [ ] All 25 requests are framed in `work/01-framing/NOTES.md`.
- [ ] Each difference from the reference answers has a one-line correction.
- [ ] You've written the 3 lessons that surprised you most at the top of the notes.

## Stretch

Write 5 requests of your own from an industry you know, and frame them.

## Reflect

- Which problem types were you least sure about? Those are the challenges to pay most attention to.
- Fill in Step 1 of [the decision map](../decision-map.md) in your own words.
