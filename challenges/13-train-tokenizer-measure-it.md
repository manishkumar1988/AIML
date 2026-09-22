# Challenge 13 — Train a tokenizer and measure it

[Previous: Challenge 12 — Datasets, splits, and a dataset card](12-datasets-splits-dataset-card.md) · [Next: Challenge 14 — Trainer, pipeline, and a model card](14-trainer-pipeline-model-card.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 13 — Train a tokenizer and measure it

- **Goal:** Train a byte-level BPE tokenizer on WikiText-2 train text only, and compare it with BERT’s tokenizer on the test text.
- **Why an engineer needs it:** Vocabulary choice sets the ceiling for every later language model. Unknown-token rate and tokens-per-word are measurable. “It tokenizes” is not.
- **What to build:** Using the `tokenizers` library, train a BPE tokenizer on the train split of [Salesforce/wikitext](https://huggingface.co/datasets/Salesforce/wikitext), config `wikitext-2-raw-v1`. Choose a vocab size and write why (start near 8k or 16k). On the WikiText-2 test split, report tokens-per-word and unknown-token behavior for your tokenizer and for `bert-base-uncased`. Include 10 test sentences where yours is clearly worse, quoted in the note.
- **Skills practiced:** BPE, special tokens, fertility, train/test separation for tokenizers.
- **Stack and data:** Hugging Face `tokenizers`. [Salesforce/wikitext](https://huggingface.co/datasets/Salesforce/wikitext) `wikitext-2-raw-v1`.
- **Difficulty:** core
- **Rough time:** 3–4 days
- **GPU:** CPU-ok
- **Acceptance criteria:**
  - The tokenizer file reloads and encodes a sentence in a fresh process.
  - Train text and test text are disjoint in the training step. The note says so.
  - The comparison table (tokens-per-word, and how `<unk>` or byte fallback shows up) is in the repo.
  - Ten worse-case sentences are quoted.
- **Stretch goal:** The same comparison on 200 Banking77 test utterances, with a note on domain shift from Wikipedia to chat.
- **Builds on:** Challenge 12.
