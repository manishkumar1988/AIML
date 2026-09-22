# Challenge 14 — Trainer, pipeline, and a model card

[Previous: Challenge 13 — Train a tokenizer and measure it](13-train-tokenizer-measure-it.md) · [Next: Challenge 15 — Run an SLM and measure it](15-run-slm-measure-it.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 14 — Trainer, pipeline, and a model card

- **Goal:** Fine-tune DistilBERT on the Challenge 6 split, beat that challenge’s best macro-F1, and ship a local pipeline plus a model card.
- **Why an engineer needs it:** The Trainer is the default team tool. It is only useful if it beats a baseline on a frozen split and if someone else can load the pipeline.
- **What to build:** Fine-tune `distilbert-base-uncased` with the Trainer on the Challenge 12 saved split. Early-stop on dev macro-F1. Publish one test macro-F1. Run `pipeline("text-classification")` on 20 utterances that Challenge 6 got wrong, and record wins and remaining failures. Write a model card: intended use, eval numbers, label map, and limitations. If you can create a free Hub account, push the model and load it back by repo id. If you cannot, the local card plus a local load counts, and the push stays the stretch goal.
- **Skills practiced:** Trainer, metrics callback, pipelines, model cards, Hub upload.
- **Stack and data:** `transformers`, `datasets`, `evaluate`. Base model `distilbert-base-uncased`. Data from Challenge 12.
- **Difficulty:** core
- **Rough time:** 4–6 days
- **GPU:** small GPU. Colab-or-Kaggle fallback. A `prajjwal1/bert-tiny` run may debug the loop on CPU and does not replace the DistilBERT test number.
- **Acceptance criteria:**
  - Test macro-F1 is in the log next to the Challenge 6 number, same test ids.
  - The pipeline returns labels from the 77-intent map, checked on 5 known examples.
  - The model card states a use you do not recommend.
  - Dev, not test, was used for early stopping.
- **Stretch goal:** The Hub model loads in a clean environment with `pipeline(..., model="your-repo")` and reproduces the 5 known examples.
- **Builds on:** Challenges 6 and 12.
