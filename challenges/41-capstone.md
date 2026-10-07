# 41 — Capstone

**Phase 13 · Capstone** · ⏱ 3–4 weeks · 💻 Laptop + Colab as needed · Level: stretch

[← 40 Kaggle NLP competition](40-kaggle-nlp.md) · [Index](../README.md)

## The problem

Design, build, evaluate and ship a system **you choose**, end to end. This is the project you'll talk about in interviews, so pick something you care about and can explain deeply.

There are no Build steps. You have a decision map, 40 challenges' worth of code, and a way of working. Use them.

## Requirements

Your capstone must have all of these:

1. **Problem framing doc** (Challenge 01 style), written first: input → output, users, problem type(s), labels/data, baseline, metric, and why ML is needed.
2. **Real, public data** (or data you create yourself), with a data card: source, license, size, splits, and known issues.
3. **A baseline**, and at least **two of these components**:
   - a classical ML model,
   - a fine-tuned model (classifier, LoRA adapter…),
   - RAG,
   - an agent with tools.
4. **An evaluation set written before building**, a one-command eval script, and results for the baseline and every major version.
5. **Error analysis** with buckets, and at least one improvement driven by it.
6. **Served** behind an API (Challenge 38) with a **demo UI** (Challenge 39).
7. **A model/system card:** intended use, evaluation results, limitations, and uses you'd refuse.
8. **A README** with an architecture diagram, setup and one-command reproduction, and results.
9. **A 5-minute walkthrough** (a written one is fine; a screen recording is better) that you could give in an interview.

## Example ideas

Pick one, or better, your own.

- **Job-posting assistant:** extract structured fields from job posts (Challenge 27), classify seniority (fine-tuned model), and answer "which of these jobs fit my CV?" with RAG over postings, with citations.
- **Personal finance categorizer:** categorize bank transactions (classical ML + embeddings), detect unusual spending (anomaly detection), and an agent that answers "how much did I spend on food last quarter vs this quarter?" using tools over the data. Use synthetic or public data, never your own real bank data in a public repo.
- **Research paper helper:** RAG over arXiv abstracts in one field, a retrieval eval with your own questions, a summarizer fine-tuned with LoRA, and an agent that builds a mini literature review.
- **Plant disease assistant:** an image classifier with transfer learning on a public plant-disease dataset, plus RAG over treatment guides, with a careful "consult an expert" boundary in the system card.

## How to approach it

1. **Week 1:** framing doc, data, data card, evaluation set, baseline. *Don't build the fancy part yet.*
2. **Week 2:** the core components, evaluated against the baseline.
3. **Week 3:** error analysis, one or two improvements, serving and demo.
4. **Week 4:** system card, README, walkthrough, cleanup.

If you run out of time, cut scope, not evaluation. A smaller system with honest numbers beats a bigger one with none.

## Self-review rubric

Score yourself 1–3 on each before calling it done. Aim for no 1s.

| Area | 1 | 3 |
| --- | --- | --- |
| Framing | Vague goal | Clear input/output, metric tied to user value |
| Baseline | None or trivial afterthought | Sensible baseline, honestly compared |
| Evaluation | A few hand-picked demos | Held-out set written first, one-command eval, numbers per version |
| Error analysis | "It's 87% accurate" | Error buckets drove a measured improvement |
| Engineering | Notebook only | Tested API, demo, reproducible setup |
| Communication | Code with no explanation | README, card with limitations, clear walkthrough |
| Judgment | Used the fanciest tools | Each component justified with evidence (decision map) |

## Done when

- [ ] All 9 requirements are met.
- [ ] Self-review with no 1s, or a written plan to fix them.
- [ ] Someone else can clone the repo and run your eval command.

## Reflect — the end of the path

- Redo [Challenge 01](01-problem-framing.md) one last time. Compare all attempts.
- Read your whole [decision map](../decision-map.md). Clean it up. It's your personal playbook now.
- Pick your 5 best `NOTES.md` files and the capstone for your portfolio. Polish their READMEs.
- Write `work/milestones.md`: what you can do now that you couldn't when you started, and what you want to learn next.
