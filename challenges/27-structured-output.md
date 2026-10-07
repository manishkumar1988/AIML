# 27 — Structured output and extraction

**Phase 8 · Working with LLMs (GenAI)** · ⏱ 1 week · 💻 Laptop · Level: core

[← 26 Run LLMs](26-run-llms.md) · [Index](../README.md) · [Next: 28 Evaluating LLMs →](28-evaluating-llms.md)

## The problem

The bank's support system needs more than an intent label. For each incoming message it wants a record its software can use directly:

```json
{"intent": "card_payment_wrong_exchange_rate", "amount": 52.0, "currency": "EUR", "urgent": false}
```

If the LLM returns broken JSON even 2% of the time, the pipeline crashes thousands of times a day. You'll make extraction **reliable** and measure it.

Data: 100 messages from your Banking77 **validation** set, plus 200 from the **test** set. You'll label the extra fields yourself.

## Decide first

1. Which fields could a regular expression extract without any LLM? Which can't it?
2. What could go wrong with JSON coming out of an LLM? List at least four things.
3. How would you measure "extraction quality" when there are four fields?

## Learn

- **Structured output** means the model must return data in a fixed **schema**. Three levels of strength:
  1. **Prompting** ("reply only with JSON like this…"). Works most of the time.
  2. **JSON mode / schema-constrained decoding:** the server forces the output to match a JSON schema. Ollama supports a `format` parameter that takes a JSON schema; most hosted APIs have an equivalent.
  3. **Validate and retry:** parse with **Pydantic**; if validation fails, send the error back and ask again (limit the number of retries).
- **Pydantic models** define the schema in Python, generate the JSON schema, and validate output (types, allowed values, ranges).
- **Enums for labels:** restricting `intent` to the 77 allowed values stops the model inventing new ones.
- **`null` is an answer:** the schema must allow "not mentioned" (`amount: null`), or the model will invent an amount.
- **Field-level metrics:** accuracy per field; for numbers, exact match after normalizing; plus the JSON validity rate.
- **Rules + LLM:** use regex for what it does well (amounts, currencies), and the LLM for what needs understanding (intent, urgency). Compare.

Read: [Pydantic docs](https://docs.pydantic.dev/latest/) ("Models" and "JSON Schema"), and Ollama's [structured outputs](https://ollama.com/blog/structured-outputs) post.

## Build

Work in `work/27-structured-output/`. `uv add pydantic`.

1. **Label data.** Take 100 validation and 200 test messages from your frozen split. For each, label `amount` (number or null), `currency` (ISO code or null) and `urgent` (true/false). The intent label already exists. Write your labelling rules first (what counts as urgent?).
   ✅ `labels_val.jsonl` and `labels_test.jsonl` are committed, with the rules in `NOTES.md`.

2. **Schema.** A Pydantic model `TicketInfo` with `intent` as a `Literal`/`Enum` of the 77 intents, `amount: float | None`, `currency: str | None`, `urgent: bool`.

3. **Regex baseline** for `amount` and `currency` only.
   ✅ Field accuracy for those two fields on validation.

4. **Level 1 — prompt only.** Prompt your local 7B model to return JSON. Parse with `json.loads`, then validate with Pydantic. Record: JSON parse failures, schema-validation failures, per-field accuracy.
   ✅ You'll likely see some failures (extra text around the JSON, wrong field names, invented intents).

5. **Level 2 — schema-constrained.** Pass the schema via Ollama's `format`. Same measurements.
   ✅ Parse failures drop to (near) zero. Did field accuracy change?

6. **Level 3 — validate and retry**, up to 2 retries, feeding back the validation error. Measure success rate and the average number of calls.

7. **Improve on validation only.** Try few-shot examples and clearer field definitions. Keep a log of prompt versions and their validation scores.

8. **Test once.** Run your best configuration on the 200 test messages. Report JSON validity, per-field accuracy, intent accuracy (compared with DistilBERT from Challenge 20 on the same messages), and latency per message.

9. **Errors.** Read 15 wrong extractions. Group them: wrong intent, invented amount, missed currency, wrong urgency.

10. `NOTES.md`: the level 1/2/3 table, regex vs LLM for amount/currency, the test results, and your design for a production extraction pipeline.

## Hints

<details><summary>Hint 1 — building the schema from Pydantic</summary>

`TicketInfo.model_json_schema()` gives a JSON schema dict to pass as `format`. Parse with `TicketInfo.model_validate_json(text)`.
</details>

<details><summary>Hint 2 — the prompt is huge with 77 intents</summary>

That's fine for a 7B model with a big enough context (set `num_ctx`). Alternatively, use a short description per intent. Note the token cost per call either way.
</details>

## Common mistakes

- No `null` option, so the model invents values.
- Tuning prompts on the test messages.
- Counting "valid JSON" as success. Valid JSON with wrong values is still wrong.

## Done when

- [ ] Labelling rules and labelled validation/test sets.
- [ ] A results table for prompt-only, schema-constrained, and validate-and-retry.
- [ ] A regex vs LLM comparison for amount and currency.
- [ ] One test run with per-field accuracy and latency.
- [ ] A written production design (which parts are rules, which are LLM, how failures are handled).

## Stretch

Use the [`instructor`](https://python.useinstructor.com/) library to do the same thing in fewer lines, and compare with your own implementation.

## Reflect

- Fill in "how I get reliable structured output" in the **Using LLMs** section of your [decision map](../decision-map.md).
