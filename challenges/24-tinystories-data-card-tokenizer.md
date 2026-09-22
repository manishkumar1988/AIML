# Challenge 24 — TinyStories data card and a tokenizer

[Previous: Challenge 23 — Grounded generation, scored apart from retrieval](23-grounded-generation-scored-apart-from-retrieval.md) · [Next: Challenge 25 — Train and evaluate an 8M–33M model](25-train-evaluate-8m-33m-model.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 24 — TinyStories data card and a tokenizer

- **Goal:** Freeze a train/holdout split of TinyStories and train a BPE tokenizer on train only.
- **Why an engineer needs it:** Small-model quality is capped by data leaks and by a vocabulary that was fit on the test stories. This is the same discipline as Challenge 13, on the corpus you will actually train on.
- **What to build:** Start from [roneneldan/TinyStories](https://huggingface.co/datasets/roneneldan/TinyStories). Prefer the official train and valid files named on that dataset card (`TinyStories-train` / `tinystories-valid`) if you download the source bundle. If you only use the Hub split, cut a holdout yourself with a fixed seed and record the ids. Exact-duplicate drop is required on train. Write a data card: counts, length distribution, dedup rule, holdout size. Train a BPE tokenizer on train only (reuse the Challenge 13 code path). Justify a vocab size with fertility on the holdout. Do not train on `Evaluation_prompts.yaml` from the dataset card.
- **Skills practiced:** Dedup, contamination control, tokenizer training on the target corpus.
- **Stack and data:** `datasets`, `tokenizers`. [roneneldan/TinyStories](https://huggingface.co/datasets/roneneldan/TinyStories).
- **Difficulty:** core
- **Rough time:** 4–6 days
- **GPU:** CPU-ok
- **Acceptance criteria:**
  - The data card and the holdout ids are in the repo.
  - A check shows zero exact string overlap between train and holdout after dedup.
  - The tokenizer reloads, and fertility (tokens per word) on the holdout is reported.
  - The note states that evaluation prompts were not in the tokenizer training data.
- **Stretch goal:** A second vocab size on the same holdout, and a one-paragraph choice of which one Challenge 25 will use, written before training.
- **Builds on:** Challenge 13.
