# Challenge 28 — Evidence-grounded claim checker

[Previous: Challenge 27 — PII detection, competition metric](27-pii-detection-competition-metric.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 28 — Evidence-grounded claim checker

- **Goal:** A local CLI that labels a scientific claim as SUPPORT or REFUTE, cites retrieved doc ids, and abstains when the evidence is weak.
- **Why an engineer needs it:** This is the job interview project: data handling, retrieval, a small trained model, a generative model, a classical calibrator, and an eval that attributes errors.
- **What to build:**
  - CLI: input a claim, output a label, cited doc ids, retrieval scores, and an abstain flag.
  - Retrieval: the Challenge 22 SciFact index. BM25 remains a row in the final table.
  - System A: prompt-only SmolLM2-360M with retrieved text (the Challenge 23 setup, rerun so the capstone repo still reproduces it).
  - System B: full fine-tune of `distilbert-base-uncased` (or `prajjwal1/bert-tiny` if you are on the CPU fallback) as a classifier on claim + gold-or-retrieved passage. Train only on the SciFact train claims.
  - System C: optional QLoRA of the Challenge 20 model size on the train claims, formatted as a stance task. If time or GPU is gone, System C can be the prompt-only SLM, and you say so. Do not drop System B.
  - Abstain model: a logistic regression on retrieval features (score gap, overlap, rank) that predicts whether the gold doc is in the top-k. Fit on train claims only. Use it to abstain at a precision you set on dev.
  - Final report: retrieval Recall@5, label quality, abstention coverage, and the Challenge 23 error buckets for each system. A model card. A one-command eval.
- **Skills practiced:** System composition, calibration for abstention, comparison writeups, model cards.
- **Stack and data:** The stack you already have. BEIR SciFact and [allenai/scifact](https://github.com/allenai/scifact). Models named above.
- **Difficulty:** stretch
- **Rough time:** 2 weeks
- **GPU:** CPU-ok for BM25, DistilBERT on this small claim set, and SmolLM2-360M. small GPU or Colab-or-Kaggle fallback if you include QLoRA System C.
- **Acceptance criteria:**
  - `eval` writes the comparison table without manual edits.
  - Systems include BM25-or-retrieval diagnostics, the prompt-only SLM, and the fine-tuned encoder.
  - Test claims were not in the fine-tune or the abstain-model fit.
  - Every cited id in a sampled 20 outputs was retrieved for that claim.
  - The model card names a use you reject (for example, clinical or legal advice) and the abstain condition.
  - The README has the one command and the hardware.
- **Stretch goal:** Point the same CLI at BEIR NFCorpus queries and write what breaks (metric, abstain rate, or citation behavior) without retuning on that corpus’s test split.
- **Builds on:** Challenges 16, 19, 22, and 23. System C also uses Challenge 20.
