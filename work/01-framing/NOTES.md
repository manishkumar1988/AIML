# Challenge 01 — Problem framing

## Top 3 lessons

1. **Problems without a fixed label are different types, and the wording gives them away.**
   - "Related" or "similar" → similarity search / ranking (#12, #20).
   - "Copied from each other" → near-duplicate detection (#21).
   - "Strange" or "unusual" with no labelled incidents → anomaly detection (#13).
   - "What types of … do we have" → clustering (#5).
   - I mixed these up in four requests.
2. **Labels are past examples of the correct *output*; inputs are what the model reads.**
   - Past sale prices are labels; house size and location are inputs (#3).
   - Radiologist-drawn masks are labels (#8).
   - Boxes drawn around objects are labels (#9).
3. **The metric starts with "which mistake is worse?", and sometimes the answer isn't ML at all.**
   - False alarms vs misses decides precision vs recall (#2, #7, #21).
   - #24 is a SQL query. #23 should use an existing translation tool.
   - Regex, rules and thresholds are baselines worth measuring first (#11, #13, #16).

---

## 1. An online store wants to predict how many units of each product will sell next week.

- **Input → output:** each product's weekly sales history + things known in advance (price, planned promotions, holidays, season) → units sold next week, per product
- **Problem type:** time series forecasting (many series, one per product)
- **Labels:** yes — past weekly units sold per product
- **Baseline:** seasonal naive (same week last year), or the average of the last 4 weeks
- **Metric (and which mistake is worse):** MAE per product; WAPE across products, so big and small sellers are compared fairly. Which mistake is worse depends on the product: for perishables, over-forecasting (waste) is worse; for durable, high-margin items, under-forecasting (stockout, lost sales) is worse. Ask the business.
- **Is ML needed, and why?:** probably. Thousands of products with promotions and holidays are hard for simple rules, but first measure how good the seasonal-naive baseline already is. Evaluate with a time-based split.

**Correction after checking the reference:** Original matched the reference closely. Input listed only the output; the metric line was missing which mistake is worse; the "Is ML needed" line contained the overstock/stockout sentence, which belongs in the metric line.

---

## 2. A bank wants to flag credit-card transactions that might be fraud, for a team that can review 200 a day.

- **Input → output:** one transaction (amount, time, merchant, country, device) + the customer's usual behaviour → fraud score; the top 200 per day go to reviewers
- **Problem type:** imbalanced binary classification, used as a ranking for a fixed review capacity
- **Labels:** confirmed fraud cases (chargebacks, investigation outcomes). They arrive late, weeks after the transaction.
- **Baseline:** rules (amount > X, new country, many transactions in a short time)
- **Metric (and which mistake is worse):** precision in the top 200 per day (capacity); share of fraud value caught; PR-AUC to compare models. Missing fraud costs money; false alarms waste the limited 200 review slots.
- **Is ML needed, and why?:** yes. Fraud patterns are many and change over time, so fixed rules miss them. Keep rules as the baseline and as features. Split by time.

**Correction after checking the reference:** Original matched the reference closely. Input was too thin (only amount and time); the mistake-cost sentence was in the "Is ML needed" line.

---

## 3. A real-estate site wants to suggest a listing price for a house from its details.

- **Input → output:** house details (size, rooms, location, age, condition, photos) → suggested price
- **Problem type:** regression
- **Labels:** past sale prices of houses (ideally recent sales in the same area)
- **Baseline:** median price per square metre in the neighbourhood × the house's size
- **Metric (and which mistake is worse):** MAE in currency, or median percentage error (prices vary a lot, so a % treats cheap and expensive homes fairly). Overpricing → the house sits unsold; underpricing → the seller loses money.
- **Is ML needed, and why?:** yes. Many factors interact (location × size × condition), but the neighbourhood-median baseline is strong and must be beaten clearly.

**Correction after checking the reference:** Original input "price, time" was the output, not the input. Labels "house feature" were features, not labels; labels are past sale prices. Baseline should be per neighbourhood, not one global median. "Yes" needed a reason.

---

## 4. A telecom company wants to know which customers are likely to cancel next month, to offer them a discount.

- **Input → output:** a customer's history (tenure, contract type, usage, complaints, billing) → probability of cancelling next month
- **Problem type:** binary classification, often imbalanced; time matters (train on past months, test on a later month)
- **Labels:** past cancellations — which customers left in each month
- **Baseline:** "customers with a complaint last month," or "month-to-month contracts"
- **Metric (and which mistake is worse):** precision and recall at the number of discounts the company can afford (precision@k); PR-AUC to compare models. A missed churner loses revenue; a discount given to someone who would have stayed wastes money.
- **Is ML needed, and why?:** yes, many weak signals combine. Note the real goal is *who would stay because of the discount* (uplift modelling), which is harder than predicting who leaves.

**Correction after checking the reference:** Labels "past data" were too vague; labels are past cancellations. Metric was blank. The uplift point was missed.

---

## 5. A marketing team wants to "understand our different types of customers." They have purchase history but no customer categories.

- **Input → output:** each customer's purchase history (recency, frequency, spend, product categories) → a segment for each customer
- **Problem type:** clustering (unsupervised)
- **Labels:** none
- **Baseline:** simple rule segments: spend (high/medium/low) × recency (recent/lapsed)
- **Metric (and which mistake is worse):** no single right metric. Silhouette score as a sanity check; the real test is whether segments are distinct, stable over time, and marketing can name and act on them. The bad outcome is too many or meaningless segments.
- **Is ML needed, and why?:** maybe. Simple RFM rules often answer this. Clustering helps only if it finds groups the rules miss.

**Correction after checking the reference:** Input described the goal, not the data. Metric and "Is ML needed" were blank.

---

## 6. A support team receives 5,000 emails a day and wants each one routed to one of 30 departments.

- **Input → output:** email subject + body (+ sender) → one of 30 departments
- **Problem type:** multiclass text classification
- **Labels:** past emails with the department that actually handled them (check for misrouted ones)
- **Baseline:** keyword rules; TF-IDF + logistic regression
- **Metric (and which mistake is worse):** macro-F1 (small departments count) plus accuracy; confusion matrix for departments that get confused. A misroute delays the customer, so send low-confidence emails to a human triage queue.
- **Is ML needed, and why?:** yes. 5,000 a day across 30 classes is too much for hand-written rules, and TF-IDF is likely enough to start.

**Correction after checking the reference:** Labels "department" were the label name, not the data; labels are past emails with their department. "Is ML needed" was blank.

---

## 7. A factory wants to spot cracked parts from photos on a production line. Cracks are rare.

- **Input → output:** a photo of one part → cracked / not cracked (and optionally where)
- **Problem type:** image classification, imbalanced. If there are very few crack photos, anomaly detection trained on good parts only. Segmentation only if they need the crack's size or shape.
- **Labels:** photos marked good/cracked by inspectors; cracked examples are rare
- **Baseline:** pretrained image model + linear probe; or the current manual-inspection result
- **Metric (and which mistake is worse):** recall on cracked parts at an acceptable false-alarm rate (e.g. ≤ 1% of good parts flagged). A missed crack (a faulty part shipped) is worse than an extra manual check.
- **Is ML needed, and why?:** yes, for visual inspection at line speed. But check whether classic machine vision (fixed lighting + edge detection) already works.

**Correction after checking the reference:** Original said segmentation. The task is to *spot* cracked parts (yes/no per part), so classification or anomaly detection. "Cracks are rare" points to imbalance or anomaly detection.

---

## 8. A hospital wants to outline tumors in MRI scans, pixel by pixel, to help radiologists.

- **Input → output:** an MRI scan → a pixel mask of the tumour region
- **Problem type:** semantic segmentation
- **Labels:** tumour outlines (masks) drawn by radiologists. Expensive, and radiologists sometimes disagree.
- **Baseline:** a pretrained medical segmentation model; agreement between two radiologists as the ceiling
- **Metric (and which mistake is worse):** Dice / IoU per scan, plus the share of tumours detected at all (small ones matter). Missing tumour tissue (FN) is worse.
- **Is ML needed, and why?:** yes. Manual outlining is slow. The tool assists radiologists; a human always decides.

**Correction after checking the reference:** Type correct. Labels "tumor images" should be pixel masks drawn by experts. Baseline, metric and "Is ML needed" were blank.

---

## 9. A warehouse wants to count and locate boxes on shelves from camera images.

- **Input → output:** a shelf camera image → a bounding box around each box, plus a count
- **Problem type:** object detection
- **Labels:** boxes drawn around each box in a sample of images
- **Baseline:** a pretrained detector used as-is; manual counts on a sample
- **Metric (and which mistake is worse):** mAP@0.5 for detection; count error per shelf (MAE) for the business. Missed boxes undercount stock.
- **Is ML needed, and why?:** yes, unless barcode/RFID inventory data already exists. Then counting from images may not be needed at all.

**Correction after checking the reference:** Type correct. Output said "outlining," which is segmentation; detection outputs boxes. Labels "Object" were too vague.

---

## 10. A legal team wants to ask questions about 3,000 internal contracts and get answers with the clause cited.

- **Input → output:** a question → an answer citing the exact clause(s), or "not found"
- **Problem type:** RAG
- **Labels:** none exist. Write 50–100 test questions with the correct answer and source clause, including unanswerable ones.
- **Baseline:** keyword search (BM25) showing matching clauses; an LLM with no retrieval
- **Metric (and which mistake is worse):** retrieval Recall@k (did the right clause come back?); answer correctness; citation accuracy; correct "not found." A confident wrong answer or wrong citation is a legal risk, so prefer abstaining.
- **Is ML needed, and why?:** yes for question answering, though good search over the contracts may cover much of the need.

**Correction after checking the reference:** Type correct. Metric "precision@k" covered only part of retrieval; RAG needs retrieval *and* answer quality measured.

---

## 11. An HR team wants to pull name, email, years of experience, and skills out of PDF résumés into a spreadsheet.

- **Input → output:** a résumé PDF → one spreadsheet row: name, email, years of experience, skills
- **Problem type:** extraction (structured output)
- **Labels:** hand-label ~100 résumés with the correct fields
- **Baseline:** regex for email and phone; an LLM with a JSON schema for experience and skills
- **Metric (and which mistake is worse):** accuracy per field; precision/recall for the skills list; JSON validity rate. A made-up value (invented skill) is worse than an empty one, so allow `null`.
- **Is ML needed, and why?:** partly. Regex for emails; an LLM for messy fields like experience and skills. Watch privacy, and bias if the output feeds hiring decisions.

**Correction after checking the reference:** Type and baseline correct. Input and labels were blank; the metric should be per field.

---

## 12. A news site wants to show "related articles" under each article.

- **Input → output:** an article → a ranked list of the most related articles
- **Problem type:** similarity search / recommendation (ranking), using embeddings
- **Labels:** none needed to start; click data later
- **Baseline:** same category or tags + most recent; TF-IDF/BM25 similarity
- **Metric (and which mistake is worse):** offline: judged relevance of the top 5 (precision@5); online: click-through in an A/B test. Low stakes: a bad suggestion is just ignored.
- **Is ML needed, and why?:** embeddings help, but tag-based suggestions may already be good enough.

**Correction after checking the reference:** Original said text classification. The output is an ordered list of items, not a category, so it's ranking/similarity.

---

## 13. A server team wants to be alerted when a machine "behaves strangely." They have metrics but no history of labeled incidents.

- **Input → output:** a stream of machine metrics (CPU, memory, latency, error rate) → alert when the behaviour is unusual
- **Problem type:** anomaly detection (unsupervised)
- **Labels:** none. Collect engineers' feedback on alerts to create labels over time.
- **Baseline:** thresholds per metric (rolling mean ± 3 standard deviations)
- **Metric (and which mistake is worse):** precision of alerts (as judged by engineers), incidents missed, alerts per day. Too many false alarms → people ignore alerts (alert fatigue); misses → outages.
- **Is ML needed, and why?:** start with thresholds. Use ML when many metrics interact and simple thresholds miss problems or fire too often.

**Correction after checking the reference:** Original said clustering. "Behaves strangely" + no labels = anomaly detection. Clustering finds groups; it doesn't flag the odd one out.

---

## 14. A company wants a chatbot that answers questions about its HR policies.

- **Input → output:** an employee's question → an answer from the HR policy documents, with a link to the source, or "please ask HR"
- **Problem type:** RAG (not fine-tuning: policies change)
- **Labels:** write test questions with correct answers and sources, including unanswerable ones
- **Baseline:** the existing HR FAQ page or intranet search; an LLM without documents
- **Metric (and which mistake is worse):** answer correctness, citation accuracy, retrieval recall, and correct refusal rate. A confident wrong policy answer is worse than "please ask HR."
- **Is ML needed, and why?:** maybe. If 20 questions cover most of the traffic, a good FAQ page could be enough.

**Correction after checking the reference:** Type correct; all other fields were blank.

---

## 15. A travel company wants an assistant that can search flights, check the user's calendar, and book a trip after the user confirms.

- **Input → output:** the user's request in chat → tool calls (search flights, read calendar, book) and replies
- **Problem type:** agent with tools, with a **human confirmation step** before booking
- **Labels:** write a task suite: requests with the correct outcome
- **Baseline:** a fixed workflow / form: search → show options → user picks → book
- **Metric (and which mistake is worse):** task success rate over repeated runs; zero bookings without confirmation (safety); steps, cost and latency per task. Booking the wrong trip, or without confirmation, is the worst mistake: costly and hard to undo.
- **Is ML needed, and why?:** yes for flexible natural-language requests, but a structured booking form may serve most users.

**Correction after checking the reference:** Type correct; all other fields were blank. The confirmation step is the key guardrail.

---

## 16. An app wants to block toxic comments. Some comments are toxic in several ways at once (insult *and* threat).

- **Input → output:** comment text → a set of labels (insult, threat, obscene, …), possibly several; block if any label is above its threshold
- **Problem type:** multi-label text classification
- **Labels:** comments tagged by moderators with every label that applies
- **Baseline:** a keyword/regex block list; TF-IDF + one logistic regression per label
- **Metric (and which mistake is worse):** per-label precision/recall (or average precision), with a threshold per label. Missing a threat is worse than wrongly blocking mild language; but over-blocking frustrates users and can unfairly hit some dialects.
- **Is ML needed, and why?:** yes. Regex alone misses context and blocks innocent words.

**Correction after checking the reference:** Original said "regex, text classification." Regex is a baseline, not a problem type. "Several ways at once" = multi-label.

---

## 17. A bank wants product descriptions rewritten in its brand voice. It has 2,000 examples of approved rewrites.

- **Input → output:** an original product description → the same content rewritten in the brand voice
- **Problem type:** text generation (style transfer)
- **Labels:** the 2,000 approved before/after pairs
- **Baseline:** few-shot prompting an LLM with a style guide and examples. If style isn't consistent, fine-tune (LoRA) on the 2,000 pairs.
- **Metric (and which mistake is worse):** human rating against a style rubric, plus checks that facts (rates, fees, terms) are unchanged; an LLM judge only after checking it agrees with humans. Changing a fact is a compliance risk and is worse than imperfect style.
- **Is ML needed, and why?:** yes (an LLM). Fine-tuning is optional, and worth it if prompting can't hold the style.

**Correction after checking the reference:** Generation was right. Missed that 2,000 examples make fine-tuning a strong option for style, and that fact-preservation is the key check.

---

## 18. A retailer wants to know whether a product review is positive or negative.

- **Input → output:** review text → positive / negative
- **Problem type:** binary text classification (sentiment)
- **Labels:** star ratings as proxy labels (4–5 = positive, 1–2 = negative)
- **Baseline:** an off-the-shelf sentiment model; TF-IDF + logistic regression
- **Metric (and which mistake is worse):** accuracy or F1 if balanced; check per product category. If the goal is finding unhappy customers, recall on negative reviews matters most.
- **Is ML needed, and why?:** yes, but an existing pretrained model is probably enough. Don't train first.

**Correction after checking the reference:** Type correct; all other fields were blank. Star ratings give free labels.

---

## 19. A city wants to predict hourly bike-rental demand to plan bike redistribution.

- **Input → output:** station × hour history + weather forecast + calendar (weekday, holidays, events) → rentals per hour for the next day
- **Problem type:** time series forecasting
- **Labels:** past hourly rentals
- **Baseline:** same hour, same weekday, last week (seasonal naive)
- **Metric (and which mistake is worse):** MAE in bikes per hour, per station. Under-forecasting busy stations → empty docks and lost rides; over-forecasting → wasted truck trips.
- **Is ML needed, and why?:** probably. Weather and events move demand a lot. Split by time, and use only the weather *forecast* (actual weather isn't known in advance).

**Correction after checking the reference:** Type correct; all other fields were blank.

---

## 20. A company wants to know which of its 50 support macros to suggest to an agent while they type a reply.

- **Input → output:** the customer's message + the agent's draft reply → top 3 suggested macros
- **Problem type:** ranking / retrieval (or multiclass classification over 50 macros, shown as a ranked list)
- **Labels:** past tickets with the macro the agent actually used
- **Baseline:** the most-used macros overall; BM25 or embedding similarity between the draft and macro text
- **Metric (and which mistake is worse):** Recall@3 (was the macro the agent used in the top 3?), MRR. Low stakes: a bad suggestion is ignored, but it must be fast (while typing).
- **Is ML needed, and why?:** yes, though plain embedding similarity may be enough. No training needed at first.

**Correction after checking the reference:** Originally blank.

---

## 21. A school wants to detect whether essays were copied from each other.

- **Input → output:** a set of essays → pairs of essays that are suspiciously similar, for a teacher to review
- **Problem type:** similarity / near-duplicate detection (pairwise), with n-gram overlap (MinHash) or embeddings
- **Labels:** none needed; teacher-confirmed cases for evaluation
- **Baseline:** exact matching sentences / n-gram overlap
- **Metric (and which mistake is worse):** precision of flagged pairs (teacher review), recall on deliberately planted copies. Falsely accusing a student is very costly, so favour precision and keep a human in the loop.
- **Is ML needed, and why?:** barely. Classic text similarity works without training any model.

**Correction after checking the reference:** Original said anomaly detection. Copying is two essays being similar *to each other* (comparing pairs), not one odd essay.

---

## 22. A game company wants to generate new background art in the style of its existing game.

- **Input → output:** a text prompt (+ style examples) → new background images in the game's style
- **Problem type:** image generation (a diffusion model, fine-tuned with LoRA on their own art)
- **Labels:** their existing art, with captions
- **Baseline:** an off-the-shelf image model with style prompts; artists' normal output
- **Metric (and which mistake is worse):** human review by the art team (style match, usable without edits); share of usable images per batch. Off-style or legally risky images (copying others' work) are the main failures.
- **Is ML needed, and why?:** yes (a generative model), as a tool that assists artists. Check the base model's license and training-data terms.

**Correction after checking the reference:** Originally blank.

---

## 23. A company wants to translate its help center into Spanish.

- **Input → output:** English help-center articles → Spanish versions
- **Problem type:** machine translation, using an **existing** translation service or LLM. Don't train a model.
- **Labels:** none needed; a glossary of product terms; a sample checked by a Spanish speaker
- **Baseline:** an off-the-shelf translation API
- **Metric (and which mistake is worse):** human review of a sample (accuracy, fluency); glossary terms used consistently. Mistranslated instructions or legal terms are the worst errors.
- **Is ML needed, and why?:** it uses ML, but don't build anything. Use an existing tool and measure it on your content.

**Correction after checking the reference:** Originally blank.

---

## 24. A manager wants a weekly report of "how many tickets were opened per category." Tickets already have a category field.

- **Input → output:** the tickets table → count of tickets per category per week
- **Problem type:** **not ML** — a SQL `GROUP BY` (and maybe a dashboard)
- **Labels:** not applicable
- **Baseline:** not applicable
- **Metric (and which mistake is worse):** the report is correct and on time
- **Is ML needed, and why?:** **no**. The category already exists; this is counting.

**Correction after checking the reference:** Originally blank.

---

## 25. A clinic wants to predict a patient's risk of readmission within 30 days, for use in care planning.

- **Input → output:** a patient's record at discharge (diagnoses, age, prior admissions, medications, length of stay) → 30-day readmission risk
- **Problem type:** binary classification with **calibrated probabilities** (imbalanced; time and patient matter for the split)
- **Labels:** past discharges, marked readmitted within 30 days or not
- **Baseline:** an established clinical risk score (e.g. the LACE index) or a simple rule (number of prior admissions)
- **Metric (and which mistake is worse):** calibration (does 30% risk mean 30%?), PR-AUC, recall at the chosen risk level; check fairness across patient groups. Missing a high-risk patient is worse than extra follow-up for a low-risk one.
- **Is ML needed, and why?:** yes, if it beats the existing clinical score. High stakes: explanations, fairness checks, and a clinician always decides.

**Correction after checking the reference:** Originally blank.
