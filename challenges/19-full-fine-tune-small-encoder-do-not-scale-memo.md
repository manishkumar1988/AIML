# Challenge 19 — Full fine-tune of a small encoder, and a do-not-scale memo

[Previous: Challenge 18 — Failure modes on a set you wrote](18-failure-modes-set-you-wrote.md) · [Next: Challenge 20 — QLoRA on a 1B-class model](20-qlora-1b-class-model.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 19 — Full fine-tune of a small encoder, and a do-not-scale memo

- **Goal:** Full-fine-tune DistilBERT for coarse NER on the Challenge 8 test ids, then write why that recipe stops at this size.
- **Why an engineer needs it:** Full fine-tune is the right tool for a 66M encoder and the wrong default for a multi-billion-parameter model on a personal GPU. You should be able to say why in bytes, not slogans.
- **What to build:**
  - Full-fine-tune `distilbert-base-uncased` for the 8 coarse Few-NERD tags, same test ids as Challenge 8. Headline: the same span F1 as Challenge 8.
  - A one-page memo, written with the formulas visible, that estimates memory for a full AdamW fine-tune of a 7B model (weights, fp32 master weights, two optimizer states, and a note about activations). Use that memo to state the rule you will follow in Challenge 20. Do not launch a 7B full fine-tune.
- **Skills practiced:** Token classification with the Trainer, span F1 reuse, memory arithmetic.
- **Stack and data:** `transformers`. [DFKI-SLT/few-nerd](https://huggingface.co/datasets/DFKI-SLT/few-nerd) supervised, same subset rule as Challenge 8. Base model `distilbert-base-uncased`.
- **Difficulty:** core
- **Rough time:** 1 week
- **GPU:** small GPU. Colab-or-Kaggle fallback. If you truly cannot get a GPU for this phase, full-fine-tune `prajjwal1/bert-tiny`, label the result as tiny-encoder, and still write the 7B memo.
- **Acceptance criteria:**
  - Span F1 for Challenge 8’s best model and for DistilBERT are in the log on the same test ids.
  - The memo states a personal-hardware rule: full fine-tune up to about 110M; above that, use a parameter-efficient method or a hosted API.
  - The 7B estimate shows the terms you added. A 7B training run was not started.
- **Stretch goal:** A learning-rate sweep of three values on dev span F1 only, with the test number reported for the winner alone.
- **Builds on:** Challenges 8 and 14.
