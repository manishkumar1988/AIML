# 21 — Embeddings and semantic search

**Phase 6 · NLP with Hugging Face** · ⏱ 1 week · 💻 Laptop · Level: core

[← 20 Fine-tune a transformer](20-fine-tune-transformer.md) · [Index](../README.md) · [Next: 22 Build a tokenizer →](22-build-a-tokenizer.md)

## The problem

The bank's help center wants a search box. A customer types "my card still hasn't come," and should find the article about card delivery even though the article never uses the word "come." Keyword search fails here. You need **meaning**-based search.

This is also the foundation of RAG (Phase 9).

Dataset: your frozen Banking77 split (training messages are the "documents" to search; validation and test messages are the "queries").

## Decide first

1. "My card still hasn't come" and "When will my card arrive?" share almost no words. How could a model know they're similar?
2. How would you measure whether a search is good, if you know each message's intent?
3. When might plain keyword search still be the better choice?

## Learn

- **Sentence embeddings:** a model maps a whole sentence to one vector (e.g. 384 numbers). Sentences with similar meanings get nearby vectors.
- **Cosine similarity:** the angle between two vectors. 1 = same direction. With normalized vectors, it's just the dot product.
- **Semantic search:** embed all documents once; embed the query; return the documents with the highest similarity.
- **Vector index:** for thousands of vectors, a NumPy dot product is fine. For millions, use an index such as FAISS (approximate nearest neighbours).
- **Bi-encoder vs cross-encoder:** a bi-encoder embeds query and document separately (fast, used for search). A cross-encoder reads both together (slower, more accurate, used for re-ranking, Challenge 30).
- **Evaluation:** **Recall@k**: is a relevant result in the top k? **MRR**: how high is the first relevant result?
- Embeddings also give you **k-NN classification** (label = the most common label among the nearest neighbours) and **clustering** of text.

Read: [Sentence Transformers documentation](https://sbert.net/): "Quickstart" and "Semantic Search."

## Build

Work in `work/21-embeddings/`. `uv add sentence-transformers`.

1. **First embeddings.** Load `sentence-transformers/all-MiniLM-L6-v2`. Embed 6 sentences you write (3 pairs of paraphrases plus unrelated ones). Print the similarity matrix.
   ✅ Paraphrases have high similarity (around 0.7+), unrelated pairs are low.

2. **Embed the corpus.** Embed all training messages (normalized). Save the matrix to `data/` as `.npy`.
   ✅ Shape is (number of training messages, 384). Write how long it took.

3. **Search function.** `search(query, k=5)` returns the top-k training messages with scores and intents. Try 5 queries of your own.

4. **Evaluate search.** For each validation message, a result counts as relevant if it has the same intent. Compute Recall@1, Recall@5 and MRR@10.
   ✅ Recall@5 is high (well above 0.8).

5. **Keyword baseline.** Same evaluation with TF-IDF cosine similarity, and with BM25 (`uv add rank-bm25`).
   ✅ A table: TF-IDF vs BM25 vs embeddings. Embeddings should win, but check by how much.

6. **Where keywords win.** Find 5 validation queries where BM25 ranks a correct result higher than embeddings. What do they have in common? (Hint: exact terms, codes, names.)

7. **k-NN classifier.** Predict each test message's intent by majority vote of its 10 nearest training messages. Compare accuracy and macro-F1 with TF-IDF (Challenge 19) and DistilBERT (Challenge 20) on the same test set.
   ✅ Good, with no training at all. Usually below the fine-tuned model.

8. **Map.** Reduce the embeddings to 2D (UMAP or PCA) and plot 10 intents in colour. Do similar intents sit next to each other?

9. `NOTES.md`: search table, the keyword-wins examples, the k-NN comparison, and when you'd use each.

## Hints

<details><summary>Hint 1 — fast evaluation</summary>

Embed all validation queries at once (`model.encode(list, batch_size=64, normalize_embeddings=True)`), compute `scores = Q @ D.T`, then `np.argsort(-scores, axis=1)[:, :10]`. No loops over the corpus needed.
</details>

<details><summary>Hint 2 — BM25 tokenization</summary>

`rank_bm25` needs a list of tokens per document. Lowercase and split on non-letters. Use the same tokenization for queries.
</details>

## Common mistakes

- Forgetting to normalize embeddings, then using dot product as if it were cosine.
- Mixing up corpus and query sets (searching the test messages within themselves).
- Assuming embeddings always beat keywords. Exact identifiers, product codes and rare names are keyword territory.

## Done when

- [ ] A working `search()` function.
- [ ] Recall@1, Recall@5, MRR@10 for TF-IDF, BM25 and embeddings.
- [ ] Examples where keywords win, with your explanation.
- [ ] k-NN accuracy next to TF-IDF and DistilBERT on the same test set.
- [ ] An embedding map plot.

## Stretch

Try a stronger embedding model (e.g. `BAAI/bge-small-en-v1.5`) and compare Recall@5 and speed. Check the [MTEB leaderboard](https://huggingface.co/spaces/mteb/leaderboard) to see how models compare more broadly.

## Reflect

- Fill in the **Embeddings and search** section of your [decision map](../decision-map.md).
