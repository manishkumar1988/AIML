# 22 — Build a tokenizer

**Phase 7 · Build a language model from scratch** · ⏱ 1 week · 💻 Laptop · Level: core

[← 21 Embeddings and semantic search](21-embeddings-semantic-search.md) · [Index](../README.md) · [Next: 23 GPT from scratch →](23-gpt-from-scratch.md)

## The problem

Every language model starts with a tokenizer, and its choices affect everything downstream: sequence length, speed, cost, and what the model can even represent. You'll implement the BPE algorithm from scratch, then train a production-grade tokenizer that your own language model will use in Challenge 24.

Dataset: [TinyStories](https://huggingface.co/datasets/roneneldan/TinyStories): about 2 million short, simple stories written by GPT-3.5/GPT-4 for small children. Use the official `train` split for training and the official `validation` split as your **holdout**. Never train a tokenizer or model on the holdout.

## Decide first

1. Why not just use one token per word? Why not one token per character?
2. A tokenizer trained on children's stories is used on legal text. What happens to the number of tokens per word?
3. Bigger vocabulary → shorter sequences, but what does it cost?

## Learn

- **Word-level:** huge vocabulary, and any unseen word becomes `<unk>`.
- **Character-level:** tiny vocabulary, but very long sequences, so the model must spend capacity learning to spell.
- **BPE (byte-pair encoding):** start from bytes or characters; repeatedly find the most frequent adjacent pair and merge it into a new token; repeat until you reach the vocabulary size. Frequent words become single tokens; rare words split into pieces. **Byte-level** BPE starts from the 256 bytes, so nothing is ever unknown.
- **Fertility:** average tokens per word on held-out text. Lower = more efficient for that kind of text.
- **Vocabulary size trade-off:** larger vocab → shorter sequences, but a bigger embedding table and output layer, and rarer tokens get fewer training examples.
- **Special tokens:** `<|endoftext|>` marks where one document ends and the next begins.

Watch/read: Andrej Karpathy, [Let's build the GPT Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE). Your local copy of Raschka's book has a clean implementation at `~/projects/LLMs-from-scratch/ch02/05_bpe-from-scratch/`. Read it *after* you've tried your own.

## Build

Work in `work/22-tokenizer/`.

1. **Data.** Load TinyStories. Write the first 20,000 training stories to a text file for the from-scratch part. Print 3 stories.
   ✅ You know the size of train and validation (stories and characters).

2. **BPE from scratch (small).** Implement `train_bpe(text, vocab_size)` on bytes, plus `encode(text)` and `decode(ids)`. Train with `vocab_size=512` on the 20,000 stories.
   ✅ `decode(encode(s)) == s` for 100 random holdout stories, including one with an emoji or non-English character. Print the first 20 merges. Do they make sense (`"th"`, `"the"`, `" the"`…)?

3. **Production tokenizer.** Use the Hugging Face `tokenizers` library to train a byte-level BPE on the **full** training split (or a large sample, e.g. 500,000 stories), for vocab sizes 2k, 4k, 8k and 16k. Add `<|endoftext|>` as a special token.
   ✅ Each trains in minutes. Save each to `models/tokenizers/`.

4. **Fertility.** On 2,000 holdout stories, compute tokens-per-word for your 4 tokenizers and for GPT-2's tokenizer (`tiktoken` or `AutoTokenizer.from_pretrained("gpt2")`).
   ✅ A table and a plot of fertility vs vocab size. Your tokenizers beat GPT-2 on TinyStories at a much smaller vocab. Explain why.

5. **Out-of-domain test.** Measure fertility on a paragraph of Python code and a paragraph of non-English text.
   ✅ Your tokenizer does much worse there than GPT-2. Write why.

6. **Choose a vocab size** for Challenge 24, using the fertility curve and the embedding-size cost (vocab × model width). Write the reason.

7. **Reload test.** Load your chosen tokenizer in a fresh script and encode a sentence.

8. `NOTES.md`: the merges, the fertility table, the out-of-domain result, and your chosen vocab size with justification.

## Understanding check

AI can write the BPE code for you. Do these without AI help:

- [ ] **By hand:** run 3 BPE merges on paper for the text `"low lower lowest"`. Then compare with your code's first merges on the same text.
- [ ] **Predict before running:** will the fertility of your 2k tokenizer be higher or lower than GPT-2's on TinyStories? On Python code? Write your prediction first.
- [ ] **Explain it:** why does byte-level BPE never produce an unknown token, while a word-level vocabulary does?

## Hints

<details><summary>Hint 1 — from-scratch BPE is slow</summary>

That's normal in pure Python. Keep it at 20,000 stories and vocab 512. The point is understanding, not speed. Count pairs with a `Counter` over consecutive id pairs; merge by rebuilding the list once per merge.
</details>

<details><summary>Hint 2 — <code>tokenizers</code> setup</summary>

`ByteLevelBPETokenizer()` or the `Tokenizer(models.BPE())` API with `pre_tokenizers.ByteLevel` and a `BpeTrainer(vocab_size=..., special_tokens=["<|endoftext|>"])`. Train with `train_from_iterator` over batches of stories.
</details>

## Common mistakes

- Training the tokenizer on the validation stories (they're your holdout for perplexity later).
- Measuring fertility on training text, which flatters the tokenizer.
- Forgetting the end-of-text token, so stories run into each other during pretraining.

## Done when

- [ ] Every item in the Understanding check is done, without AI help.
- [ ] Your own BPE round-trips correctly.
- [ ] Four trained tokenizers, saved.
- [ ] Fertility table vs GPT-2, in-domain and out-of-domain.
- [ ] A justified vocab size for Challenge 24.

## Stretch

Encode the holdout with your chosen tokenizer and count how many vocabulary tokens never appear. What does that say about your vocab size?

## Reflect

- Start the **Language models from scratch** section of your [decision map](../decision-map.md).
