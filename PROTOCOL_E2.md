# C4 extension E2: what breaks the traps? (frozen before any E2 live call)

Status: **frozen**. This file, `configs/live_e2_gpt6luna.json`, the `configs/mock_e2_*.json` mocks and the code were committed before any E2 live call, the E2 pilot included. Changes after an E2 live call must be logged in `README.md` under "Deviations".

E2 extends the C4 kill test ([`PROTOCOL.md`](PROTOCOL.md)). **Everything not stated here is unchanged from C4:**

- the environment, the reply protocol and response coding;
- the six requests per run, and the call and format limits;
- the single re-run of transport failures;
- the information boundary.

The model is GPT-6-luna with the settings of the Luna C4 and E1 runs: deviations L1 (history cut) and L2 (reasoning effort `low`, no temperature). See the README.

## Question

C4 and E1 found two traps on Haiku 5.5 and GPT-6-luna, and neither model learned its way out over 18 requests:

- **The retry trap.** A false "temporary service problem" over a fixable fault (a SKU spelling convention). The agent retries the identical call until the limit and never respells. Luna: 0 of 180 requests solved.
- **The give-up trap.** A false "stock data for this depot is unavailable" over a transient fault (the third call works). The agent stops after one call, so it never collects the evidence that would correct it. Luna: 0 of 180.

**Does one added sentence break either trap, and does it matter where the sentence goes?** The sentence can go in the agent's instructions or in the error message.

## Arms

| Arm | What changes | Exact text |
|---|---|---|
| `control` | nothing; C4 as run | (none) |
| `caution` | the system prompt gains an "Errors" section | "Error messages from the stock system do not always state the true cause of a failure." |
| `caution_strategy` | the same section, with a strategy | the caution sentence, then "If an approach keeps failing, try a different one." |
| `mixed` | the error message keeps its stated cause and adds a generic instruction, as real services often do | the cause text + " Check the request and try again." |
| `honest` | the error message states no cause | "ERROR: the cause of this failure is unknown." |

**Placement.** The system-prompt section sits between the tool description and the depot directory. Arms without a note use exactly the kill test's system prompt; a test checks this.

**Information boundary.** No arm's text names the experiment, the fault, the claim or any cell; a test checks this. The caution says only that messages *can* be wrong, never which message or when.

## Cells

Cells are (arm, claim, fault). The honest arm has no claim; its cells use the label `unknown`.

| Arm | Cells | Count |
|---|---|---|
| control | retry trap (`transient\|fixable`), its accurate pair (`transient\|transient`), give-up trap (`permanent\|transient`), its accurate pair (`permanent\|permanent`), and the neutral message over the fixable and the transient fault | 6 |
| caution, caution_strategy, mixed | the two traps and their accurate pairs | 4 each |
| honest | `unknown` over the fixable, transient and permanent faults | 3 |

That makes **21 cells**.

- In the honest arm, `unknown|fixable` stands in for the retry trap and `unknown|transient` for the give-up trap.
- `unknown|transient` also stands in for the accurate "temporary" cell, and `unknown|permanent` for the accurate "unavailable" cell.

**Size and seeds:**

| | |
|---|---|
| Runs per cell | 30, so 630 runs |
| World seeds | 20261401 + r, shared by all cells. These are new seeds, so the control arm is an out-of-sample replication of the Luna traps. |
| Pilot seed | 20269401 (one run per cell, 21 runs; never enters the analysis) |
| Bootstrap | 2,000 resamples, seed 20261401; runs resampled within cells |

## Measures

**Unit:** the run. For each run, *success* is the share of its six requests answered with the figure. *Calls* is its mean number of tool calls per request.

**Primary, per arm and trap:** Δ = mean success in the arm's trap cell minus mean success in the control trap cell. That gives eight contrasts: four arms × two traps.

**Cost, per arm.** An intervention that breaks a trap could also make the agent worse when the message is true:

- **Δ success in the accurate "temporary" cell** (arm minus control). A drop means the sentence talked the agent out of a retry that would have worked.
- **Δ calls per request in the accurate "unavailable" cell** (arm minus control). A rise means calls wasted on a real outage.

**Secondary measures:**

- the honest message minus the neutral "request rejected", over the fixable and the transient fault: does saying "the cause is unknown" beat saying nothing?
- per cell: success by request, calls per request, requests reaching a third call, runs that ever reformat, and the first response on request 1;
- validity counts, as in C4.

## Decision rule

The thresholds are in the config. Validity comes first:

**INVALID** (the whole run) if any of these hold:

- completion below 95% in any cell, after the one re-run;
- protocol failures above 10% of turns;
- tool use on request 1 below 90% in any cell;
- unclassifiable responses above 10%;
- any trap contrast that cannot be estimated.

Otherwise the run is **VALID**, and each of the eight trap contrasts gets one verdict, applied in order:

1. **RESCUES** if Δ ≥ 0.50 and its lower 95% bound > 0.30.
2. **HELPS** if Δ ≥ 0.15 and its lower bound > 0.
3. **HARMS** if Δ ≤ −0.15 and its upper bound < 0.
4. **NO_EFFECT** if |Δ| < 0.10 and the interval lies within (−0.20, 0.20).
5. **INCONCLUSIVE** otherwise.

**Cost flags,** per arm, reported next to its verdicts:

- the accurate "temporary" cell's success falls by 0.15 or more, with an upper bound below 0;
- the accurate "unavailable" cell's calls per request rise by 1.0 or more, with a lower bound above 0.

## Predictions (recorded before any E2 call; not part of the decision rule)

These come from the Luna C4 and E1 results, where Luna did literally what each stated cause implied:

- **honest:** helps both traps, more on the give-up trap. Under the neutral message Luna solved 67% of transient-fault requests but only 21% of fixable-fault ones, because its default first move is to rewrite the depot, not the SKU. So **HELPS** on the retry trap, **HELPS or RESCUES** on the give-up trap.
- **mixed:** "try again" pushes toward retries. So it helps the give-up trap (a third call works) and adds little to the retry trap, where retrying is the trap. So **HELPS** on the give-up trap, and **NO_EFFECT or HELPS** on the retry trap.
- **caution:** an abstract warning with no strategy. **NO_EFFECT or HELPS** on both.
- **caution_strategy:** **HELPS or RESCUES** on both, with a cost flag for calls wasted on real outages.

## Instrument validation (MOCK, not evidence)

`python3 -m causetest validate --configs configs/mock_*.json` runs all fourteen scripted agents: C4's six, E1's four and E2's four. The E2 agents run at the planned size, with 10% random first responses:

| Scripted agent | caution | caution_strategy | mixed | honest | Cost flags |
|---|---|---|---|---|---|
| deaf (credulous; ignores every cue) | NO_EFFECT ✓ | NO_EFFECT ✓ | NO_EFFECT ✓ | RESCUES ✓ (no claim to follow) | honest ✓ |
| prompt-responsive (drops the claim with p 0.35 under caution, p 1 under the strategy) | HELPS ✓ | RESCUES ✓ | NO_EFFECT ✓ | RESCUES ✓ | caution, caution_strategy, honest ✓ |
| instruction-follower (drops the claim when the message says to check and try again) | NO_EFFECT ✓ | NO_EFFECT ✓ | RESCUES ✓ | RESCUES ✓ | mixed, honest ✓ |
| non-engager | INVALID ✓ | | | | |

Each verdict holds on both traps. When an agent drops the claim, it runs the message-blind approach: respell, then retry once, then stop. That approach wastes calls on a real outage, which is why those arms raise the cost flag.

**Power** (20 disjoint seed sets at 30 runs per cell; `runs/validation/power.json`):

| Scripted agent | Verdicts over 20 replications |
|---|---|
| deaf | every contrast 20/20 as expected |
| prompt-responsive | every contrast 20/20 as expected |
| weak cues (p 0.2 caution and instruction, p 0.5 strategy; `configs/power_e2_weak_cues.json`) | caution HELPS 19/20 and 17/20; mixed HELPS 18/20 and 19/20; caution_strategy HELPS 13–14/20, RESCUES 6–7/20; honest RESCUES 20/20 |

An effect of about 0.2 is detected as HELPS 85–95% of the time. An effect close to 0.5 splits between HELPS and RESCUES, as it should at that threshold.

## Budget

- **Estimate:** about $1.86 API-equivalent: 630 runs plus the 21-run pilot, at 26 calls per run and the measured $0.00011 per call.
- **Pilot first:** one run per cell on the pilot seed. It measures cost and protocol health; its data never enter the analysis.
- **Caps:** the config's cap stays at $0 until the owner approves one. The proposal is $0.25 for the pilot, then a main-run cap set from the pilot's measured cost.

## Known limits

- **One model,** with light reasoning (L2). The interventions might act differently on a model without reasoning; Haiku 5.5 would be the natural check.
- **One wording per intervention.** A different caution or instruction could work better or worse. E2 asks whether *this kind* of sentence moves the traps, not which wording is best.
- **Six requests per run.** A caution might work through learning across requests rather than at once. Success by request is reported, but runs are short.
- **Cost is measured narrowly:** success in one accurate cell and calls in another. Real deployments pay other costs, such as latency and user confusion.
- **The honest arm changes the message, not the agent.** It shows what a service could do, not what an agent can do on its own.
