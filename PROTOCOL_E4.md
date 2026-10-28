# C4 extension E4: mixed accurate and misleading errors (frozen before any E4 live call)

Status: **frozen**. This file, `configs/live_e4_gpt6luna.json`, the `configs/mock_e4_*.json` mocks and the code were committed before any E4 live call, the E4 pilot included. Changes after an E4 live call must be logged in `README.md` under "Deviations".

E4 builds on E3 ([`PROTOCOL_E3.md`](PROTOCOL_E3.md)). **Everything not stated here is unchanged:**

- the environment, reply protocol and response coding;
- the call and format limits;
- the single re-run of transport failures;
- the information boundary;
- the model and its settings: GPT-6-luna with L1 and L2;
- the arms' agent-facing text.

## Question

E3 found that a caution with a stopping rule, "Error messages … do not always state the true cause … If the same error keeps coming back after a few different attempts, accept it", rescues the give-up trap at the floor cost of about 2 extra calls on a true outage. But every E3 run saw one message type, all true or all false. Real error messages are mostly accurate. Two questions follow:

1. **Does the bounded caution still work when most messages in a run are accurate?** That is: is the rescue kept, is the extra cost still near the floor, and is anything lost on accurate requests?
2. **Does the share of false messages change how often the agent follows them?** E1 tested learning when every message in a run was false. E4 tests it when evidence is mixed, as it would be in deployment.

## Design

**Runs.** Each run is 12 requests in one conversation: three depots, each visited four times; a 24-item pool; every request about a different item.

**Request types.** The stated cause and the true fault are set per request:

| Request type | Stated cause | True fault | Accurate? |
|---|---|---|---|
| true "unavailable" | unavailable | permanent | yes |
| give-up trap | unavailable | transient | no |
| true "temporary" | temporary | transient | yes |
| retry trap | temporary | fixable | no |
| true "format" | format | fixable | yes |

**Mixes.** Each message type appears 4 times in every run. The mix changes only how many of them are false:

| Mix | true "unavailable" | give-up trap | true "temporary" | retry trap | true "format" | Misleading share |
|---|---|---|---|---|---|---|
| `rare` | 3 | 1 | 3 | 1 | 4 | 2 of 12 (17%) |
| `common` | 2 | 2 | 2 | 2 | 4 | 4 of 12 (33%) |

**Order.** The order of requests is drawn from the seed and the mix alone, so both arms see identical runs. A test checks the counts and the reproducibility.

**Arms:**

- `control`: the C4 system prompt.
- `caution_bounded`: E3's bounded caution, word for word.

**Cells.** 2 arms × 2 mixes = **4 cells**.

| | |
|---|---|
| Runs per cell | 40, so 160 runs |
| World seeds | 20261601 + r |
| Pilot seed | 20269601 (one run per cell; never enters the analysis) |
| Bootstrap | 2,000 resamples, seed 20261601; runs resampled within cells |

## Measures

The unit is the run. For each run and request type, success is the share of those requests answered with the figure, and calls is their mean calls per request. The contrasts below are bounded caution minus control, within each mix.

**Primary measures:**

- **Give-up rescue:** success on give-up-trap requests.
- **Outage cost:** calls per request on true "unavailable" requests.

**Harm checks:**

- success on true "temporary" requests;
- success on true "format" requests. This is new in E4: a three-attempt habit could stop the spelling search before the right spelling. The original spelling plus three alternatives can need four calls.

**Net effect, reported without a verdict:**

- success and calls over all 12 requests;
- their ratio: extra calls per extra success, when the success gain exceeds 0.01.

**Adaptation (secondary, descriptive).** At a request's first failure, a true message and a false one look the same. So the share of first responses that follow the message is a measure of trust that does not depend on whether the message was true. "Following" means stopping after "unavailable", or an identical retry after "temporary". Per arm and message:

- **common minus rare:** does a higher share of false messages lower trust?
- **requests 7–12 minus requests 1–6, within each mix:** does trust drift over the run?

**Multiplicity.** There are 12 adaptation intervals, so one or two may exclude 0 by chance. In validation, a scripted agent that cannot adapt showed +0.07 on one of them. **Adaptation is reported as found only if |Δ| ≥ 0.15 and its interval excludes 0.**

## Decision rule

Validity uses the C4 rules (completion, protocol failures, tool use on request 1, unclassifiable responses), over all four cells. If any fails, or a mix cannot be estimated, the verdict is **INVALID**. Otherwise each mix gets one verdict for the bounded caution, applied in order:

1. **FADES** unless the give-up rescue is at least 0.50, with a lower bound above 0.30.
2. **HOLDS** if the outage cost is at most 2.5 extra calls per request, with an upper bound below 3.0. This means near E3's +2.08.
3. **RESCUE_ONLY** otherwise.

**Harm flags,** reported next to each verdict: success on true "temporary" or true "format" requests falls by 0.15 or more, with an upper bound below 0.

## Predictions (recorded before any E4 call; not part of the decision rule)

- **Control:**
  - both traps stay unsolved in both mixes (success ≤ 0.05);
  - no adaptation for either message, so |common − rare| < 0.15. Under "unavailable" the agent stops after one call and never sees that the message was false, so there is nothing to adapt to.
- **Bounded caution:**
  - **HOLDS in both mixes,** with a rescue of at least 0.8 and about 2 extra calls on true outages;
  - **a harm flag on true "format" in at least one mix.** Doubting the format message, Luna will rewrite the depot first, as in E2 and E3, which leaves too few attempts to find the spelling. No harm flag on true "temporary";
  - no adaptation, so |common − rare| < 0.15.
- **Net effect:**
  - in `common`, the overall success gain is above 0;
  - in `rare`, it is uncertain. A format loss could cancel the trap gains when only 2 of 12 messages are false.

## Instrument validation (MOCK, not evidence)

`python3 -m causetest validate --configs configs/mock_*.json` runs all 23 scripted agents. The E4 agents run at the planned size, with 10% random first responses:

| Scripted agent | rare | common | Harm flags |
|---|---|---|---|
| bounded (drops the claim under the caution; stops after 3 calls) | HOLDS ✓ | HOLDS ✓ | true "format", both mixes ✓ (a three-call limit cuts the spelling search: success −0.39 and −0.35) |
| unbounded (drops the claim under the caution; no limit) | RESCUE_ONLY ✓ | RESCUE_ONLY ✓ | none ✓ |
| deaf (credulous; ignores the caution) | FADES ✓ | FADES ✓ | none ✓ |
| non-engager | INVALID ✓ | | |

**Power** (20 disjoint seed sets at 40 runs per cell; `runs/validation/power.json`):

- bounded: HOLDS 20/20 in each mix;
- deaf: FADES 20/20 in each mix.

## Budget

- **Estimate:** about $1.48 API-equivalent: 160 runs plus a 4-run pilot, at 36 calls per run and about $0.00025 per call. Twelve-request conversations cost more per call than six-request ones.
- **The config's cap is $0 in this commit.**
- The owner asked for this experiment on 2026-10-20 after a quoted cost of $2–4. The cap and its conditions are recorded in the README in a separate commit, before any E4 call.

## Known limits

- **One model,** with light reasoning (L2).
- **Two base rates.** Both are higher than most real systems would have; `rare` (17%) is the closer one.
- **Fixed counts per run, not independent draws.** A run always contains its mix's exact counts.
- **Twelve requests per run.** That gives each message type 4 occurrences, which is short for detecting slow adaptation.
- **The format harm depends on this environment's four spellings and six-call limit.**
