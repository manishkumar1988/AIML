# Challenge 27 — PII detection, competition metric

[Previous: Challenge 26 — Porto Seguro, local Gini, no leaderboard tuning](26-porto-seguro-local-gini-no-leaderboard-tuning.md) · [Next: Challenge 28 — Evidence-grounded claim checker](28-evidence-grounded-claim-checker.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 27 — PII detection, competition metric

- **Goal:** Reproduce [The Learning Agency Lab - PII Data Detection](https://www.kaggle.com/competitions/pii-detection-removal-from-educational-data) with the competition’s positive-class F-beta and a regex baseline.
- **Why an engineer needs it:** This is NER under a product constraint: missing a name is worse than a false alarm, and essays repeat. It uses the span skill from Phases 3 and 8 on a messy public contest.
- **What to build:** Token classification on the competition training essays. Read the Evaluation page and implement that metric (F-beta with beta = 5, focused on PII tokens rather than the sea of non-PII tokens). Check it on a hand-built example. Baseline: rules for emails, phone numbers, and obvious ids. Then a small encoder (DistilBERT or DeBERTa-v3-small) trained with the same span discipline as Challenge 19. Before CV, check for near-duplicate essays across folds and write the rule you used (document-level split at minimum). Do not copy a public winning ensemble. One model plus the regex baseline is the job.
- **Skills practiced:** Competition span metrics, document-level splits, regex baselines, encoder NER.
- **Stack and data:** `transformers`. Kaggle competition [PII Data Detection](https://www.kaggle.com/competitions/pii-detection-removal-from-educational-data).
- **Difficulty:** core
- **Rough time:** 1–2 weeks
- **GPU:** small GPU. Colab-or-Kaggle fallback.
- **Acceptance criteria:**
  - The metric matches the competition definition on your hand-built example, and the example is in the repo.
  - Regex and encoder scores are in the log under document-level CV.
  - The duplicate check is written down.
  - The public leaderboard was not used to pick the threshold. The threshold comes from CV.
- **Stretch goal:** Either enter one Kaggle competition that is open in the week you start this stretch, using the same rules file, or reproduce [Cassava Leaf Disease Classification](https://www.kaggle.com/competitions/cassava-leaf-disease-classification) with a near-duplicate-aware image split and a per-disease error table.
- **Builds on:** Challenges 8, 14, and 19.
