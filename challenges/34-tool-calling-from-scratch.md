# 34 — Tool calling from scratch

**Phase 11 · Agents** · ⏱ 1 week · 💻 Laptop · Level: core

[← 33 Prompt vs RAG vs fine-tune](33-prompt-rag-or-finetune.md) · [Index](../README.md) · [Next: 35 A research agent →](35-research-agent.md)

## The problem

LLMs can't check today's exchange rate, do exact arithmetic reliably, or look up a customer's account. But they can **ask your code to do it**. That's tool calling, and an LLM calling tools in a loop is an **agent**.

You'll build the agent loop with no framework, for a bank support assistant with four tools.

## Decide first

1. What should the model output when it wants to use a tool? Who actually runs the tool?
2. A user asks "What's 15% of my last transaction in USD?" Which tools, in which order?
3. What could go wrong in a loop where the model decides what to do next? List three failure modes.
4. Which tools should *never* run without a human confirming first?

## Learn

- **Tool definition:** name, description, and a JSON schema for the arguments. The description is a prompt: the model decides based on it.
- **The agent loop:**
  ```
  messages = [system, user]
  for step in range(max_steps):
      reply = llm(messages, tools)
      if reply has tool_calls:
          for call in tool_calls:
              result = run_tool(call.name, call.arguments)   # YOUR code runs it
              messages.append(tool result message)
      else:
          return reply.text                                    # final answer
  return "stopped: too many steps"
  ```
- **Native tool calling:** many models (and Ollama, for models that support tools) return structured `tool_calls`. Older models need a text protocol you parse yourself.
- **Validate arguments** before running a tool (Pydantic again). Return errors to the model as the tool result, so it can try again.
- **Observability:** log every step (model output, tool call, arguments, result, time). Without traces, you can't debug an agent.
- **Side effects:** read-only tools (look up, calculate) are low-risk. Tools that change things (send, pay, delete) need confirmation and strict limits.

Read: Anthropic's [Building effective agents](https://www.anthropic.com/research/building-effective-agents) (read all of it; you'll come back to it in Challenge 37) and Ollama's [tool support](https://ollama.com/blog/tool-support) post.

## Build

Work in `work/34-tools/`. Use a local model that supports tools (e.g. `qwen2.5:7b` or a current equivalent) through your OpenAI-compatible client.

1. **Four tools,** each a plain Python function with a Pydantic argument model:
   - `calculator(expression)`: safe arithmetic (parse with `ast`; never use `eval`).
   - `get_exchange_rate(from_currency, to_currency)`: from a small fixed table you create (mock data).
   - `get_transactions(customer_id, n)`: last n transactions from a small fake JSON "database" you create (5 customers).
   - `search_help(query)`: your Challenge 29/30 retriever over the docs (or a small FAQ you write).
   ✅ Each tool has unit tests, including bad input (`calculator("__import__('os')")` is rejected).

2. **Tool schemas.** Generate the JSON schema for each from its Pydantic model. Write clear descriptions.

3. **The loop.** Implement the loop above with `max_steps=6`. Validate arguments; on a validation error or exception, return an error message as the tool result instead of crashing.
   ✅ "What is 17.5% of 2,340?" → one `calculator` call → correct answer.

4. **Tracing.** Log each run as JSON: every message, tool call, result and duration. Write a small `show_trace(run_id)` that prints it readably.

5. **A task set (write before testing).** 20 tasks in `tasks.jsonl`, each with the expected final answer or behaviour:
   - 4 needing no tool ("Hi, what can you do?")
   - 6 needing one tool
   - 6 needing two or more tools in sequence ("Convert customer C3's largest recent transaction to USD")
   - 4 impossible or out of scope (unknown customer, unsupported currency, "transfer €500 to my friend")
   ✅ Committed first.

6. **Run and grade.** For each task: final answer correct? Right tools? Valid arguments? Number of steps?
   ✅ A results table, and failure tags (wrong tool, bad arguments, unnecessary tool call, made up a result without calling a tool, didn't stop, didn't admit it can't do something).

7. **Improve one thing** (tool descriptions, system prompt, an example) based on the most common failure. Rerun.

8. **Text-protocol version (no native tool calling).** Implement the same loop where the model writes `ACTION: tool_name {json}` and you parse it. Run it with a 3B model. Compare reliability with native tool calling.

9. `NOTES.md`: the loop design, results before/after your fix, native vs text protocol, and the three failure modes you'd guard against first.

## Hints

<details><summary>Hint 1 — the tool-result message format</summary>

In the OpenAI-style API: append the assistant message containing `tool_calls`, then one message per call with `role: "tool"`, the matching `tool_call_id`, and the result as a string (JSON-encode dicts).
</details>

<details><summary>Hint 2 — the model makes up a transaction instead of calling the tool</summary>

Tell it explicitly in the system prompt: "Never invent account data; always use `get_transactions`." And check the tool description says exactly what it returns.
</details>

## Common mistakes

- Using `eval()` for the calculator.
- No step limit, so a confused agent loops forever (and costs money with an API).
- Letting exceptions crash the loop instead of reporting them back to the model.
- Testing only the happy path.

## Done when

- [ ] Four tested tools with schemas.
- [ ] An agent loop with a step limit, argument validation and error handling.
- [ ] JSON traces for every run.
- [ ] 20 tasks written first, run and graded, with failure tags.
- [ ] One measured improvement.
- [ ] A native vs text-protocol comparison.

## Stretch

Add a `transfer_money` tool that requires a human confirmation step in the terminal (`y/n`) before it "runs" (it should only print what it would do). Test that the agent can't bypass the confirmation.

## Reflect

- Start the **Agents** section of your [decision map](../decision-map.md): what an agent is, and what guardrails you always add.
