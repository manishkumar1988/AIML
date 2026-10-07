# 05 — Learning without labels: clustering and anomaly detection

**Phase 1 · Classical ML** · ⏱ 1 week · 💻 Laptop · Level: core

[← 04 Fraud detection](04-fraud-imbalanced-data.md) · [Index](../README.md) · [Next: 06 Forecasting demand →](06-time-series-forecasting.md)

## The problem

Two requests from two teams. Neither has labels.

- **Part A — Marketing:** "We want to understand our different types of customers so we can treat them differently." They have two years of online-shop transactions.
- **Part B — Risk:** "We don't have fraud labels for a new product. Can you find the weirdest transactions for someone to review?" You'll simulate this with the fraud data from Challenge 04, *pretending* you don't have labels, then use the hidden labels to check how well you did.

Datasets:
- Part A: [Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii) (UCI). About 1 million invoice lines from a UK online shop, 2009–2011.
- Part B: the Challenge 04 fraud CSV.

## Decide first

1. Without labels, how could you tell whether a clustering is "good"?
2. Is "number of customer groups" something the data tells you, or something you choose?
3. Part B: what's the difference between "rare" and "fraud"?
4. When would you pick anomaly detection over a supervised classifier, if a few labels did exist?

## Learn

- **Clustering** groups similar items. **K-means** is the standard first choice: you pick k, it finds k centers. It needs **scaled** features and works best on roundish, similar-sized groups.
- **Choosing k:** the elbow plot (inertia vs k) and **silhouette score** help, but the real test is whether the business can *use* the groups. 3–6 named segments beat 15 unexplainable ones.
- **RFM features** describe customers: **R**ecency (days since last purchase), **F**requency (number of orders), **M**onetary (total spend). Simple and powerful.
- **Anomaly detection** scores how unusual each point is. **Isolation Forest** isolates points with random splits; weird points get isolated quickly.
- **Unusual ≠ bad.** Anomaly detection finds rare things. Whether rare means fraud depends on the data. That's why you check it against labels when you can.
- **PCA** squashes many features into 2 for plotting. It's for looking, not for proof.

Read: scikit-learn [Clustering overview](https://scikit-learn.org/stable/modules/clustering.html) (first table + K-means section) and [Outlier detection](https://scikit-learn.org/stable/modules/outlier_detection.html) (Isolation Forest section).

## Build

Work in `work/05-unsupervised/`.

### Part A — Customer segments

1. **Clean.** Load both sheets/years. Drop rows with no `Customer ID`. Handle returns: invoices starting with `C` have negative quantities. Decide whether to drop them or net them out, and write why.
   ✅ You can say how many rows you dropped and why. Roughly 20% of rows have no customer id.

2. **Build RFM per customer.** Reference date = the day after the last invoice.
   ✅ One row per customer (about 5,000–6,000 customers), three columns.

3. **Look at the distributions.** Frequency and Monetary are very skewed. Apply `np.log1p`, then `StandardScaler`.
   ✅ Histograms after the transform look far less lopsided.

4. **K-means for k = 2…10.** Plot inertia and silhouette score vs k. Pick k (usually 3–5) and write why.

5. **Describe the segments.** For each cluster: size, and median R, F, M on the *original* scale. Give each a name ("loyal big spenders", "lapsed one-timers", …).
   ✅ A table a marketer could read, with a suggested action per segment.

6. **Baseline check.** Compare with simple rules: split customers into thirds by spend and by recency (a 3×3 grid). Are your clusters more useful than that? Be honest.

### Part B — Anomalies without labels

7. **Isolation Forest** on the fraud data's features (drop `Class` — you "don't have it"). Fit on the training period only (first 60% by time, as in Challenge 04).
8. **Score the validation period.** Take the 200 most anomalous transactions. *Now* look at the labels: how many are fraud?
   ✅ Precision in the top 200 is far above the 0.17% base rate, but below your supervised model from Challenge 04. Write down both numbers.
9. **Compare** PR-AUC of the Isolation Forest scores vs your Challenge 04 model, on the same validation rows.

10. Write `NOTES.md`: the segment table, the anomaly-vs-supervised comparison, and when you'd use each.

## Hints

<details><summary>Hint 1 — reading the Excel file is slow</summary>

Read it once with `pd.read_excel(path, sheet_name=None)` (it returns both sheets), concatenate, and save as Parquet (`df.to_parquet`). Load the Parquet file afterwards. (`uv add openpyxl pyarrow`.)
</details>

<details><summary>Hint 2 — one cluster has almost everyone</summary>

You probably forgot to log-transform or scale. K-means uses distances, so one huge-valued column dominates everything.
</details>

## Common mistakes

- Clustering raw, unscaled features.
- Picking k only from the silhouette score, ignoring whether the segments make sense.
- Calling anomalies "fraud" without checking. Anomaly detection gives you a review queue, not a verdict.

## Done when

- [ ] A cleaned RFM table, with your cleaning decisions written down.
- [ ] An elbow/silhouette plot and a justified k.
- [ ] A named segment table with suggested actions.
- [ ] Isolation Forest top-200 precision and PR-AUC, next to the supervised model's.
- [ ] `NOTES.md` answers: when would you use anomaly detection instead of a classifier?

## Stretch

Try `DBSCAN` or a Gaussian Mixture on the RFM data. Plot the customers in 2D with PCA, coloured by cluster.

## Reflect

- How would you check, six months later, whether the segments helped marketing?
- Update the **No labels** section of your [decision map](../decision-map.md).
