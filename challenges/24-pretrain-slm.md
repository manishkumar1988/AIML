# 24 — Pretrain a small language model

**Phase 7 · Build a language model from scratch** · ⏱ 2 weeks · 💻 Laptop (long runs) or Colab · Level: stretch

[← 23 GPT from scratch](23-gpt-from-scratch.md) · [Index](../README.md) · [Next: 25 Instruction-tune a GPT →](25-instruction-tuning.md)

## The problem

You'll pretrain your own small language model (SLM), with your own tokenizer, on a dataset designed so that small models can learn to write coherent English: TinyStories. The [TinyStories paper](https://arxiv.org/abs/2305.07759) showed that models with only 10–30M parameters can write simple, grammatical stories. You'll reproduce a version of that on your laptop.

This is "LLM from scratch" at a scale you can afford. Real LLMs follow the same recipe with thousands of GPUs. Knowing the recipe is the point.

Data: TinyStories `train` and `validation` splits, and your tokenizer from Challenge 22.

## Decide first

1. Your GPT from Challenge 23 used characters. What changes when you switch to your BPE tokenizer?
2. How would you know the model is learning *language*, not just memorizing stories?
3. You can only afford a few hours of training. More parameters, or more tokens? (Look up "Chinchilla scaling" after you answer.)
4. Before looking at any outputs, what would a "good" story from a 20M-parameter model look like? Write the rubric now.

## Learn

- **Pretraining data pipeline:** tokenize all text once, join stories with `<|endoftext|>`, save as one big array of token ids (`np.uint16` if vocab < 65,536). Training samples random windows of `block_size` tokens.
- **Perplexity** = exp(average validation loss). "How many tokens is the model choosing between, on average?" Only comparable between models **with the same tokenizer** and the same validation text.
- **Token budget:** a rough rule from the Chinchilla paper is ~20 tokens per parameter for compute-efficient training. A 15M model → about 300M tokens. On a laptop you may train less. Record what you used.
- **Learning-rate schedule:** warmup (rise for a few hundred steps) then cosine decay. Standard for transformers.
- **Checkpoints:** save model, optimizer state, step and config, so you can resume.
- **Sampling settings:** temperature, top-k, top-p. Record them with every sample you show.
- **Evaluation of generations:** a rubric written *before* you see samples, scored on fixed prompts. Otherwise you'll grade generously.

Read: the [TinyStories paper](https://arxiv.org/abs/2305.07759), sections 1–3. Raschka chapter 5 (`~/projects/LLMs-from-scratch/ch05/01_main-chapter-code/`) covers the training loop, evaluation and sampling. Skim `gpt_train.py`.

## Build

Work in `work/24-pretrain/`.

1. **Rubric first.** Write `rubric.md`: 3–4 criteria (grammar, coherence, stays on topic, story has an ending), each scored 1–5, with an example of a 1 and a 5. Write 20 story-opening prompts. **Commit before step 6.**

2. **Tokenize.** Encode the training split (or a large subset) and the full validation split with your Challenge 22 tokenizer. Save as `.bin` files with `np.memmap`.
   ✅ You know the number of training tokens. Write it.

3. **Baseline perplexity.** Compute the perplexity of a unigram model (token frequencies from train) on validation.
   ✅ A large number. That's what your model has to beat.

4. **Model config.** Reuse your Challenge 23 GPT. Target ~15–25M parameters (e.g. 8 layers, 8 heads, width 384–512, block size 256). Write the parameter count *before* training.

5. **Learning-rate sanity sweep.** Three short runs (e.g. 500 steps) with lr 1e-3, 6e-4, 3e-4. Pick the best by validation loss.

6. **Main run.** Warmup + cosine schedule, AdamW, weight decay 0.1, gradient clipping 1.0. Log training and validation loss, and tokens per second. Save checkpoints. Let it run for hours (overnight is fine).
   ✅ Validation loss keeps falling; final perplexity far below unigram. Write tokens/sec and total tokens seen.

7. **Reload and generate.** In a fresh process, load the checkpoint and generate stories for your 20 prompts (temperature 0.8, top-k 50, record the settings).
   ✅ Most stories are grammatical and loosely coherent, with recurring characters.

8. **Score with your rubric.** Fill in the scores for all 20. Average per criterion.

9. **Compare with a published model.** Generate for the same prompts with [roneneldan/TinyStories-33M](https://huggingface.co/roneneldan/TinyStories-33M) and score them with the same rubric.
   ✅ A side-by-side table. Note: you **cannot** compare perplexities directly, because the tokenizers differ. Write this in your notes.

10. **Memorization check.** For 5 of your generated stories, search the training text for their longest 8-word phrase. Are they copied?

11. `NOTES.md`: config, token budget, loss curves, perplexity vs unigram, rubric results vs TinyStories-33M, and an honest paragraph on what your model can and can't do.

## Hints

<details><summary>Hint 1 — tokenizing 2 million stories is slow</summary>

Use `tokenizer.encode_batch` on batches of 1,000 stories, and write to the memmap as you go. Or tokenize a 500,000-story subset first, then add more if training gets that far.
</details>

<details><summary>Hint 2 — training will take days</summary>

Shrink the model (6 layers, width 288), or reduce the block size to 128, or use Colab for the main run. A smaller model trained on more tokens usually beats a bigger one trained on too few.
</details>

<details><summary>Hint 3 — loss spikes or becomes NaN</summary>

Lower the learning rate, check that warmup is on, keep gradient clipping at 1.0, and train in fp32 on `mps` if you tried lower precision.
</details>

## Common mistakes

- Evaluating perplexity on training text.
- Comparing your perplexity with another model's when the tokenizers differ.
- Writing the rubric after seeing the samples.
- Losing a multi-hour run because you didn't save checkpoints.

## Done when

- [ ] Rubric and prompts committed before generation.
- [ ] Parameter count and token budget written down.
- [ ] Learning-rate sweep, then a main run with loss curves.
- [ ] Holdout perplexity vs a unigram baseline.
- [ ] A checkpoint that generates after a fresh reload.
- [ ] Rubric scores for your model and TinyStories-33M on the same prompts.
- [ ] A memorization check.

## Stretch

Implement a KV cache for generation (Raschka has a bonus folder at `ch04/03_kv-cache/`) and measure how much faster generation becomes.

## Reflect

- Write in your [decision map](../decision-map.md) why you would almost never pretrain an LLM at work, and what you'd do instead.
