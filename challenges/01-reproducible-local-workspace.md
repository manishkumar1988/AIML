# Challenge 1 — Reproducible local workspace

[Next: Challenge 2 — Data audit and an experiment log](02-data-audit-experiment-log.md) · [Index](../aiml-engineer-challenges.md)

Standing standard for every challenge: [Standing standard](../aiml-engineer-challenges.md#standing-standard) in the index. It is not copied here.

### Challenge 1 — Reproducible local workspace

- **Goal:** One Python project that later challenges will grow, with a fixed seed and a one-command smoke check.
- **Why an engineer needs it:** Untracked environments make every later comparison arguable. Hiring loops and team handoffs start from “can someone else run this.”
- **What to build:**
  - A git repo with a real `.gitignore` (virtualenvs, data, checkpoints, secrets).
  - Pinned dependencies (`pyproject.toml` or a lockfile).
  - A `src/` layout, a config file for paths and seeds, and a seed helper.
  - A README with the commands to create the environment and run the smoke check.
  - A smoke check that loads the config, prints the seed, and exits 0. It does not train a model.
- **Skills practiced:** Project layout, pinning, git hygiene, config, seeds.
- **Stack and data:** Python 3.11+. No dataset yet.
- **Difficulty:** revision
- **Rough time:** 2–3 days
- **GPU:** CPU-ok
- **Acceptance criteria:**
  - From a clean checkout, the README commands create the environment and the smoke check exits 0.
  - Two runs print the same seed.
  - `.gitignore` excludes data and checkpoints. `git status` is clean of those paths.
  - The README states the Python version and the OS you used.
- **Stretch goal:** The smoke check also fails loudly when a required config key is missing, and a one-line test proves that failure.
- **Builds on:** nothing. This is the base.
