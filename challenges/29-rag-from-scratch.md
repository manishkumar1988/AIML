# 29 — RAG from scratch

**Phase 9 · RAG** · ⏱ 1–2 weeks · 💻 Laptop · Level: core

[← 28 Evaluating LLMs](28-evaluating-llms.md) · [Index](../README.md) · [Next: 30 Measure and improve retrieval →](30-improve-retrieval.md)

## The problem

A data-science team wants an assistant that answers questions about the **scikit-learn User Guide**, with answers that cite the exact section they came from. A plain LLM answers from memory: sometimes right, sometimes confidently wrong, never with a source. **Retrieval-augmented generation (RAG)** fixes this: find the relevant passages first, then have the LLM answer *from those passages*.

You'll build every piece without a RAG framework, so you know what the frameworks do.

Corpus: the scikit-learn User Guide source files. Clone the repo (`git clone --depth 1 https://github.com/scikit-learn/scikit-learn.git` into `data/`) and use the `.rst` files under `doc/modules/`. You've used scikit-learn for months, so you can write good test questions.

## Decide first

1. Why not just paste the whole User Guide into the prompt?
2. A section is 3,000 words long. Would you embed it as one vector, or split it? What's lost either way?
3. How will the system say "I don't know" instead of making something up?
4. Before building: how will you know whether the answers are right?

## Learn

- **The RAG pipeline:**
  1. **Ingest:** load documents, clean them, keep metadata (file, section title).
  2. **Chunk:** split into pieces of a few hundred tokens, often with some overlap.
  3. **Embed:** turn every chunk into a vector (Challenge 21).
  4. **Index/store:** keep vectors and metadata; a NumPy array first, then a vector database.
  5. **Retrieve:** embed the question and take the top-k most similar chunks.
  6. **Generate:** prompt the LLM with the question and the chunks, telling it to answer *only* from them, cite chunk ids, and say "I don't know" if the answer isn't there.
- **Chunking strategies:** fixed size (simple, can cut sentences in half) vs structure-aware (split on headings and paragraphs; keeps meaning together).
- **Vector databases** (Chroma, LanceDB, Qdrant, pgvector…) store embeddings with metadata and search them quickly. For a few thousand chunks, NumPy is honestly enough. Use a database for persistence and filtering.
- **Gold set:** questions with known answers and known source sections, written **before** you tune anything. Include questions the docs *can't* answer.

Read: Anthropic's [Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) post (for the problems with naive chunking) and the [Chroma getting started](https://docs.trychroma.com/) page.

## Build

Work in `work/29-rag/`. `uv add chromadb` (or `lancedb`).

1. **Gold set first.** Write 50 questions in `gold.jsonl`: 40 answerable (with the answer in your words, and the source file + section) and 10 unanswerable from the User Guide (e.g. about a library that isn't scikit-learn, or opinions). Split them into 15 **dev** and 35 **test**, keeping both answerable and unanswerable questions in each. Commit.
   ✅ Committed before any code below.

2. **Ingest.** Load the `.rst` files under `doc/modules/`. Strip directives and markup you don't need (`.. code-block::`, `:class:` roles → plain text). Keep file name and section titles.
   ✅ Print one cleaned section. It reads like plain text. Count documents and total words.

3. **Two chunkers.** (a) Fixed windows of ~300 tokens with 50-token overlap. (b) Section-aware: split on headings, then on paragraphs if a section is too long. Each chunk gets an id and metadata (file, section).
   ✅ Length histograms for both. Quote 5 bad chunks (cut mid-sentence, heading with no content, leftover markup) and say which chunker made them.

4. **Embed and index (NumPy).** Embed all chunks with `all-MiniLM-L6-v2` or `BAAI/bge-small-en-v1.5`. Write `retrieve(question, k)`.
   ✅ For 5 dev questions, the right section appears in the top 5 for most of them.

5. **Generate.** Prompt template: system rules (use only the context, cite `[chunk_id]` after each claim, say "I don't know based on the documentation" if not covered) + numbered chunks + question. Use your local 7B model.
   ✅ Answers include citations. An unanswerable dev question gets "I don't know."

6. **No-RAG baseline.** The same model and questions with no retrieved context.

7. **Move to a vector database.** Store chunks, embeddings and metadata in Chroma (persisted to disk). Check that results match your NumPy version on the dev questions.
   ✅ Same top results, and the index survives restarting Python.

8. **First evaluation (by hand).** On the 35 test questions, run RAG and no-RAG once. Mark each answer: correct / partly correct / wrong / correctly refused / wrongly refused. Check whether every citation points to a chunk that was actually retrieved.
   ✅ A table: RAG vs no-RAG. RAG should be clearly better on answerable questions and on refusing unanswerable ones.

9. **A CLI.** `uv run python -m rag "How do I handle class imbalance in SVC?"` prints the answer, citations, and the retrieved chunk titles.

10. `NOTES.md`: the pipeline design, the chunking comparison with bad examples, the evaluation table, and three improvement ideas (you'll test them in Challenges 30 and 31).

## Hints

<details><summary>Hint 1 — cleaning <code>.rst</code></summary>

Regex is enough: drop lines starting with `..` (directives) and their indented blocks if they're not prose; turn ``:class:`~sklearn.svm.SVC` `` into `SVC`; keep code examples as plain text, since people ask about them. Don't aim for perfect. Look at 10 chunks and fix what's worst.
</details>

<details><summary>Hint 2 — the model ignores "use only the context"</summary>

Put the rule in the system message *and* repeat it after the context. Show one example of a refusal. Smaller models follow this less reliably. Note how the 3B and 7B models differ.
</details>

## Common mistakes

- Writing the gold set after seeing what the system can answer.
- Never reading the chunks.
- Citations that look right but point to chunks that weren't retrieved.
- Evaluating with 5 questions you picked because they worked.

## Done when

- [ ] A 50-question gold set (with unanswerable questions) committed first.
- [ ] Two chunkers, with length stats and bad examples.
- [ ] Retrieval + generation with citations and "I don't know."
- [ ] A persisted vector database.
- [ ] RAG vs no-RAG on the test questions.
- [ ] A working CLI.

## Stretch

Add metadata filtering: let the user restrict the search to one file (e.g. only `ensemble.rst`).

## Reflect

- Fill in "when RAG is the right answer" and "default pipeline" in the **RAG** section of your [decision map](../decision-map.md).
