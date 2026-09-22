# Challenge 17 — API vs local on the same harness

[Previous: Challenge 16 — An eval harness with a frozen slice](16-eval-harness-frozen-slice.md) · [Next: Challenge 18 — Failure modes on a set you wrote](18-failure-modes-set-you-wrote.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 17 — API vs local on the same harness

- **Goal:** Run Challenge 16’s frozen slice on one hosted chat model and on the local SLM, and compare quality, latency, and cost.
- **Why an engineer needs it:** Model choice is a cost and failure-overlap decision. A better score that costs 50× and fails the same hard items may be the wrong buy.
- **What to build:** Point the harness at one hosted chat API you can actually call, and at SmolLM2-360M. Add columns: mean latency, estimated cost per 1,000 examples, and the count of items both models miss. Keep the slice and the task prompts fixed. A 30-example dev slice is the only place you may adapt the prompt to the API’s chat format, and that adaptation is logged. If you have no API key, run [Qwen/Qwen2.5-0.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct) as the second model, write the cost column as “no API key,” and leave a slot in the table for the hosted run. Do not block the challenge on a secret.
- **Skills practiced:** API clients, cost estimates, paired error analysis.
- **Stack and data:** Challenge 16 harness. Any hosted chat model you can call under its terms. Local model from Challenge 15.
- **Difficulty:** core
- **Rough time:** 4–6 days
- **GPU:** CPU-ok for the local 360M side. The API side needs no GPU.
- **Acceptance criteria:**
  - One results file with two models, both tasks, latency, and a cost column.
  - The slice ids match Challenge 16.
  - A short note lists items both models miss and items only the stronger model gets.
  - Secrets are not committed. The README says where the key comes from.
- **Stretch goal:** A third row for a larger local model only if it fits in 4-bit on hardware you have (`Qwen2.5-1.5B-Instruct`). Otherwise skip.
- **Builds on:** Challenge 16.
