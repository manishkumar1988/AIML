# Challenge 21 — Ingestion and chunking

[Previous: Challenge 20 — QLoRA on a 1B-class model](20-qlora-1b-class-model.md) · [Next: Challenge 22 — Retrieval evaluation against qrels](22-retrieval-evaluation-against-qrels.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 21 — Ingestion and chunking

- **Goal:** A rerunnable ingestion pipeline for a capped Simple English Wikipedia snapshot, with two chunkers and a written reject list.
- **Why an engineer needs it:** RAG quality is mostly data plumbing. Chunk boundaries decide what the retriever can find. You need to see bad chunks before you embed a million of them.
- **What to build:** Stream [wikimedia/wikipedia](https://huggingface.co/datasets/wikimedia/wikipedia), config `20231101.simple`. If that config name is unavailable, stream `20231101.en` and stop at the same cap. Cap at 20,000 articles, pre-register the cap, and store the article ids. Clean leftover markup. Implement two chunkers: a fixed token window, and a paragraph-aware chunker. Persist chunks to a local parquet or sqlite file (no hosted database). Report chunk-length distributions. Quote 10 bad chunks (broken sentences, leftover markup, headers with no body).
- **Skills practiced:** Streaming datasets, cleaning, chunking, local storage.
- **Stack and data:** `datasets`. [wikimedia/wikipedia](https://huggingface.co/datasets/wikimedia/wikipedia) `20231101.simple`.
- **Difficulty:** core
- **Rough time:** 4–6 days
- **GPU:** CPU-ok
- **Acceptance criteria:**
  - A fresh run can rebuild or reload the chunk store from the saved ids.
  - Both chunkers’ length stats are in the note.
  - Ten bad chunks are quoted, and you say which chunker produced each.
  - You did not download the full English dump (about 6.4 million articles).
- **Stretch goal:** A third chunker that keeps section headings attached to the body, and a count of how many chunks lost their heading under the first two.
- **Builds on:** Challenge 12.
