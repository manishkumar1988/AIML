# 15 — Sequence models: embeddings and LSTMs

**Phase 5 · Advanced deep learning** · ⏱ 1 week · 💻 Laptop · Level: core

[← 14 Image segmentation](14-image-segmentation.md) · [Index](../README.md) · [Next: 16 Attention from scratch →](16-attention-from-scratch.md)

## The problem

A streaming service wants to know whether a movie review is positive or negative. Text is a **sequence**: word order matters ("not good" ≠ "good"). You'll compare a classical text baseline with neural sequence models, and find out when the neural model is worth it.

Dataset: **IMDB reviews** via Hugging Face: `load_dataset("stanfordnlp/imdb")`. 25,000 train and 25,000 test reviews, balanced positive/negative. Hold out 5,000 training reviews as validation.

## Decide first

1. What's the simplest way to turn a review into numbers a model can use?
2. Would you expect a bag-of-words model (which ignores word order) to do well on sentiment? Why or why not?
3. The classes are balanced. Which metric is fine here?

## Learn

- **TF-IDF + logistic regression:** counts words (and word pairs), down-weights very common ones, and fits a linear model. The standard text baseline. Hard to beat on sentiment.
- **Tokenization:** splitting text into tokens. Here, simple lowercase word splitting. You'll do proper subword tokenizers in Challenge 22.
- **Vocabulary:** map each frequent word to an id; rare words → `<unk>`; padding → `<pad>`.
- **Embeddings:** `nn.Embedding` turns each word id into a learned vector. Words used in similar ways end up with similar vectors.
- **Embedding bag:** average the word vectors, then classify. Fast and surprisingly good.
- **RNN / LSTM:** read the sequence one token at a time, keeping a hidden state (memory). LSTMs use gates to remember things over longer distances. They're slower to train and largely replaced by transformers, but they teach you how sequence modelling works.
- **Padding and lengths:** batches need equal lengths. Pad shorter reviews, and truncate long ones (e.g. at 256 tokens).

Read: Christopher Olah, [Understanding LSTM Networks](https://colah.github.io/posts/2015-08-Understanding-LSTMs/).

## Build

Work in `work/15-sequence/`. `uv add datasets`.

1. **Load and split.** 20,000 train / 5,000 validation (stratified, seed 42) / 25,000 test. Plot review length (in words).
   ✅ Most reviews are under 500 words; a few are very long.

2. **TF-IDF baseline.** `TfidfVectorizer(ngram_range=(1, 2), min_df=2)` + `LogisticRegression`, fitted on train only.
   ✅ Validation accuracy around 88–90%. This is the bar.

3. **Vocabulary.** Build your own from training text only: the top 20,000 words + `<pad>` + `<unk>`. Encode and pad/truncate to 256 tokens.
   ✅ `<unk>` rate on validation is low (a few percent of tokens). Write it down.

4. **Embedding bag model.** `nn.Embedding` → mean over non-pad tokens → linear layer.
   ✅ Validation accuracy in the mid-to-high 80s, trained in a minute or two.

5. **LSTM model.** Embedding → `nn.LSTM` (1–2 layers, hidden 128, optionally bidirectional) → last hidden state → linear. Use gradient clipping (`clip_grad_norm_`, max norm 1.0).
   ✅ Similar to, or slightly below, TF-IDF. Write down training time compared with TF-IDF.

6. **Pretrained word vectors (optional but recommended).** Initialize the embedding with GloVe vectors (e.g. 100-dimensional) and compare.

7. **Errors.** Read 10 reviews all models got wrong. What makes them hard? (Sarcasm, mixed opinions, "the first half was terrible but…")

8. **Test once.** `NOTES.md`: table of TF-IDF, embedding bag, LSTM (accuracy, training time, parameters), plus your judgment: was the neural model worth it here?

## Hints

<details><summary>Hint 1 — LSTM doesn't learn (stuck at 50%)</summary>

Common causes: taking the hidden state at a *padded* position (use `pack_padded_sequence` or pad at the start); learning rate too high (try 1e-3 with Adam); forgetting gradient clipping. First, overfit 64 examples.
</details>

<details><summary>Hint 2 — the mean in the embedding bag includes padding</summary>

Multiply by a mask `(ids != pad_id)` and divide by the number of real tokens. Or use `nn.EmbeddingBag` with offsets.
</details>

## Common mistakes

- Fitting the vectorizer or vocabulary on all text, including test.
- Concluding "deep learning is better" without a strong classical baseline.
- Truncating from the end when the verdict is often in the last sentences. Try keeping the *last* 256 tokens and see.

## Done when

- [ ] A TF-IDF baseline plus two neural models on the same split.
- [ ] Vocabulary built from training text only, with the `<unk>` rate recorded.
- [ ] An error read of 10 reviews.
- [ ] One test score per model.
- [ ] A written judgment: when would you choose TF-IDF over a neural model for text?

## Stretch

Plot the learned embeddings of 50 sentiment words in 2D (PCA). Do "great" and "excellent" end up near each other?

## Reflect

- Start the **Text classification** and **Sequence and generative models** sections of your [decision map](../decision-map.md).
