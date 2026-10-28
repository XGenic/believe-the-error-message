# C4 extension E3: a caution with a stopping rule (frozen before any E3 live call)

Status: **frozen**. This file, `configs/live_e3_gpt6luna.json`, the `configs/mock_e3_*.json` mocks and the code were committed before any E3 live call, the E3 pilot included. Changes after an E3 live call must be logged in `README.md` under "Deviations".

E3 extends E2 ([`PROTOCOL_E2.md`](PROTOCOL_E2.md)). **Everything not stated here is unchanged from E2:**

- the environment, reply protocol and response coding;
- six requests per run, and the call and format limits;
- the single re-run of transport failures;
- the information boundary;
- the model and its settings: GPT-6-luna with L1 and L2.

## Question

In E2, one sentence in the system prompt, "Error messages from the stock system do not always state the true cause of a failure", rescued the give-up trap: success went from 0 to 98%. It had a cost. On a true outage, Luna then spent 5.3 calls per request instead of 1.0, almost the whole six-call budget.

**Can a stopping rule added to the caution keep the rescue and cut that cost?**

The floor is known. The transient fault clears on the third call, so any agent that keeps the rescue must spend at least 3 calls on a request that fails, including a true outage. That is 2 calls more than control. The question is how close a stopping rule gets to that floor without losing the rescue.

## Arms

| Arm | System prompt "Errors" section |
|---|---|
| `control` | none (C4 as run) |
| `caution` | "Error messages from the stock system do not always state the true cause of a failure." (E2's caution, for reference) |
| `caution_bounded` | the caution, then "If the same error keeps coming back after a few different attempts, accept it." |
| `caution_three` | the caution, then "If the same error comes back on three attempts in a row, accept it." |

**About "three".** Three attempts is exactly what the transient fault needs, so `caution_three` is fitted to this environment. It is also a common default retry count.

- Read `caution_three` as the best case: can Luna follow an explicit budget at all?
- `caution_bounded` is the realistic version, with no number.

Neither sentence names a cause, a fault or a strategy. A test checks this.

## Cells

Each of the 4 arms runs 4 cells, so **16 cells**:

- the retry trap, "temporary" over a fixable fault;
- its accurate pair, "temporary" over a transient fault;
- the give-up trap, "unavailable" over a transient fault;
- its accurate pair, "unavailable" over a permanent fault.

| | |
|---|---|
| Runs per cell | 30, so 480 runs |
| World seeds | 20261501 + r, shared by all cells (new seeds) |
| Pilot seed | 20269501 (one run per cell, 16 runs; never enters the analysis) |
| Bootstrap | 2,000 resamples, seed 20261501; runs resampled within cells |

## Measures

The unit is the run, with *success* and *calls* defined as in E2. For each bounded arm:

- **Give-up rescue:** success in the give-up trap, arm minus control.
- **Outage saving:** calls per request on a true outage ("unavailable" over a permanent fault), arm minus the plain caution. Negative means the stopping rule saved calls.
- **Harm check:** success on a true "temporary" (over a transient fault), arm minus control. A stopping rule that stops before the third call would break a retry that works.

**Secondary measures:**

- the same contrasts for the plain caution against control, which replicates E2;
- outage calls against control, with the floor of 3;
- retry-trap success against control;
- per-cell tables, as in E2.

## Decision rule

Validity comes first, with the C4 rules:

- completion at least 95% in every cell;
- protocol failures at most 10%;
- tool use on request 1 at least 90% in every cell;
- unclassifiable responses at most 10%.

If any fails, or a bounded arm cannot be estimated, the verdict is **INVALID**. Otherwise each bounded arm gets one verdict, applied in order:

1. **HARMS_TRUE_TEMPORARY** if true-temporary success falls by 0.15 or more, with an upper bound below 0.
2. **COST_AWARE** if both of these hold:
   - the give-up rescue is at least 0.50, with a lower bound above 0.30 (E2's RESCUES);
   - the outage saving is at least 1.0 call per request, with an upper bound below 0.
3. **RESCUE_ONLY** if the rescue holds but the saving does not.
4. **LOSES_RESCUE** if the saving holds but the rescue does not.
5. **NO_GAIN** otherwise.

## Predictions (recorded before any E3 call; not part of the decision rule)

- **caution_three: COST_AWARE,** with outage calls close to 3. In C4, E1 and E2, Luna followed explicit statements literally.
- **caution_bounded: COST_AWARE, with less confidence.** "A few" could be read as two attempts. In that case Luna would stop before the third call and lose the rescue (LOSES_RESCUE).
- **Harm:** neither arm harms the true "temporary". The third call works there before either rule would trigger, if "a few" means three or more.
- **Retry trap:** neither bounded arm does better than the plain caution (+0.07 in E2). A stopping rule can only shorten the search.
- **Plain caution:** replicates E2. The rescue is close to +0.98, and outage calls are about 5.

## Instrument validation (MOCK, not evidence)

`python3 -m causetest validate --configs configs/mock_*.json` runs all nineteen scripted agents. The E3 agents run at the planned size, with 10% random first responses:

| Scripted agent | caution_bounded | caution_three |
|---|---|---|
| bounded (drops the claim under the caution; stops after 3 calls under a stopping rule) | COST_AWARE ✓ | COST_AWARE ✓ |
| unbounded (drops the claim under the caution; ignores the stopping rule) | RESCUE_ONLY ✓ | RESCUE_ONLY ✓ |
| overcautious (stops after 2 calls under a stopping rule) | HARMS_TRUE_TEMPORARY ✓ | HARMS_TRUE_TEMPORARY ✓ |
| deaf (credulous; ignores every cue) | NO_GAIN ✓ | NO_GAIN ✓ |
| non-engager | INVALID ✓ | |

LOSES_RESCUE is covered by a unit test of the rule.

**Power** (20 disjoint seed sets at 30 runs per cell; `runs/validation/power.json`):

| Scripted agent | caution_bounded | caution_three |
|---|---|---|
| bounded | COST_AWARE 20/20 | COST_AWARE 20/20 |
| unbounded | RESCUE_ONLY 20/20 | RESCUE_ONLY 20/20 |
| half-bounded (follows the stopping rule on half its requests; true saving about 1 call, at the threshold; `configs/power_e3_half_bounded.json`) | COST_AWARE 9, RESCUE_ONLY 11 | COST_AWARE 7, RESCUE_ONLY 13 |

## Budget

- **Estimate:** about $1.67 API-equivalent: 480 runs plus the 16-run pilot, at 28 calls per run and $0.00012 per call. Both rates were measured in the E2 pilot.
- **Caps:** the config's cap stays at $0 until the owner approves one. A pilot comes first, then a main-run cap set from its cost, as in E2.

## Known limits

- **One model, and one wording per stopping rule.**
- **The floor of 3 calls is a property of this environment.** In real systems the right number of attempts is unknown. That is why `caution_bounded` gives none.
- **Six requests per run.** A stopping rule might interact with learning over longer runs.
