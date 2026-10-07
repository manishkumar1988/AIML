# AI/ML Engineer Practice Path

A hands-on path from "I finished a course" to "I can pick the right tool for a problem, build it, and explain why it works."

You will build 42 small projects, in order. They cover classical ML, deep learning, computer vision, advanced deep learning, Hugging Face, building a language model from scratch, working with LLMs, RAG, fine-tuning, agents, deployment, and Kaggle.

**Start here:** read this page, then do [Challenge 00](challenges/00-workspace-setup.md).

---

## What you will be able to do at the end

- Look at a problem and say what *kind* of problem it is, what to try first, and how to tell whether it worked.
- Train and evaluate classical models, neural networks, CNNs, and transformers yourself.
- Build a small GPT from scratch, and fine-tune real open models.
- Build RAG systems and agents, and measure them instead of guessing.
- Ship a model behind an API.
- Show a portfolio of projects you can explain in an interview without notes.

---

## How each challenge works

Every challenge file has the same sections, in this order.

| Section | What you do |
| --- | --- |
| **The problem** | Read a short, realistic scenario. |
| **Decide first** | Answer a few questions in your notes *before* reading further: what kind of problem is this, what would you try first, how would you measure it? Being wrong here is fine. It is the most important habit in the whole path. |
| **Learn** | A short concept primer plus one or two links. Read or watch only what you need. |
| **Build** | Numbered steps, in the order you'd implement them. Turn each into a precise prompt for your AI coding tool. Each step has a ✅ checkpoint that tells you what you should see. If you don't see it, stop and find out why before moving on. That's where most of the learning happens. |
| **Hints** | Hidden behind a click. Open them only after you've been stuck for about 30 minutes. |
| **Common mistakes** | Traps that almost everyone falls into once. |
| **Done when** | A checklist. When every box is ticked, you're done. Move on. |
| **Stretch** | Optional extra. Do it if you're enjoying it, or come back later. |
| **Reflect** | A few questions, plus a line to add to your [decision map](decision-map.md). |

---

## How you work: AI writes the code, you own the decisions

Use AI coding tools freely: Cursor, Claude Code, Copilot, autocomplete, all of it. That's how engineers work now. What AI can't do for you is **decide what to build, specify it precisely, and notice when the result is wrong**. That's the job, and it's what this path trains.

Every challenge follows the same five steps:

| Step | You do | AI does |
| --- | --- | --- |
| **1. Decide** | Answer "Decide first": problem type, baseline, metric, split, risks. | Nothing yet. Don't ask it to decide for you. |
| **2. Specify** | Write a short design note in `NOTES.md` (approach, data split, metric, what "done" looks like). Turn it into a precise prompt. | — |
| **3. Generate** | Give the AI the spec, one Build step at a time, not the whole challenge in one go. | Writes the code. |
| **4. Verify** | Run it. Check every ✅ checkpoint. Review the code against the [review checklist](#review-checklist-for-ai-written-ml-code) below. | Can help you investigate, but *you* judge. |
| **5. Explain** | Write the results and decisions in `NOTES.md` in your own words. | Don't let it write your notes. They're your proof of understanding. |

**The test for every challenge:** could you explain each design choice, and each number in your notes, to an interviewer without looking? Could you spot it if the AI had quietly done something wrong? If not, you're not done.

### Two rules

1. **Decide before you prompt.** Write your "Decide first" answers and design note before the AI writes any code. If you let the AI choose the approach, you learn nothing about *what to apply where*, which is the skill a course doesn't give you.
2. **Write it down.** Each challenge produces a `NOTES.md`: your decisions, your numbers, what went wrong, and what you'd do next. A result that isn't written down didn't happen. These notes become your portfolio and your interview stories.

### Good and bad prompts

| ❌ Vague (AI decides everything) | ✅ Specified (you decided, AI implements) |
| --- | --- |
| "Build a fraud detection model." | "Sort by `Time`; split 60/20/20 by time. Fit a `StandardScaler` + `LogisticRegression(class_weight='balanced')` pipeline on train only. Report PR-AUC on validation. Don't touch the test split." |
| "Make a RAG system for these docs." | "Chunk the `.rst` files by section heading, max 400 tokens. Embed with `bge-small-en-v1.5`. Store in Chroma with file and section metadata. `retrieve(q, k)` returns ids, titles and scores." |

### Review checklist for AI-written ML code

These are the bugs AI tools make most often in ML code. None of them crash. They just give you wrong numbers that look good. Check for them every time.

- [ ] **Leakage through preprocessing:** a scaler, encoder, vectorizer, imputer or tokenizer is fitted on all the data instead of train only.
- [ ] **Wrong split:** a random split on time-ordered data, or groups (users, stores, duplicate documents) spread across train and test.
- [ ] **Test set misuse:** a threshold, hyperparameter, prompt or epoch chosen using test results.
- [ ] **Leaky features:** a column that wouldn't be known at prediction time, or that's derived from the target.
- [ ] **Wrong metric:** accuracy on imbalanced data; `average="micro"` where you meant macro; a metric that doesn't match the competition's definition.
- [ ] **Silent truncation:** text cut to a max length, or a context window overflowed, without anyone noticing.
- [ ] **Train/eval mode:** `model.eval()` and `torch.no_grad()` missing during evaluation; augmentation applied to validation data.
- [ ] **Seeds and reproducibility:** randomness not seeded, so results change on every run.
- [ ] **Made-up APIs:** a function or parameter that doesn't exist in the installed library version (check the docs).
- [ ] **Swallowed errors:** a `try/except` that hides failures, or a fallback value that makes broken output look normal.

### When to type it yourself

A few challenges exist to build *understanding* of how something works inside: [09](challenges/09-neural-net-from-scratch.md) (backprop), [16](challenges/16-attention-from-scratch.md) (attention), [22](challenges/22-build-a-tokenizer.md) (BPE), [23](challenges/23-gpt-from-scratch.md) (GPT). AI can write these too, but each one has an "Understanding check" you must pass yourself: predict outputs before running, break it on purpose, and explain it line by line. That's the knowledge you need to architect systems and review AI code. Nobody needs you to type it.

---

## Your hardware

You have an **Apple M4 Pro with 24 GB of memory**. That's a good learning machine.

| Runs well locally | Use free Colab or Kaggle GPU for |
| --- | --- |
| All classical ML | QLoRA with `bitsandbytes` (it needs an NVIDIA GPU) |
| PyTorch on the `mps` device (Apple GPU) for CNNs and small transformers | Long training runs you don't want tying up your laptop |
| Training a 10–30M parameter GPT | Anything a challenge marks **Colab** |
| Running 3B–8B LLMs with Ollama | |
| LoRA fine-tuning of 0.5B–3B models with MLX | |

Each challenge says **Laptop** or **Laptop or Colab** or **Colab**.

---

## Roadmap

About 8–10 hours a week, about one challenge a week. Some take two. Total: roughly 10–12 months. Going slower is fine. Skipping the "Decide first" and "Reflect" sections to go faster is not.

### Phase 0 — Setup and problem framing
| # | Challenge | Main skill |
| --- | --- | --- |
| 00 | [Workspace setup](challenges/00-workspace-setup.md) | Python env, git, project layout, GPU check |
| 01 | [Problem framing](challenges/01-problem-framing.md) | Turn a vague request into a problem type, a baseline, and a metric |

### Phase 1 — Classical machine learning
| # | Challenge | Main skill |
| --- | --- | --- |
| 02 | [Your first end-to-end model](challenges/02-first-end-to-end-model.md) | Regression, train/test split, baselines |
| 03 | [Customer churn](challenges/03-customer-churn-classification.md) | Classification, preprocessing pipelines, precision/recall |
| 04 | [Fraud detection](challenges/04-fraud-imbalanced-data.md) | Imbalanced data, PR curves, thresholds, cost |
| 05 | [Learning without labels](challenges/05-learning-without-labels.md) | Clustering, anomaly detection |
| 06 | [Forecasting demand](challenges/06-time-series-forecasting.md) | Time series, time-based splits, leakage |
| 07 | [Tune, validate, explain](challenges/07-tune-validate-explain.md) | Cross-validation, tuning, SHAP, leakage hunting |

### Phase 2 — Kaggle I
| # | Challenge | Main skill |
| --- | --- | --- |
| 08 | [Your first Kaggle competition](challenges/08-kaggle-playground.md) | Competition workflow, local CV vs leaderboard |

### Phase 3 — Deep learning foundations
| # | Challenge | Main skill |
| --- | --- | --- |
| 09 | [A neural network in NumPy](challenges/09-neural-net-from-scratch.md) | Forward pass, backprop, gradient descent, with no framework |
| 10 | [PyTorch training loop](challenges/10-pytorch-training-loop.md) | Tensors, autograd, `nn.Module`, CNNs |
| 11 | [Debugging training](challenges/11-debugging-training.md) | Overfitting, learning rates, regularization, augmentation |

### Phase 4 — Computer vision
| # | Challenge | Main skill |
| --- | --- | --- |
| 12 | [Transfer learning](challenges/12-transfer-learning.md) | Pretrained backbones, fine-tuning vs feature extraction |
| 13 | [Object detection](challenges/13-object-detection.md) | YOLO, bounding boxes, IoU, mAP |
| 14 | [Image segmentation](challenges/14-image-segmentation.md) | Pixel-level prediction, U-Net, Dice/IoU |

### Phase 5 — Advanced deep learning
| # | Challenge | Main skill |
| --- | --- | --- |
| 15 | [Sequence models](challenges/15-sequence-models.md) | Embeddings, RNN/LSTM, text classification |
| 16 | [Attention from scratch](challenges/16-attention-from-scratch.md) | Self-attention, the transformer block |
| 17 | [Autoencoders and VAEs](challenges/17-autoencoders-vae.md) | Latent spaces, generative models, reconstruction-based anomalies |
| 18 | [A tiny diffusion model](challenges/18-diffusion-model.md) | Noise schedules, denoising, image generation |

### Phase 6 — NLP with Hugging Face
| # | Challenge | Main skill |
| --- | --- | --- |
| 19 | [The Hugging Face ecosystem](challenges/19-hugging-face-tour.md) | Hub, `datasets`, tokenizers, pipelines |
| 20 | [Fine-tune a transformer classifier](challenges/20-fine-tune-transformer.md) | Trainer, DistilBERT, model cards, pushing to the Hub |
| 21 | [Embeddings and semantic search](challenges/21-embeddings-semantic-search.md) | Sentence embeddings, similarity, vector search |

### Phase 7 — Build a language model from scratch
| # | Challenge | Main skill |
| --- | --- | --- |
| 22 | [Build a tokenizer](challenges/22-build-a-tokenizer.md) | BPE, vocabulary, fertility |
| 23 | [GPT from scratch](challenges/23-gpt-from-scratch.md) | Decoder-only transformer, causal masking |
| 24 | [Pretrain a small language model](challenges/24-pretrain-slm.md) | Pretraining, perplexity, sampling, checkpoints |
| 25 | [Instruction-tune a GPT](challenges/25-instruction-tuning.md) | Supervised fine-tuning, chat formatting |

### Phase 8 — Working with LLMs (GenAI)
| # | Challenge | Main skill |
| --- | --- | --- |
| 26 | [Run LLMs locally and by API](challenges/26-run-llms.md) | Ollama, decoding settings, prompting, speed and memory |
| 27 | [Structured output and extraction](challenges/27-structured-output.md) | JSON schemas, validation, retries |
| 28 | [Evaluating LLMs](challenges/28-evaluating-llms.md) | Eval harnesses, LLM-as-judge, LLM vs fine-tuned model |

### Phase 9 — RAG
| # | Challenge | Main skill |
| --- | --- | --- |
| 29 | [RAG from scratch](challenges/29-rag-from-scratch.md) | Chunking, embedding, retrieval, grounded answers with citations |
| 30 | [Measure and improve retrieval](challenges/30-improve-retrieval.md) | Recall@k, BM25, hybrid search, reranking |
| 31 | [Evaluate RAG answers](challenges/31-evaluate-rag.md) | Faithfulness, "I don't know", splitting retrieval vs generation errors |

### Phase 10 — Fine-tuning LLMs
| # | Challenge | Main skill |
| --- | --- | --- |
| 32 | [LoRA fine-tuning](challenges/32-lora-fine-tuning.md) | LoRA, QLoRA, adapters, MLX on Mac |
| 33 | [Prompt vs RAG vs fine-tune](challenges/33-prompt-rag-or-finetune.md) | Choosing the right approach with evidence |

### Phase 11 — Agents
| # | Challenge | Main skill |
| --- | --- | --- |
| 34 | [Tool calling from scratch](challenges/34-tool-calling-from-scratch.md) | The agent loop, tools, observations |
| 35 | [A research agent](challenges/35-research-agent.md) | ReAct, a RAG tool, memory, guardrails |
| 36 | [Evaluating agents](challenges/36-evaluating-agents.md) | Task suites, success rate, failure taxonomy |
| 37 | [Frameworks, MCP, and multi-agent](challenges/37-frameworks-mcp-multi-agent.md) | LangGraph, MCP servers, when *not* to use multiple agents |

### Phase 12 — Deployment
| # | Challenge | Main skill |
| --- | --- | --- |
| 38 | [Serve a model](challenges/38-serve-a-model.md) | FastAPI, Docker, tests, latency |
| 39 | [Demo and monitoring](challenges/39-demo-and-monitoring.md) | Gradio UI, prediction logging, drift checks |

### Phase 13 — Kaggle II and capstone
| # | Challenge | Main skill |
| --- | --- | --- |
| 40 | [Kaggle NLP competition](challenges/40-kaggle-nlp.md) | The whole workflow, on your own |
| 41 | [Capstone](challenges/41-capstone.md) | Design, build, evaluate, and ship a system you choose |

---

## Files in this repo

| Path | What it is |
| --- | --- |
| `challenges/` | The curriculum. Read it, don't edit it. |
| `work/NN-name/` | Your code and `NOTES.md` for each challenge. You create these. |
| [`decision-map.md`](decision-map.md) | **Your** guide to "which approach for which problem." You fill it in as you go. |
| [`glossary.md`](glossary.md) | Plain-language definitions of the terms you'll meet. |
| [`progress.md`](progress.md) | Tick off challenges and record dates. |

---

## When you are stuck

1. Re-read the step and its ✅ checkpoint. Print shapes, types, and the first few rows. Most bugs show up there.
2. Give it 30 minutes of real effort.
3. Open the first hint. Then the next.
4. Ask your AI tool to **explain** the concept or the error, not just to "fix it." If it fixes something, make sure you understand why the fix works before moving on.
5. Still stuck after a day? Write down what you tried in `NOTES.md`, mark the challenge "partial" in `progress.md`, and move on. Come back after the next challenge. Sometimes the next one teaches what you were missing.

## Can I skip a challenge?

Yes, if you can already make every decision in the challenge yourself (approach, split, metric, risks) and explain every "Done when" item without hints. Write one line in `progress.md` saying what you skipped and why. Don't skip Phase 0. Challenge 01 matters most of all.
