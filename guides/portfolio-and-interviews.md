# Portfolio and interviews

How to turn the work in this repo into a portfolio and interview answers. Without job experience, **your projects are your experience**, so present them the way an engineer would describe work.

---

## 1. What employers want to see

For an entry-level AI/ML engineer, the signals that matter most:

1. **Judgment:** you picked a sensible approach, a baseline, a metric that fits the problem, and you can say why.
2. **Honest evaluation:** held-out data, no leakage, errors analysed, limitations stated.
3. **Engineering:** code someone else can run; an API or demo; tests; clean repo.
4. **GenAI fluency:** RAG, fine-tuning, agents, and how to evaluate them.
5. **Communication:** clear write-ups with numbers and decisions.

Many candidates have notebooks with high accuracy. Fewer can explain why their split was right, what their baseline was, and where their model fails. That's your advantage.

---

## 2. What to put in your portfolio

Don't show all 42 challenges. Pick **4–6 strong projects** that cover different areas, plus the capstone.

| Area | Good candidates |
| --- | --- |
| Classical ML + evaluation | 04 Fraud (thresholds and costs), 06 Forecasting (leakage), 08 Kaggle |
| Deep learning / CV | 12 Transfer learning, 13 Detection |
| LLM from scratch | 24 Pretrained SLM (a strong conversation starter) |
| NLP / Hugging Face | 20 Fine-tuned transformer + model card (pushed to the Hub) |
| GenAI | 29–31 RAG with evaluation; 33 Prompt vs RAG vs fine-tune |
| Agents | 34–36 Agent with evaluation and safety tests |
| Deployment | 38–39 API + demo + monitoring |
| Capstone | 41 |

Pin them on GitHub, each with its own polished README.

---

## 3. Project README template

```markdown
# <Project name>

**One sentence:** what it does and for whom.

## Problem
The situation, input → output, and why it matters. Which mistake is costly.

## Approach
- Problem type and why.
- Data: source, size, license, split (and why that split).
- Baseline(s).
- Models/system tried, and the final choice with the reason.
- Architecture diagram (for RAG/agent/deployment projects).

## Results
| System | Main metric | Second metric | Latency/cost |
|---|---|---|---|
| Baseline | … | … | … |
| Final | … | … | … |
(Test set, used once. Include the uncertainty range if the test set is small.)

## What I learned from the errors
2–4 bullet points from error analysis, with one or two concrete examples.

## Limitations
Where it fails; what I would not use it for.

## Run it
One command to set up, one to reproduce the results, one to run the demo.
```

Your `NOTES.md` files already contain most of this. The README is the polished version.

---

## 4. Interview stories (STAR)

Prepare 5–6 stories from your challenges. Use **STAR**:

- **Situation:** the problem and context.
- **Task:** what you had to decide or build.
- **Action:** what *you* did, especially the decisions.
- **Result:** numbers, and what you learned.

**Example (from Challenge 06):**
> *Situation:* forecasting hourly bike demand for next-day planning.
> *Task:* a model the operations team could trust.
> *Action:* I listed every feature and whether it would be known the evening before. Two columns were the target split in two, so I excluded them. I compared a random split with a time split: the random split looked 30% better, but that's because it leaked neighbouring hours. I used a time split with a seasonal-naive baseline.
> *Result:* the model beat the baseline by X% MAE on the final three months. The biggest errors were in bad-weather hours, which I flagged as a limitation.

Good stories to prepare:
- A time you found **leakage** or a too-good-to-be-true result.
- A time the **simple model won** (and you shipped it).
- A **metric choice** driven by business costs.
- A **debugging** story (training wouldn't converge; what you checked).
- A **GenAI evaluation** story (retrieval vs generation errors; judge agreement).
- A **trade-off** (quality vs latency/cost; fine-tune vs RAG).

### About AI-assisted coding
Be honest: "I use AI coding tools to implement; I make the design decisions and verify the output." Then show it: explain *why* a split was chosen, or how you caught a bug in generated code. Interviewers care that you understand the code you ship.

---

## 5. Common interview question types

### ML fundamentals
- Bias vs variance; overfitting and how to detect and fix it.
- Precision vs recall; when to use which; PR-AUC vs ROC-AUC.
- How gradient boosting works; why trees don't need scaling.
- Regularization (L1 vs L2, dropout, early stopping).
- Cross-validation and data leakage.
- How you'd handle imbalanced data, missing values, high-cardinality categories.

The [guides](README.md) cover these. If you can explain each from the guides in your own words, with an example from a challenge, you're well prepared.

### Deep learning and LLMs
- Backpropagation in simple terms; vanishing gradients.
- CNN vs transformer; how attention works.
- What pretraining, instruction tuning and RLHF/DPO each do.
- Tokenization; context windows; why LLMs hallucinate.
- LoRA: what it changes and why it saves memory.
- Prompt vs RAG vs fine-tuning: when each.

### ML system design (the format)

You'll get an open question like "Design a system to detect fraudulent listings" or "Design a support chatbot for our docs." Walk through it in this order:

```
1. Clarify    — users, scale, latency needs, what "success" means, constraints
2. Frame      — input → output, problem type, labels available?
3. Metrics    — offline metric and business metric; which mistake is worse
4. Data       — sources, labels, split strategy, leakage risks
5. Baseline   — the simplest thing that could work
6. Model      — approach and why; alternatives considered
7. Evaluation — how you'd test it before launch; error analysis
8. Serving    — batch or real-time; latency and cost; fallbacks
9. Monitoring — drift, quality checks, feedback loop, retraining
10. Risks     — failure modes, safety, privacy, fairness
```

This is Challenge 01 + the guides, stretched to a whole system. Practise by answering one design question per week out loud, using the framework.

### Coding
- Python and pandas data manipulation; writing a metric (precision, IoU) from scratch; a training loop; sometimes general algorithm questions.
- You may not have an AI tool in the interview, so practise the basics: pandas groupby/merge, NumPy, a PyTorch training loop.

---

## 6. Online presence (light touch)

- **GitHub:** clean, pinned projects with READMEs. Delete or archive messy repos.
- **Hugging Face:** your fine-tuned model with a model card (Challenge 20), and a Space demo (Challenge 39).
- **Kaggle:** a published notebook write-up (Challenge 40).
- **A short write-up or post** about one project, e.g. what you learned comparing prompting, RAG and fine-tuning. Explaining clearly is a skill employers notice.
