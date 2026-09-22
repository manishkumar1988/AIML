# Challenge 23 — Grounded generation, scored apart from retrieval

[Previous: Challenge 22 — Retrieval evaluation against qrels](22-retrieval-evaluation-against-qrels.md) · [Next: Challenge 24 — TinyStories data card and a tokenizer](24-tinystories-data-card-tokenizer.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 23 — Grounded generation, scored apart from retrieval

- **Goal:** Given a SciFact claim, retrieve evidence and have the local SLM mark SUPPORT or REFUTE, with abstention, and split the errors.
- **Why an engineer needs it:** A RAG demo that “found a paper” does not tell you whether retrieval or the generator failed. Shipping requires that split.
- **What to build:** Use AllenAI SciFact claim files (SUPPORT and REFUTE labels, with gold evidence doc ids) from [allenai/scifact](https://github.com/allenai/scifact). Join to the BEIR corpus on document id. If a join fails, stop and document the id mismatch instead of hand-fixing test labels. For each labeled claim in the split you pre-register as test:
  - Retrieve top-k with the better Challenge 22 system.
  - SmolLM2-360M predicts SUPPORT or REFUTE from the claim plus retrieved text, or ABSTAIN when the top retrieval score is below a threshold chosen on the train/dev claims.
  - Baseline: the same prompt with no retrieved text.
  Error table buckets: gold doc missing from top-k; gold doc present and the label is wrong; abstained. Headline: label accuracy on non-abstained test claims, plus abstention coverage. A 10-claim demo does not count.
- **Skills practiced:** Grounding, abstention thresholds, error attribution.
- **Stack and data:** Challenge 15 runner and Challenge 22 index. Claims from [allenai/scifact](https://github.com/allenai/scifact). Corpus from BEIR SciFact.
- **Difficulty:** core
- **Rough time:** 1 week
- **GPU:** CPU-ok
- **Acceptance criteria:**
  - The script writes the bucket counts and the no-retrieval baseline on the same claims.
  - The abstain threshold was chosen without the test claims.
  - The writeup says whether the system beat the no-retrieval baseline, and which bucket dominates the remaining errors.
  - Cited doc ids in the output are ids that were actually retrieved for that claim.
- **Stretch goal:** Replace the generator with the Challenge 17 hosted model on the same claims and show whether the bucket mix changes. If you have no API key, skip.
- **Builds on:** Challenges 15, 16, and 22.
