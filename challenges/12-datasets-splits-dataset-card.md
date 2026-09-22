# Challenge 12 — Datasets, splits, and a dataset card

[Previous: Challenge 11 — Object detection on Pascal VOC 2007](11-object-detection-pascal-voc-2007.md) · [Next: Challenge 13 — Train a tokenizer and measure it](13-train-tokenizer-measure-it.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 12 — Datasets, splits, and a dataset card

- **Goal:** Reload Banking77 only through Hugging Face `datasets`, save it to disk, and write a dataset card.
- **Why an engineer needs it:** Teams share data through cards and saved splits, not through a notebook cell that half-ran. Schema drift is an incident.
- **What to build:** A loader that builds the Challenge 6 train/dev/test split with `datasets`, saves it with `save_to_disk`, and reloads it in a fresh process. A dataset card (local README) with: summary, source link, license pointer, splits and counts, label names, and known issues (short utterances, overlapping intents). A schema check on reload.
- **Skills practiced:** `datasets`, split serialization, dataset cards.
- **Stack and data:** `datasets`. [PolyAI/banking77](https://huggingface.co/datasets/PolyAI/banking77).
- **Difficulty:** core
- **Rough time:** 3–4 days
- **GPU:** CPU-ok
- **Acceptance criteria:**
  - A fresh process reloads the saved split and prints the same sizes and label names.
  - The dev/test ids match Challenge 6. Show a count of overlapping ids if you need to prove it.
  - The dataset card exists in the repo and lists the 77 labels.
- **Stretch goal:** Push the saved split to a personal or private dataset repo on the Hub, and load it back by repo id on a second machine or a fresh environment.
- **Builds on:** Challenge 6.
