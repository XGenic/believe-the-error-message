# C4 study R1: does the stopping rule depend on how long faults take to clear? (frozen before any R1 live call)

Status: **frozen**. This file, `configs/live_r1_*.json`, the `configs/mock_r1_*.json` and `configs/power_r1_weak.json` scripted agents, `causetest/r1.py`, the two arms' text in `causetest/e2.py`, the R1 wiring in `causetest/runner.py`, the `bound_claims` option in `causetest/mocks.py` and the tests were committed before any R1 live call, the pilots included. Changes after an R1 live call must be logged in `NOTEBOOK.md` under "Deviations".

## Question

The paper recommends a two-sentence instruction: "Error messages from the stock system do not always state the true cause of a failure. If the same error comes back on three attempts in a row, accept it." It was RECOMMENDABLE on 8 of 8 subject arms (W6, W2-C, W2-D). Three things limit that result:

1. **The count matches the environment by construction.** In every study so far the transient fault cleared on the third call, so "three attempts" named exactly the count that recovers it.
2. **It has not been compared with a retry policy written in code,** the obvious alternative for anyone who controls the tool's client.
3. **The rule was always tested after the caution sentence,** never alone.

R1 draws the recovery time per request and adds two arms: the rule without the caution, and the same count retried in code. It asks:

- **Q1 (primary): when recovery times vary, does the instruction do as well as the same count written in code?**
- **Q2: does the rule need the caution?**
- **Q3 (descriptive): what does each arm gain and lose against no instruction, by recovery time? Do agents keep to the count when it is wrong?**

## Design

**Recovery times.** A transient fault fails the request's first k calls that reach the stock system, whatever they send, and clears on call k + 1. In every earlier study k = 2. In R1, k is 1, 2, 3 or 4, set per request: each run of 6 requests has every value once, plus two drawn at random, in an order drawn from the world seed alone (`causetest/r1.py`, `schedule_for`). Every arm and cell of a run therefore meets the same recovery times. A strict count of three recovers the requests with k ≤ 2: 86 of the 180 requests per cell on the main seeds (0.48).

**Arms.** The agent-facing text is fixed in `causetest/e2.py`:

| Arm | Instructions ("Errors" section) | The tool's client | Source |
|---|---|---|---|
| `control` | none | sends each call once | C4 |
| `caution` | "Error messages from the stock system do not always state the true cause of a failure." | once | E2; persistence without a count |
| `caution_three` | the caution, then "If the same error comes back on three attempts in a row, accept it." | once | E3, W6: **the recommended instruction** |
| `three_only` | "If the same error comes back on three attempts in a row, accept it." | once | **new:** the rule without the caution |
| `code_retry` | none (the control text, word for word) | **resends a failed call unchanged, up to three attempts in all; the agent sees only the last result** | **new:** the same count, written in code |

The code retry is the simplest policy: it retries every failure at once, whatever the message says. Its retries are invisible to the agent and do not count against the 6 tool calls the instructions allow; they are counted as calls to the stock system.

**Cells:** the accurate "temporary" (a true transient fault), the give-up trap ("unavailable" over a transient fault) and the accurate "unavailable" (a true outage). The retry trap is left out: W6 showed that the count does nothing for it, and no R1 arm targets it. 5 arms × 3 cells = 15 cells × 30 runs = 450 runs per subject, each of 6 requests.

**Seeds: new ones,** 20262101 + r (pilot 20262911).

**Subjects:** four, chosen for how they responded in W6, each with its settings and host copied unchanged from its W6 config (a test checks this):

| Subject | W6 config | In W6: caution alone / "three in a row" (give-up rescue) | Without instruction, after "temporary" |
|---|---|---|---|
| GPT-6.1 Sol, native calls, reasoning `low` | `live_w2d_w6_sol_low` | +1.00 / +1.00 | retried until it worked |
| GPT-6-luna, native calls, reasoning `low` | `live_w6_gpt6luna_native_low` | +0.98 / +1.00 | retried until it worked |
| Claude Haiku 5.5, native tool use, thinking off | `live_w2c_w6_haiku_t0` | 0.00 / +0.97 | gave up (30% solved) |
| DeepSeek V4.1 Flash, reasoning off, DeepInfra fp8 | `live_w6_deepseek_v4_1_flash_r0` | +0.18 / +0.98 | retried until it worked |

Two subjects follow the caution alone and two do not, so Q2 is tested where the caution matters and where it does not.

## Measures

Calls are counted **at the stock system**: an agent's call is one call, and the code retry's own retries are added. Success is the share of requests answered with the figure, per run, averaged over runs.

| Measure | Definition |
|---|---|
| Give-up-trap success | success in the give-up trap |
| True-"temporary" success | success in the accurate "temporary" cell |
| Outage calls | calls per request on a true outage ("unavailable" over a permanent fault) |

Intervals are 95% percentile bootstraps over runs (2,000 resamples), unpaired, as in every C4 study.

## Decision rule (per subject)

**INVALID** under C4's validity rules, or if the primary contrast cannot be estimated.

**Primary: the instruction (`caution_three`) minus the code retry (`code_retry`),** on the three measures. Each difference gets a fixed label:

- **Success measures:** study N1's rule. SAME if |Δ| < 0.15 and the interval lies within ±0.25; DIFFERENT if |Δ| ≥ 0.15 and the interval excludes 0; otherwise UNCLEAR.
- **Outage calls:** the same rule on a scale of calls. SAME if |Δ| < 0.5 and the interval lies within ±1.0; DIFFERENT if |Δ| ≥ 0.5 and the interval excludes 0; otherwise UNCLEAR. Half a call is W6's margin above the 3-call floor (3.5).

**The verdict, in order:**

1. **WORSE_THAN_CODE** if either success measure is DIFFERENT and negative. A loss of real successes comes first, as W6's harm check does.
2. **COSTLIER_THAN_CODE** if outage calls are DIFFERENT and higher.
3. **MATCHES_CODE** if all three labels are SAME.
4. **BETTER_THAN_CODE** if a success measure is DIFFERENT and positive, or outage calls are DIFFERENT and lower.
5. **UNCLEAR** otherwise.

**Study-level answer to Q1,** over the subjects that are VALID (at least three are needed):

- the instruction **can stand in for code** if it is MATCHES_CODE or BETTER_THAN_CODE on all but at most one;
- **code is preferable** if it is WORSE_THAN_CODE or COSTLIER_THAN_CODE on all but at most one;
- **mixed** otherwise.

**Secondary:**

- **Q2:** the rule alone (`three_only`) minus the instruction, on the three measures, with the same labels.
- **Each arm against control,** with W6's measures (give-up rescue, outage calls, true-"temporary" change) and W6's verdict. W6's verdict is reported for reference only: its bars were set for a fault that always cleared on the third call, and a strict count of three can now rescue at most about half of the give-up trap.
- **Q3 (descriptive), by recovery time k:** success, calls, and the share of requests that went past three calls, per arm, in the give-up trap and the accurate "temporary".

No correction for multiple comparisons is applied. The labels use fixed bars, not significance tests, and only Q1 is primary.

## Predictions (recorded before any R1 call; not part of the decision rule)

- **Q1: WORSE_THAN_CODE on at least three of the four subjects, through the true "temporary"**, so code is preferable. Told to accept an error that comes back three times, agents will also stop on true "temporary" faults that clear on the fourth or fifth call. A control agent behind the code retry keeps going on those.
- **The give-up trap is SAME for the instruction and the code retry on at least three of the four:** both recover about the requests that clear within three calls (0.48).
- **Q2: the rule alone is SAME as the instruction on the give-up trap on at least three of the four.** The count does the work. On Haiku and DeepSeek the caution alone rescued little in W6.
- **Q3: agents keep to the count when it is wrong.** Under `caution_three`, on every subject, at most 20% of give-up-trap requests whose fault needs four or five calls go past three calls.
- **The plain caution rescues more of the give-up trap than the instruction on Sol and Luna,** because it has no count to stop at, and costs more calls on a true outage.

## Instrument validation (MOCK, not evidence)

`python -m causetest validate --configs configs/mock_*.json` runs all 45 scripted agents. The five R1 ones run at the planned size, with 10% random first responses:

| Scripted agent | Primary verdict |
|---|---|
| counts (stops at 3 calls after every error under a stopping rule) | WORSE_THAN_CODE ✓ (true "temporary" −0.54) |
| matches (stops at 3 only after "unavailable"; retries "temporary" on) | MATCHES_CODE ✓ |
| unbounded (follows the caution; ignores the count) | COSTLIER_THAN_CODE ✓ (give-up trap +0.49, outage calls +1.51) |
| deaf (ignores every instruction) | WORSE_THAN_CODE ✓ (give-up trap −0.44) |
| non-engager | INVALID ✓ |

**Power** (20 disjoint seed sets at 30 runs per cell; `runs/validation/power.json`):

| Scripted agent | Primary verdicts over 20 replications |
|---|---|
| counts | WORSE_THAN_CODE 20/20 |
| matches | MATCHES_CODE 15/20, BETTER_THAN_CODE 5/20 |
| unbounded | COSTLIER_THAN_CODE 20/20 |
| weak (counts, but keeps to the count in 65% of requests; `configs/power_r1_weak.json`) | WORSE_THAN_CODE 20/20 |

The "matches" agent splits because of its random first responses: behind the code retry, each extra call after "unavailable" costs three calls at the stock system, so its code arm spends about 0.46 more calls on a true outage, at the 0.5 threshold. This is real retry amplification, not an artifact of the rule, and it is reported as such if it appears in a live run.

## Procedure

1. **Freeze** (this commit): protocol, configs at a $0 cap, code, scripted agents and tests.
2. **Approval:** the owner's approval and the caps, in a separate commit, before any call.
3. **Public registration, before any call:** the frozen files are pushed to the public repository and published as a GitHub release (`r1-protocol`), and the owner registers the same files on OSF. No pilot runs before both exist.
4. **Pilots:** one run per cell on the pilot seed, for each subject, and the W2 health gate: every run complete, protocol failures of 10% or less, the tool called on request 1 in at least 90% of runs, and the estimate within the cap.
5. **Main runs,** each only after its pilot passes the gate, within its cap. A subject whose pilot fails the gate, or whose estimate exceeds its cap, is not run and is reported. The OpenAI runs must finish before the credit lapses on 2026-11-09; if the credit cannot cover both, Luna runs first.
6. A run INVALID on completion through transport failures gets the W2-4 re-run (completed runs from the cache), logged as a deviation.

## Budget

Estimates come from each subject's measured cost per run in its W6 run, cell by cell: control's cost for `code_retry`, and `caution_three`'s for `three_only`. Cells with a transient fault are scaled by 1.25 for the longer recoveries. Each cap covers that subject's pilot and main run.

| Subject | Paid from | Estimate | Proposed cap |
|---|---|---|---|
| GPT-6.1 Sol | OpenAI API credit (the owner's Pro plan; lapses 2026-11-09) | $13.90 | $18.00 |
| GPT-6-luna | the same credit | $1.19 | $2.50 |
| Claude Haiku 5.5 | the owner's Anthropic API key | $0.53 | $1.00 |
| DeepSeek V4.1 Flash | OpenRouter credit | $0.37 | $1.00 |
| **Total** | | **$15.99** | **$22.50** |

The configs are at $0 in this commit.

## Known limits

- **One count (three) and one spread of recovery times** (1–4 failed calls). A different spread would move every success figure. It would not change Q1's comparison, because the instruction and the code retry use the same count.
- **The code retry is the simplest policy.** Real clients retry only some errors, wait and back off between attempts, and cap total time. Time is not modelled here.
- **Four subjects,** chosen to span W6's behaviours, not sampled from the models available. Sol and Luna run at reasoning `low` only.
- **The retry trap is not tested.**
- **One environment,** with the faults and messages of C4. The stated causes are still chosen to mislead in the give-up trap.
