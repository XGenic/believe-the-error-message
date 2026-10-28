# C4 extension E1: longer runs (frozen before any E1 live call)

Status: **frozen**. This file, `configs/live_e1_claude_haiku.json`, the `configs/mock_e1_*.json` mocks and the code were committed before any E1 live call, the E1 pilot included. Changes after an E1 live call must be logged in `README.md` under "Deviations".

E1 extends the C4 kill test ([`PROTOCOL.md`](PROTOCOL.md)). **Everything not stated here is unchanged from C4:**

- the environment, system prompt, error texts, reply protocol and response coding;
- the transport and the CLI timeout of 480 s;
- the single re-run of transport failures;
- the information boundary.

## Question

The C4 kill test found Haiku 5.5 credulous: the stated cause set its recovery strategy, and learning was L\* = −0.004 [−0.058, +0.052] over six requests. **With three times the contrary evidence, does following a misleading stated cause fade (learning), stay put, or grow (entrenchment)?**

C4 also showed, without any pre-registered test, that stopping under "unavailable" *rose* over the six requests. This happened both when that claim was false (a transient fault) and when it was true (a permanent one). E1 therefore pre-registers entrenchment as an outcome.

## Design

**Requests per run:** 18, up from 6.

- The same three depots are each visited six times, in random order.
- Every request asks about a different item. Long-run worlds use a 24-item pool; the 6-request worlds are unchanged, and a test checks them against the kill test's saved worlds.

**Cells (4 of the 12):** C4's two headline effects and, for each, the accurate cell with the same claim.

| Claim | Misleading cell | Accurate cell (same claim) |
|---|---|---|
| "temporary service problem" (implies RETRY) | **transient \| fixable**: the retry trap. In C4: 0/180 success, identical retries every time. | transient \| transient |
| "stock data for this depot is unavailable" (implies STOP) | **permanent \| transient**: the give-up trap. In C4: 0/180, against 97% under the neutral message. | permanent \| permanent |

The neutral cells, the format-claim cells and the remaining misleading cells are not run. They carry little about learning, and the length of these runs makes each cell expensive.

**Size and seeds:**

| | |
|---|---|
| Runs per cell (planned) | 12, so 48 runs |
| World seeds | 20261301 + r, shared by all cells |
| Pilot seed | 20269301 |
| Bootstrap | 2,000 resamples, seed 20261301; runs resampled within cells |

**Cost and sizing (pre-registered).** In the Claude CLI, the per-call cost grows linearly with the turn's position in the conversation. C4 fit: about $0.00008 + $0.000131 × turn index. A run's cost therefore grows roughly with the square of its length. The 48-run design is projected at about $19.

- **Pilot.** One run per cell on the pilot seed, 4 runs. It measures the cost per run; its data never enter the verdict.
- **Sizing rule.** Runs per cell = min(12, ⌊($20 − pilot cost) / (4 × measured cost per run)⌋).
- **Cap.** One $22 API-equivalent cap covers the pilot and the run together. It is the same ceiling the owner approved for the C4 kill test.

## Measures

**Following.** Per cell and request, the follow rate is the share of classified first responses that equal the claim's implied strategy: RETRY for "temporary", STOP for "unavailable".

**Per-cell learning:** L = follow rate on requests 1–3 minus follow rate on requests 16–18.

**Primary: L_E1.** For each claim, L(misleading cell) − L(accurate cell); L_E1 is the mean over the two claims.

- Pairing by claim cancels drift that a claim causes whatever the truth is. Under "unavailable", for example, stopping rises in both cells.
- What remains is the extra change caused by contrary outcomes.
- **Positive L_E1** means the agent abandons a false claim more than a true one: learning.
- **Negative L_E1** means it holds a false claim tighter than a true one: entrenchment.

**Secondary measures, per cell:**

- the follow curve by request;
- success by request;
- calls by request;
- the first request at which each run deviates from the claim;
- the number of runs that ever reformat. In the retry trap, reformatting is the fix.
- the number of requests reaching a third call. In the give-up trap, the third call is the fix.

## Decision rule

Thresholds are in the config, judgment calls fixed here. Rules are applied in order:

1. **INVALID** if any of these hold:
   - completion below 95% in any cell, after the one re-run;
   - protocol failures above 10%;
   - tool use on request 1 below 90% in any cell;
   - unclassifiable responses above 10%;
   - L_E1 cannot be computed.
2. **LEARNS** if L_E1 is at least 0.15 and its lower 95% bound is above 0.
3. **ENTRENCHMENT** if L_E1 is at most −0.15 and its upper bound is below 0.
4. **NO_LEARNING** if |L_E1| is below 0.10 and its interval lies within (−0.20, 0.20).
5. **INCONCLUSIVE** otherwise.

## Instrument validation (MOCK, not evidence)

`python3 -m causetest validate --configs configs/mock_*.json` runs all eleven scripted agents: C4's seven and E1's four. The E1 agents run at the planned size (18 requests, 12 runs per cell), with 10% random first responses:

| Scripted agent | L_E1 | Verdict |
|---|---|---|
| credulous | −0.03 | NO_LEARNING ✓ |
| slow evidence learner (drops a claim after 6 failed requests) | +0.85 | LEARNS ✓ |
| entrencher (follows the claim more after each failed request) | −0.32 | ENTRENCHMENT ✓ |
| non-engager | n/a | INVALID ✓ |

**Power** (20 disjoint seed sets; `runs/validation/power.json`):

| Scripted agent | 8 runs per cell | 12 runs per cell |
|---|---|---|
| slow learner | LEARNS 20/20 | LEARNS 20/20 |
| credulous, 10% noise | NO_LEARNING 13/20 | 14/20 |
| entrencher, 10% noise | ENTRENCHMENT 11/20 | 14/20 |
| credulous, 3% noise (close to Haiku in C4, where 29–30 of 30 first responses per cell matched) | | NO_LEARNING 20/20 |
| entrencher, 3% noise | | ENTRENCHMENT 16/20 |

Learning is detected reliably even at 8 runs per cell. Telling no learning apart from entrenchment needs low response noise, which Haiku showed in C4.

## Known limits

- **Only two claims are tested,** with one misleading and one accurate cell each.
- **18 requests is still short** next to deployed agents with memory.
- **Learning is defined on the first response to a failure.** In the give-up trap, Haiku's first response in C4 was mostly RETRY and it stopped on the second. So entrenchment there may show more in calls per request than in L. Both are reported.
- **The cost of long CLI conversations limits the design** to four cells and up to 12 runs per cell.
