# 26 — Run LLMs locally and by API

**Phase 8 · Working with LLMs (GenAI)** · ⏱ 1 week · 💻 Laptop · Level: core

[← 25 Instruction-tune a GPT](25-instruction-tuning.md) · [Index](../README.md) · [Next: 27 Structured output →](27-structured-output.md)

## The problem

Your team wants to add an LLM feature. The first questions are always practical: Which model? Local or hosted? How fast is it? How much memory does it need? Do the settings matter? You'll answer these with measurements, not opinions.

## Decide first

1. What could make you choose a local 3B model over a large hosted model? And the reverse?
2. If you ask the same question twice and get different answers, which setting is responsible?
3. What would you measure to compare two models fairly?

## Learn

- **Ollama** runs open models locally on your Mac, using the Apple GPU. Models are downloaded **quantized** (usually 4-bit), so a 7B model needs about 5 GB of memory. With 24 GB, you can comfortably run 3B–8B models.
- **Hosted APIs** (Anthropic, OpenAI, Google and others) run much bigger models. You pay per token, and your data leaves your machine.
- **OpenAI-compatible API:** Ollama exposes `http://localhost:11434/v1`, the same format many providers use. Write your code against one client interface and switch models by changing the base URL and model name.
- **Chat format:** a list of messages with roles (`system`, `user`, `assistant`). The system message sets behaviour.
- **Decoding settings:** `temperature` (randomness), `top_p`, `max_tokens` (a hard limit that can cut answers off), `seed` (if supported). Always record them.
- **Speed metrics:** time to first token (TTFT), tokens per second, and total latency.
- **Prompting basics:** be specific; give the output format; give examples (**few-shot**); ask for step-by-step reasoning for tricky problems; put instructions before long content and restate them after it.
- **Secrets:** API keys go in a `.env` file (ignored by git) and are read with `python-dotenv`.

Read: [Ollama docs](https://github.com/ollama/ollama/tree/main/docs) (quickstart + OpenAI compatibility), and one provider's prompt-engineering guide, e.g. Anthropic's [prompt engineering overview](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview).

## Build

Work in `work/26-run-llms/`. `uv add openai python-dotenv`. Install Ollama and pull two models of different sizes, e.g. a ~3B and a ~7–8B instruct model (`ollama pull qwen2.5:3b`, `ollama pull qwen2.5:7b`, or current equivalents).

1. **A prompt suite, written first.** Write 20 prompts in `prompts.jsonl`, 4 of each type: a simple instruction; "answer in JSON only"; a question the model can't know (e.g. about your own life, or a made-up product); a long input (paste a 2,000-word article and ask a specific question); a strict format ("exactly 3 bullet points, each under 10 words").
   ✅ Committed before you run anything.

2. **One client for everything.** Write `llm.py` with `chat(model, messages, **settings) -> (text, stats)`, where stats include TTFT, total time, input/output tokens. Use streaming to measure TTFT.

3. **Run the suite** on both local models at temperature 0. Save every raw output with model name and settings to `results/`.

4. **Measure.** Tokens/sec and TTFT for each model on the same prompt; memory use (Activity Monitor or `ollama ps`).
   ✅ A table: model, size, memory, TTFT, tokens/sec.

5. **Grade.** For each output: pass/fail, plus a failure tag (format broken, made something up, didn't follow the instruction, truncated, refused).
   ✅ A pass-rate table per prompt type, per model.

6. **Temperature experiment.** Run 3 prompts 5 times each at temperature 0, 0.7 and 1.2.
   ✅ You can describe what changes: wording, facts, format reliability.

7. **Prompting experiment.** Take your worst-performing prompt type. Improve the prompt (clearer format, an example, a system message). Rerun.
   ✅ Before/after pass rate. Write which change helped most.

8. **Hosted model (optional, needs an API key).** Run the same suite through one hosted API with the same client. Add latency and an estimated cost per 1,000 runs (from the provider's pricing page). If you don't have a key, skip it and leave a placeholder row.

9. `NOTES.md`: the speed table, pass rates, the temperature finding, the prompting finding, and your local-vs-hosted recommendation.

## Hints

<details><summary>Hint 1 — counting tokens</summary>

The API response usually includes `usage` with prompt and completion tokens. With streaming, set `stream_options={"include_usage": True}` where supported, or count with the model's tokenizer.
</details>

<details><summary>Hint 2 — the long-input prompt gets cut off or ignored</summary>

Ollama's default context window can be smaller than the model's maximum. Set `num_ctx` (through Ollama's own options) and check your prompt fits. Silent truncation is a classic failure. Write down if it happened to you.
</details>

## Common mistakes

- Judging a model from 3 chats in a UI.
- Not recording temperature and max tokens, so results can't be reproduced.
- Committing an API key. Check `git diff` before committing.

## Done when

- [ ] 20 prompts written before any runs.
- [ ] One client function that works for every model.
- [ ] A speed/memory table and a pass-rate table for at least two models.
- [ ] Temperature and prompting experiments recorded.
- [ ] A written recommendation: when local, when hosted.

## Stretch

Try the same 7B model at two quantization levels (e.g. `q4` vs `q8` tags) and compare speed, memory and pass rate.

## Reflect

- Fill in "local model vs API" in the **Using LLMs** section of your [decision map](../decision-map.md).
