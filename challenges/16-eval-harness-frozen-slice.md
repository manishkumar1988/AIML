# Challenge 16 — An eval harness with a frozen slice

[Previous: Challenge 15 — Run an SLM and measure it](15-run-slm-measure-it.md) · [Next: Challenge 17 — API vs local on the same harness](17-api-vs-local-same-harness.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 16 — An eval harness with a frozen slice

- **Goal:** A script that scores a local SLM on intent classification and on answerable vs unanswerable questions.
- **Why an engineer needs it:** Later API, prompt, RAG, and fine-tune comparisons are meaningless without one harness and one frozen slice.
- **What to build:** One command that takes a model id and writes a results table.
  - Task A: Banking77 official test, a pre-registered sample of at least 300 examples (or the full test if CPU time allows). The prompt must return one of the 77 labels. Metric: exact label match and macro-F1, next to the Challenge 6 and Challenge 14 numbers.
  - Task B: [rajpurkar/squad_v2](https://huggingface.co/datasets/rajpurkar/squad_v2), a pre-registered mix of 200 questions including unanswerable ones. Metrics: exact match on answerable questions, and abstention rate on unanswerable ones. A prompt that always answers does not get credit for abstention.
  - Use a 30-example dev slice if you edit the prompt. Do not edit the prompt after seeing the frozen-slice score. Record the prompt hash or the prompt file’s git revision.
- **Skills practiced:** Eval harnesses, prompt freezes, abstention, comparison to non-LLM baselines.
- **Stack and data:** Your Challenge 15 runner. [PolyAI/banking77](https://huggingface.co/datasets/PolyAI/banking77), [rajpurkar/squad_v2](https://huggingface.co/datasets/rajpurkar/squad_v2), model [SmolLM2-360M-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct).
- **Difficulty:** core
- **Rough time:** 4–6 days
- **GPU:** CPU-ok for 360M on these sample sizes. small GPU if you want the full Banking77 test.
- **Acceptance criteria:**
  - The results file is produced by the script, not copied by hand.
  - Banking77 numbers sit beside Challenge 6 and Challenge 14.
  - SQuAD v2 reports answerable exact match and unanswerable abstention separately.
  - The sample ids and the prompt revision are in the results file.
- **Stretch goal:** Add [Qwen/Qwen2.5-0.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct) as a second row in the same file without changing the slice.
- **Builds on:** Challenges 6, 14, and 15.
