# Challenge 22 — Retrieval evaluation against qrels

[Previous: Challenge 21 — Ingestion and chunking](21-ingestion-and-chunking.md) · [Next: Challenge 23 — Grounded generation, scored apart from retrieval](23-grounded-generation-scored-apart-from-retrieval.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 22 — Retrieval evaluation against qrels

- **Goal:** Compare BM25 and a small dense retriever on SciFact with Recall@5 and nDCG@10.
- **Why an engineer needs it:** Generation hides retrieval failure. Ranking metrics against qrels are the contract for the index.
- **What to build:** Use the BEIR SciFact release: corpus, queries, and qrels (Hub mirror [BeIR/scifact](https://huggingface.co/datasets/BeIR/scifact); if qrels are missing from the Hub loader, take them from the official BEIR `scifact` archive, which is linked from that dataset card and from [beir-cellar/beir](https://github.com/beir-cellar/beir)). Corpus size is about 5,183 abstracts. Score:
  - BM25 (`bm25s` or `rank-bm25`).
  - Dense retrieval with [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2).
  Metrics: Recall@5 and nDCG@10 on the official test qrels. If you need a dev set to pick `k` or chunking, pre-register a query split and do not use those queries in the published test number. Also run one chunk-size ablation (whole abstract vs a smaller window) and report it even if the smaller window loses.
- **Skills practiced:** BM25, dense retrieval, nDCG, Recall@k, qrels.
- **Stack and data:** `bm25s` or `rank-bm25`, `sentence-transformers`. BEIR SciFact via [BeIR/scifact](https://huggingface.co/datasets/BeIR/scifact) and the BEIR archive.
- **Difficulty:** core
- **Rough time:** 1 week
- **GPU:** CPU-ok
- **Acceptance criteria:**
  - One table: system, Recall@5, nDCG@10, on the official test qrels.
  - BM25 is a row, not an afterthought.
  - The chunk ablation is a second table, and the dev queries used to prefer a chunker are not in the test number.
  - A short error sample lists 10 queries whose gold document is missing from the top 5, with a reason you can see (vocabulary, too-narrow chunk, ambiguous query).
- **Stretch goal:** Add BEIR NFCorpus (`nfcorpus` in the same BEIR release) with the same two systems and say what does not transfer.
- **Builds on:** Challenge 21 for pipeline habits. The SciFact corpus can use a one-document-per-abstract chunk as the default.
