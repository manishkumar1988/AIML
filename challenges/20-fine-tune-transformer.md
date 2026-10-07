# 20 — Fine-tune a transformer classifier

**Phase 6 · NLP with Hugging Face** · ⏱ 1 week · 💻 Laptop · Level: core

[← 19 Hugging Face tour](19-hugging-face-tour.md) · [Index](../README.md) · [Next: 21 Embeddings and semantic search →](21-embeddings-semantic-search.md)

## The problem

The bank wants to route customer messages to one of 77 intents. TF-IDF gets about 88%. Can a pretrained transformer, fine-tuned on the bank's labelled examples, do clearly better? And which intents still fail?

Dataset: your frozen Banking77 split from Challenge 19.

## Decide first

1. In Challenge 16, your transformer trained from scratch didn't beat TF-IDF. Why should a *pretrained* one do better?
2. Which metric matters for 77 intents where some are rare and some are similar?
3. How will you choose how many epochs to train without touching the test set?

## Learn

- **Fine-tuning:** take a pretrained model (here `distilbert-base-uncased`, 66M parameters) and add a classification head with 77 outputs. Train the whole thing for a few epochs with a small learning rate (2e-5 to 5e-5).
- **`Trainer`:** Hugging Face's training loop. It handles batching, the device, evaluation each epoch, saving checkpoints, and loading the best one.
- **Label maps:** `id2label` and `label2id` must be saved in the model config, or a reloaded model will output `LABEL_42` instead of `card_arrival`.
- **Dynamic padding:** `DataCollatorWithPadding` pads each batch only to its longest example. Faster.
- **Early stopping:** evaluate on validation each epoch, keep the best checkpoint (`load_best_model_at_end=True`, `metric_for_best_model="macro_f1"`).
- **Model card:** documents intended use, data, metrics, and **limitations**. An honest card is part of a professional deliverable.

Read: Hugging Face LLM Course, [chapter 3: Fine-tuning a pretrained model](https://huggingface.co/learn/llm-course/chapter3/1).

## Build

Work in `work/20-finetune/`. Load the split with `load_from_disk`, never re-split.

1. **Tokenize.** `AutoTokenizer.from_pretrained("distilbert-base-uncased")`. Check the token-length distribution of the training messages and choose `max_length`.
   ✅ Almost all messages fit in 64 tokens. Write the 99th percentile.

2. **Model.** `AutoModelForSequenceClassification` with `num_labels=77` and `id2label`/`label2id` from the dataset's label names.

3. **Metrics function.** `compute_metrics` returning accuracy and macro-F1.

4. **Train.** `Trainer` with lr 5e-5, batch size 32, up to 5 epochs, evaluation each epoch, `load_best_model_at_end`. Use `mps`.
   ✅ Validation macro-F1 clearly above your TF-IDF baseline (roughly 92–94% accuracy). Plot validation macro-F1 per epoch.

5. **Test once.** Evaluate on the official test set. Put it in a table next to TF-IDF on the same test set.

6. **Per-class view.** Per-class F1 from `classification_report`. List the 10 worst intents, and the 10 most confused pairs from the confusion matrix. Read 3 real examples of each of the top 3 pairs.
   ✅ You can explain at least one confused pair with real messages (e.g. two intents that genuinely overlap).

7. **Save and reload.** `trainer.save_model(...)`, then in a fresh script: `pipeline("text-classification", model=path)`. Run it on 5 messages you write.
   ✅ Outputs are real intent names, not `LABEL_n`.

8. **Model card.** Write `README.md` in the model folder: base model, data, training settings, test accuracy and macro-F1, worst intents, and **one use you don't recommend**.

9. **Push to the Hub** (needs a free account and token; keep the token out of git). Load it back by repo id.
   ✅ The model page shows your card. (If you'd rather not publish, skip this step and note it.)

## Hints

<details><summary>Hint 1 — <code>compute_metrics</code> shape</summary>

It receives `(logits, labels)`; take `preds = logits.argmax(-1)` and use `sklearn.metrics.f1_score(labels, preds, average="macro")`.
</details>

<details><summary>Hint 2 — training on MPS crashes or is slow</summary>

Make sure `fp16=False` (fp16 mixed precision is for CUDA). Try a smaller batch size. If it still fails, set `use_cpu=True` to check that the code works, then use Colab for the full run.
</details>

## Common mistakes

- Re-splitting the data, so the result isn't comparable with Challenge 19.
- Using the test set for early stopping.
- Missing `id2label`, so the pipeline returns meaningless labels.
- Writing a model card with no limitations.

## Done when

- [ ] TF-IDF vs DistilBERT on the same test set: accuracy and macro-F1.
- [ ] The 10 worst intents and 10 most-confused pairs, with real example messages.
- [ ] A reloaded pipeline returns intent names.
- [ ] A model card with metrics, limitations and a not-recommended use.

## Stretch

Train `prajjwal1/bert-tiny` (4M parameters) on the same split. How much accuracy do you lose, and how much faster is inference? That's a real deployment trade-off.

## Reflect

- When is fine-tuning a transformer worth it over TF-IDF? Update **Text classification** in your [decision map](../decision-map.md).
