---
name: cost-review
description: >
  Diff-driven audit of a change for cost implications before merge — paid external API calls, LLM token spend, and repeat/fan-out processes (loops, polling, retries, per-request/per-user work, background jobs). Use when asked to "check cost implications", "will this increase spend/API calls", "review for cost", or before merging anything that adds an outbound paid call, an LLM call, a background job, or a frontend polling/fetch. Triggers: "cost review", "API spend", "token cost", "will this cost more".
---

# Cost Review (API calls, LLM tokens, repeat processes)

Diff-driven audit of a change for cost implications before merge — paid external API calls, LLM token spend, and repeat/fan-out processes (loops, polling, retries, per-request/per-user work, background jobs). Use when asked to "check cost implications", "will this increase spend/API calls", "review for cost", or before merging anything that adds an outbound paid call, an LLM call, a background job, or a frontend polling/fetch. Triggers: "cost review", "API spend", "token cost", "will this cost more".

A change can be functionally correct and still be a cost regression. The expensive
mistakes are almost never one call — they're one call placed **inside a loop** that runs
per-item across a fan-out, or a fetch that re-runs **on every request/view**. Always
reason about the **multiplier**, not the unit cost. A one-cent call inside an
`N items × M workers` fan-out is not a one-cent change.

## When to use

- Reviewing a change/PR/branch for cost, spend, billing, or API-call volume.
- Before adding: a new outbound paid API call, a new LLM agent/call, a new background
  job, a new frontend polling/`useEffect` fetch, or a new retry/back-off.
- When a run's cost or latency jumped and you need to localise the regression.

## Build the cost map (do this once per project, then anchor every review to it)

List every **paid surface** the codebase touches. For each: where it's called, the unit
cost driver, and the guard in front of it. Example shape:

| Surface | Where | Unit cost / knob | Guard |
|---|---|---|---|
| External search/data API | `clients/foo.py` | per-query HTTP; rate plan | concurrency cap, cache |
| Maps/Places/Geocoding | `tools/places.py` | per billed call; field-mask SKU tiers | budget cap, cross-run cache |
| LLM provider | `model_factory.py` | per-token in+out; **model tier** | tier choice, prompt cache |
| Embeddings | vector paths | per-embed | cache per immutable key |
| Email/SMS | `jobs/email.py` | per-send | idempotency column |
| Cloud Tasks / Run / job runtime | `dispatcher.py` | per-invocation + wall-clock; retries multiply | claim guard, dispatch deadline |

## The multiplier rule

Before judging any new call, compute where it sits in the fan-out. Sketch the tree:

```
request/run
  └─ per item (N)
       └─ per worker/parallel branch (K)
            └─ per sub-item (M)
                 └─ the paid call        ← unit cost × N × K × M
frontend: per user × per view × per surface
```

- A call added **per item** with no cache is the classic regression: "what bounds the
  loop, and is there a cache/budget cap/short-circuit in front of it?"
- A frontend fetch in a render/`useEffect` path runs **per user per view** — recurring
  spend. A shared query-cache layer exists to dedupe these; a raw fetch effect bypasses it.
- A retry/back-off without an idempotency or claim guard multiplies the whole chain.

## Review procedure

1. **Get the diff** (`git diff <base>...HEAD`) and read every hunk — don't sample.
2. **Flag cost-touching lines** — grep for the tells:
   ```bash
   git diff <base>...HEAD | grep -nE \
     'httpx|requests\.|aiohttp|fetch\(|axios|geocode|places|search|embed|LlmAgent|model=|generate_content|invoke|send_email|enqueue|dispatch|for .* in |while |useEffect|setInterval|poll'
   ```
   Also: removed `cache`/`limit`/`max_calls` guards, widened API field masks, new agents,
   new deps that imply a provider.
3. **For each flagged call answer four questions:**
   - **Unit** — which paid surface, cost of one call?
   - **Multiplier** — how many times per run / request / view? (use the fan-out map)
   - **Guard** — is there a cache-read, budget cap, idempotency key, claim gate, or
     short-circuit in front of it? A *removed/bypassed* guard is the finding.
   - **Tier** — for LLM calls, is the model tier right? A cheap job promoted to a frontier
     model is a silent 10–30× token jump.
4. **Check known invariants weren't regressed** — caches still front the paid calls,
   budget caps intact, idempotency/claim gates intact, frontend fetches go through the
   shared cache, no new unbounded poll.
5. **Quantify concretely** — "+1 API call per item ⇒ up to +N/run, cache-warm runs
   unaffected" beats "might cost more".
6. **Measure, don't predict** — if you have per-run cost counters (a trace, structured
   log, or billing export), diff them before/after on a representative input.

## Output template

```
COST VERDICT: <none | low | medium | high | blocker>

New/changed paid calls:
- <surface> — <unit> × <multiplier> = <expected delta>, guard: <cache/budget/none>

Regressions found:
- <file:line> — <guard removed/bypassed and the resulting multiplier>

Recommendations:
- <add cache / restore budget cap / lower model tier / batch / dedupe fetch>

Verify: <counters/test to run>
```

If nothing paid is touched: `COST VERDICT: none — change touches no paid surface or fan-out.`

## Don'ts

- Don't approve on unit cost alone — locate the multiplier.
- Don't accept "it's cached" without finding the cache read in the diff's call path.
- Don't ignore the frontend — a per-view re-fetch is recurring spend.
- Don't wave through model-tier changes — token price varies >10× across tiers.
- Don't skip measurement when real counters are available.
