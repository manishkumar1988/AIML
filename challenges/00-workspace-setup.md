# 00 — Workspace setup

**Phase 0** · ⏱ 2–3 hours · 💻 Laptop · Level: warm-up

[Index](../README.md) · [Next: 01 Problem framing →](01-problem-framing.md)

## The problem

You're about to write a lot of code over many months. If your environment is messy, you'll lose hours to "it worked yesterday." Set it up once, properly.

## Decide first

Write your answers in a scratch file before reading on.

1. Why might a notebook that ran fine last month fail today?
2. What should *never* go into git for an ML project?
3. Why does a fixed random seed matter when comparing two models?

## Learn

- **Virtual environment:** an isolated set of Python packages for one project. You'll use [`uv`](https://docs.astral.sh/uv/), which is already installed on your Mac. It creates the environment and a lockfile (`uv.lock`) that records exact package versions, so the project still runs months later.
- **Notebooks vs scripts:** notebooks are great for exploring. Scripts are better for anything you want to rerun. In this path, explore in a notebook, then move the final version into a `.py` file.
- **Git:** saves the history of your code. Data files, model weights, and secrets (API keys) stay out of git. They're too big, or private.
- **Seeds:** many ML steps are random (data shuffling, weight initialization). Fixing the seed makes runs repeatable, so a difference in score comes from your change, not luck.
- **Apple GPU (`mps`):** PyTorch can use your M4 Pro's GPU through the `mps` device. You'll use it from Challenge 10 on.

## Build

1. **Python version.** Pin Python 3.12 for this project (3.14 is too new for some ML libraries):
   ```bash
   uv python pin 3.12
   uv init --no-package
   ```
   ✅ You have `pyproject.toml` and `.python-version` containing `3.12`.

2. **Install the first packages:**
   ```bash
   uv add numpy pandas scikit-learn matplotlib jupyter ipykernel
   ```
   ✅ `uv.lock` exists. `uv run python -c "import sklearn; print(sklearn.__version__)"` prints a version.

3. **Folder layout.** Create:
   ```
   work/            # one folder per challenge: work/02-first-model/ ...
   data/            # downloaded datasets (not in git)
   models/          # saved models and checkpoints (not in git)
   ```
   ✅ The folders exist.

4. **`.gitignore`.** It must ignore: `.venv/`, `data/`, `models/`, `__pycache__/`, `.ipynb_checkpoints/`, `.env`, `.DS_Store`.
   ✅ Create `data/test.csv`, run `git status`, and confirm it doesn't appear. Then delete the test file.

5. **Seed helper.** Write `work/common/seed.py` with a function `set_seed(seed)` that seeds Python's `random` and NumPy. (You'll add PyTorch to it in Challenge 10.)
   ✅ Calling `set_seed(42)` then `np.random.rand()` twice in two separate runs prints the same number both times.

6. **Smoke check.** Write `work/00-setup/check.py` that prints: Python version, NumPy, pandas and scikit-learn versions, and the seed. Run it with `uv run python work/00-setup/check.py`.
   ✅ It runs and prints all four lines.

7. **Set up your AI coding tool.** Write a project rules file your AI tool reads automatically: `CLAUDE.md` for Claude Code, `.cursor/rules/` for Cursor, or the equivalent for your tool. Put in it the conventions you want every generated script to follow, for example:
   - use `uv run`, Python 3.12, and the `set_seed` helper
   - data lives in `data/`, models in `models/`, never commit them
   - split before any preprocessing; fit preprocessing on train only
   - never use the test split for choosing anything
   - every script prints the numbers it saves
   ✅ Ask your AI tool to write `work/00-setup/check.py` again from scratch. It should follow your rules without you repeating them.

8. **Commit.** Commit everything (except ignored files) with a clear message.
   ✅ `git log` shows your commit. `git status` is clean.

## Hints

<details><summary>Hint 1 — <code>uv init</code> complains the project already exists</summary>

If a `pyproject.toml` already exists, skip `uv init` and just run `uv add ...`.
</details>

<details><summary>Hint 2 — how do I run a notebook with this environment?</summary>

`uv run jupyter lab` starts Jupyter inside the project environment. In VS Code or Cursor, pick the `.venv` interpreter as the kernel.
</details>

## Common mistakes

- Installing packages with plain `pip install` outside the project environment. Always use `uv add` or `uv run`.
- Committing a 150 MB CSV. Once it's in git history, it's painful to remove. Check `git status` before every commit.
- Putting API keys in code. Later challenges use a `.env` file, which is ignored.

## Done when

- [ ] `uv run python work/00-setup/check.py` works from a fresh terminal.
- [ ] `.gitignore` covers data, models, environments and secrets.
- [ ] `set_seed` gives repeatable random numbers.
- [ ] An AI rules file that makes your tool follow the project conventions.
- [ ] Everything is committed.
- [ ] `work/00-setup/NOTES.md` has your three "Decide first" answers, plus one line on anything that confused you.

## Stretch

Install `ruff` (`uv add --dev ruff`) and run `uv run ruff check work/`. Fix what it reports. A linter catches silly bugs early.

## Reflect

- Delete `.venv/`, then run `uv sync`. Did everything come back? That's what "reproducible" means.
- Update `progress.md`.
