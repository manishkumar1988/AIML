# Data preparation

How to get a raw dataset ready for a model, and which preprocessing each kind of model actually needs.

**Golden rule:** anything that *learns from the data* (a mean for filling gaps, a scaler, an encoder's categories, a vocabulary) is fitted on the **training split only**, then applied to validation and test. Split first, prepare second. See [Splits, validation and leakage](splits-validation-leakage.md).

---

## 1. First look: the EDA checklist

Do this before deciding anything. Fifteen minutes here saves days later.

```python
df.shape                      # rows, columns
df.head(); df.sample(5)       # what a row actually looks like
df.dtypes                     # numbers stored as text? dates as text?
df.isna().mean().sort_values(ascending=False)   # missing share per column
df.duplicated().sum()         # exact duplicate rows
df.nunique().sort_values()    # constant columns, ID-like columns
df.describe()                 # ranges, impossible values (age = -1, price = 0)
df[target].value_counts(normalize=True)          # class balance, or a histogram for numbers
```

Then answer, in writing:

- [ ] **What is one row?** A customer? A transaction? A customer-month? This decides how you split.
- [ ] **What's the target, exactly,** and when is it known?
- [ ] **Which columns would I know at prediction time?** (Anything filled in *after* the event is leakage.)
- [ ] **Which columns are IDs** (unique per row, no meaning)? Drop them as features.
- [ ] **Is there a time column?** Then you'll probably split by time.
- [ ] **Are there duplicate or near-duplicate rows?** They can sit in both train and test and inflate your score.
- [ ] **What looks wrong?** Impossible values, placeholders (`-1`, `999`, `"unknown"`), a spike at a round number (capped values).

---

## 2. Data types and what they need

| Column type | Examples | What to do |
| --- | --- | --- |
| **Numeric, continuous** | price, age, temperature | Check range and skew. Scale for linear models, neural nets, k-NN, k-means, SVM. Trees don't care. |
| **Numeric, but really a category** | zip code, product id, store number | Treat as categorical. Averaging zip codes is meaningless. |
| **Categorical, few values** (< ~20) | contract type, colour | One-hot encode (linear models, neural nets) or native categorical support (LightGBM, CatBoost, `HistGradientBoosting`). |
| **Categorical, many values** (high cardinality) | city, product SKU | Group rare values into "other"; target encoding *inside CV folds*; frequency encoding; or embeddings for neural nets. |
| **Ordinal** (ordered categories) | small / medium / large; education level | Map to ordered integers (0, 1, 2). |
| **Boolean** | has_phone | 0/1. |
| **Date/time** | signup date, timestamp | Never feed the raw timestamp. Extract parts: hour, weekday, month, is_holiday; compute durations ("days since signup"). |
| **Free text** | review, description | TF-IDF, embeddings, or a transformer (see the NLP challenges). |
| **IDs** | customer_id, row number | Drop as a feature. Keep it for joining, grouping splits, and tracing errors. |

**Text that should be numbers:** `pd.to_numeric(col, errors="coerce")` turns unparseable values into `NaN`, so you can see them instead of crashing. Then find out *why* they weren't numbers.

---

## 3. Missing values

### First ask: why is it missing?

| Kind | Meaning | Example | Consequence |
| --- | --- | --- | --- |
| Missing at random | Gaps unrelated to anything | A sensor dropped a reading | Simple imputation is fine |
| Missing for a reason | The gap itself is information | "Total charges" blank because the customer is brand new | Add an **"is_missing" flag**, and fill sensibly (0 here) |
| Not applicable | The value can't exist | "Spouse income" for single people | Fill with 0 or a special category, plus a flag |

### Options

| Method | When | Note |
| --- | --- | --- |
| **Drop rows** | Very few rows missing, and they're random | Check you're not dropping a specific group (e.g. all new customers) |
| **Drop the column** | Mostly missing and not informative | Check the missing-flag isn't predictive first |
| **Median** (numbers) | Default for numeric columns | Robust to outliers. Fit on train only |
| **Most frequent / "missing" category** | Categorical columns | A "missing" category keeps the information |
| **Indicator column** | Missingness may carry meaning | `SimpleImputer(add_indicator=True)` does both |
| **Model-based** (KNN, iterative imputer) | Many related columns with gaps | Slower; rarely worth it at first |
| **Leave it** | Gradient boosting libraries | LightGBM, XGBoost and `HistGradientBoosting` handle `NaN` natively |

---

## 4. Scaling: which models need it?

| Needs scaling | Doesn't need scaling |
| --- | --- |
| Linear and logistic regression (especially with regularization) | Decision trees |
| k-NN, k-means, SVM, PCA | Random forest |
| Neural networks | Gradient boosting (XGBoost, LightGBM, CatBoost, `HistGradientBoosting`) |

**Why:** these models use distances or weight sizes. Without scaling, a column measured in thousands (salary) drowns out a column measured in units (number of children).

| Scaler | Does | Use when |
| --- | --- | --- |
| `StandardScaler` | Mean 0, std 1 | Default |
| `MinMaxScaler` | Range 0–1 | Neural nets with bounded inputs; images (often just ÷ 255) |
| `RobustScaler` | Uses median and IQR | Outliers present |

---

## 5. Skewed numbers and outliers

**Skewed** (a long tail of large values: income, prices, counts):
- `np.log1p(x)` squeezes the tail. Helps linear models, k-means and neural nets. Trees mostly don't care.
- If you log-transform the **target**, convert predictions back (`np.expm1`) before computing the metric, and report the metric in the original units.

**Outliers.** Decide which kind you have:
- **Error** (age 250, negative price) → fix or remove, and write down the rule.
- **Real but extreme** (a billionaire customer) → keep. Consider clipping the feature (`clip` at the 1st/99th percentile, computed on train), robust scaling, or a robust metric (MAE).
- **The thing you're looking for** (fraud) → definitely keep.

---

## 6. Feature engineering that often helps

| Idea | Example |
| --- | --- |
| Ratios | price per square metre; debt-to-income |
| Differences / durations | days since last purchase; time between events |
| Aggregates per entity | a customer's average order value, number of orders in last 30 days |
| Date parts | hour of day, weekday, month, holiday flag |
| Lags (time series) | sales 7 days ago, 28-day rolling mean (computed only from past data) |
| Counts / frequencies | how often this category appears |
| Interactions | "is weekend × hour" for demand |
| Domain flags | "first purchase," "international transaction" |

**Two rules:** every feature must be known at prediction time, and aggregates are computed from training data only (or from the past only, for time series).

Gradient boosting finds many interactions by itself. Feature engineering helps linear models most, but good domain features help everything.

---

## 7. Imbalanced targets

If one class is rare (< ~10%):
1. **Use the right metric first** (PR-AUC, precision/recall at a threshold). See the [metrics guide](problem-types-baselines-metrics.md#part-3--metrics).
2. **Stratify** your splits, so every split has some positives.
3. **Class weights** (`class_weight="balanced"`): usually the best first move.
4. **Choose the threshold** on validation, from costs or capacity.
5. **Resampling** (SMOTE, undersampling) only *inside* the training split, and only if it beats class weights on validation.

---

## 8. Put it in a Pipeline

Do all preprocessing inside a scikit-learn `Pipeline` with a `ColumnTransformer`. It guarantees preprocessing is fitted on train only, applied identically to new data, and saved together with the model.

```python
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression

numeric = ["age", "monthly_charges"]
categorical = ["contract", "payment_method"]

preprocess = ColumnTransformer([
    ("num", Pipeline([("impute", SimpleImputer(strategy="median")),
                      ("scale", StandardScaler())]), numeric),
    ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                      ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical),
])

model = Pipeline([("prep", preprocess), ("clf", LogisticRegression(max_iter=1000))])
model.fit(X_train, y_train)       # everything learns from train only
model.score(X_val, y_val)         # same transformations applied to val
```

`handle_unknown="ignore"` matters: new data will contain categories training never saw.

---

## 9. Images, text and audio (short version)

| Data | Typical preparation |
| --- | --- |
| **Images** | Resize to a fixed size; scale pixels (÷ 255) and normalize with the **pretrained model's** mean/std; augment (flip, crop, colour) on **training images only**; resize masks with nearest-neighbour. |
| **Text (classical)** | Lowercase, tokenize, TF-IDF (fit on train). Don't over-clean: punctuation and negation ("not") carry meaning. |
| **Text (transformers)** | Use the model's own tokenizer; choose `max_length` from the token-length distribution; check how much gets truncated. |
| **Audio** | Resample to one rate; convert to spectrograms; or use the pretrained model's feature extractor. |

---

## 10. Write it down

Every challenge's `NOTES.md` should have a short **data section**:
- rows, columns, target balance;
- what you cleaned and why (rows dropped, values fixed, fill rules);
- which columns you excluded and why (IDs, leaky columns);
- any surprise you found.

These decisions are often what interviewers ask about, because they show judgment.
