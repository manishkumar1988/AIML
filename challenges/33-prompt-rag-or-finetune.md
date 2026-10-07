# 33 — Prompt vs RAG vs fine-tune

**Phase 10 · Fine-tuning LLMs** · ⏱ 1–2 weeks · 💻 Laptop · Level: core — a key "what to apply where" challenge

[← 32 LoRA fine-tuning](32-lora-fine-tuning.md) · [Index](../README.md) · [Next: 34 Tool calling from scratch →](34-tool-calling-from-scratch.md)

## The problem

The most common question in applied GenAI: "Should we fine-tune, use RAG, or just prompt better?" People argue about it endlessly. You'll settle it for three different needs with experiments on the same models, so your answer comes from evidence.

| Need | Example |
| --- | --- |
| **Knowledge** — the model must know facts it wasn't trained on | Answer questions about the scikit-learn User Guide (Challenges 29–31) |
| **Behaviour/format** — the model must reliably do a narrow task | Ticket extraction (Challenges 27, 32) |
| **Style** — the model must write in a particular voice | Rewrite technical answers in a friendly "bank support" voice |

## Decide first

Before any experiment, predict the winner for each need (prompting, RAG, or fine-tuning) and write *why*. You'll check your predictions at the end.

Also: if the documentation changes next week, what happens to each approach?

## Learn

- **Prompting** (zero-/few-shot): cheapest, fastest to change. Limited by context length and by what the model already knows.
- **RAG:** brings in knowledge at query time. Easy to update (re-index the documents), and gives citations. Adds retrieval latency and can fail at retrieval.
- **Fine-tuning:** changes the model's behaviour. Good for format, style, narrow tasks, and making a small model do what a big one does. **Poor at adding new facts reliably**, and must be retrained when facts change.
- **They combine:** a fine-tuned model *inside* a RAG pipeline is common.
- **Hidden costs:** data preparation, evaluation, retraining, serving the adapter, latency, per-token prices.

Read: OpenAI's [optimizing LLM accuracy guide](https://platform.openai.com/docs/guides/optimizing-llm-accuracy) (the matrix of prompt/RAG/fine-tuning is useful regardless of provider).

## Build

Work in `work/33-prompt-rag-finetune/`. Use the same 0.5B–1.5B base model for all fine-tuning, and your Challenge 31 regression eval.

### Need 1 — Knowledge

1. **Training data for a "knowledge" fine-tune:** generate ~500 question/answer pairs from the User Guide chunks with your 7B model (a few per chunk). Include the chunks that answer your test questions, but never the test questions themselves. The point is to give fine-tuning its best chance to learn the facts.
2. **Three systems** on your Challenge 29 test questions: (a) small model, prompt only; (b) small model + your RAG pipeline; (c) small model LoRA-tuned on the generated Q&A, no retrieval.
   ✅ Graded with your Challenge 31 eval. RAG should clearly beat the knowledge fine-tune, even though the fine-tune saw that content.
3. **The update test.** Edit one section of the documentation (change a default value or a parameter name), re-index, and ask about it. Which system gives the new answer?

### Need 2 — Behaviour/format

4. Reuse Challenge 32: prompt-only vs few-shot vs LoRA on the extraction test set (and RAG doesn't really apply — write why).

### Need 3 — Style

5. **Write a style guide** (5 rules: e.g. "short sentences," "no jargon," "start with the answer," "friendly sign-off") and 15 example rewrites by hand.
6. **Generate training data:** have the 7B model rewrite 300 technical answers following the guide; hand-check 30.
7. **Two systems:** small model with few-shot style prompt vs small model LoRA-tuned on the rewrites. Rate 30 test rewrites yourself on style adherence (1–5) and meaning preserved (yes/no).

### Wrap-up

8. **One table** with all results, plus columns: setup effort (hours), latency per request, ease of updating.
9. **Check your predictions** from "Decide first." Which were wrong, and why?
10. `NOTES.md`: your rule for choosing, written as a flowchart or a short list, backed by your numbers.

## Hints

<details><summary>Hint 1 — the knowledge fine-tune seems to "know" some answers</summary>

Check whether it's right for the right reason: ask paraphrased versions of the same question, and questions about neighbouring details in the same section. Memorized Q&A pairs often don't generalize to new phrasing.
</details>

## Common mistakes

- Concluding "fine-tuning doesn't work" from the knowledge experiment. It works for other needs, as Need 2 shows.
- Comparing systems that use different base models.
- Ignoring maintenance cost: what happens next month when things change.

## Done when

- [ ] Your predictions written before the experiments.
- [ ] Knowledge: prompt vs RAG vs fine-tune, plus the update test.
- [ ] Behaviour: the Challenge 32 comparison, summarized.
- [ ] Style: few-shot vs fine-tune, rated by you.
- [ ] One combined table with effort, latency and update cost.
- [ ] A written decision rule.

## Stretch

Combine them: the style-tuned model inside the RAG pipeline. Does it keep faithfulness while improving style?

## Reflect

- Fill in "Prompting vs RAG vs fine-tuning — my rule" in the **Fine-tuning** section of your [decision map](../decision-map.md). This is one of the most-asked interview questions in GenAI roles.
