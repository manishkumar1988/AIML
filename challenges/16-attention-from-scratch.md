# 16 — Attention from scratch

**Phase 5 · Advanced deep learning** · ⏱ 1–2 weeks · 💻 Laptop · Level: core

[← 15 Sequence models](15-sequence-models.md) · [Index](../README.md) · [Next: 17 Autoencoders and VAEs →](17-autoencoders-vae.md)

## The problem

Every modern LLM, and most vision and speech models, is built from one block: the transformer. Its core is **attention**. You'll implement attention and a transformer block without library shortcuts, check it against PyTorch's version, and prove it can learn a task an LSTM struggles with.

This challenge is the bridge to Phase 7 (building GPT).

## Decide first

1. An LSTM reads a sentence word by word. What's the problem with remembering a word from 200 positions back?
2. In "The animal didn't cross the street because **it** was too tired," how would a model know what "it" refers to?
3. Attention looks at every pair of tokens. What does that cost for a sequence of length n?

## Learn

- **Self-attention:** each token creates a **query** (what am I looking for?), a **key** (what do I contain?), and a **value** (what do I pass on?). Attention weights = `softmax(Q Kᵀ / √d)`, and the output = weights × V. Every token can look at every other token in one step.
- **Why √d:** keeps the dot products from getting so large that softmax becomes nearly one-hot.
- **Multi-head attention:** several attention "heads" in parallel, each able to focus on different relationships, then concatenated.
- **Positional encoding:** attention itself ignores order, so you add position information to the embeddings.
- **Transformer block:** attention → add & layer-norm → feed-forward network → add & layer-norm. The "add" parts are **residual connections**.
- **Masking:** a padding mask ignores pad tokens. A **causal mask** stops a token seeing the future (needed for GPT, Challenge 23).
- **Cost:** attention is O(n²) in sequence length.

Read: Jay Alammar, [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/). Then chapter 3 of Sebastian Raschka's *Build a Large Language Model (From Scratch)*, which you have locally at `~/projects/LLMs-from-scratch/ch03/`.

## Build

Work in `work/16-attention/`.

1. **Scaled dot-product attention.** Write `attention(Q, K, V, mask=None)` with plain tensor operations. Test it against `torch.nn.functional.scaled_dot_product_attention` on random inputs.
   ✅ Outputs match to about 1e-5.

2. **Multi-head attention.** Write a `MultiHeadAttention(d_model, n_heads)` module (Q/K/V projections, split into heads, attention, merge, output projection).
   ✅ Output shape equals input shape `(batch, seq, d_model)`. A unit test checks that changing a padded position doesn't change the outputs at real positions when the padding mask is applied.

3. **Transformer block.** Attention + feed-forward + residuals + LayerNorm. Add sinusoidal or learned positional embeddings.

4. **Toy task: sequence reversal.** Generate random digit sequences of length 20 and train your model to output the reversed sequence (one prediction per position). Compare with an LSTM of similar size, applied the same way.
   ✅ The transformer reaches near-100% accuracy. The per-position LSTM struggles, because position 0's answer is the *last* input. Write why attention makes this easy.

5. **Visualize attention.** For one reversal example, plot the attention weights (heatmap) of one head.
   ✅ You see an anti-diagonal pattern: each position attends to its mirror position.

6. **Remove the position encoding** and retrain on reversal.
   ✅ It fails. Write why.

7. **Real task.** Train a 2-layer transformer classifier (mean-pool or `[CLS]` token) on IMDB from Challenge 15, same vocabulary and split.
   ✅ Compare with your LSTM and TF-IDF numbers. (A small transformer from scratch often does *not* beat TF-IDF on this data. That's a useful finding, and it's why pretraining matters — Phase 6.)

8. `NOTES.md`: your test results, the attention plot, and an explanation of attention in your own words, as if to a friend.

## Understanding check

AI can write the attention code for you. Do these without AI help:

- [ ] **By hand:** compute attention for 3 tokens with 2-dimensional Q, K and V that you choose (small integers), on paper. Then check it against your code.
- [ ] **Predict before running:** what happens to the attention weights if you remove the √d scaling and use large vectors? Write your prediction, then test it.
- [ ] **Explain each tensor:** for multi-head attention, write the shape after every reshape and transpose, and why it's there.
- [ ] **Explain it:** describe query, key and value in plain words, with the "it" example from Decide first.

## Hints

<details><summary>Hint 1 — splitting into heads</summary>

`(B, T, d_model)` → `.view(B, T, n_heads, d_head)` → `.transpose(1, 2)` gives `(B, n_heads, T, d_head)`. Reverse the steps after attention, using `.contiguous()` before `.view`.
</details>

<details><summary>Hint 2 — applying a mask</summary>

Before softmax: `scores = scores.masked_fill(mask == 0, float("-inf"))`. Check the mask's shape broadcasts to `(B, heads, T, T)`.
</details>

## Common mistakes

- Forgetting to scale by √d, so training is unstable.
- Masking after the softmax instead of before.
- Mixing up `(batch, seq)` and `(seq, batch)` layouts. PyTorch modules often need `batch_first=True`.

## Done when

- [ ] Every item in the Understanding check is done, without AI help.
- [ ] Your attention matches PyTorch's.
- [ ] Multi-head attention with a padding-mask test.
- [ ] The reversal task solved by the transformer, with an LSTM comparison.
- [ ] An attention heatmap you can explain.
- [ ] The no-positional-encoding experiment.
- [ ] IMDB results next to Challenge 15's.

## Stretch

Implement a causal mask and check that output at position t doesn't change when you modify tokens after t. You'll need this in Challenge 23.

## Reflect

- RNN vs transformer: write your rule in the **Sequence and generative models** section of your [decision map](../decision-map.md).
