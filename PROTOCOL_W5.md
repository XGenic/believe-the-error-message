# C4 study W5: does reasoning effort change the traps? (frozen before any W5 live call)

Status: **frozen**. This file, `configs/live_w5_*.json` and the tests were committed before any W5 live call, the pilots included. Changes after a W5 live call must be logged in `README.md` under "Deviations".

W5 is workstream W5 of [`PAPER_PLAN.md`](PAPER_PLAN.md). It runs under the owner's delegation of 2026-10-27, which covers Luna runs on the OpenAI key (see the README).

## Question

GPT-6-luna has so far run at reasoning effort `low` (C4–E5 in the text format, N1-A and N1-B through native calls) and `none` (N1-C). A reviewer will ask whether the traps are a symptom of too little thinking. Two facts make the question sharper:

- **At `low`, Luna hardly reasons in this task.** Across N1-A's 8,862 calls it used 1.3 reasoning tokens per call on average (W6: 0.4). So N1-C (`none`) against N1-A (`low`) was not a test of reasoning.
- **On the open-weight panel, reasoning changed details** (W2-A): it loosened DeepSeek's retry trap (16% solved), but neither trap disappeared.

**Question: does Luna, made to reason (`medium`, `high`), still fall into both traps, and is its first-encounter effect (E5) unchanged?**

## Design

Luna through native tool calls (transport `openai_responses_native`), exactly as N1, at several reasoning efforts. Every design element, seed and decision rule is N1's.

| Run | Design | Reasoning | Output-token limit | Seeds (pilot) |
|---|---|---|---|---|
| `w5-c4-low` | the C4 grid, 12 cells × 30 runs | `low` | 2,000 | 20261201 + r (20269201) |
| `w5-c4-medium` | the C4 grid | `medium` | 8,000 | the same |
| `w5-c4-high` | the C4 grid | `high` | 8,000 | the same |
| `w5-e5-none` | E5, 3 primes × 60 runs | `none`, temperature 1.0 | 2,000 | 20261701 + r (20269701) |
| `w5-e5-low` | E5 | `low` | 2,000 | the same |
| `w5-e5-medium` | E5 | `medium` | 8,000 | the same |
| `w5-e5-high` | E5 | `high` | 8,000 | the same |

- **The `low` runs repeat N1-A and N1-B** on the same seeds, in the same week as the new efforts. Every comparison of effort is therefore made between runs of the same days, and the repeats also measure drift since N1 (2026-10-20).
- **The seeds are N1's,** so every effort sees the same worlds.
- **The output-token limit is raised to 8,000 at `medium` and `high`,** because reasoning tokens count against it. At `low` the limit never bound: the longest output in N1-A was 191 tokens. A reply that reaches its limit is counted (descriptive, below); it stays in the analysis as whatever the episode scores it as.
- `none` keeps N1-C's temperature 1.0. The other efforts set no temperature, as N1-A.

## Comparisons (`python -m causetest compare`, N1's rule, unchanged)

Δ = A − B, with a 95% percentile bootstrap interval (2,000 resamples, seed 20261801). **SAME** if |Δ| < 0.15 and the interval lies within ±0.25; **DIFFERENT** if |Δ| ≥ 0.15 and the interval excludes 0; **UNCLEAR** otherwise. Overall: SAME if every primary measure is SAME, DIFFERENT if any is DIFFERENT, UNCLEAR otherwise.

Primary measures as N1: on the C4 grid, S, retry-trap success and give-up-trap success; for E5, D1.

| Comparison | Role |
|---|---|
| **`w5-c4-high` − `w5-c4-low`** | **primary** (the one primary question of W5) |
| `w5-c4-medium` − `w5-c4-low` | secondary |
| `w5-e5-high` − `w5-e5-low`, `w5-e5-medium` − `w5-e5-low`, `w5-e5-none` − `w5-e5-low` | secondary |
| `w5-c4-low` − N1-A, `w5-e5-low` − N1-B | drift checks |

Each run also gets its own pre-registered verdict from the C4 or E5 decision rule.

**Reading of the primary:**

- **SAME:** making Luna reason does not change the traps or steering. The traps are not a symptom of too little thinking.
- **DIFFERENT:** reasoning changes at least one primary measure. Which one, and in which direction, is the finding.
- **If a drift check is DIFFERENT,** the model or its serving changed since N1. The W5 comparisons stay valid, because they are made between runs of the same days, but N1's numbers are then reported as dated.

**Descriptive:** reasoning tokens per call by effort; the share of replies that reach the output-token limit; calls per request in each trap.

No correction for multiple comparisons is applied. There is one primary comparison; the rest are secondary and reported with their intervals.

## Procedure

As N1 and W6:

1. **Pilots:** one run per cell on the development seed, for each of the seven runs. The W2 health gate applies to each: every run complete, protocol failures of 10% or less, the tool called on request 1 in at least 90% of runs, and the estimate within the cap.
2. **Main runs,** cheapest first. A run that fails its gate is not run, and is reported to the owner.
3. A run that is INVALID on completion through transport failures gets the W2-4 re-run (same config, completed runs from the cache), logged as a deviation.

## Predictions (recorded before any W5 call; not part of the decision rule)

- **Primary: high − low is not SAME, through the retry trap.** At `high`, Luna will sometimes vary the SKU after a "temporary" error that keeps recurring (retry-trap success 0.15–0.40, against about 0 at `low`), as DeepSeek did with reasoning. **S and the give-up trap SAME.** Low-to-moderate confidence.
- **The give-up trap holds at every effort** (success under 0.10): "unavailable" ends the request before any reasoning about the cause is needed.
- **E5: D1 SAME at every effort,** with the first-encounter effect CONFIRMED in each run.
- **Medium lies between low and high.**
- **Drift checks SAME.**

## Validation

W5 adds no code. It reuses N1's native transport, the C4 and E5 decision rules, and `causetest/compare.py`, all already tested. A new test (`TestStudyW5`) checks that every W5 config keeps N1's transport, model, cells, seeds, thresholds and prices, changes only the reasoning effort (and the output limit, and `none`'s temperature as N1-C), is gated, and cannot be cut short by its call cap.

## Budget

API-equivalent, at the third-party prices of N1 (input $0.10, output $0.50 per million tokens). The cost is driven by input (about 1,000 tokens per call); reasoning adds output.

| Run | Calls (N1) | Estimate | Cap |
|---|---|---|---|
| `w5-c4-low` | ~8,900 | $1.00 | $2.50 |
| `w5-c4-medium` | ~8,900 | ~$2 (if ~200 reasoning tokens per call) | $6.00 |
| `w5-c4-high` | ~8,900 | ~$4 (if ~700) | $12.00 |
| `w5-e5-none` | ~2,100 | $0.15 | $0.50 |
| `w5-e5-low` | ~2,100 | $0.16 | $0.50 |
| `w5-e5-medium` | ~2,100 | ~$0.40 | $1.50 |
| `w5-e5-high` | ~2,100 | ~$1.00 | $3.00 |
| **Total** | | **about $9** | **$26** |

The reasoning-token figures are guesses; the pilots replace them with measured costs. A pilot whose estimate exceeds its cap stops that run (the gate), and is reported to the owner.

## Known limits

- **One model.** An Anthropic model with extended thinking is part of the plan's W5, but it is a frontier-model run and outside the owner's delegation.
- **Reasoning summaries are not collected,** so W5 cannot say what Luna reasons about. The plan's trace coding needs a model that exposes its reasoning.
- **Reasoning items are not passed back between calls** (as in N1). A production agent might keep them, which could change how reasoning accumulates over a request.
- **The output-token limit differs between `low` and the higher efforts.** It did not bind at `low`; replies that reach it at `medium` or `high` are reported.
