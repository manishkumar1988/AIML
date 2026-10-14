# GenAI system design

How to choose between prompting, RAG, fine-tuning and agents, how to design each, and how to evaluate them. This is the "architect" view of Phases 8–11.

---

## 1. The ladder: start at the bottom

Climb only when the step below is measured and isn't good enough.

```
5. Agent (LLM decides steps and calls tools in a loop)
4. Fine-tuning (LoRA) — for behaviour, format, style, or a smaller/cheaper model
3. RAG — for knowledge the model doesn't have, or that changes
2. Workflow — several fixed LLM calls chained (extract → check → write)
1. One good prompt (with examples and structured output)
0. No LLM at all — rules, search, classical ML
```

Each step up adds cost, latency, failure modes and maintenance.

---

## 2. Choosing the approach

### By what's missing

| What the model lacks | Approach | Why |
| --- | --- | --- |
| Clear instructions or examples | **Better prompt**, few-shot | Cheapest fix; try first |
| **Knowledge** (your documents, recent facts, private data) | **RAG** | Easy to update; gives citations |
| **Behaviour** (strict format, a narrow skill, consistent output) | Structured output → **fine-tuning** | Fine-tuning teaches *how*, not *what* |
| **Style/voice** | Few-shot → **fine-tuning** if examples don't hold | |
| **Speed/cost** at scale | **Fine-tune a smaller model** (distillation) | Small model, big model's quality on one task |
| **Ability to act** (look up, calculate, call APIs, multi-step) | Tools → **workflow** → **agent** | Agent only if steps can't be fixed in advance |

### Quick decision flow

```
Does the information change, or is it private/large?  → RAG
Do I need a fixed output format reliably?             → structured output; fine-tune if still unreliable
Is the cost/latency of a big model too high?          → fine-tune a small model on big-model outputs
Are the steps always the same?                        → workflow (fixed chain)
Do the steps depend on what's found along the way?    → agent, with guardrails
```

### Comparison

| | Prompting | RAG | Fine-tuning | Agent |
| --- | --- | --- | --- | --- |
| Adds knowledge | No | **Yes** | Weakly, unreliably | Via tools |
| Changes behaviour/format | Somewhat | No | **Yes** | No |
| Easy to update | **Yes** | **Yes** (re-index) | No (retrain) | Yes |
| Citations | No | **Yes** | No | If tools return sources |
| Setup effort | Low | Medium | Medium–high | High |
| Latency | Low | Medium | Low | **High** (many calls) |
| Main risks | Wording sensitivity | Retrieval misses | Overfitting, stale facts | Loops, wrong actions, cost |

Combinations are normal: a fine-tuned model *inside* a RAG pipeline; an agent whose main tool is RAG search.

---

## 3. RAG design

### Pipeline and choices

| Stage | Main choices | Good default |
| --- | --- | --- |
| **Ingest** | Parsing PDFs/HTML/markdown; cleaning; metadata | Keep title, section, source URL, date |
| **Chunk** | Fixed size vs structure-aware; size; overlap | Split by headings/paragraphs, ~200–500 tokens, small overlap |
| **Embed** | Model; dimension | A small strong embedding model; evaluate 2 options |
| **Store** | NumPy, Chroma, LanceDB, Qdrant, pgvector… | NumPy/Chroma to learn; pgvector if you already use Postgres |
| **Retrieve** | Dense, BM25, hybrid; top-k | **Hybrid** (BM25 + dense, RRF), k = 5–10 |
| **Rerank** | Cross-encoder over top 20–50 | Usually the biggest single quality gain |
| **Generate** | Prompt rules; citations; refusal | "Answer only from context; cite ids; say you don't know" |

### Common failures

| Failure | Cause | Fix |
| --- | --- | --- |
| Right document never retrieved | Vocabulary mismatch; bad chunking | Hybrid search; better chunks; query rewriting |
| Retrieved but answer wrong | Weak generator; too much noisy context | Rerank; fewer, better chunks; bigger model |
| Confident answer, no support | Model used its own memory | Stricter prompt; faithfulness check; refusal examples |
| Answer spread across chunks | Chunks too small | Larger or structure-aware chunks; retrieve neighbours |
| Outdated answer | Stale index | Re-index on change; date metadata and filters |

### Evaluate in two parts
1. **Retrieval:** Recall@k on a gold set of questions with known relevant chunks.
2. **Generation:** correctness, faithfulness, citation accuracy, correct refusals.
3. **Attribute every error:** was the relevant chunk in the context? No → retrieval problem. Yes → generation problem.

---

## 4. Fine-tuning design

- **Use it for:** consistent format, a narrow task, style, or making a small model do a big model's job.
- **Don't use it for:** facts that change, or as a first resort before trying prompts.
- **Data:** a few hundred to a few thousand high-quality examples beat many noisy ones. Big-model outputs (distillation) work if you check their quality.
- **Method:** LoRA (MLX on Mac) or QLoRA (CUDA). Full fine-tuning only for small models.
- **Evaluate:** against prompt-only and few-shot baselines **on the same held-out set**, plus latency and cost.
- **Format:** train and run with the same chat template and system prompt.

---

## 5. Agent design

### Workflow patterns (fixed steps; often enough)

| Pattern | Shape | Example |
| --- | --- | --- |
| **Chain** | A → B → C | Extract fields → validate → write summary |
| **Router** | Classify, then send to a specialized path | Billing question → billing prompt; tech → tech prompt |
| **Parallel** | Several calls at once, then combine | Check a document against 5 policies in parallel |
| **Evaluator–optimizer** | Generate → critique → revise | Draft an answer, check against rules, fix |

### Agent (dynamic steps)

```
loop until done or limits hit:
    LLM decides: answer, or call a tool (with arguments)
    your code validates and runs the tool
    result goes back to the LLM
```

### Guardrails (always)
- **Limits:** max steps, token/cost budget, timeout.
- **Tool allowlist**, and **argument validation** (Pydantic).
- **Human confirmation** for anything with side effects (send, pay, delete, book).
- **Least privilege:** tools can only reach what they need (paths, accounts, data).
- **Treat tool output and documents as data**, never as instructions (prompt injection). Enforce permissions in code, not just in the prompt.
- **Traces:** log every step.

### Single agent vs multi-agent
- Start with **one agent and good tools**.
- Multi-agent (planner/researcher/writer, orchestrator/workers) can help when tasks split cleanly into independent parts that benefit from separate context. It multiplies cost and adds coordination failures.
- Measure: same task suite, compare success rate *and* cost.

### Evaluate agents
- A **task suite** with automatic checks of the outcome (right answer, right action, right refusal).
- **Repeated runs** (3–5 per task): average success, and "passes every time" for reliability.
- **Safety tasks:** things the agent must *not* do.
- **Cost and steps** per task.
- A **failure taxonomy** from reading traces.

---

## 6. Evaluation for every GenAI system

1. **Write the eval set before building.** Include hard and unanswerable cases.
2. **Split prompts' dev and test** like any model: tune on dev, run test once.
3. **Automate** with code checks where possible (exact match, schema validity, field accuracy, retrieval recall).
4. **Human grading** with a rubric for open-ended output, on a sample at least.
5. **LLM-as-judge** only after measuring its agreement with your grading.
6. **Track cost and latency** next to quality.
7. **Regression test** after every change to prompt, model, data or tools.

---

## 7. Cost and latency

| Lever | Effect |
| --- | --- |
| Smaller or fine-tuned model | Big cost/latency drop; check quality |
| Shorter prompts; fewer retrieved chunks | Fewer input tokens |
| Prompt caching (many APIs support it) | Cheaper repeated long prefixes |
| Caching answers for repeated questions | Skip the call entirely |
| Batching | Higher throughput for offline jobs |
| Streaming | Faster *perceived* response |
| Routing: cheap model first, expensive only when needed | Lower average cost |

**Estimate before building:** requests per day × (input tokens × input price + output tokens × output price). Agents multiply this by the number of steps.

---

## 8. Production concerns

- **Privacy:** what data is sent to which provider; redact what isn't needed; log responsibly.
- **Safety:** refusal and escalation paths; human review for high-stakes outputs.
- **Monitoring:** quality on sampled traffic, user feedback, refusal rate, cost, latency, drift in input topics.
- **Versioning:** prompts, models, indexes and eval sets are all versioned, so you can explain any past answer.
- **Fallbacks:** what happens when the model or a tool is down or times out.
