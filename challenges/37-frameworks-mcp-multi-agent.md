# 37 — Frameworks, MCP, and multi-agent systems

**Phase 11 · Agents** · ⏱ 1–2 weeks · 💻 Laptop · Level: stretch

[← 36 Evaluating agents](36-evaluating-agents.md) · [Index](../README.md) · [Next: 38 Serve a model →](38-serve-a-model.md)

## The problem

You've built agents without a framework, so you know what's inside. At work you'll meet frameworks (LangGraph, the OpenAI Agents SDK, CrewAI, the Claude Agent SDK…), the **Model Context Protocol (MCP)** for sharing tools, and "multi-agent" designs. You need to know what they give you, what they hide, and when *not* to use them.

Three parts:
- **A.** Rebuild your research agent (Challenge 35) in LangGraph.
- **B.** Expose your documentation search as an MCP server that any MCP-capable app can use.
- **C.** Try a multi-agent design and test whether it beats your single agent.

## Decide first

1. What does a framework do that your 100-line loop doesn't? What might it make harder?
2. Every team in a company builds its own "search the wiki" tool for its own agent. What problem does a shared protocol solve?
3. Three agents (planner, researcher, writer) vs one agent with the same tools: which do you expect to be better? At what cost?

## Learn

- **LangGraph** models an agent as a **graph**: nodes (LLM calls, tool execution) and edges (including conditional ones), with an explicit **state** object. It gives you checkpointing (resume a run), human-in-the-loop interrupts, and streaming. The cost: more concepts, and more to debug when the abstraction leaks.
- **MCP (Model Context Protocol)** is an open standard for exposing **tools**, **resources** (data) and **prompts** to LLM applications. You write a server once; any MCP client (Claude Desktop, Claude Code, IDEs and others) can use it.
- **Multi-agent patterns:** orchestrator–workers, planner/executor, critic/reviewer. They can help with tasks that split cleanly and benefit from separate context windows. They multiply cost and add coordination failures. Many tasks are better with one agent and good tools.
- **Choose the simplest thing that works:** a fixed workflow → a single agent → multiple agents, in that order.

Read: LangGraph [documentation](https://langchain-ai.github.io/langgraph/) (quickstart and "agent" tutorial); the [MCP introduction](https://modelcontextprotocol.io/introduction) and the Python SDK [README](https://github.com/modelcontextprotocol/python-sdk); and Anthropic's [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) (note what they say about cost).

## Build

Work in `work/37-frameworks/`.

### Part A — LangGraph

1. `uv add langgraph langchain-ollama` (or the OpenAI-compatible integration). Rebuild the Challenge 35 agent: a state with messages and notes, an LLM node, a tool node, a conditional edge ("tool call or finish"), and an **interrupt** before `save_report` for human approval.
   ✅ It answers a dev question end to end, and pauses for approval before saving a report.

2. **Same evaluation.** Run your Challenge 35 test questions (or the Challenge 36 suite, adapted) through the LangGraph version.
   ✅ A comparison with your hand-built agent: quality, steps, latency, and lines of code.

3. **Write down** what LangGraph made easier and what it made harder (debugging, errors, understanding what is sent to the model).

### Part B — MCP server

4. `uv add "mcp[cli]"`. Write an MCP server exposing `search_docs` and `read_chunk` as tools (and optionally the list of documentation files as a resource), using the Python SDK's `FastMCP`.
   ✅ The MCP Inspector (`mcp dev server.py`) lists your tools and runs a search.

5. **Connect a client.** Add the server to an MCP client you have (Claude Desktop or Claude Code), and ask it a scikit-learn question that should use your tool.
   ✅ The client calls your tool and cites your chunks. (If you have no MCP client, write a minimal one with the SDK's client API.)

6. **Security notes.** Write: what could a malicious MCP server do to a client? What should your server refuse? (Think file paths, very large outputs, and secrets.)

### Part C — Multi-agent

7. **Build a 3-role system:** a planner (splits the question into sub-questions), a researcher (answers each sub-question with the tools, in its own context), and a writer (combines the findings with citations). Plain Python or LangGraph.

8. **Compare** single agent vs multi-agent on the same test questions: correctness, citation validity, total tokens, latency.
   ✅ A table and an honest verdict. Write the conditions under which you'd use multi-agent.

9. `NOTES.md`: all three parts, with a final section, "My agent architecture rules."

## Hints

<details><summary>Hint 1 — LangGraph versions</summary>

The API changes quickly. Follow the version of the docs that matches the version `uv` installed (`uv pip show langgraph`), and pin it in your `pyproject.toml`.
</details>

<details><summary>Hint 2 — MCP server runs but the client doesn't see it</summary>

Check the client's MCP config uses the absolute path to `uv` and your script (e.g. `uv --directory /path/to/repo run server.py`), and look at the client's MCP logs. Servers using stdio must not print anything to stdout except protocol messages.
</details>

## Common mistakes

- Reaching for a framework before you understand the loop. (You've avoided this.)
- Multi-agent by default, because it sounds impressive.
- An MCP server that reads any file path it's given.

## Done when

- [ ] A LangGraph agent with a human-approval interrupt, compared with your hand-built one.
- [ ] A working MCP server, used by a real client.
- [ ] MCP security notes.
- [ ] A single vs multi-agent comparison with cost.
- [ ] "My agent architecture rules" written.

## Stretch

Build the same agent with a second framework (e.g. the OpenAI Agents SDK, Claude Agent SDK, or PydanticAI) and compare the developer experience.

## Reflect

- Complete the **Agents** section of your [decision map](../decision-map.md).
- **Milestone:** redo [Challenge 01](01-problem-framing.md) again. Compare all three attempts.
