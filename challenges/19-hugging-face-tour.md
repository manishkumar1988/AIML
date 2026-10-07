# 19 — The Hugging Face ecosystem

**Phase 6 · NLP with Hugging Face** · ⏱ 1 week · 💻 Laptop · Level: core

[← 18 Tiny diffusion model](18-diffusion-model.md) · [Index](../README.md) · [Next: 20 Fine-tune a transformer →](20-fine-tune-transformer.md)

## The problem

Hugging Face is where most open models and datasets live. Before you train anything, learn to *use* what's already there: find a model, read its card, run it, and check whether it's good enough for your problem. Often it is, and that's the cheapest solution.

You'll also prepare the **Banking77** dataset that Challenges 20, 21, 28 and 33 reuse.

Datasets: **IMDB** (from Challenge 15) and [**Banking77**](https://huggingface.co/datasets/PolyAI/banking77): 13,083 customer-service messages for a bank, 77 intents ("card_arrival", "lost_or_stolen_card"…). Official split: 10,003 train, 3,080 test.

## Decide first

1. A pretrained sentiment model exists on the Hub. How would you decide whether it's good enough for the IMDB task, without training anything?
2. Banking77 has 77 classes. What's the majority-class baseline roughly? What metric would you use?
3. What should you check in a model card before using a model at work?

## Learn

- **The Hub:** models, datasets and Spaces (demos). Every model has a **model card**: what it was trained on, intended use, limitations, **license**.
- **`pipeline()`:** one line to run a model for a task ("sentiment-analysis", "zero-shot-classification", "ner", "summarization"…). Great for trying things.
- **`datasets`:** `load_dataset`, `.map()` for preprocessing in batches, `.train_test_split()`, `.save_to_disk()` / `load_from_disk()`.
- **`AutoTokenizer` / `AutoModel...`:** load the matching tokenizer and model by name. Different models split text differently. Always use the model's own tokenizer.
- **Zero-shot classification:** an NLI model scores how well each candidate label "fits" the text. No training needed. Works for simple label sets, struggles with 77 fine-grained ones.
- **Freezing a split:** once you've created train/validation/test, save it with ids and reuse it everywhere. Otherwise results from different challenges aren't comparable.

Read: Hugging Face [LLM Course](https://huggingface.co/learn/llm-course), chapters 1–2 and chapter 5 (Datasets).

## Build

Work in `work/19-hf-tour/`. `uv add transformers datasets evaluate accelerate`.

1. **Pipelines tour.** Run 4 pipelines (sentiment, zero-shot, NER, summarization) on sentences you write. For each, find the default model's name and open its model card.
   ✅ For each model, one line: what it was trained on, and its license.

2. **Tokenizers.** Tokenize the same 3 sentences with `bert-base-uncased`, `gpt2`, and `Qwen/Qwen2.5-0.5B`. Print the tokens.
   ✅ You can describe two differences (lowercasing, how words are split, special tokens).

3. **Off-the-shelf sentiment on IMDB.** Run `distilbert-base-uncased-finetuned-sst-2-english` on 2,000 IMDB test reviews (truncate to the model's max length).
   ✅ Accuracy compared with your Challenge 15 TF-IDF baseline. Write: would you ship the pretrained model, train your own, or neither? Why?

4. **Freeze the Banking77 split.** Load Banking77. Carve a stratified validation set (about 1,000 examples) from train with seed 42. Keep the official test set. Save all three with `save_to_disk` to `data/banking77_split/`, and also save the list of ids.
   ✅ Reloading in a fresh process gives the same sizes (about 9,003 / 1,000 / 3,080) and label names.

5. **Baselines on Banking77.** (a) Majority class. (b) TF-IDF + logistic regression. Report accuracy and **macro-F1** on validation.
   ✅ TF-IDF is far above majority class (roughly 85–90% accuracy).

6. **Zero-shot on Banking77.** Use `facebook/bart-large-mnli` zero-shot with the 77 intent names (replace `_` with spaces) on 300 validation examples.
   ✅ Much worse than TF-IDF. Write why fine-grained labels are hard for zero-shot.

7. **Dataset card.** Write `data/banking77_split/README.md`: source, license, split sizes, how validation was made, and 2 known issues you noticed (e.g. very short messages, overlapping intents).

8. `NOTES.md` with all results.

## Hints

<details><summary>Hint 1 — <code>load_dataset("PolyAI/banking77")</code> fails</summary>

Newer `datasets` versions don't run dataset loading scripts. Try `load_dataset("PolyAI/banking77", revision="refs/convert/parquet")`, which loads the auto-converted Parquet files. Note what you used in your dataset card.
</details>

<details><summary>Hint 2 — the pipeline is slow</summary>

Pass `device="mps"` and `batch_size=32`. Feed a list of texts, not one at a time.
</details>

## Common mistakes

- Using a model without reading its license.
- Comparing results on different splits ("the pretrained model got 93%", but on which data?).
- Creating a new random split each time you load Banking77.

## Done when

- [ ] Four pipelines run, with model names and licenses noted.
- [ ] A tokenizer comparison.
- [ ] Pretrained sentiment vs your Challenge 15 baseline on the same reviews.
- [ ] Banking77 split frozen, saved, and documented with a dataset card.
- [ ] Banking77 baselines: majority, TF-IDF, zero-shot.

## Stretch

Make a [Gradio](https://www.gradio.app/) demo of your TF-IDF Banking77 classifier and run it locally.

## Reflect

- When is an off-the-shelf model good enough? Add a line to the **Text classification** section of your [decision map](../decision-map.md).
