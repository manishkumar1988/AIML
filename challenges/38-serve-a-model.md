# 38 — Serve a model

**Phase 12 · Deployment** · ⏱ 1 week · 💻 Laptop · Level: core

[← 37 Frameworks, MCP, and multi-agent](37-frameworks-mcp-multi-agent.md) · [Index](../README.md) · [Next: 39 Demo and monitoring →](39-demo-and-monitoring.md)

## The problem

A model in a notebook helps nobody. The support platform team wants to call your Banking77 intent classifier (Challenge 20) over HTTP: send a message, get the intent and a confidence back, fast. They also want to know how fast it is, how many requests it can handle, and that it won't break on weird input.

## Decide first

1. What should the API return besides the label? Think about what the calling team needs.
2. What inputs could break it? List five.
3. Load the model once at startup, or on every request? Why?
4. Which number matters more to the platform team: average latency or 95th-percentile latency?

## Learn

- **FastAPI:** a Python web framework. You define request/response shapes with **Pydantic**, and it validates inputs and generates API docs automatically (`/docs`).
- **Model loading:** load once at startup (FastAPI's `lifespan`), keep it in memory, reuse it for every request.
- **Endpoints:** `POST /predict` (one or a batch of texts), `GET /health` (is it alive and loaded?), and a version field in the response (which model answered?).
- **Input validation:** empty strings, very long text, wrong types, non-English, emoji. Decide what to do with each: reject with a clear error, or handle.
- **Latency percentiles:** p50 (typical) and p95/p99 (slow tail). Users feel the tail.
- **Throughput:** requests per second. Batching several texts into one model call usually increases it.
- **Making inference cheaper:** ONNX export and **dynamic quantization** (8-bit weights) can cut latency and size with a small accuracy loss. Measure both.
- **Docker** packages code + environment so it runs the same on any machine. On a Mac, you'll need Docker Desktop or an alternative such as OrbStack or Colima.
- **Tests:** FastAPI's `TestClient` lets you test endpoints with `pytest` without starting a server.

Read: FastAPI [tutorial](https://fastapi.tiangolo.com/tutorial/) (first steps, request body, response model), and [Lifespan events](https://fastapi.tiangolo.com/advanced/events/).

## Build

Work in `work/38-serving/`. `uv add fastapi uvicorn httpx` and `uv add --dev pytest`.

1. **API.** `POST /predict` takes `{"texts": [...]}` (1–32 texts, each 1–1,000 characters) and returns, for each text, `intent`, `confidence`, and the top 3 alternatives, plus `model_version`. `GET /health` returns status and model version. Load the model in `lifespan`.
   ✅ `uv run uvicorn app:app` starts; `/docs` shows the schema; a `curl` request returns sensible intents.

2. **Tests.** At least 8 `pytest` tests: a valid single text, a batch, an empty string, an empty list, too many texts, a too-long text, a wrong type, and a check that predictions for 5 known messages match the expected intents.
   ✅ `uv run pytest` passes.

3. **Low-confidence handling.** Add a `needs_review` flag when confidence is below a threshold. Choose the threshold on your **validation** set so that, above it, accuracy is at least 97%. Report what fraction of messages get flagged.

4. **Load test.** Write a small async script with `httpx` (or use [Locust](https://locust.io/)) sending 1,000 requests at concurrency 1, 8 and 32. Record p50, p95, p99 and requests/second.
   ✅ A table. Write where the bottleneck is.

5. **Batching.** Compare 100 requests with 1 text each vs 10 requests with 10 texts each. Which gives more texts per second?

6. **Faster model.** Export to ONNX and apply dynamic int8 quantization (e.g. with Hugging Face `optimum` and ONNX Runtime). Compare with the original: test accuracy, model size on disk, p50/p95 latency.
   ✅ A trade-off table and a recommendation.

7. **Docker.** Write a `Dockerfile` (slim Python base, install with `uv`, copy the model, run uvicorn). Build and run it, then rerun your tests against the container.
   ✅ `docker run -p 8000:8000 ...` serves predictions. Image size written down.

8. **README for the platform team:** how to run it, the API contract with examples, latency numbers, the `needs_review` meaning, and known limitations (from your Challenge 20 model card).

## Hints

<details><summary>Hint 1 — the Docker image is huge</summary>

PyTorch is large. Use the ONNX Runtime version in the container (no PyTorch needed at inference), a slim base image, and a `.dockerignore` that excludes `data/`, `.venv/` and notebooks.
</details>

<details><summary>Hint 2 — latency gets worse with concurrency</summary>

A single worker runs model inference one request at a time. Try `--workers 2` (each loads its own model; watch memory), or batch requests. Measure, don't guess.
</details>

## Common mistakes

- Loading the model inside the request handler.
- No input validation, so a 1 MB text crashes the server or takes 30 seconds.
- Reporting only average latency.
- Shipping a quantized model without re-measuring accuracy.

## Done when

- [ ] An API with validation, health and version.
- [ ] 8+ passing tests.
- [ ] A `needs_review` threshold chosen on validation.
- [ ] A load-test table with percentiles.
- [ ] An original vs ONNX-quantized comparison.
- [ ] A working Docker container.
- [ ] A README another team could use.

## Stretch

Add a GitHub Actions workflow that runs the tests on every push.

## Reflect

- Fill in "what production-ready means for a model" in the **Deployment** section of your [decision map](../decision-map.md).
