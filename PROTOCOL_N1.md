# C4 study N1: does native tool calling change the results? (frozen before any N1 live call)

Status: **frozen**. This file, `configs/live_n1_*.json`, `causetest/compare.py`, the native transport and its tests were committed before any N1 live call, the N1 pilots included. Changes after an N1 live call must be logged in `README.md` under "Deviations".

N1 is workstream W1 of [`PAPER_PLAN.md`](PAPER_PLAN.md).

## Question

Every C4 run so far had the agent write its tool calls as a text line, `CALL stock_lookup {...}`. Deployed agents call tools through the provider's function-calling API instead. The text format also forced two Luna-only deviations:

- **L1:** the conversation history kept each reply only up to its first CALL or ANSWER line.
- **L2:** reasoning effort `low`, because with reasoning off Luna could not follow the format.

**Questions:**

1. **Are the C4 and E5 results the same when the agent calls the tool natively?**
2. **With native calls, does Luna run with reasoning off, and does that change anything?** This is secondary.

## What changes, and what does not

**Changes.** Transport `openai_responses_native`:

- The model gets a `stock_lookup` function with string arguments `site` and `sku`, in strict mode. Parallel calls are off.
- Its function call is passed to the unchanged episode as the line `CALL stock_lookup {...}`.
- The harness's next message goes back as that call's output: the tool result, or "No tool calls remain…".
- Text replies pass through as before.
- As in the text transport, reasoning items are not passed back.
- No history cut (L1) is needed: a native call never shares a reply with text.

**One sentence of the instructions changes.** The "How to reply" rule for tool calls becomes:

> - To use the tool, call stock_lookup. Make one call at a time; its result comes back to you.

It replaces the three-line CALL rule. A test checks that this is the only difference from the text prompt.

**Unchanged:** the environment, the error texts, the requests, the response coding, the limits, the seeds, every measure and decision rule of C4 and E5, and the model.

## Runs

| Study | Design | Transport | Reasoning | Seeds | Compared with |
|---|---|---|---|---|---|
| **N1-A** | the C4 grid: 12 cells × 30 runs | native | `low` | 20261201 + r (as C4) | `runs/live-gpt-6-luna` (text, `low`, L1) |
| **N1-B** | E5: 3 primes × 60 runs | native | `low` | 20261701 + r (as E5) | `runs/e5-live-gpt-6-luna` (text, `low`, L1) |
| **N1-C** | the C4 grid: 12 cells × 30 runs | native | `none`, temperature 1.0 | 20261201 + r | N1-A |

Each run also gets its own pre-registered verdict, from the C4 or E5 decision rule.

Each study has a one-run-per-cell pilot on its design's development seed; pilots never enter an analysis.

## Comparison (`python -m causetest compare`)

**Measure:** Δ = A − B, with a 95% percentile bootstrap interval. Runs are resampled within each cell of each run independently, with 2,000 resamples and seed 20261801.

**Verdict per measure:**

- **SAME:** |Δ| < 0.15 and the interval lies within (−0.25, +0.25).
- **DIFFERENT:** |Δ| ≥ 0.15 and the interval excludes 0.
- **UNCLEAR:** otherwise.

**Primary measures:**

- **C4 grid:** steering S, success in the retry trap ("temporary" over a fixable fault), and success in the give-up trap ("unavailable" over a transient fault).
- **E5:** D1, the share stopping at once after no error minus after a cleared error.

**Secondary measures:** L\*, success in every cell, and each prime's stop-at-once rate.

**Overall verdict per comparison:**

- **SAME** if every primary measure is SAME;
- **DIFFERENT** if any is DIFFERENT;
- **UNCLEAR** otherwise.

**Reading:**

- N1-A or N1-B **SAME** means the text format did not drive the Luna results, and L1 did not matter.
- **DIFFERENT** means the format matters. That would be a finding to report, and the native results would be the ones to carry forward.
- N1-C against N1-A isolates reasoning effort (none against low) under native calls. If N1-C is INVALID by C4's rules, that is reported as such.

## Predictions (recorded before any N1 call; not part of the decision rule)

- **N1-A: SAME.** Luna followed stated causes with S = +0.96 and solved 0 of 180 trap requests in the text format. I expect the same through native calls; S may fall slightly from its ceiling.
- **N1-B: SAME.** I expect D1 near +0.97 again.
- **N1-C: valid,** with protocol failures well under 10%. Native calls remove the format failures that blocked reasoning-off runs. **SAME against N1-A,** with low confidence: E2–E5 suggest the behavior comes from the message, not from reasoning.

## Validation

There are no scripted agents for a transport. Instead, unit tests check:

- the translation in both directions against a mocked API: a call becomes one CALL line; the next harness message becomes that call's output; an open call is closed before a new request; parallel calls are off;
- that the native prompt differs from the text prompt only in the call rule;
- that native configs are gated;
- the comparison rule's verdicts, and that a run compared with itself gives Δ = 0.

The comparison was also checked on existing data. Luna's C4 run compared with itself is SAME. Luna against Haiku is DIFFERENT on S (+0.61 [+0.57, +0.64]) and SAME on both traps, both of which solved 0.

## Budget

These are API-equivalent estimates at the measured Luna rates:

| Study | Estimate |
|---|---|
| N1-A | about $1.07 |
| N1-B | about $0.16 |
| N1-C | about $0.77; no reasoning tokens, so likely less |

The total is about $2.00, within the owner's phase-1 approval of under $5. The caps are recorded in the README in a separate commit, before any N1 call.

## Known limits

- **One model.** Haiku through native calls needs the Anthropic Messages API and an Anthropic key. That comes with the panel of models (W2).
- **The episode still scores the same CALL/ANSWER protocol.** Native calls are translated into it, so format errors can still occur in text replies, for example an answer without the ANSWER word.
- **Not passing reasoning items back** matches the text transport, but may not be how a production agent would run a reasoning model.
