# Choosing an algorithm

You know how the algorithms work. This guide is about **which one to pick**, and which few settings actually matter.

**The short version:**
- **Tables:** start with logistic/linear regression, then **gradient boosting**. Gradient boosting wins most tabular problems.
- **Images, audio:** a **pretrained neural network** (transfer learning).
- **Text:** **TF-IDF + logistic regression** first, then a **fine-tuned transformer** or an **LLM**.
- **Small data, need to explain it:** linear models or a shallow tree.
- Try the simple model first. Use the complex one only if it beats the simple one by enough to justify it.

---

## 1. The default path for tabular data

```
1. Baseline (mean / majority class / rule)
2. Linear or logistic regression         ← fast, explainable, a strong reference point
3. Gradient boosting (LightGBM / XGBoost / CatBoost / HistGradientBoosting)
4. Tune gradient boosting a little (with CV)
5. Only if there's a reason: random forest, a neural net, or an ensemble
```

Most real tabular projects stop at step 3 or 4.

---

## 2. Algorithm cards

### Linear regression / logistic regression
- **Good at:** small data; linear-ish relationships; **explaining** (coefficients); fast training and prediction; a strong baseline.
- **Weak at:** non-linear patterns and interactions (unless you engineer features).
- **Needs:** scaled numeric features, one-hot categories, no huge outliers.
- **Settings that matter:** regularization strength (`C` in logistic regression, `alpha` in Ridge/Lasso); `class_weight="balanced"` for imbalance.
- **Variants:** Ridge (L2, shrinks weights), Lasso (L1, sets some weights to zero, so it selects features).

### Decision tree (single)
- **Good at:** explaining to humans (it's a flowchart); mixed feature types; no scaling needed.
- **Weak at:** accuracy, stability (small data changes → very different tree). Overfits when deep.
- **Use it:** when a simple, readable rule set is the goal. Rarely as the final model.
- **Settings:** `max_depth`, `min_samples_leaf`.

### Random forest
- **Good at:** solid accuracy with almost no tuning; robust to outliers and noise; no scaling needed.
- **Weak at:** usually a bit below gradient boosting; large models; slow prediction with many trees.
- **Settings:** `n_estimators` (more is better, until it's too slow), `max_features`, `min_samples_leaf`.

### Gradient boosting (XGBoost, LightGBM, CatBoost, scikit-learn `HistGradientBoosting`)
- **Good at:** **the best accuracy on most tabular data**; handles missing values and non-linear interactions; no scaling needed.
- **Weak at:** can overfit if over-tuned; less transparent (use SHAP to explain); more settings.
- **Settings that matter most:**
  - `learning_rate` (0.03–0.1) with **early stopping** on validation to choose the number of trees;
  - tree size: `num_leaves` / `max_depth` / `max_leaf_nodes`;
  - `min_child_samples` / `min_samples_leaf` (larger = less overfitting);
  - subsampling of rows and columns (`subsample`, `colsample_bytree`).
- **Which library:** `HistGradientBoosting` (built into scikit-learn, good default); **LightGBM** (fast, popular on Kaggle); **CatBoost** (excellent with many categorical columns); **XGBoost** (mature, widely used). The differences are usually small.

### k-nearest neighbours (k-NN)
- **Good at:** simple; no training; works well with good **embeddings** (similar items have similar labels).
- **Weak at:** slow on large data; poor with many raw features; needs scaling.
- **Use it:** with embeddings (Challenge 21), or as a sanity check.
- **Settings:** `k`, distance metric.

### Support vector machine (SVM)
- **Good at:** medium-sized data with many features (e.g. text with TF-IDF); a clear margin between classes.
- **Weak at:** large datasets (slow); probability outputs need extra calibration; needs scaling.
- **Today:** mostly replaced by logistic regression (text) and gradient boosting (tables). Fine to know, rarely the first choice.

### Naive Bayes
- **Good at:** very fast text classification baselines; tiny data.
- **Weak at:** usually beaten by logistic regression on TF-IDF.

### Neural networks
- **Good at:** **images, text, audio, sequences** — unstructured data where features must be learned; huge data; transfer learning from pretrained models.
- **Weak at:** plain tabular data (gradient boosting usually wins, with far less effort); small data without pretraining; explaining.
- See the [Deep learning field guide](deep-learning-field-guide.md) for which architecture.

### Unsupervised
| Algorithm | Use for | Note |
| --- | --- | --- |
| **K-means** | Clustering roundish, similar-sized groups | Scale features; choose k with the business |
| **DBSCAN / HDBSCAN** | Clusters of odd shapes; finds "noise" points | No k needed; sensitive to the distance threshold |
| **Gaussian mixture** | Soft clustering (probability of each cluster) | Like a flexible K-means |
| **Isolation Forest** | Anomaly detection on tables | Fast, good default |
| **Autoencoder** | Anomaly detection on images, complex data | Train on normal data only |
| **PCA** | Compress features; 2D plots | For looking and compressing, not proof |
| **UMAP / t-SNE** | 2D maps of embeddings | For looking only. Distances between clusters are not reliable |

---

## 3. Decision table: data → first and second choice

| Data and goal | First choice | Second choice |
| --- | --- | --- |
| Table, < 1,000 rows | Logistic/linear regression | Random forest |
| Table, 1,000+ rows | Gradient boosting | Logistic/linear (for comparison and explanation) |
| Table, must be explainable to regulators | Logistic regression or a shallow tree | Gradient boosting + SHAP, if allowed |
| Text, any size | TF-IDF + logistic regression | Fine-tuned transformer (DistilBERT, etc.) |
| Text, very few labels | LLM with a prompt (zero/few-shot) | Embeddings + k-NN or logistic regression |
| Images | Pretrained CNN/ViT, fine-tuned | Train from scratch only with lots of data |
| Time series, one series | Seasonal naive → ETS/ARIMA/Prophet | Gradient boosting with lags |
| Time series, many related series | Gradient boosting with lag and calendar features | Deep learning forecasting models |
| Similarity / search | Embeddings + nearest neighbours; BM25 for keywords | Hybrid + reranker |
| No labels: groups | K-means on scaled features | HDBSCAN on embeddings |
| No labels: anomalies | Isolation Forest | Autoencoder |

---

## 4. Choosing between two models that score similarly

Prefer the one that is:
1. **Simpler** — fewer things to break, easier to explain.
2. **Faster and cheaper** to train and serve.
3. **Easier to explain**, if anyone needs to trust or audit it.
4. **More stable** — smaller spread across CV folds and seeds.

"Similar" means the difference is within the uncertainty range (CV spread or bootstrap interval). See [Splits, validation and leakage](splits-validation-leakage.md#5-is-the-difference-real-uncertainty).

---

## 5. Tuning: how much is enough?

- **Defaults first.** Gradient boosting defaults are often close to their best.
- **Random search beats grid search** for the same budget. 20–50 trials with CV is plenty for most problems.
- **Tune what matters** (see the cards); ignore the rest.
- **Early stopping** saves a lot of guessing for boosting and neural nets.
- **Stop when** the gain is smaller than the fold-to-fold spread.
- Tuning almost never fixes a bad split, leaky features or the wrong metric. Fix those first.

---

## 6. Ensembles

- **Averaging** predictions of 2–3 *different* models (e.g. gradient boosting + logistic regression + a neural net) often gives a small boost, because their mistakes differ.
- **Stacking** (a model on top of other models' out-of-fold predictions) gives a bit more; it's common on Kaggle, less so in production.
- In production, ensembles cost complexity and latency. Use them only if the gain is worth it.
