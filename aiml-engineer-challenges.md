# AI/ML Engineer Practice Curriculum

A sequenced set of build-it-yourself challenges for Manish. Theory is assumed. Each challenge is a piece of engineering work on a personal machine, scored by an artifact and an observable check, not by a vibe that the notebook “works.”

## How to use this

Do the challenges in order, on your own machine. One at a time. We start **Challenge 1** when you say go. This document has no solution code.

Skip ahead only if you can already meet that challenge’s acceptance criteria. If you skip, write a short note that lists the checks you can meet and points at the artifact (repo path, metric table, model card). Do not skip a challenge whose artifact a later challenge reuses — the experiment log, the Banking77 split, the eval harness, the SciFact index — unless that artifact already exists.

Finish the acceptance criteria before the stretch goal. Difficulty (`revision`, `core`, `stretch`) says how hard the work is. It does not mean the challenge is optional.

Hardware is a personal computer plus free Colab or Kaggle GPUs. Where a full-size LLM train would not fit, the challenge names a memory-safe size. Do that fallback. A 7B full fine-tune is out of scope on purpose.

Use public data only. Read the dataset license and any competition rules before you train. Keep data and checkpoints out of git when the license or the file size says so.

A result that is not written down in the repo does not count.

## Standing standard

These rules apply to every challenge after the first.

- **Baseline first.** A dumb, named baseline exists before any neural net: majority class, median, keyword rules, BM25, lead-3, or the previous challenge’s model.
- **Split before fit.** The split unit matches the decision (time, store, document, image group, user). Preprocessing statistics are fit on train only.
- **One held-out set.** Choose models on a dev split. Touch the final test split once, or as the competition’s local CV protocol says.
- **Metric matches the cost.** Record the metric you would actually ship on. If a second number looks flattering and would change the decision, explain it in writing.
- **Error analysis.** Break errors by slice (class, time, length, score band). A single average is not an analysis.
- **Eval before vibes.** For generative models, a fixed set and a script that writes the table come before any demo.
- **Rerun.** A second person can rerun the scored command from the README on a clean environment. Seeds are fixed.
- **Decision.** End with what you would ship, what you would not, and what evidence is still missing.

**Memory ceiling for this curriculum**

| Work | Size that counts |
| --- | --- |
| Full fine-tune | Encoder around 4M–110M (`prajjwal1/bert-tiny`, `distilbert-base-uncased`). |
| Local SLM inference | 135M–360M on CPU. Up to `Qwen/Qwen2.5-1.5B-Instruct` or `HuggingFaceTB/SmolLM2-1.7B-Instruct` in 4-bit if you have a small GPU or a free T4. |
| LoRA / QLoRA | Those same 0.5B–1.7B models, 4-bit. |
| Train a language model from scratch | About 8M–33M parameters on TinyStories. |
| Out of scope | Full fine-tune or pretrain of a 7B+ model. |

**GPU labels**

- **CPU-ok** — the scored run finishes on a laptop CPU.
- **small GPU** — about 8 GB, or a free T4-class GPU.
- **Colab-or-Kaggle fallback** — use a free hosted GPU for the scored run. Keep the code in the same repo.

## Phase 1 — Engineering setup and habits

Two challenges. Enough process to make later results believable. No modeling yet.

**Pitfalls.** Notebook-only work you cannot rerun. Unpinned packages. Data files committed to git. A seed that changes every run. Starting a model before you can say what the table contains.

**What good looks like.** A teammate clones the repo, creates the environment from the README, and gets the same smoke-check output. The experiment log has a row before any model score exists.

- [Challenge 1 — Reproducible local workspace](challenges/01-reproducible-local-workspace.md)
- [Challenge 2 — Data audit and an experiment log](challenges/02-data-audit-experiment-log.md)

## Phase 2 — Classical ML with serious evaluation

Three challenges. You already know the algorithms. The work is baselines, splits, metrics, and a decision.

**Pitfalls.** Accuracy on a rare class. A random split that straddles time. Target encoding or imputation fit on the full frame. Tuning on the Kaggle public test file. Reporting the best seed after the fact.

**What good looks like.** A baseline and a stronger model on the same split, a metric a product owner could use, an error slice, and a sentence that says what you would ship.

- [Challenge 3 — Imbalanced classification and a decision metric](challenges/03-imbalanced-classification-decision-metric.md)
- [Challenge 4 — Leakage and a split that matches the decision](challenges/04-leakage-split-that-matches-decision.md)
- [Challenge 5 — Regression, heavy tails, and a model memo](challenges/05-regression-heavy-tails-model-memo.md)

## Phase 3 — NLP

Three challenges, still without the Hugging Face Trainer. You should feel the task (labels, spans, thresholds) before a library hides it.

**Pitfalls.** Accuracy on 77 imbalanced intents. A tokenizer or vectorizer fit on the test text. Thresholds picked on the test set. Token-level accuracy for NER, which scores the `O` tag and looks excellent. Shuffling tokens across sentences.

**What good looks like.** A keyword or linear baseline, a metric per label, and a sheet of confused pairs or broken spans you have actually read.

- [Challenge 6 — Fine-grained intent classification](challenges/06-fine-grained-intent-classification.md)
- [Challenge 7 — Multi-label moderation and an operating point per label](challenges/07-multi-label-moderation-operating-point-label.md)
- [Challenge 8 — Named entity recognition at span level](challenges/08-named-entity-recognition-at-span-level.md)

## Phase 4 — Computer vision, then advanced CV

Three challenges. Classification with a real image set, transfer learning judged against your own from-scratch run, then detection.

**Pitfalls.** Resizing or normalizing with statistics from the full set. Augmentations applied before the split. Accuracy when classes are easy to separate by background. Near-duplicate photos in train and test. Judging a detector by classification accuracy. Chasing a private VOC test server.

**What good looks like.** A from-scratch number you can beat honestly, a per-class failure list, and a detection metric with a localization-vs-classification split.

- [Challenge 9 — Image classification with noisy training labels](challenges/09-image-classification-noisy-training-labels.md)
- [Challenge 10 — Transfer learning with a pre-registered win](challenges/10-transfer-learning-pre-registered-win.md)
- [Challenge 11 — Object detection on Pascal VOC 2007](challenges/11-object-detection-pascal-voc-2007.md)

## Phase 5 — Hugging Face

Three challenges. Datasets, tokenizers, Trainer, pipelines, and a model card. The point is to beat a baseline you already trust, on a split you already froze.

**Pitfalls.** A new random split that makes the Hub model look better than Challenge 6. Training a tokenizer on the test text. A model card with no limitation and no number. Pushing weights and forgetting the label map, so the pipeline’s id-to-label mapping is wrong.

**What good looks like.** The same Banking77 test ids as Challenge 6, a tokenizer report with fertility on held-out text, and a pipeline that fails in the ways the card describes.

- [Challenge 12 — Datasets, splits, and a dataset card](challenges/12-datasets-splits-dataset-card.md)
- [Challenge 13 — Train a tokenizer and measure it](challenges/13-train-tokenizer-measure-it.md)
- [Challenge 14 — Trainer, pipeline, and a model card](challenges/14-trainer-pipeline-model-card.md)

## Phase 6 — Small language models

Two challenges. Run a model that fits in memory, then score it with the harness you will reuse for APIs, RAG, and the capstone.

**Pitfalls.** Judging a model by five hand-picked prompts. No temperature or decoding settings written down. Comparing to Challenge 6 on a different label set. Silent truncation.

**What good looks like.** A results file a script wrote, with model id, decoding settings, and the same metrics as the classical models.

- [Challenge 15 — Run an SLM and measure it](challenges/15-run-slm-measure-it.md)
- [Challenge 16 — An eval harness with a frozen slice](challenges/16-eval-harness-frozen-slice.md)

## Phase 7 — Large language models as an engineer

Two challenges. Use a hosted model and a local SLM on the same harness. Then write down failure modes from a set you authored. This is defensive measurement of ordinary failures (format breaks, unanswerable questions, conflicting instructions in one user message). It is not an attack toolkit.

**Pitfalls.** Tuning the prompt on the test slice. Comparing an API model to a local model with different slices. Declaring a model “good” from a chat window. Treating a refusal and a hallucination as the same failure.

**What good looks like.** One table with quality, latency, and cost, plus a failure note that says what you would not ship the model for.

- [Challenge 17 — API vs local on the same harness](challenges/17-api-vs-local-same-harness.md)
- [Challenge 18 — Failure modes on a set you wrote](challenges/18-failure-modes-set-you-wrote.md)

## Phase 8 — Fine-tuning

Two challenges. Full fine-tune only where the model is small enough. QLoRA for a 1B-class instruct model. A written rule for when full fine-tune is the wrong tool.

**Pitfalls.** Copying a BERT fine-tune recipe onto a 7B model and discovering it only after the machine swaps itself to death. Tuning LoRA rank on the test set. Declaring victory on ROUGE when the summary adds a fact that was not in the dialogue. Forgetting to evaluate the prompt-only model on the same test.

**What good looks like.** A small full fine-tune that beats your span tagger, a QLoRA run with a prompt-only and an extractive baseline, and a memory note you calculated before training.

- [Challenge 19 — Full fine-tune of a small encoder, and a do-not-scale memo](challenges/19-full-fine-tune-small-encoder-do-not-scale-memo.md)
- [Challenge 20 — QLoRA on a 1B-class model](challenges/20-qlora-1b-class-model.md)

## Phase 9 — RAG

Three challenges. Ingestion and chunking, then retrieval measured with qrels, then generation measured separately from retrieval. One notebook that answers a question you wrote is not done.

**Pitfalls.** Chunks that split a sentence in a way you never look at. Fitting the chunk size on the test queries. Dense retrieval with no BM25 baseline. Blaming the generator for a miss when the gold document was never retrieved. Trusting a fluent answer that cites the wrong id.

**What good looks like.** A chunk report with bad examples, a retrieval table where BM25 is a row, and an error table that splits retrieval misses from generation misses.

- [Challenge 21 — Ingestion and chunking](challenges/21-ingestion-and-chunking.md)
- [Challenge 22 — Retrieval evaluation against qrels](challenges/22-retrieval-evaluation-against-qrels.md)
- [Challenge 23 — Grounded generation, scored apart from retrieval](challenges/23-grounded-generation-scored-apart-from-retrieval.md)

## Phase 10 — Train a custom small language model

Two challenges. Personal-hardware scale: TinyStories, your own tokenizer, a model in the 8M–33M range. This is a real train-and-eval loop, not a web-scale pretrain.

**Pitfalls.** A tokenizer fit on the holdout. A diverging loss that you “fix” by quoting training loss only. Comparing perplexity to `TinyStories-33M` under a different tokenizer and calling it a win. Generating five cute stories and stopping. Training on the paper’s evaluation prompts.

**What good looks like.** A data card, a reloadable checkpoint, holdout perplexity, and a rubric you wrote before you looked at samples.

- [Challenge 24 — TinyStories data card and a tokenizer](challenges/24-tinystories-data-card-tokenizer.md)
- [Challenge 25 — Train and evaluate an 8M–33M model](challenges/25-train-evaluate-8m-33m-model.md)

## Phase 11 — Kaggle-style competitions

Two reproductions of public competitions whose data is still available. Late submission or a local reconstruction both count. The public leaderboard is not a validation set.

**Pitfalls.** Peeking at the leaderboard to pick the model. Computing target encodings on all rows. Near-duplicate documents in more than one fold. A metric script that does not match the competition. Ensembles you cannot explain.

**What good looks like.** A local CV protocol you could have run during the competition, a baseline, one stronger model, and a writeup that says what would have been leakage.

- [Challenge 26 — Porto Seguro, local Gini, no leaderboard tuning](challenges/26-porto-seguro-local-gini-no-leaderboard-tuning.md)
- [Challenge 27 — PII detection, competition metric](challenges/27-pii-detection-competition-metric.md)

## Phase 12 — Capstone

One challenge. A local claim-checking tool that uses the retrieval index, a small fine-tuned encoder, an SLM, and a classical abstain model. Portfolio-sized, still personal-hardware.

**Pitfalls.** A CLI that only works on five claims you picked. No baseline from Challenge 23. A fine-tune that leaks test claims. An abstain model fit on the same rows you report. Citations that were not retrieved.

**What good looks like.** One command that evaluates the frozen SciFact test claims, a table of systems, and a model card that says when the tool should abstain.

- [Challenge 28 — Evidence-grounded claim checker](challenges/28-evidence-grounded-claim-checker.md)

## Suggested pace

One numbered challenge at a time. Check the acceptance criteria before the stretch goal.

| Kind | Pace |
| --- | --- |
| Revision (1, 2, 3) | Two of these can share a week if the log stays honest. |
| Most core challenges | About one week each. |
| Challenges 11, 20, 25, 26, 27, 28 | Up to two weeks each. |

At that pace the full sequence is about 34 focused weeks. It is a pace, not a deadline. If you already meet a challenge’s checks, write the skip note and move on. If hardware blocks a scored run, use the CPU-scale or Colab fallback written in that challenge and label the result. Do not replace the fallback with a 7B full fine-tune.

When you are ready for Challenge 1, say go.

## Portfolio artifacts

Ship these. The others can stay as lab notes unless you want them public.

| Challenge | Artifact | Why it earns a place |
| --- | --- | --- |
| 1–2 | Repo template and experiment log | Shows you can rerun work and write a data decision before a model. |
| 3–5 | Eval memos (fraud, Rossmann leakage, Allstate tails) | Shows metric choice, leakage, and a shipping decision. |
| 6–8 | NLP error writeups (Banking77, Jigsaw, Few-NERD span F1) | Shows you read errors and test the metric. |
| 9–11 | Food-101 comparison and VOC detection note | Shows from-scratch vs transfer, then mAP with an error taxonomy. |
| 14 | DistilBERT intent model card (Hub if you pushed it) | A loadable model with limitations, tied to a frozen test. |
| 16–18 | Eval harness and failure-mode note | The artifact you reuse; shows API vs local with cost and failures. |
| 20 | QLoRA summarizer on SAMSum, with the faithfulness read | Shows parameter-efficient training and why ROUGE was not enough. |
| 22–23 | SciFact retrieval table and RAG error buckets | Shows retrieval and generation scored apart. |
| 25 | TinyStories checkpoint, data card, holdout perplexity | Shows you trained a small model and did not over-claim. |
| 26–27 | Porto Seguro and PII writeups | Shows competition protocol without leaderboard tuning. |
| 28 | Claim-checker CLI, eval table, model card | The capstone. Links classical abstention, retrieval, a small fine-tune, and an SLM. |

Challenges 4, 5, 7, 12, 13, 15, 19, 21, and 24 are the supporting work. Keep them in the same repo. Link them from the capstone README so a reader can see the sequence.
