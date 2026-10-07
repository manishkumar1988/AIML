# 36 — Evaluating agents

**Phase 11 · Agents** · ⏱ 1 week · 💻 Laptop · Level: core

[← 35 A research agent](35-research-agent.md) · [Index](../README.md) · [Next: 37 Frameworks, MCP, and multi-agent →](37-frameworks-mcp-multi-agent.md)

> **Before you start:** if you skipped the Challenge 34 stretch, add the `transfer_money` tool now (it only prints what it would do, and requires a `y/n` confirmation). The safety tasks below need it.

## The problem

An agent that works in a demo can fail one time in three in practice: it picks the wrong tool, loops, or gives up. Agents are also **non-deterministic**: the same task can pass on Monday and fail on Tuesday. Before anyone can rely on your Challenge 34 support agent, you need an evaluation that measures how often it succeeds, how consistently, and at what cost.

## Decide first

1. An agent passes a task once. How confident are you that it will pass next time? What would you need to measure?
2. Should you grade only the final answer, or also the path the agent took to get there? When does the path matter?
3. How can you check "the agent did the right thing" automatically, without an LLM judge?

## Learn

- **Outcome checks** are the gold standard: check the *end state* or answer with code (the right number, the right record, the right refusal). Deterministic and cheap.
- **Trajectory metrics:** number of steps, tool calls, tool errors, tokens, cost, time. A correct answer after 14 steps may still be a failure in production.
- **Repeated trials:** run each task several times (e.g. 3–5).
  - **pass@1:** average success rate across runs.
  - **pass^k (all k runs pass):** reliability. A customer-facing agent needs this high.
- **Failure taxonomy:** wrong tool, bad arguments, ignored a tool result, made up data, looped, gave up too early, didn't refuse an out-of-scope request, followed injected instructions.
- **Safety cases:** tasks that check the agent *doesn't* do something (doesn't transfer money without confirmation, doesn't reveal another customer's data).
- **Regression testing:** rerun the suite after every prompt, tool or model change, and compare.

Read: Anthropic's engineering post on [writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) (for how tool design affects success), and skim the [τ-bench paper](https://arxiv.org/abs/2406.12045) (abstract + section 1) for the pass^k idea.

## Build

Work in `work/36-agent-eval/`. Use the Challenge 34 support agent.

1. **Expand the task set to 30 tasks**, each with an automatic checker:
   - Answer checks: the expected number or text (with tolerance for numbers), or "must contain"/"must not contain."
   - Behaviour checks: "must call `get_transactions` with customer_id=C3," "must not call `transfer_money`," "must refuse."
   - At least 5 safety tasks (other customer's data, transfer without confirmation, an injected instruction inside a help article).
   ✅ Every task has a checker function, tested on a hand-written good and bad trajectory.

2. **Runner.** `uv run python -m agent_eval --model <name> --trials 3` runs every task 3 times, saves all traces, and writes a results table.

3. **Metrics:** pass@1, pass^3, average steps, average tool errors, average tokens and time per task, plus pass rate for safety tasks separately.

4. **Failure taxonomy.** For every failed run, assign a failure tag (read the trace, don't guess).
   ✅ A table of tag counts. The top tag tells you what to fix.

5. **Compare models:** run the suite with a 3B and a 7–8B local model (and a hosted model if you have a key).
   ✅ One table: model × pass@1, pass^3, safety pass rate, steps, time, cost.

6. **Fix and rerun.** Make one change targeting the top failure tag (tool description, tool design, prompt, or an argument check in code). Rerun the full suite.
   ✅ Before/after numbers. Did anything else get worse? (That's why you rerun everything.)

7. **Flakiness.** Find tasks that pass in some trials and fail in others. Read their traces. What makes them unstable?

8. `NOTES.md`: metrics definitions, the model comparison, the taxonomy, the fix, and a readiness statement: "I'd let this agent handle X without review, Y with review, and never Z."

## Hints

<details><summary>Hint 1 — checking trajectories</summary>

Your traces are JSON: write helpers like `called(trace, "get_transactions", customer_id="C3")` and `never_called(trace, "transfer_money")`. Checkers combine them with the final-answer check.
</details>

<details><summary>Hint 2 — runs take too long</summary>

Run tasks in parallel with a thread pool (Ollama can serve a few requests at once), or start with 1 trial while building the suite and use 3 trials for the final comparison.
</details>

<details><summary>Hint 3 — the <code>y/n</code> confirmation blocks automated runs</summary>

Make confirmation a function you pass into the agent. In eval mode, pass one that automatically answers "no" and records that a confirmation was requested. Then a safety checker can assert "confirmation was requested" or "transfer was never requested."
</details>

## Common mistakes

- Running each task once and calling the pass rate "the" success rate.
- Using an LLM judge where a simple code check would do.
- Making a fix and testing only the tasks it was meant to fix.
- No safety tasks.

## Done when

- [ ] 30 tasks with tested automatic checkers, including 5+ safety tasks.
- [ ] A runner with repeated trials and saved traces.
- [ ] pass@1, pass^3, cost and step metrics for at least two models.
- [ ] A failure taxonomy built from traces.
- [ ] One fix with full before/after results.
- [ ] A readiness statement.

## Stretch

Add an LLM-judge check for answer *quality* (helpfulness, tone) on top of the outcome checks, and validate it against your own grades on 20 runs.

## Reflect

- Fill in "how I evaluate an agent" in the **Agents** section of your [decision map](../decision-map.md).
