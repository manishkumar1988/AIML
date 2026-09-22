# Challenge 25 — Train and evaluate an 8M–33M model

[Previous: Challenge 24 — TinyStories data card and a tokenizer](24-tinystories-data-card-tokenizer.md) · [Next: Challenge 26 — Porto Seguro, local Gini, no leaderboard tuning](26-porto-seguro-local-gini-no-leaderboard-tuning.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 25 — Train and evaluate an 8M–33M model

- **Goal:** Train a decoder-only model that reloads, report holdout perplexity, and compare samples with a published TinyStories model under an honest protocol.
- **Why an engineer needs it:** Training a language model is a systems and evaluation skill: parameter count, stability, checkpointing, and not over-claiming against a paper’s model.
- **What to build:** A decoder-only Transformer. Write the parameter count from the config before the long run. Target about 15M–33M parameters, context 256 or 512. CPU-only variant: at most about 8M parameters, shorter context, labeled CPU-scale. Train on the Challenge 24 train split only. Run a small sanity sweep of two or three learning rates on a short run before the long run. Save a checkpoint and load it in a fresh process. Report holdout perplexity (your tokenizer). Score 20 prompts with a rubric you wrote beforehand (grammar, coherence, stays in the TinyStories register). The public prompts in the dataset card’s `Evaluation_prompts.yaml` may be part of those 20. Compare qualitative samples to [roneneldan/TinyStories-33M](https://huggingface.co/roneneldan/TinyStories-33M). You may claim a lower perplexity than that model only if you compute both under a protocol you can defend in writing. A tokenizer mismatch blocks the claim.
- **Skills practiced:** Transformer training, checkpointing, perplexity, pre-registered rubrics.
- **Stack and data:** PyTorch. Data and tokenizer from Challenge 24. Reference model [roneneldan/TinyStories-33M](https://huggingface.co/roneneldan/TinyStories-33M).
- **Difficulty:** stretch
- **Rough time:** 1–2 weeks
- **GPU:** small GPU. Colab-or-Kaggle fallback for the 15M–33M run. CPU-ok only for the labeled ≤8M variant.
- **Acceptance criteria:**
  - The config’s parameter count is in the log and matches a function you can rerun.
  - The holdout perplexity and the learning-rate sanity sweep are in the log.
  - The checkpoint generates text after a fresh load.
  - The 20-prompt rubric sheet is filled in, and it was committed before generation.
  - The comparison to TinyStories-33M states whether perplexity is comparable.
  - Training loss alone is not the published result.
- **Stretch goal:** A second checkpoint at a clearly different size (for example the CPU 8M vs the 33M-class) on the same holdout and the same 20 prompts.
- **Builds on:** Challenges 9 (training logs) and 24.
