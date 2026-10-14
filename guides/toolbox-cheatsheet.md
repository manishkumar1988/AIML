# Toolbox cheat sheet

The commands you'll keep forgetting. Run them from the project root (`/Users/manish/projects/AIML_challenges`) unless noted.

---

## uv (Python environment and packages)

| Task | Command |
| --- | --- |
| Run a script in the project environment | `uv run python work/03-churn/train.py` |
| Add a package | `uv add lightgbm` |
| Add a dev-only package (tests, linters) | `uv add --dev pytest ruff` |
| Remove a package | `uv remove lightgbm` |
| Rebuild the environment from `uv.lock` | `uv sync` |
| Upgrade one package | `uv lock --upgrade-package torch` then `uv sync` |
| See an installed package's version | `uv pip show torch` |
| See the dependency tree | `uv tree` |
| Pin the Python version | `uv python pin 3.12` |
| Start Jupyter Lab | `uv run jupyter lab` |
| Run tests | `uv run pytest -q` |
| Lint | `uv run ruff check work/` |

Never use plain `pip install`: it bypasses `pyproject.toml` and `uv.lock`.

---

## git

| Task | Command |
| --- | --- |
| What changed? | `git status` / `git diff` |
| Stage and commit | `git add <files>` then `git commit -m "challenge 03: logistic baseline"` |
| History | `git log --oneline -10` |
| Undo uncommitted changes to a file | `git restore <file>` |
| Unstage a file | `git restore --staged <file>` |
| New branch for an experiment | `git switch -c try-lightgbm` |
| Back to main | `git switch master` |
| Park changes temporarily | `git stash` / `git stash pop` |
| Check nothing big or secret is staged | `git diff --cached --stat` |

**Commit after every working step.** Small commits make it easy to go back.

---

## PyTorch on your Mac

```python
import torch
device = "mps" if torch.backends.mps.is_available() else "cpu"
model = model.to(device)
x, y = x.to(device), y.to(device)
```

| Task | Code |
| --- | --- |
| Check the GPU is available | `torch.backends.mps.is_available()` |
| Count parameters | `sum(p.numel() for p in model.parameters())` |
| Save weights | `torch.save(model.state_dict(), "models/x.pt")` |
| Load weights | `model.load_state_dict(torch.load("models/x.pt", map_location=device))` |
| Free MPS memory between experiments | `torch.mps.empty_cache()` |

If an operation isn't supported on MPS, setting the environment variable `PYTORCH_ENABLE_MPS_FALLBACK=1` runs it on the CPU instead (slower, but it works).

---

## Kaggle

One-time setup: Kaggle → Settings → API → "Create New Token". Save the downloaded `kaggle.json` to `~/.kaggle/kaggle.json`, then `chmod 600 ~/.kaggle/kaggle.json`. Never put it in the repo.

| Task | Command |
| --- | --- |
| Download a dataset | `uv run kaggle datasets download -d mlg-ulb/creditcardfraud -p data/ --unzip` |
| Download competition data (accept the rules on the website first) | `uv run kaggle competitions download -c nlp-getting-started -p data/nlp-disaster` |
| Submit | `uv run kaggle competitions submit -c nlp-getting-started -f submission.csv -m "tfidf baseline, cv f1 0.79"` |
| List your submissions | `uv run kaggle competitions submissions -c nlp-getting-started` |

Put your CV score in the submission message, so you can compare CV vs leaderboard later.

---

## Hugging Face

| Task | Command / code |
| --- | --- |
| Log in (needed to push, or for gated models) | `uv run hf auth login` (older versions: `huggingface-cli login`) |
| Load a dataset | `load_dataset("stanfordnlp/imdb")` |
| Save / reload a split | `ds.save_to_disk("data/x")` / `load_from_disk("data/x")` |
| Load a model and tokenizer | `AutoTokenizer.from_pretrained(name)`, `AutoModelForSequenceClassification.from_pretrained(name, num_labels=…)` |
| Quick inference | `pipeline("text-classification", model=path, device="mps")` |
| Push a model | `model.push_to_hub("your-name/model-name")`, `tokenizer.push_to_hub(...)` |
| Where downloads are cached | `~/.cache/huggingface/` (can get large) |

---

## Ollama (local LLMs)

| Task | Command |
| --- | --- |
| Download a model | `ollama pull qwen2.5:7b` |
| Chat in the terminal | `ollama run qwen2.5:7b` |
| List downloaded models | `ollama list` |
| See what's loaded in memory | `ollama ps` |
| Model details (context, template) | `ollama show qwen2.5:7b` |
| Delete a model | `ollama rm qwen2.5:7b` |

**From Python (OpenAI-compatible):**
```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
r = client.chat.completions.create(model="qwen2.5:7b", temperature=0,
        messages=[{"role": "user", "content": "Hello"}])
print(r.choices[0].message.content)
```
Switching to a hosted provider = change `base_url`, `api_key` (from `.env`) and `model`.

---

## MLX (fine-tuning on Apple Silicon)

| Task | Command |
| --- | --- |
| Install | `uv add mlx-lm` |
| Generate text | `uv run mlx_lm.generate --model Qwen/Qwen2.5-0.5B-Instruct --prompt "Hello"` |
| LoRA fine-tune | `uv run mlx_lm.lora --model <model> --train --data <dir with train.jsonl, valid.jsonl> --iters 600` |
| Generate with the adapter | `uv run mlx_lm.generate --model <model> --adapter-path adapters --prompt "..."` |
| Merge the adapter into the model | `uv run mlx_lm.fuse --model <model> --adapter-path adapters` |

Run `uv run mlx_lm.lora --help` to see the options for your installed version.

---

## API keys and `.env`

```
# .env  (already in .gitignore)
ANTHROPIC_API_KEY=...
OPENAI_API_KEY=...
HF_TOKEN=...
```
```python
from dotenv import load_dotenv
import os
load_dotenv()
key = os.environ["ANTHROPIC_API_KEY"]
```
Before every commit: `git diff --cached` and make sure no key appears.

---

## Docker

| Task | Command |
| --- | --- |
| Build an image | `docker build -t intent-api .` |
| Run it | `docker run -p 8000:8000 intent-api` |
| Running containers | `docker ps` |
| Logs | `docker logs <container-id>` |
| Stop | `docker stop <container-id>` |
| Image sizes | `docker images` |

On a Mac you need Docker Desktop, OrbStack or Colima installed.

---

## FastAPI

| Task | Command |
| --- | --- |
| Run the API with auto-reload | `uv run uvicorn app:app --reload` |
| Interactive docs | open `http://localhost:8000/docs` |
| Call it | `curl -X POST localhost:8000/predict -H "Content-Type: application/json" -d '{"texts": ["my card hasnt arrived"]}'` |

---

## Disk space

ML eats disk. Check from time to time:

```bash
du -sh data models ~/.cache/huggingface ~/.ollama
```

Delete datasets and models you've finished with (they can be re-downloaded), and unused Ollama models with `ollama rm`.
