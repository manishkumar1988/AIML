# Problem types, baselines and metrics

A reference to keep open while you work. Every new problem goes through the same three questions:

1. **What kind of problem is it?** → Part 1
2. **What's the dumbest thing that could work?** → Part 2 (baselines)
3. **How will I know it worked?** → Part 3 (metrics)

Don't try to memorize this page. Use it every time. After a few months, you won't need it.

---

## Part 1 — What kind of problem is it?

### The 30-second decision path

Answer these in order. Stop at the first one that settles it.

```
1. Is it actually ML?
   Could a SQL query, a fixed rule, a lookup, or an existing tool answer it?
   └─ yes → NOT ML. Write the query / rule. Done.

2. What comes out?
   ├─ a number ......................................... → REGRESSION
   │     └─ a number about the FUTURE, over time ...... → TIME SERIES FORECASTING
   ├─ one category from a fixed list
   │     ├─ 2 categories ............................... → BINARY CLASSIFICATION
   │     │     └─ one category is very rare ........... → IMBALANCED CLASSIFICATION
   │     └─ 3+ categories .............................. → MULTICLASS CLASSIFICATION
   ├─ several categories at once (0, 1 or many) ......... → MULTI-LABEL CLASSIFICATION
   ├─ an ordered list of items ........................... → RANKING / RECOMMENDATION / SEARCH
   ├─ groups, with no categories given in advance ....... → CLUSTERING
   ├─ "which ones are weird?", with no examples of weird → ANOMALY DETECTION
   ├─ fields pulled out of text or documents ............ → EXTRACTION (NER / structured output)
   ├─ new text, images or audio ......................... → GENERATION
   ├─ an answer about MY documents, with sources ........ → RAG
   └─ ACTIONS taken in other systems (search, book, send) → AGENT

3. What goes in?
   Images → computer vision version of the above:
     one label per image ............ IMAGE CLASSIFICATION
     boxes around objects ........... OBJECT DETECTION
     a label for every pixel ........ SEGMENTATION
   Text → NLP version: text classification, NER, embeddings/search, LLMs.
   Table of columns → classical ML (gradient boosting is king).

4. Do I have labels (examples of the right answer)?
   ├─ yes → supervised (regression, classification, ...)
   ├─ no  → unsupervised (clustering, anomaly detection), or
   │        create labels (hand-label a sample, use an LLM to label, use proxy labels)
   └─ only "normal" examples → anomaly detection, or one-class methods

5. Does time matter?
   If I'm predicting the future from the past → split by time, and only use
   features I'd know at prediction time. Even if it's "just" classification.
```

### Problem-type cards

Each card shows how to recognize the type, and what to do first.

---

#### Regression — predict a number
- **Sounds like:** "how much," "how many," "what price," "how long."
- **Examples:** a used car's price; delivery time in minutes; a house's energy use.
- **Baseline:** predict the training **mean** (or **median**, if there are outliers).
- **Then:** linear regression → gradient boosting (LightGBM/XGBoost/`HistGradientBoosting`).
- **Metric:** **MAE** (easy to explain: "off by 7 minutes on average"); RMSE if big errors are especially bad.
- **Watch out:** heavy tails (a few huge values); the target's units; whether over- or under-predicting costs more.

#### Binary classification — yes or no
- **Sounds like:** "will they," "is it," "should we flag."
- **Examples:** will a user click this ad; is this email spam; will a loan be repaid.
- **Baseline:** predict the **majority class** for everyone; or a simple rule from a domain expert.
- **Then:** logistic regression → gradient boosting.
- **Metric:** depends on balance and costs (see Part 3): F1, precision/recall at a threshold, ROC-AUC.
- **Watch out:** the threshold is a business decision, not 0.5 by default.

#### Imbalanced classification — yes/no where "yes" is rare
- **Sounds like:** "fraud," "defect," "failure," "disease," "churn" — anything rare and costly.
- **Rule of thumb:** if the rare class is under ~10%, treat it as imbalanced. Under 1%, very imbalanced.
- **Baseline:** "always no" (shows why accuracy is useless); a rule ("flag if amount > X").
- **Then:** logistic regression or gradient boosting with class weights → choose the threshold by cost.
- **Metric:** **PR-AUC (average precision)**; precision and recall at your chosen threshold; **precision@k** if a team can only review k cases.
- **Watch out:** accuracy and ROC-AUC look great while the model is useless; very few positives means noisy numbers.

#### Multiclass classification — one of many categories
- **Sounds like:** "which category," "route to which team," "what type."
- **Examples:** which of 20 product categories; which language a text is in.
- **Baseline:** majority class; keyword rules.
- **Then:** logistic regression / gradient boosting (tables), TF-IDF + linear model (text), fine-tuned transformer (text with enough data).
- **Metric:** **macro-F1** (every class counts equally) + accuracy; look at the confusion matrix for confused pairs.
- **Watch out:** rare classes vanish inside overall accuracy.

#### Multi-label classification — several tags at once
- **Sounds like:** "tag with all that apply," "can be both X and Y."
- **Examples:** movie genres (action *and* comedy); topics of a news article.
- **How it differs from multiclass:** multiclass = pick exactly one; multi-label = any number, including zero.
- **Baseline:** predict each label's most common value; keyword rules per label.
- **Then:** one binary classifier per label (one-vs-rest), or a single model with one sigmoid output per label.
- **Metric:** per-label precision/recall/F1 (or average precision), then micro/macro averages. **A threshold per label.**

#### Ranking / recommendation / search — an ordered list
- **Sounds like:** "show the most relevant," "suggest," "related items," "search results."
- **Examples:** product search; "people you may know"; which help article to show first.
- **Baseline:** most popular items; same category; keyword search (**BM25**) for text.
- **Then:** embeddings + similarity search; learning-to-rank; collaborative filtering for recommendations.
- **Metric:** **Recall@k**, **precision@k**, **MRR**, **nDCG@k** offline; click-through or conversion in an A/B test online.
- **Watch out:** only the top few positions matter to users.

#### Clustering — find groups, no labels
- **Sounds like:** "segment," "group," "what types of … do we have," with no predefined categories.
- **Examples:** grouping shoppers by behaviour; grouping support tickets into themes.
- **Baseline:** simple hand-made segments (e.g. high/medium/low spend × recent/old).
- **Then:** K-means (scaled features) → Gaussian mixtures, DBSCAN; for text, cluster embeddings.
- **Metric:** no single right answer. Silhouette score helps, but the real test is **"can the business name and act on each group?"**
- **Watch out:** forgetting to scale features; picking the number of groups by a number alone.

#### Anomaly detection — find the weird ones, no labels for weird
- **Sounds like:** "unusual," "strange behaviour," "outliers," and there are few or no examples of the bad thing.
- **Examples:** a sensor reading drifting; a sudden spike in logins from one account.
- **Baseline:** simple thresholds (value > mean + 3 standard deviations) per metric.
- **Then:** Isolation Forest; autoencoder reconstruction error; for time series, deviation from a forecast.
- **Metric:** if some labels exist later: precision of the top-k alerts. Otherwise, human review of alerts.
- **Anomaly detection vs imbalanced classification:** if you have *labelled examples* of the rare bad thing, use classification (it's usually better). If you don't, use anomaly detection.

#### Time series forecasting — a number in the future
- **Sounds like:** "next week," "next month," "tomorrow," "how many will we need."
- **Examples:** call-centre volume per hour; electricity demand; daily website visits.
- **Baseline:** **naive** (same as last period) or **seasonal naive** (same day last week / same month last year). Surprisingly hard to beat.
- **Then:** gradient boosting with lag and calendar features; classical models (ETS, ARIMA) or libraries like Prophet for single series.
- **Metric:** **MAE**, **WAPE** (total absolute error ÷ total actual, good for many products); avoid plain MAPE when actual values can be near zero.
- **Watch out:** **split by time, never randomly**; only use features you'd know at forecast time; seasonality and holidays.

#### Image classification — one label per image
- **Examples:** which plant species; is this X-ray normal.
- **Baseline:** majority class.
- **Then:** **transfer learning** from a pretrained CNN/ViT (almost always better than training from scratch with small data).
- **Metric:** accuracy and macro-F1; per-class recall; confusion matrix.

#### Object detection — where are the objects?
- **Sounds like:** "locate," "count," "where."
- **Examples:** counting cars in a parking lot; finding helmets on construction workers.
- **Baseline:** a pretrained detector used as-is (e.g. COCO-trained YOLO).
- **Then:** fine-tune a detector on your labelled boxes.
- **Metric:** **mAP@0.5** (and mAP@0.5:0.95); for counting, count error.

#### Segmentation — label every pixel
- **Sounds like:** "outline," "exact shape," "cut out," "measure the area."
- **Examples:** road vs not-road for self-driving; leaf area affected by disease.
- **Baseline:** "all background"; a simple threshold on colour.
- **Then:** U-Net with a pretrained encoder; foundation models (SAM) with prompts.
- **Metric:** **IoU** or **Dice**. Not pixel accuracy (background dominates).

#### Text classification
- Same as binary/multiclass/multi-label above, with text as input.
- **Baseline:** keyword rules; **TF-IDF + logistic regression** (strong, fast, explainable).
- **Then:** a fine-tuned transformer (DistilBERT etc.) if you have hundreds+ labelled examples per class; an LLM with a prompt if you have few labels.

#### Extraction — pull fields out of text
- **Sounds like:** "pull out," "fill a spreadsheet from documents," "find the names/dates/amounts."
- **Examples:** invoice number and total from invoices; drug names from clinical notes.
- **Baseline:** **regex** for fixed patterns (emails, dates, amounts, IDs).
- **Then:** NER model (token classification) for entity types; an **LLM with a JSON schema** for messy documents and many fields.
- **Metric:** **field-level accuracy / precision / recall**; span-level F1 for NER; JSON validity rate for LLMs.

#### Generation — produce new content
- **Sounds like:** "write," "summarize," "translate," "rewrite," "create images."
- **Examples:** product descriptions from specs; meeting summaries.
- **Baseline:** a template; for summaries, the first few sentences ("lead-3"); an off-the-shelf model with a simple prompt.
- **Then:** better prompts and few-shot examples → RAG for facts → fine-tuning (LoRA) for style/format.
- **Metric:** **human ratings with a rubric written in advance**; LLM-as-judge *checked against human ratings*; task-specific checks (facts preserved? format followed?). ROUGE/BLEU only as rough signals.
- **Watch out:** "it looked good in 5 examples" is not an evaluation.

#### RAG — answer questions about specific documents
- **Sounds like:** "answer questions about our docs/policies/contracts," "with sources," "the info changes often."
- **Baseline:** keyword search that shows the matching passage (no LLM); an LLM with no retrieval.
- **Then:** chunk → embed → retrieve (hybrid BM25 + embeddings) → rerank → generate with citations.
- **Metric:** retrieval **Recall@k** (did the right passage come back?), then answer **correctness**, **faithfulness** (supported by sources?), **citation accuracy**, and correct "I don't know."
- **RAG vs fine-tuning:** facts and frequently changing information → RAG. Style, format, narrow skills → fine-tuning.

#### Agent — take actions using tools
- **Sounds like:** "and then do," "book," "update the system," multi-step tasks that need to look things up and act.
- **Baseline:** a fixed workflow (the same steps every time). If the steps never change, you don't need an agent.
- **Then:** an LLM with tools in a loop, with guardrails (step limits, confirmation for actions with side effects).
- **Metric:** **task success rate** over repeated runs, safety pass rate, steps, cost and time per task.

#### Not ML
- **Sounds like:** "count," "sum," "report," "list all," "when X happens, do Y" with a clear rule.
- **Examples:** monthly revenue per region; send an alert when stock < 10 units.
- **Do:** SQL, a dashboard, a rule. Cheaper, exact and easier to maintain.
- **Also not "build a model":** problems where an existing product or API already works (translation, speech-to-text, OCR). Use it; measure it on your data.

---

### Pairs people mix up

| Confusing pair | How to tell them apart |
| --- | --- |
| Regression vs classification | Is the output a number where "how far off" matters (price: 98 vs 100 is close)? Regression. Is it a category (A or B)? Classification. Buckets of a number ("low/medium/high spend") can go either way. Regression keeps more information. |
| Multiclass vs multi-label | Exactly one answer → multiclass. Zero, one or several → multi-label. |
| Forecasting vs regression | Forecasting is regression where the future matters: time-based split, lag features, seasonality. If a date is involved and you predict ahead, treat it as forecasting. |
| Imbalanced classification vs anomaly detection | Do you have labelled examples of the rare bad thing? Yes → classification. No → anomaly detection. |
| Clustering vs classification | Are the categories known in advance with labelled examples? Classification. Discovering the categories? Clustering. |
| Classification vs ranking | Does the user see one decision (approve/reject)? Classification. A list where order matters (top 10)? Ranking, even if you use a classifier's scores to sort. |
| Detection vs segmentation | Is a box enough (counting, locating)? Detection. Do you need the exact shape or area? Segmentation. |
| RAG vs fine-tuning | New or changing *knowledge* → RAG. New *behaviour, format or style* → fine-tuning. Try prompting first for both. |
| Workflow vs agent | Same steps every time → fixed workflow. Steps depend on what you find → agent. |
| ML vs not ML | Can you write the rule down exactly? Then write the rule. |

---

## Part 2 — Baselines

### Why bother?
A baseline is the simplest thing that could work. It tells you:
- whether your model is actually useful ("92% accuracy" means nothing if "always no" gets 91%);
- whether there's a bug (a model *worse* than the baseline is broken);
- whether the problem needs ML at all (sometimes the rule is good enough).

**Always report your model next to its baseline, on the same data.**

### Two levels of baseline

1. **Dumb baseline:** no learning at all. Shows the floor.
2. **Simple baseline:** the simplest reasonable model or rule. Shows what you have to beat for the complex model to be worth it.

| Problem type | Dumb baseline | Simple baseline |
| --- | --- | --- |
| Regression | Mean or median of training target | Linear regression; median per group (e.g. per city) |
| Binary / multiclass (tables) | Majority class | Logistic regression; a domain-expert rule |
| Imbalanced | "Always no" | Rule (amount > X); logistic regression with class weights |
| Multi-label | Most common value per label | Keyword rules per label; one logistic regression per label |
| Text classification | Majority class | Keyword rules; TF-IDF + logistic regression |
| Time series | Last value (naive) | Same period last week/year (seasonal naive); moving average |
| Ranking / search | Most popular items | BM25 keyword search; same-category items |
| Clustering | One group | Hand-made segments from 1–2 columns |
| Anomaly detection | Flag nothing | Threshold at mean ± 3 standard deviations |
| Image classification | Majority class | Pretrained model + linear layer (linear probe) |
| Object detection | — | Pretrained detector as-is |
| Segmentation | All background | Colour threshold; centred shape |
| Extraction | — | Regex for fixed patterns |
| Generation / summarization | Template; first few sentences | Off-the-shelf LLM, simple prompt |
| RAG | LLM with no retrieval | Keyword search showing the passage |
| Agent | — | A fixed workflow |

---

## Part 3 — Metrics

### Step 1: which mistake is worse?

Almost every metric choice comes from this question. In classification there are two ways to be wrong:

- **False positive (FP):** you said yes, the truth was no. *A false alarm.*
- **False negative (FN):** you said no, the truth was yes. *A miss.*

| Situation | Which is worse? | So focus on |
| --- | --- | --- |
| Cancer screening (a doctor reviews flags) | Missing cancer (FN) | **Recall** |
| Spam filter (moves email to spam) | Losing a real email (FP) | **Precision** |
| Fraud review (team reviews 100/day) | Wasting the team's limited slots (FP) *and* missing fraud (FN) | **Precision@100**, plus cost |
| Recommending a product | Neither is very costly | Ranking metrics (Recall@k) |
| Factory safety shutdown | Missing a real failure (FN) | **Recall**, at an acceptable false-alarm rate |

If you can put a cost on each mistake (e.g. a miss costs €100, a false alarm €2), you can choose the threshold that minimizes total cost. That's the most convincing way to choose.

### Step 2: the confusion matrix

```
                    Predicted YES        Predicted NO
Actually YES        True Positive (TP)   False Negative (FN)  ← misses
Actually NO         False Positive (FP)  True Negative (TN)
                    ↑ false alarms
```

Everything below comes from these four numbers.

### Classification metrics

| Metric | Plain meaning | Use when | Lies when |
| --- | --- | --- | --- |
| **Accuracy** = (TP+TN) / all | How often it's right | Classes are balanced and mistakes cost the same | The classes are imbalanced: "always no" scores 99% on 1% fraud |
| **Precision** = TP / (TP+FP) | "When it says yes, is it right?" | False alarms are costly; limited review capacity | On its own: you can get 100% by flagging only one easy case |
| **Recall** = TP / (TP+FN) | "Of all the real yeses, how many did it find?" | Misses are costly | On its own: you can get 100% by flagging everything |
| **F1** | One number balancing precision and recall | You need one number and both mistakes matter | The costs of FP and FN are very different. Use a cost or Fβ instead |
| **ROC-AUC** | How well it ranks yeses above nos, across all thresholds | Comparing models on balanced-ish data | Very rare positives. Looks great while precision is terrible |
| **PR-AUC / average precision** | Precision-recall trade-off, summarized | **Imbalanced data** | Rarely misleading, but harder to explain to non-technical people |
| **Precision@k** | Of the top k flagged, how many are right? | A team can only review k cases | — |
| **Macro-F1** | F1 per class, averaged equally | Multiclass where small classes matter | — |
| **Micro-F1** | F1 over all predictions pooled | You care about overall volume | Small classes are ignored |
| **Log loss / calibration** | Are the probabilities trustworthy? | You'll use the probability itself (risk scores, pricing) | — |

**Memory aid:** **P**recision is about your **P**redictions (of the ones you flagged…). **R**ecall is about **R**eality (of the real ones…).

### Regression metrics

| Metric | Plain meaning | Use when | Watch out |
| --- | --- | --- | --- |
| **MAE** | Average size of the error, in real units | Default. Easy to explain | Treats a few huge errors the same as many small ones |
| **RMSE** | Like MAE, but big errors count more | Big mistakes are especially bad | Harder to explain; dominated by outliers |
| **MAPE** | Average error as a percentage | Values are all well above zero | Explodes when actual values are near zero |
| **WAPE** | Total error ÷ total actual | Forecasting many items of different sizes | — |
| **R²** | Share of variation explained (1 = perfect) | Comparing models on the same data | Means nothing to a business person. Report MAE too |

### Ranking and retrieval metrics

| Metric | Plain meaning |
| --- | --- |
| **Recall@k** | Did a right item appear in the top k? (For RAG: did the right passage get retrieved?) |
| **Precision@k** | What fraction of the top k is right? |
| **MRR** | How high up is the first right item? (1st place = 1, 2nd = 0.5, 3rd = 0.33…) |
| **nDCG@k** | Rewards right items near the top, and handles "very relevant" vs "somewhat relevant" |

### Vision metrics

| Metric | Plain meaning |
| --- | --- |
| **IoU** | Overlap ÷ union of predicted and true box/mask. 1 = perfect, 0 = no overlap |
| **mAP@0.5** | Detection quality, counting a box as right if IoU ≥ 0.5 and the class is right |
| **Dice** | Similar to IoU, common for medical segmentation |

### Generation and LLM metrics

| Metric | Plain meaning | Note |
| --- | --- | --- |
| **Human rubric score** | You rate outputs on criteria you wrote *before* seeing them | The gold standard. Slow |
| **LLM-as-judge** | A strong model rates outputs | Only after checking it agrees with your own ratings |
| **Exact match / field accuracy** | Output equals the expected answer | For classification and extraction with LLMs |
| **Faithfulness** | Every claim is supported by the source | Essential for RAG and summaries |
| **Perplexity** | How surprised a language model is by real text | Only comparable with the same tokenizer |
| **ROUGE / BLEU** | Word overlap with a reference | Rough signal only. A summary can score well and still invent facts |
| **Task success rate** | Did the agent achieve the goal? | Run each task several times |

### Always report alongside quality
- **Latency** (how long per request) and **cost** (per 1,000 requests) — especially for LLMs.
- **The baseline's score, on the same data.**
- **How uncertain the number is**, when the test set is small (bootstrap or cross-validation range).

---

## Part 4 — Three worked examples

These aren't from Challenge 01. Use them to see the full thinking pattern.

### Example A: "A gym wants to know which members will cancel next month so staff can call them."
- **Input → output:** one member's history (visits, plan, tenure, payments) → probability of cancelling next month.
- **Problem type:** binary classification. Probably imbalanced (maybe 3–5% cancel per month). Time matters: train on past months, test on a later month.
- **Labels:** yes. Past cancellations are in the billing system.
- **Baseline:** "always no" (to show accuracy is useless) and a rule: "no visits in the last 3 weeks."
- **Metric:** staff can call ~50 members a month → **precision@50** (how many of those 50 were really going to cancel), plus recall@50. PR-AUC to compare models.
- **Which mistake is worse:** a missed canceller loses revenue; a wasted call costs a few minutes. So recall matters, within the 50-call capacity.
- **Is ML needed?** Probably yes, but if the 3-week rule gets similar precision, ship the rule first.

### Example B: "A hotel chain wants to know how many rooms will be booked each night for the next 30 days, per hotel."
- **Input → output:** hotel + date → number of booked rooms.
- **Problem type:** time series forecasting (regression over time, many series).
- **Labels:** yes. Past occupancy.
- **Baseline:** seasonal naive: same weekday last year (holidays need care), or same weekday last week.
- **Metric:** **MAE** in rooms per hotel per night, and **WAPE** across hotels of different sizes.
- **Which mistake is worse:** under-forecasting → too few staff, bad service. Over-forecasting → overstaffing cost. Ask the business which hurts more.
- **Watch out:** split by time; already-made bookings for future dates are a powerful and *legitimate* feature (you know them at forecast time). The final number of cancellations is not.
- **Is ML needed?** Yes, if the seasonal naive baseline isn't good enough.

### Example C: "A university wants students to ask questions about course rules and deadlines in a chat."
- **Input → output:** a question → an answer with a link to the rule it came from, or "I don't know."
- **Problem type:** RAG over the university's documents (rules change each year, so not fine-tuning).
- **Labels:** no existing ones. Write 50–100 test questions with the correct answer and source, including questions the documents can't answer.
- **Baseline:** the website's keyword search showing the matching page; an LLM with no documents.
- **Metric:** retrieval Recall@5; answer correctness; citation accuracy; correct "I don't know" rate.
- **Which mistake is worse:** a confident wrong deadline is far worse than "I don't know, please check with the office." Favour abstaining.
- **Is ML needed?** A well-organized FAQ page might solve most of it. Check the top 20 questions first.

---

## Part 5 — One-page quick card

```
FIRST:    Is it ML at all? (rule / SQL / existing tool?)
OUTPUT:   number → regression | future number → forecasting
          one class → classification | many tags → multi-label
          ordered list → ranking | groups → clustering | weird → anomaly
          fields from text → extraction | new content → generation
          answer from my docs → RAG | actions → agent
INPUT:    table → gradient boosting | text → TF-IDF, then transformer/LLM
          image → transfer learning (classify / detect / segment)
LABELS:   have them → supervised | none → unsupervised or create some
TIME:     predicting the future → split by time, no future features
BASELINE: dumb (mean / majority / last value / no retrieval)
          + simple (linear / TF-IDF / BM25 / rule / seasonal naive)
METRIC:   which mistake is worse? FP (false alarm) or FN (miss)?
          balanced → accuracy, F1 | rare positive → PR-AUC, precision@k
          number → MAE | ranking → Recall@k, nDCG | boxes → mAP
          masks → IoU | text generation → rubric + validated judge
          RAG → retrieval recall + faithfulness | agent → success rate
ALWAYS:   baseline on the same data, look at errors, write the decision
```
