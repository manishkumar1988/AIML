# ULB credit-card fraud table

Audit for Challenge 2. No classifier has been fit on this file.

## Source

Kaggle dataset `mlg-ulb/creditcardfraud` (ULB MLG, European cardholders, September 2013). This machine has no Kaggle credentials, so the file was downloaded from the Zenodo copy of that table, DOI [10.5281/zenodo.7395559](https://doi.org/10.5281/zenodo.7395559), which lists the file under CC BY 4.0. The local file matches that record's MD5 `e90efcb83d69faf99fcab8b0255024de`.

The CSV stays in `data/creditcard.csv` and is gitignored.

sha256: `76274b691b16a6c49d3f159c883398e03ccd6d1ee12d9d8ee38f4b4b98551a89`

row_count: 284807

Columns, in file order: `Time`, `V1`–`V28`, `Amount`, `Class`. `Class` is 0 or 1. `Time` is seconds since the first transaction in the file.

## What the table contains

- 284,807 rows. 492 have `Class == 1`. The positive rate is 492/284807 = 0.001727485630620034 (about 0.173%).
- Missing cells: 0.
- Duplicate rows exist. 1,081 rows are exact copies of an earlier row. 1,854 rows sit in a duplicated group. Copies share `Time`, because `Time` is part of the row, so the split below cannot place two copies on opposite sides of a boundary.
- `Time` runs from 0 to 172,792 seconds, just under 48 hours.
- `Amount` is right-skewed. Minimum 0, median 22, mean 88.34961925093134, 90th percentile 203, 99th percentile 1017.97, maximum 25,691.16. Sample skew is 16.977724453761006.

## Split rule for Challenge 3

Written before any model. `Time` is not allowed to cross a split. A later transaction is not used to train a decision about an earlier one.

Row id is the 0-based data-row number in `creditcard.csv` (the header is not a row). Another person rebuilds the same indices as follows:

1. Sort row ids by `Time` ascending. Break ties by row id ascending.
2. Let `n` be the row count above. Raw cuts on that sorted list are `dev_cut = n * 60 // 100` and `test_cut = n * 80 // 100`.
3. Snap each cut backward. While the row just before the cut has the same `Time` as the row at the cut, move the cut one row earlier. The whole equal-`Time` run stays on the later side.
4. Train is sorted positions `[0, dev_cut)`. Dev is `[dev_cut, test_cut)`. Test is `[test_cut, n)`.

On this file the raw dev cut is 170,884 and snaps back to 170,882. The test cut stays at 227,845. Sizes are train 170,882, dev 56,963, test 56,962.

Boundary times, in seconds:

| Split | Rows | Frauds | Time min | Time max |
| --- | --- | --- | --- | --- |
| Train | 170,882 | 360 | 0 | 120,395 |
| Dev | 56,963 | 57 | 120,396 | 145,247 |
| Test | 56,962 | 75 | 145,248 | 172,792 |

Every train `Time` is strictly less than every dev `Time`, and every dev `Time` is strictly less than every test `Time`.

Challenge 3 fits on train only. The operating threshold is chosen on dev. Test is held out and used once. Test is not used to pick the model class or the threshold.

## Decision

Use this split for Challenge 3. Do not ship a model from this audit. The log row records the table's positive rate, not a model score.
