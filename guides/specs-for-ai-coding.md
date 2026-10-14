# Writing specs for AI coding tools

In this path, the AI writes the code and you make the decisions. This guide is about the handoff: how to turn your decisions into prompts that produce correct ML code, and how to check what comes back.

**The core idea:** the AI fills every gap you leave with a guess. In normal software a bad guess usually crashes. In ML, a bad guess (wrong split, preprocessing fit on all data, wrong metric) runs fine and gives you a wrong number that looks good. **So in ML, the spec matters more, not less.**

---

## 1. Decide, then specify, then generate

```
1. DECIDE    (you)  problem type, split, baseline, metric, model    → "Decide first" + guides
2. SPECIFY   (you)  write the decisions as precise instructions     → this guide
3. GENERATE  (AI)   one step at a time
4. VERIFY    (you)  run it, check the ✅ checkpoint, review the code
5. EXPLAIN   (you)  write results and reasoning in NOTES.md
```

Never skip step 1. If you ask the AI to "build a fraud model," *it* decides the split, metric and threshold. You learn nothing, and it will often choose badly.

---

## 2. What every ML spec must pin down

Use this as a checklist. If a line is missing, the AI will guess it.

| Item | Example |
| --- | --- |
| **Data** | `data/telco_churn.csv`; target `Churn` (Yes/No → 1/0); drop `customerID` as a feature |
| **Split** | Stratified 60/20/20, `random_state=42`; save the indices to `data/splits/churn.json` |
| **Preprocessing** | `ColumnTransformer`: one-hot (`handle_unknown="ignore"`) for these columns, median-impute + standard-scale for these; inside a `Pipeline`, fitted on train only |
| **Model** | `LogisticRegression(max_iter=1000, class_weight="balanced")` |
| **Metric(s)** | PR-AUC and recall at precision ≥ 0.6, on validation |
| **What not to touch** | Don't evaluate on test. Don't change the split. Don't add features. |
| **Output** | Print a table of metrics; save it to `work/03-churn/results/val_metrics.csv` |
| **Location** | `work/03-churn/train_logreg.py`; use `set_seed()` from `common.seed` |
| **Done when** | The script runs with `uv run python work/03-churn/train_logreg.py` and prints the table |

Your `AGENTS.md` file already covers the repo-wide rules (seed, folders, train-only fitting). The spec covers *this* step.

---

## 3. Templates

### Template: a modelling step

```
Context: Challenge NN — <one-line problem>. Rules are in AGENTS.md.

Task: <one step only, e.g. "train and evaluate the logistic regression baseline">

Data: <file>, target <column> (<encoding>), drop <columns> as features.
Split: <type, ratios, seed>. <load existing split from X | create and save to X>.
Preprocessing (in a Pipeline, fit on train only):
  - numeric <cols>: <impute>, <scale>
  - categorical <cols>: <encoding>
Model: <class and settings>.
Evaluate on: validation only. Metrics: <list>.
Output: print <what>; save <file>.
Don't: <touch test / change split / add features / tune>.
File: work/NN-name/<script>.py
```

### Template: an exploration step

```
Write a short script (or notebook cells) for work/NN-name/eda.py that prints:
shape, dtypes, missing share per column, duplicate rows, target balance,
and describe() for numeric columns. Plot <specific plots>. Save plots to work/NN-name/figures/.
Don't clean or transform anything yet. I'll decide that after seeing the output.
```

### Template: an LLM / RAG / agent step

```
Task: <one component, e.g. "the retrieve() function">.
Inputs/outputs: <signature and return type>.
Model/tools: <exact model name, embedding model, settings: temperature, max tokens>.
Data: <corpus path; gold set path; which split (dev only)>.
Constraints: <no framework | use Chroma | timeouts | step limits>.
Logging: save every call (input, output, settings, latency) to <path>.
Evaluate on: dev questions only. Report: <metrics>.
```

---

## 4. Good and bad prompts, side by side

| ❌ Leaves the decisions to the AI | ✅ You decided; the AI implements |
| --- | --- |
| "Clean this dataset." | "Convert `TotalCharges` with `pd.to_numeric(errors='coerce')`; print the rows that became NaN; fill them with 0, because they're customers with tenure 0. Don't drop any rows." |
| "Train the best model." | "Train `HistGradientBoostingClassifier` with default settings on the same pipeline and split as `train_logreg.py`; report the same metrics on validation." |
| "Improve the accuracy." | "Try `class_weight='balanced'` vs none, and report PR-AUC for both on validation. Change nothing else." |
| "Evaluate the model." | "Evaluate the chosen model on the test split once. Print accuracy, precision, recall, F1, PR-AUC. This is the final run, so don't change anything after it." |
| "Build a chatbot for the docs." | "Implement `retrieve(question, k)` using the Chroma collection in `data/chroma/`, embedding model `BAAI/bge-small-en-v1.5`, returning ids, titles and scores." |

---

## 5. Work in small steps

- **One Build step per prompt.** Small steps are easy to check. A whole challenge in one prompt produces 300 lines you can't review.
- **Run and check the ✅ checkpoint before the next prompt.** If it's off, stop there.
- **Keep scripts small and named by purpose** (`eda.py`, `train_logreg.py`, `evaluate_test.py`), rather than one giant file.
- **Commit after each working step**, so you can go back.

---

## 6. Reviewing what comes back

### Read the code with these questions

1. **Where is the split made, and is anything fitted before it?** Search for `fit`, `fit_transform`, `TfidfVectorizer`, `StandardScaler`, `SimpleImputer` and check each runs on train only.
2. **Where is test used?** It should appear only in the final evaluation, if at all.
3. **Are the metrics the ones you asked for?** Check the `average=` argument (macro vs micro vs binary) and the positive label.
4. **Did it add anything you didn't ask for?** Extra features, a different model, silent data filtering, a `try/except` that hides errors.
5. **Is randomness seeded?** `set_seed()` and `random_state=42`.
6. **Do the printed numbers make sense?** Compare with the ✅ checkpoint and the baseline.

The full checklist of silent ML bugs is in the [README](../README.md#review-checklist-for-ai-written-ml-code).

### Ask the AI to explain, then verify yourself
- "Explain, line by line, where preprocessing is fitted and on which data."
- "Which rows does this filter remove, and why?"
- "What would change if the data were sorted by time?"

The AI's explanation can be wrong too. Check the important claims by running small tests (print shapes, row counts, which indices are in which split).

### Quick tests that catch most problems
- Print the **row count** after every step that could drop rows.
- Print the **class balance** in each split.
- Assert the train and test indices **don't overlap**.
- Run the script **twice** and confirm identical numbers.
- Make a **tiny version** (100 rows) that runs in seconds, while developing.

---

## 7. When the AI is wrong or stuck

| Problem | What to do |
| --- | --- |
| It invents a function or parameter | Check the library's docs for the installed version (`uv pip show <pkg>`); tell it the version |
| It "fixes" an error by hiding it (`try/except: pass`) | Reject it; ask for the root cause |
| It keeps changing things you didn't ask about | Restate the constraint: "only change X; keep everything else identical" |
| Its result is too good to be true | Assume leakage until proven otherwise. See [Splits, validation and leakage](splits-validation-leakage.md#4-leakage-the-silent-killer) |
| You don't understand its code | Ask it to explain, then rewrite the explanation in your own words in NOTES.md. If you can't, you're not done |

---

## 8. What stays your job, always

- The problem framing, split, metric and baseline.
- The evaluation set (especially for LLM/RAG/agent work: questions, rubrics, pass criteria). If the AI writes its own test, you can't trust its score.
- Grading outputs where judgment is needed.
- Deciding what to ship, and writing why.
