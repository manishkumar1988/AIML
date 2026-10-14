# Transformers and LLM concepts

The vocabulary and mental models you need to choose, run and reason about language models.

---

## 1. Three families of transformers

| Family | Reads text… | Good at | Examples |
| --- | --- | --- | --- |
| **Encoder-only** | In both directions at once | **Understanding**: classification, NER, embeddings, search | BERT, DistilBERT, RoBERTa, DeBERTa, sentence-embedding models |
| **Decoder-only** | Left to right, predicting the next token | **Generating**: chat, writing, code, reasoning, and almost anything via prompting | GPT family, Llama, Qwen, Mistral, Gemma, Claude |
| **Encoder–decoder** | Encodes input fully, then generates output | **Transforming text**: translation, summarization | T5, BART |

**Rule of thumb:** for a fixed set of labels with plenty of training data, a fine-tuned **encoder** is cheap, fast and accurate. For open-ended tasks, few labels, or many different tasks, use a **decoder LLM**.

---

## 2. Tokens

- Models read **tokens**, not words. In English, 1 token ≈ ¾ of a word on average, so 1,000 tokens ≈ 750 words. Other languages and code often use more tokens per word.
- **Everything is measured in tokens:** context length, speed (tokens/second), and API price (per million input and output tokens).
- Each model has its own **tokenizer**. Always use the model's own; token counts differ between models.
- Tokenization explains some odd failures: counting letters in a word, arithmetic on long numbers, rare names split into pieces.

---

## 3. Context window

- The **maximum tokens** the model can see at once: instructions + documents + conversation + the answer it's writing.
- Bigger contexts cost more (time, memory, money) and models often use information in the **middle** of a long context less reliably than information at the start or end.
- If input exceeds the context, something gets **truncated**, sometimes silently. Always check.
- Local tools (Ollama) may default to a smaller context than the model supports. Set it explicitly.

---

## 4. Choosing a model

### Open-weight (local) vs hosted (API)

| | Open-weight, run yourself | Hosted API |
| --- | --- | --- |
| **Quality** | Good up to mid-size; behind the best hosted models on hard tasks | Best available |
| **Cost** | Your hardware; free per call | Per token; adds up at scale |
| **Privacy** | Data stays on your machine | Data goes to the provider (check their terms) |
| **Speed** | Depends on your hardware | Usually fast; network latency |
| **Control** | Fine-tune, quantize, inspect | Limited to what the API offers |
| **Ops** | You run and update it | Provider handles it |

### Size guide (rough)

| Size | What it's good for | On your 24 GB Mac |
| --- | --- | --- |
| **0.5B–1.5B** | Narrow tasks after fine-tuning; classification/extraction with constraints; on-device | Fast; easy to fine-tune with LoRA |
| **3B–4B** | Simple instructions, summaries, basic extraction | Fast |
| **7B–9B** | Solid general assistant, RAG answers, tool calling | Comfortable in 4-bit |
| **14B–32B** | Noticeably better reasoning | 14B in 4-bit fits; 32B is too tight |
| **70B+ / frontier** | Hard reasoning, complex agents, coding | Use an API |

### What to check before choosing
- **License** (commercial use allowed? restrictions?) — read the model card.
- **Context length**, **languages**, **tool-calling support**, **structured-output support**.
- **Your own evaluation** on your own task. Leaderboards don't know your problem.

---

## 5. Memory math

### Inference (running the model)

**Memory for weights ≈ parameters × bytes per parameter**

| Precision | Bytes/parameter | 7B model |
| --- | --- | --- |
| fp32 | 4 | ~28 GB |
| fp16 / bf16 | 2 | ~14 GB |
| 8-bit | 1 | ~7 GB |
| 4-bit | 0.5 | ~3.5–4.5 GB |

Add room for the **KV cache** (grows with context length and batch size) and overhead. A 7B model in 4-bit uses ~5–6 GB in practice.

### Training

| Method | Rough memory | 7B model |
| --- | --- | --- |
| **Full fine-tuning** (Adam, mixed precision) | ~16 bytes × parameters + activations | ~112 GB+ → multiple large GPUs |
| **LoRA** (frozen fp16 base + small adapters) | ~2 bytes × parameters + adapters + activations | ~16 GB+ |
| **QLoRA** (frozen 4-bit base + adapters) | ~0.5 bytes × parameters + adapters + activations | ~6–10 GB |

That's why the path uses full fine-tuning only for small models (≤ ~350M) and LoRA/QLoRA above that.

---

## 6. Decoding settings

| Setting | Effect | Typical |
| --- | --- | --- |
| **temperature** | Randomness. 0 = always the most likely token | 0–0.2 for extraction/classification; 0.7 for writing |
| **top_p** | Sample only from the smallest set of tokens covering probability p | 0.9–1.0 |
| **top_k** | Sample only from the k most likely tokens | 20–50, or off |
| **max_tokens** | Hard limit on output length | Set it, and check for answers cut off |
| **stop sequences** | Stop when these appear | Useful for structured formats |
| **seed** | Reproducible sampling, where supported | Set it in evaluations |

**Record these settings with every result.** The same prompt with different settings is a different experiment.

---

## 7. Quantization

- Stores weights with fewer bits (8-bit, 4-bit), cutting memory and often speeding up inference on limited hardware.
- 8-bit: almost no quality loss. 4-bit: small loss, usually acceptable. Below 4-bit: noticeable loss.
- Formats you'll see: **GGUF** (llama.cpp / Ollama; tags like `q4_K_M`, `q8_0`), **MLX** quantized models (Apple Silicon), **GPTQ/AWQ** and **bitsandbytes** (NVIDIA).
- Always re-run your evaluation after quantizing.

---

## 8. Embeddings

- An embedding model turns text into a vector; similar meanings → nearby vectors.
- Used for **semantic search, RAG retrieval, clustering, deduplication, k-NN classification**.
- Different from the chat model. Use a dedicated embedding model (MiniLM, BGE, E5, nomic, provider embedding APIs).
- **Normalize** vectors and use cosine similarity. Embed queries and documents with the **same** model (some models need a prefix like `"query: "`).
- Choose with your own retrieval evaluation; the MTEB leaderboard is a starting point only.

---

## 9. How LLMs are made (and what each stage gives)

| Stage | Data | Gives |
| --- | --- | --- |
| **Pretraining** | Huge amounts of raw text, next-token prediction | Knowledge, language, reasoning ability, but only *continues text* |
| **Instruction tuning (SFT)** | (instruction, response) pairs | Follows requests, uses a chat format |
| **Preference tuning (RLHF, DPO…)** | Pairs of better/worse responses | More helpful, safer, better-calibrated answers |
| **Your adaptation** | Prompting, RAG, or fine-tuning (LoRA) | Your task, your data, your style |

You build a miniature of the first two stages in Challenges 24–25.

---

## 10. Known weaknesses to design around

| Weakness | What it looks like | Design response |
| --- | --- | --- |
| **Hallucination** | Confident, fluent, false statements | RAG with citations; "I don't know" instructions; verification |
| **Knowledge cutoff** | Doesn't know recent facts | RAG or tools (search) |
| **Format drift** | Broken JSON, extra text | Schema-constrained output + validation + retry |
| **Long-context weakness** | Misses facts in the middle of long input | Retrieve less, better; put key info first/last |
| **Sensitivity to wording** | Small prompt changes → different answers | Evaluate on a fixed set; version prompts |
| **Arithmetic and counting** | Simple maths mistakes | Give it a calculator tool |
| **Prompt injection** | Instructions hidden in documents/tool output get followed | Treat external text as data; enforce permissions in code |
| **Non-determinism** | Different answers each run | temperature 0 for tasks; repeated runs in evaluation |
| **Benchmark contamination** | Great on public benchmarks, worse on your task | Evaluate on a set you wrote yourself |
