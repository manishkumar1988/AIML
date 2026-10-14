# Splits, validation and leakage

How to set up data so your score tells the truth. If the split is wrong, every number after it is wrong, however good the model.

---

## 1. Why three splits?

| Split | Used for | Rule |
| --- | --- | --- |
| **Train** | The model learns from it | Fit everything here: model, scalers, encoders, vocabularies |
| **Validation (dev)** | **You** learn from it: choosing models, features, thresholds, prompts, epochs | Look as often as you like |
| **Test** | One honest final estimate | Use **once**, at the end. Never choose anything with it |

**Why test must stay untouched:** every time you choose something because it scored better on a set, your choices fit that set a little. After 50 choices, its score is optimistic. The test set is the one place you haven't done that.

**Typical sizes:** 60/20/20 or 70/15/15 for medium data. With lots of data, validation and test can be smaller fractions (10,000 examples each is plenty). With little data, use **cross-validation** instead of a single validation split.

---

## 2. Choose the split that matches real use

**The question:** *when this model is used for real, what will be new to it?* Your test set must be new in the same way.

| Situation | Split type | How |
| --- | --- | --- |
| Rows are independent, no time order | **Random** | `train_test_split(..., random_state=42)` |
| Classification, especially imbalanced | **Stratified random** | `stratify=y`, so each split has the same class ratio |
| Predicting the future from the past | **Time-based** | Sort by time; train on earliest, validate on later, test on latest |
| Several rows per customer/patient/store/document | **Group split** | All rows of one group go to the same split (`GroupShuffleSplit`, `GroupKFold`) |
| The model will be used on new stores, cities, users | **Group split by that entity** | Test only on entities not seen in training |
| Near-duplicate items (same photo twice, reposted tweets, copied essays) | **Group by duplicate cluster** | Duplicates stay in one split |
| Competition with a hidden test | Local CV that mimics how the test was created | Read how the organizers split |

**Examples:**
- A churn model will be applied to *existing customers next month* → time-based split (train on earlier months).
- A medical model will be used on *new patients* → group split by patient (many scans per patient).
- A product classifier must work on *new products* → group by product.

---

## 3. Cross-validation (CV)

Instead of one validation split, split the training data into **k folds** (usually 5). Train k times, each time validating on a different fold. You get k scores.

```
Fold 1: [VAL] [   ] [   ] [   ] [   ]
Fold 2: [   ] [VAL] [   ] [   ] [   ]
...
Fold 5: [   ] [   ] [   ] [   ] [VAL]
```

**Why:** you get a **mean and a spread**. If model A = 0.84 ± 0.02 and model B = 0.85 ± 0.02, you can't call B better.

| Variant | Use when |
| --- | --- |
| `KFold(shuffle=True, random_state=42)` | Regression, independent rows |
| `StratifiedKFold` | Classification |
| `GroupKFold` / `StratifiedGroupKFold` | Grouped rows |
| `TimeSeriesSplit` | Time series (expanding window; always validate on later data) |

**Out-of-fold (OOF) predictions:** every training row gets a prediction from the model that didn't see it. Useful for choosing thresholds, checking metrics, and blending models.

**The test set still stays aside.** CV happens inside train (+validation), not on everything.

---

## 4. Leakage: the silent killer

**Leakage** = information the model wouldn't have in real use sneaks into training or evaluation. The symptom is a score that's too good, followed by failure in production.

### The seven common types

| # | Type | Example | Prevention |
| --- | --- | --- | --- |
| 1 | **Target leakage** — a feature derived from the answer | `cnt = casual + registered`, then `casual` used as a feature | Ask of each feature: "is this the answer in disguise?" |
| 2 | **Future information** | Using next week's weather actuals to forecast this week; a "refund issued" flag to predict fraud | Feature inventory: "known at prediction time?" for every column |
| 3 | **Preprocessing fit on all data** | `scaler.fit(X)` before splitting; TF-IDF vocabulary from all text; imputing with the overall mean | Split first; use a `Pipeline` |
| 4 | **Duplicates across splits** | The same customer, photo or tweet in train and test | Deduplicate; group splits |
| 5 | **Random split on time data** | Neighbouring days in train and test; the model "interpolates" | Time-based split |
| 6 | **Tuning on test** | Picking the threshold, features or epochs because the test score was better | Choose on validation/CV only |
| 7 | **Target encoding / resampling outside folds** | Category means computed with all labels; SMOTE before splitting | Do them inside each CV fold or training split |

### Red flags that should make you suspicious

- The score is much better than you (or the literature) expected.
- One feature has huge importance, and you can't explain why in business terms.
- Validation is great; anything new (a later month, a new store) is bad.
- A random split scores much better than a time or group split.

### How to investigate

1. Sort feature importances. For the top 3, ask "would I know this at prediction time, and is it the answer in disguise?"
2. Train a model on that single feature. If it alone gets a near-perfect score, it's probably leaking.
3. Compare random vs time/group split scores. A big gap means leakage or a split mismatch.

---

## 5. Is the difference real? (uncertainty)

Small test sets give noisy numbers. Before claiming model B beats model A:

- **Count your positives.** With 60 fraud cases, catching 3 more changes recall by 5 points.
- **CV spread:** compare mean ± standard deviation across folds.
- **Bootstrap:** resample the test set with replacement ~1,000 times, recompute the metric each time, and report the 2.5th–97.5th percentile range.
- **Several seeds** for neural nets: train 3 times with different seeds and report the mean and range.
- **Never report the best of several seeds** as "the" result.

Rule of thumb: if the ranges overlap a lot, say "no clear difference," and choose the simpler or cheaper model.

---

## 6. Special cases

| Case | What to do |
| --- | --- |
| **Very small data** (hundreds of rows) | Repeated CV; simple models; be very cautious with tuning |
| **Hyperparameter tuning** | Tune with CV inside the training data; the test set stays out. For an unbiased estimate of the *whole* procedure, use nested CV (rarely needed in practice) |
| **LLM prompts** | Prompts are tuned by you, so treat them like hyperparameters: edit on a dev set, run test once per final prompt |
| **Kaggle** | Your local CV is your validation. The public leaderboard is a small, noisy test, so don't tune to it |
| **Pretrained models / LLMs** | Public benchmarks may have been in their training data (contamination). Keep a test set you wrote yourself |
| **Production** | The real test is the future. Monitor live performance (Challenge 39) |

---

## 7. Checklist before you trust a number

- [ ] The split matches how the model will be used (time? groups? new entities?).
- [ ] Preprocessing was fitted on train only (inside a Pipeline).
- [ ] Every feature is known at prediction time.
- [ ] No duplicates or near-duplicates across splits.
- [ ] All choices (model, threshold, features, prompt, epoch) were made on validation or CV.
- [ ] Test was used once.
- [ ] I know roughly how uncertain the number is.
- [ ] The baseline was evaluated on the same split.
