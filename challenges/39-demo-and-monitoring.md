# 39 — Demo and monitoring

**Phase 12 · Deployment** · ⏱ 1 week · 💻 Laptop · Level: core

[← 38 Serve a model](38-serve-a-model.md) · [Index](../README.md) · [Next: 40 Kaggle NLP competition →](40-kaggle-nlp.md)

## The problem

Two things happen after launch:

1. Stakeholders want to **try** the system themselves, without curl.
2. The world changes. The bank launches a new product, customers start writing about it, and the model, trained on old messages, quietly gets worse. Nobody notices unless something is **watching**.

You'll put a demo UI on your service, log every prediction, and build a simple drift check, then simulate a drift and see whether your check catches it.

## Decide first

1. In production you don't have labels for new messages. How could you notice the model getting worse anyway?
2. What would you log for each prediction? What should you *not* log (privacy)?
3. What would trigger an alert, and who would act on it?

## Learn

- **Gradio** builds a web UI around a Python function in a few lines. Good for demos and internal tools.
- **Prediction logging:** timestamp, model version, input (or a hash/redacted version if it's sensitive), prediction, confidence, latency, and user feedback if available.
- **Monitoring without labels:**
  - **Confidence drift:** the average confidence drops, or the share of `needs_review` rises.
  - **Prediction drift:** the distribution of predicted intents shifts.
  - **Input drift:** new inputs look different from training inputs, e.g. their embeddings are far from the training embeddings, or message length changes.
- **Population Stability Index (PSI)** compares two distributions (e.g. confidence scores this week vs the reference week). Rule of thumb: < 0.1 small change, 0.1–0.25 moderate, > 0.25 large.
- **Feedback loop:** a thumbs up/down button collects (some) labels from real use, so you can measure accuracy and build the next training set.
- **Alerts must be actionable:** each alert says what changed and what to look at.

Read: Gradio [Quickstart](https://www.gradio.app/guides/quickstart), and Evidently AI's [What is data drift](https://www.evidentlyai.com/ml-in-production/data-drift) guide.

## Build

Work in `work/39-monitoring/`. `uv add gradio`.

1. **Demo UI.** A Gradio app that calls your Challenge 38 API: a text box → top-3 intents with confidences, a `needs_review` badge, and 👍/👎 buttons.
   ✅ Works in the browser; feedback clicks are recorded.

2. **Prediction log.** Log every prediction from the API to SQLite: timestamp, model version, a redacted copy of the text (mask digits and emails), predicted intent, confidence, latency, and feedback (when given).
   ✅ After 20 demo uses, the table has 20 rows. Redaction works on a message containing a card number.

3. **Reference window.** Send your Banking77 validation messages through the API as "week 0" traffic. Save the confidence distribution, intent distribution, and the mean embedding (Challenge 21 model) as the reference.

4. **Simulate a normal week.** Send the Banking77 test messages as "week 1."
   ✅ PSI on confidence < 0.1; no alert.

5. **Simulate drift.** Create "week 2" traffic: 70% test messages + 30% messages about something the model has never seen (write 50–100 messages about, e.g., a new crypto wallet feature, or reuse unrelated text such as IMDB review sentences).
   ✅ Your drift report flags it: confidence PSI goes up, `needs_review` rate rises, and the embedding distance from the reference increases.

6. **Drift report.** `uv run python -m drift_report --week 2` prints: the metrics vs reference, PSI values, the top intents whose share changed, and 10 example low-confidence messages. Define alert thresholds and write the message an on-call person would see.

7. **Feedback accuracy.** Give 👎 to 15 wrong predictions in the demo. Show how the report would estimate accuracy from feedback, and explain why that estimate is biased (who clicks feedback?).

8. `NOTES.md`: what you log and why, the drift experiment results, your alert rules, and a runbook: "when this alert fires, do this."

## Hints

<details><summary>Hint 1 — computing PSI</summary>

Bin both distributions using the reference's quantiles (e.g. 10 bins). PSI = Σ (actual% − expected%) × ln(actual% / expected%). Add a tiny epsilon to avoid dividing by zero.
</details>

## Common mistakes

- Logging raw sensitive text (card numbers, names) without redaction.
- Monitoring only uptime and latency, not model behaviour.
- Alert thresholds so sensitive they fire every day, so people ignore them.

## Done when

- [ ] A Gradio demo with feedback.
- [ ] Redacted prediction logging.
- [ ] A reference window and a drift report.
- [ ] A simulated normal week (no alert) and drift week (alert).
- [ ] Alert rules and a runbook.

## Stretch

Deploy the Gradio demo (with the model inside it) to a free [Hugging Face Space](https://huggingface.co/spaces) and share the link in your portfolio.

## Reflect

- Fill in "what I monitor" in the **Deployment** section of your [decision map](../decision-map.md).
