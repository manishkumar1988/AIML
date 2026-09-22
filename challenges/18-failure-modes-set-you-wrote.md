# Challenge 18 — Failure modes on a set you wrote

[Previous: Challenge 17 — API vs local on the same harness](17-api-vs-local-same-harness.md) · [Next: Challenge 19 — Full fine-tune of a small encoder, and a do-not-scale memo](19-full-fine-tune-small-encoder-do-not-scale-memo.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 18 — Failure modes on a set you wrote

- **Goal:** A 40-item failure set, scored for the local SLM and the hosted model, with a “do not ship this for” note.
- **Why an engineer needs it:** Average scores hide the failures that become incidents: bad JSON, confident answers to unanswerable questions, and instructions that contradict each other.
- **What to build:** Author at least 40 items in-repo, tagged with one category each:
  - unanswerable or underspecified
  - label ambiguity
  - strict JSON schema
  - input long enough to truncate at the context length you set
  - two instructions in one user message that conflict (for example “reply in JSON” and “reply in one prose paragraph”)
  - a benign paraphrase of a Banking77 or SQuAD item that flipped a previous prediction
  Score both models from Challenge 17 with the harness style (a script, a table). Write one page: which categories fail, and which product uses you would not ship.
- **Skills practiced:** Failure taxonomies, schema checks, truncation, shipping judgment.
- **Stack and data:** Models from Challenge 17. Your authored set. No extra corpus required.
- **Difficulty:** core
- **Rough time:** 4–6 days
- **GPU:** CPU-ok for the local 360M. API side as in Challenge 17.
- **Acceptance criteria:**
  - The 40 items are in the repo with category tags, written before the scored run.
  - The results table is script-generated and reports pass/fail by category.
  - The shipping note names at least two uses you would reject based on those counts.
  - The set contains ordinary user mistakes and distribution shift, not exploit payloads.
- **Stretch goal:** Re-run the JSON category at two temperatures and show whether format validity moves when task quality does not, or the reverse.
- **Builds on:** Challenge 17.
