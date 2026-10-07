# 28 — Evaluating LLMs

**Phase 8 · Working with LLMs (GenAI)** · ⏱ 1–2 weeks · 💻 Laptop · Level: core

[← 27 Structured output](27-structured-output.md) · [Index](../README.md) · [Next: 29 RAG from scratch →](29-rag-from-scratch.md)

## The problem

A product manager asks: "Should we replace our fine-tuned DistilBERT intent classifier with an LLM? And is the LLM safe to use for answering customers?" Opinions from chatting with the model don't count. You'll build an **evaluation harness**: one command that runs a fixed test set through any model and writes a results table. You'll reuse it for RAG, fine-tuning and agents.

## Decide first

1. Why is "I tried 10 prompts and it looked great" not an evaluation?
2. If you keep editing the prompt until the test score goes up, what happens to the test score's meaning?
3. Banking77 is public and on the internet. Could an LLM have seen it during training? What does that mean for your results?
4. How would you score answers to open-ended questions?

## Learn

- **Eval harness:** fixed data (with frozen ids) + fixed prompts (versioned) + a scoring function + a script that writes results. Same harness for every model.
- **Dev vs test for prompts:** prompts are "trained" by you. Edit them using a small **dev** set only; run the **test** set once per final prompt.
- **Exact-match tasks** (classification, extraction): compute accuracy and macro-F1 directly.
- **Open-ended tasks:** use a **rubric**, scored by you on a sample and/or by an **LLM-as-judge**. Before trusting a judge, measure its agreement with your own labels.
- **Failure-mode sets:** a small set *you write*, targeting known weaknesses: unanswerable questions, conflicting instructions, strict formats, long inputs, ambiguous requests. Average scores hide these.
- **Contamination:** public benchmarks may be in a model's training data, which inflates scores. Your own hand-written set is the safest test.
- **Cost and latency** belong in the table next to quality.
- **Uncertainty:** with 300 examples, 1–2 points of difference may be noise. Bootstrap the scores to get a range.

Read: Hamel Husain, [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/), and Eugene Yan, [Evaluating the Effectiveness of LLM-Evaluators](https://eugeneyan.com/writing/llm-evaluators/).

## Build

Work in `work/28-llm-eval/`. Reuse `llm.py` from Challenge 26.

1. **Task A — intent classification.** Sample 300 test messages from your frozen Banking77 split (fixed seed, save the ids) and 50 *validation* messages as the prompt dev set.

2. **Task B — failure set.** Write 40 items by hand, 8 in each of 5 categories: (a) unanswerable from the given text (correct behaviour: say so); (b) strict JSON format; (c) two conflicting instructions in one message (correct behaviour: point out the conflict or follow a stated priority); (d) long input with the key fact in the middle; (e) ambiguous request (correct behaviour: ask a clarifying question). For each, write what a passing answer must do.
   ✅ Committed before running any model.

3. **Harness.** `uv run python -m eval --model qwen2.5:7b --task all` writes `results/<model>_<date>.json` and appends a row to `results/summary.csv`: model, prompt version, task, metric values, mean latency, tokens, estimated cost.

4. **Prompt dev.** Develop the Task A prompt on the 50 dev messages only (zero-shot, then few-shot). Version each prompt (file + git hash).

5. **Run** at least two local models (3B and 7B), and a hosted model if you have a key, on both tasks.
   ✅ One summary table with all models. Task A next to TF-IDF and DistilBERT on the same 300 ids.

6. **Grade Task B** yourself: pass/fail per item, per category.

7. **LLM judge.** Write a judge prompt for Task B using your pass criteria. Run it with your strongest model on all outputs. Compare with your own grades: agreement rate, and which category it misjudges.
   ✅ A short verdict: would you trust this judge alone? For which categories?

8. **Bootstrap.** For Task A, bootstrap the accuracy of each model (1,000 resamples). Are the differences between models bigger than the ranges?

9. **Decision memo.** In `NOTES.md`, answer the product manager's two questions using your table: should the LLM replace DistilBERT for routing? Is it safe for answering customers, and for which kinds of requests not?

## Hints

<details><summary>Hint 1 — mapping LLM output to one of 77 labels</summary>

Constrain it (schema/enum from Challenge 27), or post-process: exact match first, then closest label by string similarity. Count the outputs that needed fixing, as that's a failure mode too.
</details>

<details><summary>Hint 2 — the judge always says "pass"</summary>

Give it the pass criteria per item, ask for a reason *before* the verdict, and include examples of failing answers in the judge prompt. Then re-check agreement.
</details>

## Common mistakes

- Tuning the prompt on the test set.
- Comparing models run with different prompts or different test items.
- Treating a refusal and a hallucination as the same failure. They have different fixes.
- Trusting the judge without measuring agreement.

## Done when

- [ ] One command produces the results table for any model.
- [ ] A 40-item failure set with pass criteria, written before any runs.
- [ ] At least two models compared on both tasks, with latency and cost.
- [ ] LLM vs DistilBERT vs TF-IDF on the same Banking77 ids.
- [ ] Judge agreement measured against your grades.
- [ ] A decision memo.

## Stretch

Add a third task with a public benchmark slice (e.g. 200 SQuAD v2 questions, including unanswerable ones) to compare your models against published numbers.

## Reflect

- Fill in "how I evaluate an LLM feature before shipping" in your [decision map](../decision-map.md).
- **Milestone:** write 3 capstone ideas in `work/milestones.md`.
