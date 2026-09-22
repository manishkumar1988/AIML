# Challenge 15 — Run an SLM and measure it

[Previous: Challenge 14 — Trainer, pipeline, and a model card](14-trainer-pipeline-model-card.md) · [Next: Challenge 16 — An eval harness with a frozen slice](16-eval-harness-frozen-slice.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 15 — Run an SLM and measure it

- **Goal:** Run `HuggingFaceTB/SmolLM2-360M-Instruct` locally and record memory, speed, and a fixed smoke suite.
- **Why an engineer needs it:** “It runs on my laptop” is a deployment constraint. You need RAM, tokens per second, and a list of instruction failures before you build on the model.
- **What to build:** A small runner (transformers, or a GGUF build if you prefer one stack and stick to it) for [SmolLM2-360M-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct). Log peak RAM, tokens/sec on a fixed prompt length, and the outputs of a 20-prompt suite you write first: short instruction, JSON-only instruction, a question the model should not know, a long prompt, and a request to follow a format. Save raw outputs.
- **Skills practiced:** Local inference, chat templates, memory and latency measurement.
- **Stack and data:** `transformers`. Model [HuggingFaceTB/SmolLM2-360M-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct). Your 20 prompts, stored in-repo.
- **Difficulty:** core
- **Rough time:** 2–3 days
- **GPU:** CPU-ok
- **Acceptance criteria:**
  - The log has peak RAM, tokens/sec, and the hardware.
  - All 20 raw outputs are in the repo, with decoding settings (temperature, max new tokens).
  - At least five failures are tagged with a short reason (format, truncation, hallucination, refusal).
- **Stretch goal:** The same suite on [Qwen/Qwen2.5-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct) in 4-bit, plus a RAM and quality comparison. Skip this if you have no GPU and no Colab; the 360M run still counts.
- **Builds on:** Challenge 1. Use the same repo.
