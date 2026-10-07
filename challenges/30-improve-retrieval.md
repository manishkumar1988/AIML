# 30 — Measure and improve retrieval

**Phase 9 · RAG** · ⏱ 1–2 weeks · 💻 Laptop · Level: core

[← 29 RAG from scratch](29-rag-from-scratch.md) · [Index](../README.md) · [Next: 31 Evaluate RAG answers →](31-evaluate-rag.md)

## The problem

Most bad RAG answers aren't the LLM's fault. The right passage was never retrieved, so the model had nothing to work with. Before you touch the prompt or the model, measure and improve **retrieval** on its own.

Data:
- Your Challenge 29 corpus and gold set (dev/test questions with source sections).
- [BEIR SciFact](https://huggingface.co/datasets/BeIR/scifact): a public retrieval benchmark of 5,183 scientific abstracts and 300 test queries with official relevance labels ("qrels", in [BeIR/scifact-qrels](https://huggingface.co/datasets/BeIR/scifact-qrels)). It gives you a second, independent check with published baseline numbers.

## Decide first

1. How can you score retrieval without looking at generated answers at all?
2. Keyword search vs embedding search: which wins on scientific terminology? On paraphrased questions?
3. Retrieval improvements you could try: list four. Which do you expect to help most?

## Learn

- **Retrieval metrics:**
  - **Recall@k:** fraction of questions whose relevant chunk is in the top k. The most important one for RAG, since the LLM only sees the top k.
  - **MRR@k:** rewards ranking the relevant item higher.
  - **nDCG@10:** the standard metric on BEIR; handles several relevant documents with grades.
- **BM25:** keyword scoring (Challenge 21). Very strong on exact terms and rare words. Always a row in the table.
- **Dense retrieval:** embeddings. Strong on paraphrases.
- **Hybrid search:** combine both, e.g. with **Reciprocal Rank Fusion (RRF)**: score = Σ 1/(60 + rank) over each method's ranking. Simple and robust.
- **Reranking:** retrieve the top 20–50 cheaply, then reorder with a **cross-encoder** that reads question and passage together. Slower, but usually the biggest single gain.
- **Chunk size** and **k** are settings: choose them on dev questions only.

Read: the [BEIR paper](https://arxiv.org/abs/2104.08663), section 1 and the results table (look at where BM25 beats dense models); and the Sentence Transformers [Retrieve & Re-Rank](https://sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html) page.

## Build

Work in `work/30-retrieval/`. `uv add rank-bm25` (or `bm25s`).

1. **Relevance labels for your gold set.** For each answerable question, mark which chunk ids contain the answer (for both chunkers). Unanswerable questions are excluded from retrieval metrics.
   ✅ Every answerable question has at least one relevant chunk id.

2. **Metrics module.** `recall_at_k`, `mrr_at_k`, `ndcg_at_k`, tested on a hand-made example where you know the answer.

3. **SciFact setup.** Load corpus, queries and test qrels. Embed the corpus (one chunk per abstract).

4. **Four systems, both datasets.** BM25; dense (your embedding model); hybrid (RRF); hybrid + cross-encoder rerank (`cross-encoder/ms-marco-MiniLM-L-6-v2` over the top 30).
   ✅ One table per dataset: system × Recall@5, Recall@10, MRR@10 (+ nDCG@10 for SciFact), plus query latency. BM25 is a serious competitor on SciFact (published nDCG@10 for BM25 is about 0.67). Compare your number.

5. **Chunking ablation (your corpus, dev questions only).** Fixed 150 / 300 / 600 tokens, and your section-aware chunker. Choose the best on **dev**, then report it on **test**.
   ✅ A table, and the choice is justified with dev numbers only.

6. **Choose k.** On dev: Recall@k for k = 1, 3, 5, 10, 20. Where does it level off? Your choice of k is a trade-off with prompt length. Write it down.

7. **Failure read.** For 10 test questions where the best system misses the relevant chunk in the top 10, write the reason: vocabulary mismatch, chunk too small or too big, question ambiguous, relevant info spread across chunks, gold label wrong.

8. **Plug it in.** Update your Challenge 29 pipeline to use the best retrieval setup.

9. `NOTES.md`: both tables, the chunking and k decisions, the failure reasons, and the configuration you'd ship.

## Hints

<details><summary>Hint 1 — RRF code</summary>

For each method, a dict `{doc_id: rank}` (starting at 1). Fused score per doc = sum over methods of `1 / (60 + rank)`. Docs missing from one list just get nothing from it. Sort by fused score.
</details>

<details><summary>Hint 2 — SciFact ids</summary>

Corpus ids, query ids and qrel ids are strings in some loaders and ints in others. Normalize them to strings before comparing, or every metric will come out as 0.
</details>

## Common mistakes

- Choosing chunk size or k on the test questions.
- Leaving BM25 out because "embeddings are better."
- Tuning end-to-end answer quality when the problem is retrieval.

## Done when

- [ ] Relevance labels for your gold set.
- [ ] A tested metrics module.
- [ ] A four-system table on both your corpus and SciFact, with latency.
- [ ] A chunking ablation and k choice, made on dev.
- [ ] Ten analysed retrieval failures.
- [ ] Your RAG pipeline upgraded.

## Stretch

**Query rewriting:** have the LLM rewrite each question into a better search query (or generate a hypothetical answer and embed that, "HyDE"). Does Recall@5 improve? At what latency cost?

## Reflect

- Fill in "keyword vs embeddings vs hybrid" in the **Embeddings and search** and **RAG** sections of your [decision map](../decision-map.md).
