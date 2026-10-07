# 23 — GPT from scratch

**Phase 7 · Build a language model from scratch** · ⏱ 1–2 weeks · 💻 Laptop · Level: core

[← 22 Build a tokenizer](22-build-a-tokenizer.md) · [Index](../README.md) · [Next: 24 Pretrain a small language model →](24-pretrain-slm.md)

## The problem

ChatGPT, Claude, Llama and Qwen are all "decoder-only transformers" trained to predict the next token. You'll build one from an empty file, train it on Shakespeare at the character level, and watch it go from random gibberish to text that looks like a play.

Dataset: [Tiny Shakespeare](https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt), about 1.1 million characters. First 90% for training, last 10% for validation.

## Decide first

1. A language model predicts the next token. How does that turn into generating a whole paragraph?
2. During training, why must position 10 not be able to see position 11?
3. What's the simplest possible next-character model? What loss would you expect from it?

## Learn

- **Next-token prediction:** given tokens 1…t, predict t+1. One training sequence of length T gives T predictions at once.
- **Bigram model:** predicts the next character from the current one only. The baseline.
- **GPT architecture:** token embedding + position embedding → N transformer blocks (each: **causal** self-attention → MLP, with residuals and LayerNorm) → final LayerNorm → linear layer to vocabulary logits.
- **Causal mask:** a lower-triangular mask so each position only attends to itself and earlier positions. You built the stretch version of this in Challenge 16.
- **Loss:** cross-entropy over the vocabulary. Initial loss ≈ ln(vocab size).
- **Generation:** feed the context, take the last position's logits, sample a token, append, repeat. **Temperature** scales randomness.
- **Parameter count:** know where the parameters live: embeddings, attention, MLP.

Watch: Andrej Karpathy, [Let's build GPT: from scratch, in code, spelled out](https://www.youtube.com/watch?v=kCc8FmEb1nY). Read alongside: Raschka chapter 4 at `~/projects/LLMs-from-scratch/ch04/01_main-chapter-code/`. Watch first; then close the video and write your own code.

## Build

Work in `work/23-gpt/`.

1. **Data.** Build a character vocabulary from the training text. Encode both splits. Write `get_batch(split, batch_size, block_size)` returning inputs `x` and targets `y` (shifted by one).
   ✅ Vocabulary is about 65 characters. For a batch, `y[:, :-1] == x[:, 1:]`.

2. **Bigram baseline.** An `nn.Embedding(vocab, vocab)` model. Train it and generate 300 characters.
   ✅ Initial loss ≈ ln(65) ≈ 4.17; validation loss settles around 2.5. Output looks like letter soup with spaces.

3. **Causal self-attention.** One multi-head causal attention module.
   ✅ Test: change the token at position 7 and check that outputs at positions 0–6 don't change.

4. **GPT model.** Blocks (pre-LayerNorm style), position embeddings, final head. Write `count_parameters()`.
   ✅ A config with about 6 layers, 6 heads, width 384, block size 256 gives roughly 10M parameters. Your function's count matches a hand calculation within rounding.

5. **Train.** AdamW, lr 3e-4, batch 64, a few thousand steps on `mps`. Estimate validation loss every 250 steps (average over several batches).
   ✅ Validation loss well below the bigram (roughly 1.5–1.7). Generated text has character names, line breaks, and play-like structure.

6. **Overfitting check.** Plot training vs validation loss. Does validation start rising? Add dropout if so.

7. **Generation settings.** Generate with temperature 0.5, 1.0 and 1.5, and with top-k = 10.
   ✅ You can describe how temperature changes the output.

8. **Ablations.** Train two short runs: (a) without position embeddings, (b) with 1 layer instead of 6. Compare validation loss.

9. `NOTES.md`: loss curves, sample text at several checkpoints (early, middle, end), the ablation table, and the parameter breakdown.

## Understanding check

AI can write the GPT code for you. Do these without AI help:

- [ ] **Parameter count on paper:** for your config, compute the parameters in the embeddings, one attention layer, one MLP and the output head. Compare with `count_parameters()`.
- [ ] **Break it on purpose:** flip the causal mask (let tokens see the future). Predict what happens to training loss and to generated text, then run it.
- [ ] **Predict before running:** what generated text looks like at temperature 0.1 vs 2.0.
- [ ] **Explain it:** draw the architecture from memory, and trace one token from input id to output logits.

## Hints

<details><summary>Hint 1 — loss stuck around 2.5 (bigram level)</summary>

The attention may not be working: check the causal mask (positions should see the *past*, not only themselves), and that position embeddings are added. Overfit one batch first.
</details>

<details><summary>Hint 2 — generation crashes after many tokens</summary>

The context grows beyond `block_size`. Crop it: `idx_cond = idx[:, -block_size:]` before each forward pass.
</details>

## Common mistakes

- An upper-triangular mask instead of lower-triangular (the model can see the future: training loss drops suspiciously fast, and generation is garbage).
- Reporting training loss as the result.
- Generating with `model.train()` (dropout active).

## Done when

- [ ] Every item in the Understanding check is done, without AI help.
- [ ] Bigram baseline and GPT trained on the same split.
- [ ] A causal-mask test that passes.
- [ ] Validation loss clearly below bigram, with curves.
- [ ] Samples across training and across temperatures.
- [ ] Two ablations.
- [ ] You can draw the GPT architecture from memory.

## Stretch

Load OpenAI's GPT-2 (124M) weights into your own architecture, following Raschka chapter 5 (`~/projects/LLMs-from-scratch/ch05/`). If your model produces sensible English with those weights, your implementation is right.

## Reflect

- Add "what a decoder-only transformer is" to the **Language models from scratch** section of your [decision map](../decision-map.md).
