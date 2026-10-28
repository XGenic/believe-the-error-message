# C4 study H1: does tool withdrawal carry over to a tool that works? (frozen before any H1 live call)

Status: **frozen**. This file, `configs/live_h1_*.json`, the `configs/mock_h1_*.json` mocks and the code were committed before any H1 live call, the H1 pilots included. Changes after an H1 live call must be logged in `README.md` under "Deviations".

## Question

In W2-A (deviation W2-7), gpt-oss-120b increasingly answered requests without calling the tool at all. By request 6, 124 of its 360 C4 runs did so. Luna, Qwen and DeepSeek almost never did (at most 1 such answer on requests 4–6, against gpt-oss's 268).

Not calling a tool that keeps failing can be sensible. **H1 asks whether the withdrawal carries over once the tool works again.** That is the behavioral signature of learned helplessness that C3 tested with Seligman's triadic design. The design here borrows that logic inside the C4 environment:

- **Primary:** does uncontrollable failure lead to withdrawal from a tool that now works?
- **Secondary:** does it matter whether the failures were controllable, with the same message shown?

"Helplessness" and "withdrawal" name behavioral patterns only.

## Design

Each run is 12 requests in one conversation. The first 8 form a **training block**, set by the condition. The last 4 form a **test block**, which is the same for every condition: no fault, so every resolvable call works. An unresolvable call, such as an unknown depot, gets the neutral "request rejected".

| Condition | Training block (requests 1–8) | What the agent learns |
|---|---|---|
| `no_failure` | no fault | the tool works |
| `controllable` | the **format** message over a **fixable** fault | the tool fails, but respelling fixes it. In C4, gpt-oss solved 77–90% of these requests. |
| `uncontrollable` | the **same format** message over a **permanent** fault | the tool fails whatever the agent does |
| `uncontrollable_temporary` | "temporary service problem" over a permanent fault | the same, under the message that drew the most withdrawal in W2-7 |

- **The key contrast.** `controllable` and `uncontrollable` show the agent exactly the same error text; only whether its actions can succeed differs.
- **Unlike C3, failure counts are not yoked.** The number of failed calls in training is reported for each condition.

**Subjects:**

- **gpt-oss-120b,** reasoning `low`, through OpenRouter with native calls, pinned to Crusoe bf16, exactly as in the W2-7 run (`configs/live_h1_gpt_oss_120b.json`).
- **GPT-6-luna,** native calls, reasoning `low`, as in N1-A (`configs/live_h1_gpt6luna.json`). Luna is a reference model: it showed no withdrawal in C4.

**Size and seeds:**

- 30 runs per condition, so 120 runs per model.
- World seeds 20261901 + r, shared by all conditions and both models.
- The pilot uses one run per condition on seed 20269901, and never enters an analysis.
- Bootstrap: 2,000 resamples, seed 20261901; runs resampled within conditions.

## Measures

The unit is the run. A **no-call request** is one answered without any tool call.

**Primary measure:** the no-call share of the 4 test-block requests.

- **Primary contrast, D_H:** `uncontrollable` minus `no_failure`.
- **Secondary contrast:** `uncontrollable` minus `controllable`.
- **Message contrast (descriptive):** `uncontrollable_temporary` minus `uncontrollable`.

**Also reported per condition:**

- test-block success;
- training success;
- failed calls in training;
- no-call share on the last 3 training requests;
- the no-call curve over all 12 requests.

## Decision rule (per model)

**INVALID** if any C4 validity rule fails (completion, protocol failures, tool use on request 1, unclassifiable responses), or if D_H cannot be estimated.

**Otherwise, the primary verdict on D_H:**

1. **CARRYOVER** if D_H ≥ 0.20 and its lower 95% bound > 0.10.
2. **NO_CARRYOVER** if |D_H| < 0.10 and its interval lies within (−0.20, 0.20).
3. **INCONCLUSIVE** otherwise.

**The secondary verdict,** only if the primary is CARRYOVER:

- **NOT_APPLICABLE_CONTROLLABLE_FAILED** if `controllable`'s training success is under 0.5, because then the condition was not in fact controllable;
- otherwise, the same thresholds applied to `uncontrollable` minus `controllable`:
  - **CONTROLLABILITY_MATTERS** if it meets the CARRYOVER bar;
  - **FAILURE_GENERAL** if it meets the NO_CARRYOVER bar;
  - **INCONCLUSIVE** otherwise.

## Predictions (recorded before any H1 call; not part of the decision rule)

- **gpt-oss-120b: CARRYOVER.** In W2-7, withdrawal grew with uncontrollable failure and reached a third of runs by request 6. I expect at least 30% of test-block requests answered without a call after `uncontrollable`, against under 5% after `no_failure`.
- **gpt-oss, secondary: CONTROLLABILITY_MATTERS,** with moderate confidence. In W2-7 the format message over a fixable fault drew the least withdrawal (14 of 270 late requests).
- **gpt-oss, message:** withdrawal is higher after `uncontrollable_temporary` than after `uncontrollable`.
- **Luna: NO_CARRYOVER.** Luna made 0 no-call answers on C4 requests 4–6.

## Instrument validation (MOCK, not evidence)

`python -m causetest validate --configs configs/mock_*.json` runs all 32 scripted agents. The H1 agents run at the planned size, with 10% random first responses:

| Scripted agent | Primary | Secondary |
|---|---|---|
| persistent (never withdraws) | NO_CARRYOVER ✓ | not applicable ✓ |
| helpless (withdraws, with chance 0.8, after 3 requests ended without the figure) | CARRYOVER ✓ | CONTROLLABILITY_MATTERS ✓ |
| failure-counter (withdraws after 12 failed calls of any kind, including fixed ones) | CARRYOVER ✓ | FAILURE_GENERAL ✓ |
| fatigue (withdraws after request 8 whatever happened) | NO_CARRYOVER ✓ | not applicable ✓ |
| non-engager | INVALID ✓ | |

**Power** (20 disjoint seed sets at 30 runs per condition; `runs/validation/power.json`):

| Scripted agent | Verdicts over 20 replications |
|---|---|
| helpless | CARRYOVER and CONTROLLABILITY_MATTERS 20/20 |
| weak helpless (withdraw chance 0.35; `configs/power_h1_weak_helpless.json`) | CARRYOVER and CONTROLLABILITY_MATTERS 20/20 |
| persistent | NO_CARRYOVER 20/20 |
| fatigue | NO_CARRYOVER 18/20 (2 INCONCLUSIVE) |

## Budget

**Estimates:** gpt-oss-120b about $0.37 (OpenRouter credit), Luna about $0.93 (OpenAI).

**Proposed caps, at about 3× the estimates:**

| Model | Pilot | Main run |
|---|---|---|
| gpt-oss-120b | $0.10 | $1.00 |
| GPT-6-luna | $0.15 | $2.50 |

Both configs are at $0 in this commit. The owner approves the caps before any call; they are recorded in the README in a separate commit. Each main run follows only after its pilot passes the W2 health gate.

## Known limits

- **Failure counts are not yoked.** `controllable` and `uncontrollable` may differ in how many failed calls the agent sees, so the secondary contrast mixes controllability with exposure. The counts are reported.
- **The test block shows no error at all.** A real recovery might involve errors that happen to clear, which E5 covers.
- **One host and one reasoning setting for gpt-oss.** In W2-6 the empty-ANSWER protocol failures varied by host.
