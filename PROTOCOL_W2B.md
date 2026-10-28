# C4 study W2-B: the bounded caution on the open-weight panel (frozen before any W2-B live call)

Status: **frozen**. This file, `configs/live_w2b_*.json`, the `configs/mock_w2b_*.json` mocks and the tests were committed before any W2-B live call, the pilots included. Changes after a W2-B live call must be logged in `README.md` under "Deviations".

## Question

E3 found, on GPT-6-luna only, that a caution with a stopping rule rescues the give-up trap at about the minimum cost:

> Error messages from the stock system do not always state the true cause of a failure. If the same error keeps coming back after a few different attempts, accept it.

This is the paper's main practical recommendation. **Does it work on other models?** W2-B runs E3's design on every open-weight arm of the W2-A panel.

## Design

E3 ([`PROTOCOL_E3.md`](PROTOCOL_E3.md)) with one change: only three arms.

- `control`;
- `caution`, the plain caution and the reference for the cost saving;
- `caution_bounded` ("…after a few different attempts, accept it").

`caution_three` is dropped. On Luna it produced only identical retries, and it is not the recommended wording.

**Cells:** the retry trap, the accurate "temporary", the give-up trap and the accurate "unavailable". 3 arms × 4 cells = 12 cells × 30 runs = 360 runs per subject.

**Seeds:** E3's (20261501 + r; pilot seed 20269501), so every model sees the same worlds as Luna's E3 run.

**Subjects:** each W2-A arm, with settings and pinned host copied unchanged from its C4 config (a test checks this):

| Subject | Host | Estimate | Proposed cap |
|---|---|---|---|
| DeepSeek V4.1 Flash, r0 | DeepInfra fp8 | $0.35 | $1.00 |
| DeepSeek V4.1 Flash, r1 | DeepInfra fp8 | $0.70 | $2.00 |
| gpt-oss-120b, r1 | Crusoe bf16 | $0.51 | $1.50 |
| Qwen3.8-27B, r0 | DeepInfra bf16 | $2.21 | $6.50 |
| Qwen3.8-27B, r1 | DeepInfra bf16 | $2.88 | $8.50 |

Each estimate is that arm's billed C4 cost per run, plus 20% for the cautions' extra calls.

**Procedure:** as W2-A.

1. A pilot, and the W2 health gate.
2. Main runs in order of cost, cheapest first, each only if 1.5× its estimate fits within the remaining OpenRouter credit, less $1.
3. **A subject that fails the gate is not run, and is reported to the owner.**

## Measures and decision rule

These are E3's, unchanged (`causetest/e3.py`). For `caution_bounded`, per subject:

| Measure | Definition |
|---|---|
| Give-up rescue | success on the give-up trap, minus control |
| Outage saving | calls on the true outage, minus the plain caution |
| Harm check | success on the true "temporary", minus control |

**Verdicts:** HARMS_TRUE_TEMPORARY, COST_AWARE, RESCUE_ONLY, LOSES_RESCUE or NO_GAIN, by E3's rule. **INVALID** under C4's validity rules.

The plain caution's own contrasts against control are reported as secondary results, as in E3.

## Predictions (recorded before any W2-B call; not part of the decision rule)

- **COST_AWARE for at least 3 of the 5 subjects.**
- **The give-up rescue is weakest for gpt-oss-120b,** the model that took "unavailable" at its word even after an error had cleared (E5 D1 +0.25). RESCUE_ONLY or LOSES_RESCUE is plausible there.
- **No HARMS_TRUE_TEMPORARY.**
- **DeepSeek r1, which already loosens the retry trap at 16%,** gains the most on the retry trap from the bounded caution.

## Instrument validation (MOCK, not evidence)

The three-arm design is checked with E3's scripted behaviors, at the planned size:

| Scripted agent | `caution_bounded` verdict |
|---|---|
| bounded | COST_AWARE ✓ |
| unbounded | RESCUE_ONLY ✓ |
| deaf | NO_GAIN ✓ |

E3's power analysis (`runs/validation/power.json`) applies, since the decision rule and the size are E3's.

## Budget

- **Estimates:** about $6.65 for the main runs, plus about $0.20 for the pilots.
- **Credit:** $13.40 of OpenRouter credit on 2026-10-24.
- **Caps:** the configs are at $0 in this commit. The owner approves the caps before any call; they are recorded in the README.

## Known limits

- **One wording** of the bounded caution (W6 covers this).
- **Each subject ran on one host.**
- **The `caution_three` contrast is not repeated.**
