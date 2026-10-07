# 32 — LoRA fine-tuning

**Phase 10 · Fine-tuning LLMs** · ⏱ 1–2 weeks · 💻 Laptop (MLX) or Colab (QLoRA) · Level: core

[← 31 Evaluate RAG answers](31-evaluate-rag.md) · [Index](../README.md) · [Next: 33 Prompt vs RAG vs fine-tune →](33-prompt-rag-or-finetune.md)

## The problem

Your Challenge 27 extraction pipeline works well with a 7B model, but it's slow and needs a big prompt with 77 intents in it. Could a **0.5B model, fine-tuned for this one job**, match it, at a fraction of the cost and latency?

This is a very common real-world pattern called **distillation**: use a big model (the teacher) to label lots of data, check the labels, then fine-tune a small model (the student) on them.

Data: Banking77 training messages (to be labelled by the teacher), and your hand-labelled validation and test sets from Challenge 27.

## Decide first

1. Full fine-tuning updates every weight. Estimate the memory needed to fully fine-tune a 7B model with Adam (hint: weights + gradients + two optimizer states). Does it fit on your Mac?
2. What does LoRA change so that fine-tuning fits in much less memory?
3. If the teacher makes mistakes in its labels, what will the student learn?
4. What must be true before you'd ship the student instead of the teacher?

## Learn

- **Memory for full fine-tuning (rule of thumb):** with mixed precision and Adam, about **16 bytes per parameter** (weights, gradients, fp32 master copy, two Adam states), *plus* activations. 7B × 16 bytes ≈ 112 GB. That's why full fine-tuning of large models isn't done on a laptop.
- **LoRA (low-rank adaptation):** freeze the original weights. Next to selected weight matrices (usually attention projections), add two small matrices A (d×r) and B (r×d) with a small **rank** r (e.g. 8 or 16). Only A and B are trained, typically well under 1% of the parameters. The result is a small **adapter** file you can load on top of the base model, or merge into it.
- **QLoRA:** load the frozen base model in 4-bit to save even more memory, and train LoRA adapters on top. The standard library (`bitsandbytes`) needs an NVIDIA GPU, so use Colab for QLoRA.
- **On your Mac: [MLX-LM](https://github.com/ml-explore/mlx-lm)** (Apple's framework) runs LoRA fine-tuning natively and quickly on Apple Silicon.
- **Key settings:** rank r, which layers get adapters, learning rate (1e-4 to 2e-4 is common for LoRA), number of iterations. Watch validation loss for overfitting.
- **Chat template:** format training examples with the model's own chat template, exactly as you'll call it at inference.

Read: the [LoRA paper](https://arxiv.org/abs/2106.09685) abstract and figure 1; Sebastian Raschka's [Practical Tips for Finetuning LLMs Using LoRA](https://magazine.sebastianraschka.com/p/practical-tips-for-finetuning-llms); and the MLX-LM [LoRA documentation](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md).

## Build

Work in `work/32-lora/`. `uv add mlx-lm`.

1. **Memory memo.** In `NOTES.md`, write out the memory estimate for full fine-tuning at 0.5B, 1.5B and 7B (show the formula), and the trainable-parameter count for LoRA rank 8 on a 0.5B model's attention projections. Write your rule: when full fine-tuning, when LoRA, when QLoRA.

2. **Teacher labels.** Run your best Challenge 27 setup (7B, schema-constrained) on 2,000 Banking77 *training* messages. Keep only outputs that pass Pydantic validation. Hand-check 50 at random.
   ✅ Teacher accuracy on your 50-sample check is written down. That's roughly the ceiling for the student.

3. **Training data.** Convert to MLX-LM's chat format (`{"messages": [...]}` per line): system prompt (short, *without* the 77-intent list), user message, assistant = the JSON. Create `train.jsonl` and `valid.jsonl` (hold out 10% of the teacher-labelled data).

4. **Student baselines (no fine-tuning).** `Qwen/Qwen2.5-0.5B-Instruct` (or a current equivalent) on your Challenge 27 **validation** set: (a) short prompt, (b) full prompt with the intent list and few-shot examples. Same metrics as Challenge 27.
   ✅ The un-tuned 0.5B model is clearly worse than the 7B teacher.

5. **LoRA fine-tune.** `mlx_lm.lora --model <base> --train --data <dir> ...` with rank 8, ~600–1,000 iterations. Record peak memory and training time.
   ✅ Training and validation loss both fall. Write the iteration where validation loss stops improving.

6. **Evaluate the student** on the validation set with the short prompt.
   ✅ A large jump over the un-tuned 0.5B model. Compare with the teacher.

7. **One ablation, chosen on validation:** rank 4 vs 16, *or* 500 vs 2,000 teacher examples.

8. **Test once.** Teacher (7B prompt), 0.5B prompt-only, 0.5B LoRA, all on your Challenge 27 test set: JSON validity, per-field accuracy, intent accuracy, and latency per message.

9. **Errors.** Does the student copy the teacher's mistakes? Compare 10 student errors with the teacher's output on the same messages.

10. `NOTES.md`: the memory memo, the results table, the ablation, and a ship / don't ship decision for the student.

## Hints

<details><summary>Hint 1 — the fine-tuned model outputs extra text around the JSON</summary>

Check the training format: the assistant turn must be *only* the JSON. Use the same chat template and system prompt at inference as in training. Schema-constrained decoding can still be applied on top.
</details>

<details><summary>Hint 2 — using Colab instead (QLoRA)</summary>

Use `transformers` + `peft` + `bitsandbytes` + `trl`'s `SFTTrainer` with the same JSONL data and a 4-bit base model. Save the adapter and evaluate it in the same notebook, or merge and download.
</details>

## Common mistakes

- Training on teacher labels without checking their quality.
- Different prompt format at inference than in training.
- Evaluating on teacher-labelled data instead of your hand-labelled test set.
- Choosing rank or iterations using the test set.

## Done when

- [ ] A memory memo with formulas and your rule.
- [ ] Teacher labels with a measured quality check.
- [ ] Un-tuned vs LoRA student on validation, plus one ablation.
- [ ] One test table: teacher vs student (quality and latency).
- [ ] A ship / don't ship decision.

## Stretch

Run the same fine-tune as QLoRA on Colab with a 1.5B model. Does the bigger student close the gap with the teacher?

## Reflect

- Fill in "LoRA vs full fine-tune" in the **Fine-tuning** section of your [decision map](../decision-map.md).
