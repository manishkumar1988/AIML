# 06 — Forecasting demand

**Phase 1 · Classical ML** · ⏱ 1 week · 💻 Laptop · Level: core

[← 05 Learning without labels](05-learning-without-labels.md) · [Index](../README.md) · [Next: 07 Tune, validate, explain →](07-tune-validate-explain.md)

## The problem

A city bike-sharing company moves bikes between stations every night. To plan, it needs a forecast of **tomorrow's hourly rentals**, made the evening before.

Dataset: [Bike Sharing Dataset](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset) (UCI). Use `hour.csv`: 17,379 hourly rows over 2011–2012, with weather, season, holiday flags, and counts (`casual`, `registered`, `cnt`).

## Decide first

1. You're forecasting tomorrow from today's evening. Which columns would you *actually know* at that moment?
2. Why would a random train/test split give a misleadingly good score here?
3. What's the simplest forecast you could make for 5 pm tomorrow?
4. `cnt = casual + registered`. What happens if you use `casual` as a feature?

## Learn

- **Time series** data has an order. The future must never leak into the past.
- **Time-based split:** train on earlier dates, validate and test on later dates. A random split lets the model "see" neighbouring hours from the future.
- **Leakage:** a feature that wouldn't be available at prediction time. Here `casual` and `registered` are the answer split in two. Real weather for tomorrow is also leakage, strictly; in real life you'd have a weather *forecast*. For this challenge, using actual weather is allowed but must be stated as an assumption.
- **Seasonal naive baseline:** "same hour, same weekday, last week." Embarrassingly hard to beat sometimes.
- **Lag features:** the count 24 hours ago, 168 hours (one week) ago. They must be lags you'd actually have when forecasting (≥ 24 hours back for a next-day forecast).
- **Calendar features:** hour, weekday, holiday, month. Trees use these well.
- **Metric:** MAE (bikes per hour) is easy to explain.

Read: [Forecasting: Principles and Practice](https://otexts.com/fpp3/), chapter 5.2 (simple forecasting methods) and 5.8 (evaluating forecast accuracy). The book uses R, but the ideas are what matter.

## Build

Work in `work/06-forecasting/`.

1. **Load and plot.** Build a proper datetime column from `dteday` + `hr`. Plot `cnt` over the whole period, then one week zoomed in.
   ✅ You see daily rush-hour peaks, a weekend pattern, and growth from 2011 to 2012.

2. **Feature inventory.** Write a table in `NOTES.md`: every column, and "known the evening before? yes / no / only as a forecast." Do this **before** any model.
   ✅ `casual` and `registered` are marked "no." Weather is marked "only as a forecast."

3. **Split by time.** Train: 2011-01-01 to 2012-06-30. Validation: 2012-07-01 to 2012-09-30. Test: 2012-10-01 to 2012-12-31.

4. **Baselines on validation.** (a) Training mean. (b) Same hour yesterday. (c) Same hour, same weekday, last week.
   ✅ (c) is clearly the best baseline. Write down its MAE. That's the number to beat.

5. **Feature model.** Calendar features + weather + lag features (`cnt` 24 h and 168 h before). Use `HistGradientBoostingRegressor`.
   ✅ MAE clearly below the seasonal naive baseline.

6. **The leakage experiment.** Add `casual` and `registered` as features and retrain. Record the MAE. Then remove them again.
   ✅ The score becomes "too good to be true." Write a sentence on why that model would be useless in practice.

7. **The random-split experiment.** Train the same (non-leaky) model with a *random* 80/20 split. Compare the MAE with your time-split result.
   ✅ The random split looks better. Write down why it's the wrong number to report.

8. **Errors.** Plot actual vs predicted for two weeks of validation. Group absolute error by hour of day and by weather situation. Where is the model worst?

9. **Test once.** Retrain on train+validation, forecast the test period, and report MAE next to the seasonal naive baseline on the same period.

## Hints

<details><summary>Hint 1 — making lag features</summary>

Sort by datetime, then `df["lag_24"] = df["cnt"].shift(24)`. Check for missing hours first: the dataset has a few gaps, so `shift(24)` isn't always exactly 24 hours. A safer way is to merge on `datetime - pd.Timedelta(hours=24)`.
</details>

<details><summary>Hint 2 — the model is worse than the naive baseline</summary>

Check you included `hr` and weekday as features, and the 168-hour lag. Also check you didn't accidentally drop all rows with NaN lags from validation.
</details>

## Common mistakes

- Random splits on time series.
- Lag features shorter than the forecast horizon (using the count 1 hour ago to forecast tomorrow).
- Forgetting that the test period (Oct–Dec) is a different season from the training months you weighted most.

## Done when

- [ ] A feature inventory written before modeling.
- [ ] Three baselines and one model on a time split.
- [ ] The leakage experiment and the random-split experiment, both recorded with a sentence each.
- [ ] Errors broken down by hour and weather.
- [ ] One test MAE next to the seasonal naive baseline on the same period.

## Stretch

Use `TimeSeriesSplit` for rolling-origin validation (train on months 1–6, validate month 7; train 1–7, validate 8; …). How stable is your MAE across folds?

## Reflect

- Name one leak you might miss in a real company dataset (hint: columns updated after the event).
- Update the **Time series** section of your [decision map](../decision-map.md).
