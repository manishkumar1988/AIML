# Challenge 6 — Fine-grained intent classification

[Previous: Challenge 5 — Regression, heavy tails, and a model memo](05-regression-heavy-tails-model-memo.md) · [Next: Challenge 7 — Multi-label moderation and an operating point per label](07-multi-label-moderation-operating-point-label.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 6 — Fine-grained intent classification

- **Goal:** Classify banking requests into 77 intents and beat a serious linear baseline with an error read, not a demo.
- **Why an engineer needs it:** Support routing is a real product task. Fine-grained labels collide. Macro averages stop a model from looking good by nailing the three common intents.
- **What to build:** An intent classifier on [PolyAI/banking77](https://huggingface.co/datasets/PolyAI/banking77) (10,003 train / 3,080 test utterances, 77 intents). Carve a dev split from train only. Leave the official test split untouched until the end. Headline metric: macro-F1. Baselines: majority class, and TF-IDF (or a count vectorizer) plus a linear classifier. Then one small neural model you implement (embedding bag or a small LSTM). Both models share the dev/test split. Write the 15 most confused intent pairs from the test set and read 5 examples of each of the top 5 pairs.
- **Skills practiced:** Text splits, macro-F1, linear text baselines, confusion reading.
- **Stack and data:** scikit-learn and PyTorch. Hugging Face dataset [PolyAI/banking77](https://huggingface.co/datasets/PolyAI/banking77).
- **Difficulty:** core
- **Rough time:** 4–6 days
- **GPU:** CPU-ok
- **Acceptance criteria:**
  - Dev and test macro-F1 for the linear baseline and the neural model are in the log.
  - The vectorizer is fit on train text only.
  - The confusion writeup quotes real utterances, not only class ids.
  - The official test split was used once for the final table.
- **Stretch goal:** A per-intent table of support vs F1, and a note on whether the neural model’s wins are on rare intents or on common ones.
- **Builds on:** Challenges 1–3. Keep the same repo and log.
