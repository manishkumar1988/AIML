# 25 — Instruction-tune a GPT

**Phase 7 · Build a language model from scratch** · ⏱ 1–2 weeks · 💻 Laptop · Level: core

[← 24 Pretrain a small language model](24-pretrain-slm.md) · [Index](../README.md) · [Next: 26 Run LLMs locally and by API →](26-run-llms.md)

## The problem

A pretrained model only continues text. Ask it "What is the capital of France?" and it might reply with three more quiz questions. Chat models are made by **instruction tuning**: fine-tuning on (instruction, response) pairs. You'll do that to GPT-2 and measure the difference.

Model: OpenAI GPT-2 (124M or 355M), loaded into your own architecture or via Raschka's code. Data: the 1,100 instruction examples in `~/projects/LLMs-from-scratch/ch07/01_main-chapter-code/instruction-data.json`.

## Decide first

1. What does the model need to learn from instruction data that it didn't learn in pretraining?
2. Should the loss include the instruction tokens, or only the response tokens? What would change?
3. How will you judge whether the tuned model's answers are "better"? Who or what grades them?

## Learn

- **SFT (supervised fine-tuning):** the same next-token training, but on formatted examples like:
  ```
  ### Instruction:
  Rewrite the sentence in passive voice.
  ### Input:
  The chef cooked the meal.
  ### Response:
  The meal was cooked by the chef.
  ```
- **Prompt template:** the model learns *this exact format*. You must use the same template at inference.
- **Masking the prompt:** often the loss is only computed on response tokens (set the label to −100 for instruction tokens), so the model learns to answer, not to write instructions.
- **Padding and end-of-text:** pad batches; the end-of-text token teaches the model when to stop.
- **Evaluation:** for open-ended answers, use human ratings on a sample, and/or an **LLM-as-judge**: a larger model scores each answer. A judge must be checked against your own ratings before you trust it.
- **Overfitting risk:** 1,100 examples is small. Train for only 1–3 epochs.

Read: Raschka chapter 7 at `~/projects/LLMs-from-scratch/ch07/01_main-chapter-code/ch07.ipynb`. Read it first, then build your own version. Copying the notebook isn't the exercise.

## Build

Work in `work/25-instruction-tuning/`. Install [Ollama](https://ollama.com/) for the judge (you'll use it heavily from Challenge 26).

1. **Split.** 85% train, 5% validation, 10% test (as in the book), seed 42. Save the split.

2. **Formatting.** Write `format_example(entry)` with the template above, and a collate function that pads, adds end-of-text, and masks padding (and optionally instruction tokens) with −100.
   ✅ Decode one batch: the text looks right and the masked positions are where you expect.

3. **Base model answers.** Load pretrained GPT-2 (355M if memory allows). Generate answers for 10 test instructions *before* tuning.
   ✅ Mostly not answers: rambling continuations or repeated instructions. Save them.

4. **Fine-tune.** 2 epochs, AdamW, lr ~5e-5, on `mps`. Log training and validation loss.
   ✅ Validation loss drops, then flattens. Write the epoch you'd stop at.

5. **Generate test answers** for all test instructions with the tuned model (fixed settings: greedy or temperature 0, record it).
   ✅ Most are now attempts at an answer, in the right format, and stop at a sensible point.

6. **Your ratings.** Rate 30 test answers yourself on a 0–100 scale using a rubric you write first (correct? follows the instruction? concise?).

7. **LLM judge.** Use a local model via Ollama (e.g. `llama3.1:8b` or `qwen2.5:7b`) to rate all test answers 0–100 against the reference answer. Raschka's `ollama_evaluate.py` shows one way.
   ✅ Compute the correlation between your 30 ratings and the judge's ratings on the same answers. Write whether you'd trust the judge.

8. **Compare.** Average judge score: base GPT-2 vs instruction-tuned, on the same test set.

9. **Failure read.** Find 5 tuned answers that are fluent but wrong. What kind of errors are they?

10. `NOTES.md`: before/after examples, loss curves, your ratings vs the judge, and what SFT did and didn't fix.

## Hints

<details><summary>Hint 1 — the model never stops generating</summary>

Check that end-of-text is appended to every training response and not masked out of the loss. At inference, stop when the model emits it, and set a max token limit.
</details>

<details><summary>Hint 2 — out of memory with the 355M model</summary>

Use batch size 4 and a max length of 256–512 tokens, or use the 124M model. Training a 355M model on 935 examples takes minutes on an M-series Mac in the book's benchmarks.
</details>

## Common mistakes

- A different prompt format at inference than in training.
- Trusting an LLM judge without checking it against your own ratings.
- Judging improvement from 3 hand-picked examples.

## Done when

- [ ] Base vs tuned answers for the same instructions.
- [ ] Validation loss curve with a chosen stopping epoch.
- [ ] 30 of your own ratings and their correlation with the judge.
- [ ] Average judge scores for base vs tuned.
- [ ] Five fluent-but-wrong answers analysed.

## Stretch

Preference tuning with **DPO**, following `~/projects/LLMs-from-scratch/ch07/04_preference-tuning-with-dpo/`. Does it change the style of answers (e.g. more polite or more concise)?

## Reflect

- Add "what pretraining gives you" and "what instruction tuning adds" to the **Language models from scratch** section of your [decision map](../decision-map.md).
