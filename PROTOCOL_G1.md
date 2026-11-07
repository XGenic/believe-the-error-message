# C4 study G1: is Gemini's give-up result about reasoning or about the model? (frozen before any G1 live call)

Status: **frozen**. This file, `configs/live_g1_*.json`, `causetest/g1.py`, the G1 wiring in `causetest/runner.py` and `causetest/__main__.py`, the `reasoning_tokens` option in `causetest/mocks.py` and the tests were committed before any G1 live call, the pilots included. Changes after a G1 live call must be logged in `NOTEBOOK.md` under "Deviations".

Sonnet is paid for by the owner personally, on the owner's Anthropic account. Gemini is paid for from OpenRouter credit.

## Question

In W2-E, Gemini 3.8 Flash at its default solved 61% of the give-up trap. No other arm passed 14%, and the prediction was at most 15%. W2-E ran one setting per model, so it cannot say why. Gemini is also the only arm that reasons much on the trap's first request, the request that decides most runs:

| Give-up trap, request 1 (from finished runs) | Reasoning tokens: mean | Third call made | Requests solved |
|---|---|---|---|
| Gemini 3.8 Flash, medium (its default) | 686 | 18 of 30 runs | 61% |
| Qwen3.8-27B, reasoning on | 88 | 1 of 30 | 6% |
| DeepSeek V4.1 Flash, reasoning on | 72 | 2 of 30 | 2% |
| Claude Haiku 5.5, thinking on | 71 | 0 of 30 | 0% |
| Claude Sonnet 5.5, default | 61 | 2 of 30 | 7% |
| gpt-oss-120b | 49 | 0 of 30 | 3% |
| Every other arm | at most 58 | at most 1 of 30 | at most 14% |

So reasoning and the model cannot be told apart. **G1 asks which one it is,** by changing reasoning in both directions.

## Design

Two new runs, each compared with the W2-E run of the same model:

| Arm | Model and setting | Reasoning on request 1 | Cells | Runs | Compared with |
|---|---|---|---|---|---|
| Sonnet | `claude-sonnet-5-5`, adaptive thinking, effort `max` | about Gemini's (mean 734 in the cost probe) | give-up trap | 30 | W2-E Sonnet, effort `high` |
| Gemini | `google/gemini-3.8-flash`, reasoning `low`, flex tier | about half of its default (median 341 against 741 in the cost probes) | give-up trap, and "request rejected" over the same fault | 30 per cell | W2-E Gemini, reasoning `medium`, flex tier |

**Each arm answers a different half of the question.** Sonnet at `max` puts about Gemini's reasoning into another model, which is the stronger test: reasoning rises more than tenfold on a model that solved 7%. Gemini at `low` is the weaker test, because it cannot go lower: reasoning cannot be turned off, and at `low` it still reasons several times as much as any other arm. So Gemini at `low` still solving the trap would not clear reasoning on its own.

Seeds (20261201 + r, pilot 20269201), the error texts, the instructions and the validity thresholds are C4's, so each new run meets the same worlds as the run it is compared with. A test checks this. On Gemini, the output limit (16,000 tokens), host and tier match W2-E's, and only the reasoning effort differs. On Sonnet, the output limit also rises from W2-E's 8,000 tokens to 16,000, because effort `max` can reason at length (2,691 tokens in one probe call). There is no server-side fallback on Sonnet. Both runs use 5 workers, not 10, so that the spend guard's reserve fits under the small caps. That does not change what a model sees.

Gemini gets the "request rejected" cell because a lower setting might reduce persistence in general, as it did on GPT-6-luna (W5), and not only under "unavailable". Sonnet does not: it solved 100% there at its default, and the cell would more than double its cost.

## Cost probes and earlier data read before this protocol

G1 follows up a result already seen, and its comparison runs are W2-E's. All of W2-E's raw data had been read, including the table above. Before this protocol was written, the cost probes for both new settings had also been read for token use and cost (`runs/probe/PROBE.md`): Sonnet at `max` and Gemini at `low` on flex, three accurate cells only, on development seeds G1 does not use. **No G1 setting has run on the give-up trap or on "request rejected".**

## Decision rules

Measure: requests solved in the give-up trap, per run. New run minus W2-E run, with a 95% percentile bootstrap over runs (2,000 resamples, seed 20262401), labelled by N1's rule: SAME if |Δ| < 0.15 and the interval lies within ±0.25; DIFFERENT if |Δ| ≥ 0.15 and the interval excludes 0; UNCLEAR otherwise. `PANEL_MAX` is 0.15, just above the highest give-up-trap success on any arm but Gemini (0.144).

**First, did reasoning move?** On the trap's request 1, mean reasoning tokens per run:

- Sonnet at `max` must reach at least half of W2-E Gemini's mean.
- Gemini at `low` must be at most three quarters of W2-E Gemini's mean.

An arm that fails its check is NOT_TESTABLE.

**Then each arm:**

| Arm | Result | Rule |
|---|---|---|
| Sonnet | RISES | DIFFERENT and higher |
| Sonnet | STAYS | Δ below +0.15, and success at or below `PANEL_MAX` |
| Gemini | FALLS | DIFFERENT and lower |
| Gemini | HOLDS | not FALLS, and the interval for success lies above `PANEL_MAX` |
| Either | UNCLEAR | anything else |

**Primary, the study's verdict:**

| Sonnet | Gemini | Verdict | Reading |
|---|---|---|---|
| RISES | any | **REASONING_MATTERS** | About Gemini's reasoning also lets another model escape the trap |
| STAYS | HOLDS | **GEMINI_ITSELF** | The same reasoning is not enough on Sonnet, and less of it does not remove the result on Gemini |
| STAYS | FALLS | **GEMINI_SPECIFIC** | Reasoning matters on Gemini, but the same amount is not enough on Sonnet |
| anything else | | **UNCLEAR** | |

The verdict is INVALID if a new run fails the C4 validity rules (at least 95% of runs complete in every cell, at most 10% protocol failures, the tool called on request 1 in at least 90% of runs, at most 10% unclassifiable responses).

**Secondary, descriptive:** the third call and solved-after-a-solved-request counts for each run; Gemini under "request rejected" at each setting (N1's label), and the message's effect at each setting; reasoning per call.

**Power,** by simulation with this rule at 30 runs per arm, each run a single draw because runs are close to all-or-nothing, against W2-E's observed rates. The rule was also run through the harness on scripted agents with set reasoning, which reached each verdict and NOT_TESTABLE (see the tests).

| Sonnet's true rate at `max` | RISES | STAYS | UNCLEAR | | Gemini's true rate at `low` | FALLS | HOLDS |
|---|---|---|---|---|---|---|---|
| 0.07 | 0% | 95% | 5% | | 0.60 | 0% | 100% |
| 0.15 | 5% | 49% | 46% | | 0.45 | 12% | 88% |
| 0.25 | 48% | 8% | 44% | | 0.30 | 67% | 33% |
| 0.40 | 95% | 0% | 5% | | 0.15 | 99% | 1% |

A modest true change on Sonnet, around 0.15–0.25, will often be UNCLEAR. G1 is sized to tell a large effect from none, and it does not add runs if the answer is UNCLEAR.

## Procedure

1. **Freeze:** protocol, configs at a $0 cap, code, tests.
2. **Approval:** the owner's approval and the caps, in a separate commit, before any call.
3. **Public registration, before any G1 call:** the frozen files are pushed to the public repository and published as a GitHub release (`g1-protocol`), and the owner registers the same files on OSF. No pilot runs before both exist.
4. **Pilots:** one run per cell on the development seed, for each config. The W2 health gate applies: every run complete, protocol failures of 10% or less, the tool called on request 1 in at least 90% of runs, and the estimate within the cap.
5. **Main runs,** each only after its pilot passes the gate, at about the same time. A run whose pilot estimate exceeds its cap is not run, and is reported. Money left under one run's cap can move to the other only on the owner's word, logged as a deviation.
6. **Analysis:** each run gets `analyze`, then `python -m causetest g1` gives the study's verdict.

## Predictions (recorded before any G1 call; not part of the decision rule)

- **Primary: GEMINI_ITSELF.**
- **Sonnet at `max` STAYS,** solving at most 15% of the trap. More reasoning effort has moved this trap little where it has been tried (GPT-6-luna from 3% to at most 14%), though no arm but Gemini has reasoned this much.
- **Gemini at `low` HOLDS,** solving at least 35% of the trap.
- **Reasoning moves as intended on both arms.**
- **Gemini under "request rejected" stays at 90% or above at `low`.**
- **Cost:** each main run falls within its estimate below.

W2-E's predictions held 1 of 6, so these are weak.

## Budget

**Approved by the owner on 2026-11-07: $4.25 in all, pilots included: $3.00 for Sonnet and $1.25 for Gemini.** Each cap covers that config's pilot and main run. OpenRouter holds $1.66, which covers Gemini's cap.

Estimates are W2-E's measured cost per run in these cells, scaled by the cost probes' cost per call. The upper figure allows for W2-E's overruns and for reasoning understated in accurate cells. Prices, read 2026-11-06: Sonnet $2 in, $2.50 cache write, $0.10 cache read, $10 out per million tokens (Anthropic's pricing page). Gemini on flex $0.375 in, $0.0375 cache read, $1.875 out (OpenRouter's listing; recorded cost is OpenRouter's billed figure).

| Config | Runs | Estimate | Cap |
|---|---|---|---|
| Sonnet, effort `max` | 30 | $1.03–1.50 | $3.00 |
| Gemini, reasoning `low` | 60 | $0.71–1.00 | $1.25 |
| **Total** | 90 | **$1.74–2.50** | **$4.25** |

The caps sit above the estimates because the spend guard holds back each worker's worst-case call ($0.18 for Sonnet, $0.035 for Gemini; 5 workers).

## Known limits

- **A follow-up to a surprise.** The question comes from W2-E's data, and the comparison runs are that same data. If 61% was high partly by chance, Gemini at `low` could fall for that reason alone. G1 does not repeat Gemini at `medium`.
- **One other model.** Sonnet staying low would show that this much reasoning is not enough on Sonnet, not on every model.
- **An effort setting is not only a token count.** A setting may change more than how long a model reasons, so even REASONING_MATTERS would not show that reasoning length is the cause.
- **Gemini's manipulation is modest,** about half its default, and it never reaches the other arms' low level.
- **The give-up trap only.** G1 says nothing about the retry trap or E5 at these settings.
- **Runs a day or so apart.** The new runs follow W2-E's by about a day, on a hosted model that could change behind the same name.
