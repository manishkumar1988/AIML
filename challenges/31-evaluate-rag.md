# 31 — Evaluate RAG answers

**Phase 9 · RAG** · ⏱ 1 week · 💻 Laptop · Level: core

[← 30 Measure and improve retrieval](30-improve-retrieval.md) · [Index](../README.md) · [Next: 32 LoRA fine-tuning →](32-lora-fine-tuning.md)

## The problem

Retrieval is measured. Now the harder part: are the **answers** right, supported by the sources, and honest when the sources don't cover the question? When an answer is wrong, you need to know *why*: retrieval missed, or the model misused good context. Each needs a different fix.

Data: your Challenge 29 corpus, gold set, and the improved pipeline from Challenge 30.

## Decide first

1. An answer is correct but cites a chunk that doesn't support it. Pass or fail?
2. How could you test the generator *without* depending on retrieval quality?
3. What's worse for a documentation assistant: a wrong answer or "I don't know"? Does it depend?

## Learn

- **Answer metrics:**
  - **Correctness:** does the answer match the reference answer (by your judgment or a validated judge)?
  - **Faithfulness / groundedness:** is every claim supported by the retrieved chunks? An answer can be correct but unfaithful (right from memory, wrong citation).
  - **Citation accuracy:** do cited chunks exist in the retrieved set and support the claim?
  - **Abstention:** refuses on unanswerable questions; doesn't refuse on answerable ones.
- **Error attribution:** for each wrong answer, ask: was a relevant chunk in the context?
  - **No** → retrieval failure. Fix retrieval.
  - **Yes** → generation failure. Fix prompt or model.
- **Oracle context experiment:** give the generator the *gold* chunks directly. Its score is the ceiling for your generator. If it's low, a better retriever won't save you.
- **LLM judges for faithfulness:** ask a judge to list claims and check each against the context. Validate it against your own labels (Challenge 28).
- Libraries like [RAGAS](https://docs.ragas.io/) automate some of this. Build it yourself first; then compare.

Read: the [RAGAS metrics docs](https://docs.ragas.io/) for definitions of faithfulness and answer relevance (just the concepts).

## Build

Work in `work/31-rag-eval/`.

1. **Freeze the pipeline.** Record the config (chunker, retriever, k, generator model, prompt version) and run all **test** questions. Save question, retrieved chunk ids, answer and citations.

2. **Grade by hand.** For each test question: correctness (correct / partial / wrong), faithfulness (all claims supported / some unsupported), citations valid (yes/no), abstention correct (yes/no).
   ✅ A complete grading sheet. This is your ground truth.

3. **Error buckets.** For every non-correct answer, assign one: retrieval miss (no relevant chunk in context); context present but answer wrong; unfaithful (added unsupported claims); wrong refusal; failed to refuse.
   ✅ Counts per bucket. Write which bucket dominates.

4. **Oracle context run.** Same questions, but give the generator the gold chunks instead of retrieved ones. Grade again.
   ✅ A table: no-RAG (Challenge 29) vs RAG vs oracle. The gap between RAG and oracle is what retrieval still costs you.

5. **Generator comparison.** Rerun the RAG pipeline with your 3B model (and a hosted model if you have one). Same grading.
   ✅ Does the bigger model reduce the "context present but answer wrong" and "unfaithful" buckets?

6. **Automated judge.** Write a faithfulness judge (list claims → check each against context) and a correctness judge (compare with reference). Run on all answers. Measure agreement with your grades.
   ✅ Agreement per metric. Decide which judge you'd trust for future regression testing.

7. **One fix.** Pick the dominant bucket and try one targeted fix (better retrieval, a stricter prompt, a refusal example, a bigger model). Rerun and regrade, on **dev** first, then test once.

8. **Regression script.** `uv run python -m rag_eval` runs the whole test set and writes the table using your validated judges. You'll use it in Challenge 33.

9. `NOTES.md`: the grading summary, buckets, the oracle comparison, judge agreement, the fix and its effect, and a "ship / don't ship" paragraph for the documentation assistant.

## Hints

<details><summary>Hint 1 — grading takes long</summary>

35 questions × several runs adds up. Grade the main run fully by hand; for the comparison runs, grade by hand only the answers that changed, and use the judge for the rest once it's validated.
</details>

## Common mistakes

- Blaming the LLM for answers when the relevant chunk was never retrieved.
- Trusting citations without checking that the cited chunk supports the claim.
- Using RAGAS scores without checking them against your own grading.

## Done when

- [ ] A hand-graded sheet for the test set.
- [ ] Error buckets with counts.
- [ ] No-RAG vs RAG vs oracle comparison.
- [ ] Two generators compared.
- [ ] Judges with measured agreement.
- [ ] One targeted fix, measured.
- [ ] A one-command regression eval.

## Stretch

Run RAGAS on the same outputs. Where does it agree and disagree with your grades?

## Reflect

- Fill in "how I tell a retrieval failure from a generation failure" in the **RAG** section of your [decision map](../decision-map.md).
