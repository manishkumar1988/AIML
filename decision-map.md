# My Decision Map

**This is your document.** It answers the question a course doesn't: *given a problem, what do I try first, and how do I know whether it worked?*

You fill it in as you go. Every challenge ends with a "Reflect" step that tells you which section to update. Write in your own words. Short is better than complete. By Challenge 41 this page is your personal playbook, and it's what interviewers are really testing.

A few rows are filled in as examples. Replace them with your own wording once you've done the challenge.

---

## Step 1 — What kind of problem is it?

Ask these questions in order.

1. **What goes in, and what comes out?** (a table row → a number? an image → boxes? a question → an answer with sources?)
2. **Do I have examples of the right answer (labels)?** If yes, it's supervised. If no, it's unsupervised, or you need to create labels.
3. **Does time matter?** If the future is predicted from the past, you need time-aware splits and features.
4. **Is the output fixed (a category, a number) or open-ended (text, an image)?** Open-ended outputs usually mean generative models and harder evaluation.
5. **Does the system need to take actions or look things up?** That points to RAG or an agent.

| Signal in the problem | Problem type | First challenge that teaches it |
| --- | --- | --- |
| Predict a number from table columns | Regression | 02 |
| Predict a category from table columns | Classification | 03 |
| One class is very rare (fraud, defects, disease) | Imbalanced classification | 04 |
| "Find groups" / "find the weird ones" with no labels | Clustering / anomaly detection | 05 |
| "Predict next week / next month" | Time series forecasting | 06 |
| Images → one label | Image classification | 10, 12 |
| Images → where objects are | Object detection | 13 |
| Images → which pixels belong to what | Segmentation | 14 |
| Text → a category | Text classification | 15, 20 |
| "Find similar items / documents" | Embeddings + similarity search | 21 |
| Generate new text, images | Generative model | 18, 24, 26 |
| Pull fields out of messy text | Extraction (structured output) | 27 |
| Answer questions about *my* documents | RAG | 29 |
| Model needs a new style or format, or a narrow skill | Fine-tuning | 32 |
| Do multi-step tasks using tools | Agent | 34 |

---

## Step 2 — For each problem type: start here

Fill these in as you finish each challenge.

### Regression (02)
- **Baseline:** predict the mean or median of the training target. *(example)*
- **First real model:**
- **Stronger model:**
- **Metric I'd report:**
- **Watch out for:**

### Classification (03)
- **Baseline:**
- **First real model:**
- **Stronger model:**
- **Metric I'd report:**
- **Watch out for:**

### Imbalanced classification (04)
- **Baseline:**
- **Why accuracy is wrong here:**
- **Metric I'd report:**
- **How I choose a threshold:**
- **Watch out for:**

### No labels: clustering and anomaly detection (05)
- **When I'd cluster:**
- **When I'd use anomaly detection instead:**
- **How I'd know it's any good without labels:**
- **Watch out for:**

### Time series (06)
- **Baseline:** "same as last week" (seasonal naive). *(example)*
- **How I split:**
- **Features that leak:**
- **Watch out for:**

### Choosing between classical models (07)
- **Linear/logistic regression when:**
- **Tree ensembles (random forest, gradient boosting) when:**
- **How I tune without fooling myself:**

### Neural networks (09–11)
- **When a neural net beats gradient boosting:**
- **When it doesn't:**
- **My debugging checklist when training goes wrong:**

### Computer vision (12–14)
- **Classification vs detection vs segmentation — how I choose:**
- **Train from scratch vs transfer learning:**
- **Metric for each:**

### Sequence and generative models (15–18)
- **RNN/LSTM vs transformer:**
- **Autoencoder / VAE / diffusion — what each is good for:**

### Text classification (15, 20)
- **Baseline:** TF-IDF + logistic regression. *(example)*
- **When a fine-tuned transformer is worth it:**
- **When an LLM prompt is enough:**

### Embeddings and search (21)
- **When I'd use embeddings:**
- **Keyword (BM25) vs embeddings:**

### Language models from scratch (22–25)
- **What pretraining gives you:**
- **What instruction tuning adds:**
- **Why I wouldn't pretrain an LLM at work:**

### Using LLMs (26–28)
- **Local model vs API — how I choose:**
- **How I get reliable structured output:**
- **How I evaluate an LLM feature before shipping:**

### RAG (29–31)
- **When RAG is the right answer:**
- **Default pipeline I'd start with:**
- **How I tell a retrieval failure from a generation failure:**

### Fine-tuning (32–33)
- **Prompting vs RAG vs fine-tuning — my rule:**
- **LoRA vs full fine-tune:**

### Agents (34–37)
- **When an agent is worth it (and when a fixed pipeline is better):**
- **Guardrails I always add:**
- **How I evaluate an agent:**

### Deployment (38–39)
- **What "production-ready" means for a model:**
- **What I monitor:**

---

## Step 3 — Always, for every problem

- [ ] I wrote down the problem type and the metric *before* building.
- [ ] I have a dumb baseline.
- [ ] I split the data before doing anything that learns from it.
- [ ] I looked at actual mistakes, not just the average score.
- [ ] I can say what I'd ship, what I wouldn't, and what I still don't know.
