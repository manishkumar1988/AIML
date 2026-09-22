# Challenge 7 — Multi-label moderation and an operating point per label

[Previous: Challenge 6 — Fine-grained intent classification](06-fine-grained-intent-classification.md) · [Next: Challenge 8 — Named entity recognition at span level](08-named-entity-recognition-at-span-level.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 7 — Multi-label moderation and an operating point per label

- **Goal:** Score toxic-comment labels independently and choose a threshold per label on dev data.
- **Why an engineer needs it:** Moderation, medical coding, and tagging are multi-label. One global threshold is a product bug. Rare labels (`threat`, identity hate) disappear inside a micro average.
- **What to build:** A multi-label model on the [Jigsaw Toxic Comment Classification Challenge](https://www.kaggle.com/competitions/jigsaw-toxic-comment-classification-challenge) training file (`toxic`, `severe_toxic`, `obscene`, `threat`, `insult`, `identity_hate`). Split by comment id. Headline: per-label average precision, plus a micro and a macro summary. Baseline: a keyword or linear model. Pick a threshold per label on dev to hit a recall you declare in advance. Apply those thresholds once to test.
- **Skills practiced:** Multi-label metrics, per-label thresholds, rare-label behavior.
- **Stack and data:** scikit-learn. Kaggle competition [Jigsaw Toxic Comment Classification Challenge](https://www.kaggle.com/competitions/jigsaw-toxic-comment-classification-challenge).
- **Difficulty:** core
- **Rough time:** 1 week
- **GPU:** CPU-ok
- **Acceptance criteria:**
  - A six-row table: label, positive rate, average precision, dev-chosen threshold, test precision, test recall.
  - Thresholds were frozen before the test run.
  - The writeup says which label you would not automate.
- **Stretch goal:** Repeat the rare-label read on a stratified sample of [google/civil_comments](https://huggingface.co/datasets/google/civil_comments) and compare identity-mention slices using the identity fields that file actually contains. Pre-register the sample size.
- **Builds on:** Challenge 6.
