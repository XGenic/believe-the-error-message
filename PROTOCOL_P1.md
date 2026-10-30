# C4 study P1: does the give-up effect depend on the exact wording of the error? (frozen before any P1 live call)

Status: **frozen**. This file, `configs/live_p1_*.json`, the `configs/mock_p1_*.json` and `configs/power_p1_weak.json` scripted agents, `causetest/p1.py`, the P1 wiring in `causetest/runner.py`, the `claim_texts` option in `causetest/mocks.py` and the tests were committed before any P1 live call, the pilots included. Changes after a P1 live call must be logged in `NOTEBOOK.md` under "Deviations".

## Question

The paper's cleanest result is the give-up effect. Over a transient fault that a later call would clear, the message "ERROR: stock data for this depot is unavailable." lowered success by 64 points on average against the neutral "ERROR: request rejected.", across 15 model-and-setting arms. Every study so far used exactly these two sentences. An outside review of the paper (shared by the owner, 2026-10-30) pointed out that the effect is therefore established for one sentence, not for the wider class of messages that state the same cause.

**P1 asks: does the give-up effect hold when the same cause is stated in other words?** One primary question, per subject: does each rewording of "unavailable" still lower success against the neutral message?

## Design

Every cell has the C4 transient fault: the first two calls of each request fail, whatever they send, and any later call works. The system prompt is C4's, unchanged. Only the text of the error differs:

| Family | Wording | Error text | Kind |
|---|---|---|---|
| "unavailable" | `original` | ERROR: stock data for this depot is unavailable. | C4 |
| | `on_record` | ERROR: this depot has no stock data on record. | another sentence, the same cause |
| | `not_available` | ERROR: stock information is not available for this depot. | a close rewording |
| | `code_404` | ERROR 404: no stock data found for this depot. | a status-code style |
| neutral | `original` | ERROR: request rejected. | C4 |
| | `not_completed` | ERROR: the request could not be completed. | another neutral sentence |

The texts are fixed in `causetest/p1.py`. Like C4's, they state a cause, or none, and give no instruction; a test checks this.

**Cells:** 6 (four "unavailable" wordings and two neutral ones, all over the transient fault) × 30 runs = 180 runs per subject, each of 6 requests.

**Seeds: new ones,** 20262201 + r (pilot 20262921).

**Subjects:** four, from three developers. Each has its settings and host copied unchanged from its C4-grid config (a test checks this), and each showed a give-up effect with the original sentence:

| Subject | C4-grid config | Original give-up effect (success: "unavailable" / neutral) |
|---|---|---|
| GPT-6.1 Sol, native calls, reasoning `low` | `live_w2d_c4_sol_low` | 0.00 / 1.00 |
| GPT-6-luna, native calls, reasoning `low` | `live_n1_c4_native_low` | 0.03 / 0.49 |
| Claude Haiku 5.5, native tool use, thinking on | `live_w2c_c4_haiku_t1` | 0.00 / 0.47 |
| DeepSeek V4.1 Flash, reasoning on, DeepInfra fp8 | `live_or_c4_deepseek_v4_1_flash_r1` | 0.02 / 1.00 |

Two subjects have a full-size effect and two a moderate one. Haiku with thinking off is left out: it gave up after any error, so no wording can show an effect on it.

## Measures

Success is the share of requests in which a lookup returned the figure, per run, averaged over runs. Intervals are 95% percentile bootstraps over runs (2,000 resamples), unpaired, as in every C4 study.

| Measure | Definition |
|---|---|
| Effect of a wording | success under that "unavailable" wording minus success under the original neutral message |
| Rewording minus original | success under a rewording minus success under the original "unavailable" sentence |
| Effect against the second neutral sentence | success under an "unavailable" wording minus success under `not_completed` |
| Neutral check | success under `not_completed` minus success under the original neutral message |

## Decision rule (per subject)

**INVALID** under C4's validity rules, or if any effect cannot be estimated.

Each difference gets study N1's label: SAME if |Δ| < 0.15 and the interval lies within ±0.25; DIFFERENT if |Δ| ≥ 0.15 and the interval excludes 0; otherwise UNCLEAR. A wording **lowers success** if its effect is DIFFERENT and negative.

**The verdict, in order:**

1. **NOT_TESTABLE** if the original sentence does not lower success: there is no effect to generalize.
2. **GENERALIZES** if all three rewordings lower success.
3. **SPECIFIC** if none of them does.
4. **PARTIAL** otherwise.

**Study-level answer,** over the subjects that are VALID and testable (at least three are needed): the give-up effect **generalizes across these wordings** if every one of them is GENERALIZES; it is **wording-specific** if most are SPECIFIC; it is **mixed** otherwise.

**Secondary** (labels only, no verdict): each rewording minus the original sentence; each effect against the second neutral sentence; and the neutral check.

No correction for multiple comparisons is applied. The labels use fixed bars, not significance tests, and only the primary question is primary.

## Predictions (recorded before any P1 call; not part of the decision rule)

- **Primary: GENERALIZES on all four subjects.** Each rewording states the same cause plainly, and the subjects acted on "unavailable" in every earlier study.
- **Size:** each rewording is SAME as the original sentence in at least 10 of the 12 rewording-and-subject pairs.
- **Neutral check:** the second neutral sentence is SAME as the first on at least three of the four subjects.
- **If any rewording falls short, it is `not_available`,** the only one that reads as a statement about access rather than about the data.

## Instrument validation (MOCK, not evidence)

`python -m causetest validate --configs configs/mock_*.json` runs all 50 scripted agents. The five P1 ones run at the planned size, with 10% random first responses:

| Scripted agent | Primary verdict |
|---|---|
| generalizes (reads every rewording as "unavailable") | GENERALIZES ✓ |
| keyword (reads only the original sentence as "unavailable"; rewordings as neutral) | SPECIFIC ✓ |
| partial (reads only `on_record` as "unavailable", besides the original) | PARTIAL ✓ |
| message-blind | NOT_TESTABLE ✓ |
| non-engager | INVALID ✓ |

**Power** (20 disjoint seed sets at 30 runs per cell; `runs/validation/power.json`):

| Scripted agent | Primary verdicts over 20 replications |
|---|---|
| generalizes | GENERALIZES 20/20 |
| keyword | SPECIFIC 20/20 |
| partial | PARTIAL 20/20 |
| weak (generalizes, but follows the message in only 60% of requests; effects about −0.55; `configs/power_p1_weak.json`) | GENERALIZES 20/20 |

## Procedure

1. **Freeze** (this commit): protocol, configs at a $0 cap, code, scripted agents and tests.
2. **Approval:** the owner's approval and the caps, in a separate commit, before any call.
3. **Public registration, before any call:** the frozen files are pushed to the public repository and published as a GitHub release (`p1-protocol`), and the owner registers the same files on OSF. No pilot runs before both exist.
4. **Pilots:** one run per cell on the pilot seed, for each subject, and the W2 health gate: every run complete, protocol failures of 10% or less, the tool called on request 1 in at least 90% of runs, and the estimate within the cap.
5. **Main runs,** each only after its pilot passes the gate, within its cap. A subject whose pilot fails the gate, or whose estimate exceeds its cap, is not run and is reported. The OpenAI runs must finish before that credit lapses on 2026-11-09.
6. A run INVALID on completion through transport failures gets the W2-4 re-run (completed runs from the cache), logged as a deviation.

## Budget

Each estimate is the subject's measured cost per run in its C4-grid run: the give-up trap's for the four "unavailable" wordings, and the neutral transient cell's for the two neutral ones. Each cap covers that subject's pilot and main run.

| Subject | Paid from | Estimate | Proposed cap |
|---|---|---|---|
| GPT-6.1 Sol | OpenAI API credit (about $20.84 left; lapses 2026-11-09) | $3.79 | $5.50 |
| GPT-6-luna | the same credit | $0.22 | $0.60 |
| Claude Haiku 5.5, thinking on | the owner's Anthropic API key | $0.22 | $0.60 |
| DeepSeek V4.1 Flash, reasoning on | OpenRouter credit | $0.17 | $0.60 |
| **Total** | | **$4.40** | **$7.30** |

The configs are at $0 in this commit.

## Known limits

- **Three rewordings of one cause, and one other neutral sentence,** all in English. They are a sample of plausible wordings, not of the messages real systems send.
- **The "temporary" message is not reworded.** Its effect on the retry trap is small (12 points on average), and most of that trap comes from agents not exploring other spellings, not from the wording (paper §4.1).
- **Four subjects,** chosen because each showed the effect with the original sentence. P1 tests whether an effect that exists generalizes across wordings; it does not test models without it.
- **One environment,** with C4's task and transient fault.
