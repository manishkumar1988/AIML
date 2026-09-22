# Challenge 8 — Named entity recognition at span level

[Previous: Challenge 7 — Multi-label moderation and an operating point per label](07-multi-label-moderation-operating-point-label.md) · [Next: Challenge 9 — Image classification with noisy training labels](09-image-classification-noisy-training-labels.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 8 — Named entity recognition at span level

- **Goal:** Extract entities and score spans, on the supervised Few-NERD split.
- **Why an engineer needs it:** NER is the pattern behind PII detection, invoice parsing, and retrieval filters. Token accuracy is the wrong score.
- **What to build:** A tagger for [Few-NERD](https://huggingface.co/datasets/DFKI-SLT/few-nerd) supervised mode (the `supervised` train/dev/test files; official copy also on [thunlp/Few-NERD](https://github.com/thunlp/Few-NERD)). Use the 8 coarse types. If the full 131,767 training sentences are heavy, pre-register a subset and use the full dev/test or a pre-registered test subset. Headline metric: micro span-level F1 (entity type and character or token span must match). Implement the metric and unit-test it on at least five hand-built sentences (exact match, wrong type, partial overlap, missing span, extra span). Baseline: a gazetteer or a linear model on token features. Then one sequence model (CRF or a small BiLSTM). Read 30 errors and group them (boundary, type, missed, spurious).
- **Skills practiced:** IOB or span encoding, span F1, metric tests, error taxonomy.
- **Stack and data:** PyTorch or scikit-learn. Dataset [DFKI-SLT/few-nerd](https://huggingface.co/datasets/DFKI-SLT/few-nerd). If `load_dataset` fails on a deprecated loading script, use the GitHub `supervised` files and say so in the data note.
- **Difficulty:** core
- **Rough time:** 1 week
- **GPU:** CPU-ok on the pre-registered subset. Colab-or-Kaggle fallback for the full supervised train set.
- **Acceptance criteria:**
  - The span-F1 unit tests pass and are in the repo.
  - Baseline and sequence model are scored with that metric on the same test ids.
  - The error groups include counts, not only anecdotes.
  - The data note states whether you used the full supervised train set or a subset, and the subset rule was written first.
- **Stretch goal:** The same test ids scored with the 66 fine-grained tags, and a note on which coarse type hides the most fine-type errors.
- **Builds on:** Challenges 6–7.
