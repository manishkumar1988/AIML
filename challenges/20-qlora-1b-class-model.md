# Challenge 20 — QLoRA on a 1B-class model

[Previous: Challenge 19 — Full fine-tune of a small encoder, and a do-not-scale memo](19-full-fine-tune-small-encoder-do-not-scale-memo.md) · [Next: Challenge 21 — Ingestion and chunking](21-ingestion-and-chunking.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 20 — QLoRA on a 1B-class model

- **Goal:** Adapt a 0.5B–1.7B instruct model to dialogue summarization with QLoRA, and compare it with prompt-only and lead-3 baselines.
- **Why an engineer needs it:** Task adaptation on hardware you actually have is LoRA or QLoRA. Full fine-tune of these models is the wrong spend. ROUGE alone will lie; you need a reading check.
- **What to build:** QLoRA (`peft` + 4-bit loading) on either [Qwen/Qwen2.5-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct) or [HuggingFaceTB/SmolLM2-1.7B-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B-Instruct). CPU-only variant: QLoRA [SmolLM2-360M-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct) and label it CPU-scale. Data: [knkarthick/samsum](https://huggingface.co/datasets/knkarthick/samsum) (dialogue, summary; about 16k conversations). Prove the adapter can learn by overfitting 32 train examples, then train on the real train split and stop using the validation split. On the official test split report:
  - ROUGE-L for lead-3 (first three dialogue turns, or a rule you define before scoring), prompt-only, and QLoRA.
  - A 30-example side-by-side you read, tagged faithful / extra fact / missing fact.
  Record rank, target modules, 4-bit on or off, and peak GPU memory.
- **Skills practiced:** QLoRA, generation metrics, faithfulness reads, baseline discipline.
- **Stack and data:** `transformers`, `peft`, `bitsandbytes`. Dataset [knkarthick/samsum](https://huggingface.co/datasets/knkarthick/samsum).
- **Difficulty:** core
- **Rough time:** 1–2 weeks
- **GPU:** small GPU. Colab-or-Kaggle fallback (a free T4 is the intended machine for the 1.5B/1.7B run).
- **Acceptance criteria:**
  - The 32-example overfit is logged separately and is not the test score.
  - Test ROUGE-L for all three systems is in one table.
  - The 30-example read has counts for extra facts, and the writeup says whether ROUGE and the read agree.
  - Peak memory is recorded. Full fine-tune of the 1.5B/1.7B model was not run.
  - The Challenge 19 rule is cited in the README in one sentence.
- **Stretch goal:** The same protocol on `Qwen/Qwen2.5-3B-Instruct` in 4-bit, only on a free T4/L4-class GPU, with the memory number. If it does not fit, stop and record the OOM. That record counts.
- **Builds on:** Challenges 15, 16, and 19.
