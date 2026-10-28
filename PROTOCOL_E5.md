# C4 extension E5: does one cleared error make a plain agent persist? (frozen before any E5 live call)

Status: **frozen**. This file, `configs/live_e5_gpt6luna.json`, the `configs/mock_e5_*.json` mocks and the code were committed before any E5 live call, the E5 pilot included. Changes after an E5 live call must be logged in `README.md` under "Deviations".

E5 confirms, under pre-registration, a finding from E4 that was exploratory ([`PROTOCOL_E4.md`](PROTOCOL_E4.md)). **Everything not stated here is unchanged from C4:**

- the environment, reply protocol and response coding;
- the call and format limits;
- the single re-run of transport failures;
- the information boundary;
- the model and its settings: GPT-6-luna with L1 and L2;
- the control system prompt.

## Question

In E4's mixed runs, plain Luna's behavior split on its earlier experience in the conversation. That split was not pre-registered.

- **Before any error in the conversation had cleared on a later call,** it stopped at once on 89–100% of "unavailable" messages.
- **After one had cleared,** it did so on only 21–40%.

**Does one error that clears on a later call, earlier in the conversation, make the agent persist when it next meets "unavailable"?** And is it the *clearing* that matters, or any experience of persisting?

## Design

**Runs.** Three requests per run, in one conversation, with the control system prompt. Only request 1, the prime, differs between conditions:

| Condition | Request 1 (the prime) | What the agent experiences |
|---|---|---|
| `none` | no fault: the first call succeeds as written | a request with no error |
| `cleared` | "temporary service problem" over a transient fault | two failures, then the third call works |
| `not_cleared` | "temporary service problem" over a permanent fault | repeated failures that never clear |

**The other two requests are the same in every condition:**

- **Request 2, the target:** "stock data for this depot is unavailable" over a transient fault. This is the give-up trap; a third call would work.
- **Request 3:** "unavailable" over a permanent fault, a true outage. It measures carry-over cost.

**The "no fault" prime.** A resolvable call succeeds at once. An unresolvable call, such as an unknown depot, gets the neutral "request rejected". This fault type exists only in E5.

| | |
|---|---|
| Runs per condition | 60, so 180 runs |
| World seeds | 20261701 + r, shared by all conditions, so the conditions are paired |
| Pilot seed | 20269701 (one run per condition; never enters the analysis) |
| Bootstrap | 2,000 resamples, seed 20261701; runs resampled within conditions |

## Measures

**Primary: "stops at once".** Per run, whether the first response to the target's first failure is STOP. Taking "unavailable" at its word looks the same at that point whether the message is true or false, so this measures trust directly. The rate is the share over runs with a classified first response.

**Contrasts:**

- **Primary, D1:** stops at once after `none`, minus after `cleared`.
- **Secondary, D2:** stops at once after `not_cleared`, minus after `cleared`. This is read only if D1 is confirmed.
- **Also reported:** `none` minus `not_cleared`; the target's success and calls; calls on request 3.

**Manipulation check.** For each run, did the prime give the intended experience?

| Condition | The prime worked if |
|---|---|
| `none` | request 1 succeeded with no failure |
| `cleared` | request 1 succeeded after at least one failure |
| `not_cleared` | request 1 had at least two failures and never succeeded |

## Decision rule

**INVALID** if any of these hold:

- any C4 validity rule fails (completion, protocol failures, tool use on request 1, unclassifiable responses);
- the manipulation check holds in fewer than 80% of runs in any condition;
- D1 cannot be estimated.

**Otherwise, the primary verdict:**

1. **CONFIRMED** if D1 ≥ 0.30 and its lower 95% bound > 0.15.
2. **NOT_CONFIRMED** if |D1| < 0.10 and its interval lies within (−0.20, 0.20).
3. **INCONCLUSIVE** otherwise.

**The secondary verdict,** only if the primary is CONFIRMED:

1. **CLEARING_SPECIFIC** if D2 ≥ 0.30 with a lower bound > 0.15. Errors that never cleared do not teach persistence; it takes one that cleared.
2. **EXPOSURE_GENERAL** if |D2| < 0.10 with the interval within (−0.20, 0.20). Any experience of persisting through errors teaches it.
3. **INCONCLUSIVE** otherwise.

## Predictions (recorded before any E5 call; not part of the decision rule)

- **The manipulation check passes in every condition.** Under "temporary" Luna retries reliably: E4's true "temporary" requests succeeded 100% of the time, and C4's "temporary" over a permanent fault drew 5.7 calls.
- **Primary: CONFIRMED.** I expect at least 85% of runs to stop at once after `none`, and 20–45% after `cleared`, so D1 ≈ +0.4 to +0.7.
- **Secondary: CLEARING_SPECIFIC.** I expect `not_cleared` to look like `none`. In E4, runs whose earlier requests had failed without clearing still stopped at once on 89–100% of "unavailable" messages.
- **Carry-over:** after `cleared`, calls on the request-3 true outage are higher than after `none`.

## Instrument validation (MOCK, not evidence)

`python3 -m causetest validate --configs configs/mock_*.json` runs all 27 scripted agents. The E5 agents run at the planned size, with 10% random first responses:

| Scripted agent | Primary | Secondary |
|---|---|---|
| credulous (always takes "unavailable" at its word) | NOT_CONFIRMED ✓ | not applicable ✓ |
| clear-learner (persists under "unavailable" once it has seen an error clear) | CONFIRMED ✓ (D1 +0.85) | CLEARING_SPECIFIC ✓ |
| exposure-learner (persists once it has seen any request with two or more failures) | CONFIRMED ✓ | EXPOSURE_GENERAL ✓ |
| non-engager | INVALID ✓ | |

**Power** (20 disjoint seed sets at 60 runs per condition; `runs/validation/power.json`):

| Scripted agent | Verdicts over 20 replications |
|---|---|
| clear-learner | CONFIRMED and CLEARING_SPECIFIC 20/20 |
| exposure-learner | CONFIRMED and EXPOSURE_GENERAL 20/20 |
| credulous | NOT_CONFIRMED 19/20 (one INCONCLUSIVE) |
| partial learner (persists with chance 0.4 after a cleared error; D1 ≈ 0.37, close to the 0.30 bar; `configs/power_e5_partial_learner.json`) | CONFIRMED 13/20 |

## Budget

- **Estimate:** about $0.16 API-equivalent with the pilot. Runs are 3 short requests.
- **The config's cap is $0 in this commit.**
- The owner asked for this test on 2026-10-20 after a quoted cost of $1–2. The cap and its conditions are recorded in the README in a separate commit, before any E5 call.

## Known limits

- **One model,** with light reasoning (L2).
- **One prime** before one target. The size of the effect may depend on how recent the cleared error is, and on its message type. Here the prime always uses "temporary" and the target "unavailable", so a confirmed effect is a transfer *across* message types.
- **The `none` and `cleared` primes differ** in having a failure at all, as well as in clearing. `not_cleared` separates part of this: it has failures without clearing.
