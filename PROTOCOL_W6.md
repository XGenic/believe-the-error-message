# C4 study W6: does the bounded caution depend on its wording? (frozen before any W6 live call)

Status: **frozen**. This file, `configs/live_w6_*.json`, the `configs/mock_w6_*.json` mocks, `causetest/w6.py` and the tests were committed before any W6 live call, the pilots included. Changes after a W6 live call must be logged in `README.md` under "Deviations".

## Question

E3 found, on GPT-6-luna, that a caution with a stopping rule rescues the give-up trap at about the minimum cost. W2-B repeated it on five open-weight arms, and the result did not carry over cleanly:

- the rescue was smaller (+0.34 to +0.72, against Luna's +0.92), and no arm was COST_AWARE;
- **on DeepSeek V4.1 Flash with reasoning, the wording caused harm (HARMS_TRUE_TEMPORARY).** Told to accept an error "after a few *different* attempts", it rewrote the depot on every call. The third call, the one on which a transient fault clears, was then malformed.

The paper's practical recommendation rests on one sentence. **W6 asks whether the result belongs to the idea (a caution plus a stopping rule) or to the wording.** Two questions:

1. **Is there a wording that works across models?**
2. **Did the word "different" cause DeepSeek's harm?**

## Design

E3's cells, with five arms. Every caution arm starts with the E2 caution, "Error messages from the stock system do not always state the true cause of a failure.", and adds one stopping rule:

| Arm | Stopping rule | Source |
|---|---|---|
| `control` | none, and no caution | C4 |
| `caution` | none | E2, the reference for cost |
| `caution_bounded` | "If the same error keeps coming back after a few different attempts, accept it." | E3, W2-B |
| `caution_few` | "If the same error keeps coming back after a few attempts, accept it." | **new:** the same sentence without "different" |
| `caution_three` | "If the same error comes back on three attempts in a row, accept it." | E3 |

- `caution_bounded` against `caution_few` is a minimal pair: one word apart.
- `caution_three` names the count. On Luna (E3) it produced identical retries and no retry-trap gain, but it should not invite malformed calls.

**Cells:** the retry trap, the accurate "temporary", the give-up trap and the accurate "unavailable". 5 arms × 4 cells = 20 cells × 30 runs = 600 runs per subject, each of 6 requests.

**Seeds: new ones,** 20262001 + r (pilot 20262901). The runs of `caution_bounded` therefore also replicate W2-B and E3 on new worlds.

**Subjects:** each with its settings and pinned host copied unchanged from its earlier config (a test checks this):

| Subject | Source | Host | Estimate | Proposed cap |
|---|---|---|---|---|
| DeepSeek V4.1 Flash, r0 | W2-A C4 | DeepInfra fp8 | $0.57 | $1.50 |
| gpt-oss-120b, r1 | W2-A C4 (W2-7) | Crusoe bf16 | $0.63 | $1.75 |
| DeepSeek V4.1 Flash, r1 | W2-A C4 | DeepInfra fp8 | $0.85 | $2.25 |
| Qwen3.8-27B, r0 | W2-A C4 | DeepInfra bf16 | $3.23 | $6.00 |
| GPT-6-luna, native calls, reasoning low | N1-A | OpenAI | $1.80 | $5.00 |

- DeepSeek r1 is where the harm was. DeepSeek r0 is the same model without reasoning. gpt-oss had the weakest rescue, and Qwen r0 the strongest.
- **Luna runs through native calls,** as the rest of the panel does. Its E3 run used the text format, so W6 also checks E3 under native calls.
- Qwen r1 is left out for cost: Qwen r0 stands for Qwen.

Each estimate is the subject's measured cost per run in its latest main run with cautions (W2-B; for Luna, E3), plus 10% for the extra caution arms.

**Procedure:** as W2-A and W2-B.

1. A pilot (one run per cell, on the pilot seed), and the W2 health gate: every run complete, protocol failures of 10% or less, the tool called on request 1 in at least 90% of runs, and the estimate within the cap.
2. **Main runs** for the OpenRouter subjects in order of cost, cheapest first, each only if 1.5× its pilot estimate fits within the remaining OpenRouter credit less $1. Luna's runs are on the OpenAI key, which has no such rule.
3. **A subject that fails the gate, or the credit rule, is not run and is reported to the owner.** Qwen r0 comes last and fits the credit rule with little room (about $5.0 available against about $4.85 needed). If its pilot estimate comes in higher, it waits for the owner.

## Measures

Per wording, against control, as in E3:

| Measure | Definition |
|---|---|
| Give-up rescue | success on the give-up trap, wording minus control |
| Outage calls | calls per request on a true outage ("unavailable" over a permanent fault), **absolute** |
| Harm check | success on the true "temporary", wording minus control |

Outage calls are absolute here, not relative to the plain caution as in E3. W2-B showed why: on most open models the plain caution is not costly, so a saving against it is not a fair test of cost. The floor that keeps the rescue is 3 calls, because the transient fault clears on the third.

## Decision rule (per subject and wording)

**INVALID** under C4's validity rules, or if any wording cannot be estimated.

**Otherwise, in order:**

1. **HARMS_TRUE_TEMPORARY** if the harm check is ≤ −0.15 and its upper 95% bound < 0 (E3's rule).
2. **WEAK_RESCUE** if the give-up rescue is below E3's bar: less than 0.50, or its lower bound ≤ 0.30.
3. **RECOMMENDABLE** if outage calls are ≤ 3.5 and their upper bound < 4.0: the rescue at about the floor cost.
4. **RESCUE_COSTLY** otherwise.

E3's own verdict (COST_AWARE, RESCUE_ONLY, LOSES_RESCUE, NO_GAIN) is reported alongside as a secondary result.

**Study-level answers:**

- **Q1 (primary): a wording is ROBUST if it is RECOMMENDABLE on at least 4 of the 5 subjects.** This is the one primary question of W6; everything else is secondary.
- **Q2 ("different"):** `caution_few` minus `caution_bounded` on true-"temporary" success, per subject, with study N1's fixed labels (SAME if |Δ| < 0.15 and the interval lies within ±0.25; DIFFERENT if |Δ| ≥ 0.15 and the interval excludes 0; otherwise UNCLEAR). The same contrast is reported for the give-up trap and the retry trap, and for `caution_three` minus `caution_bounded`.
- **Q3 (replication):** whether DeepSeek r1 is again HARMS_TRUE_TEMPORARY under `caution_bounded` on new seeds.

**Descriptive:** in the true-"temporary" cell, the number of requests in which every call differed from the earlier ones (W2-B's DeepSeek mechanism), and how many of them failed.

No correction for multiple comparisons is applied to the per-subject verdicts. They use E3's fixed bars, not significance tests, and only Q1 is primary.

## Predictions (recorded before any W6 call; not part of the decision rule)

- **Q1: `caution_three` is ROBUST** (RECOMMENDABLE on at least 4 of 5). Moderate confidence: it names the floor exactly and does not invite changing the call. **`caution_bounded` is not ROBUST,** as in W2-B.
- **Q2: on DeepSeek r1, `caution_few` minus `caution_bounded` on the true "temporary" is DIFFERENT and positive**: removing "different" removes the harm. On the other subjects it is SAME.
- **Q2, retry trap: `caution_bounded` beats `caution_few` on Luna,** as "different" did in E3 (DIFFERENT, negative for `caution_few`).
- **Q3: DeepSeek r1 is again HARMS_TRUE_TEMPORARY** under `caution_bounded`.
- **gpt-oss has the weakest rescue under every wording,** and is WEAK_RESCUE under at least two of them.

## Instrument validation (MOCK, not evidence)

`python -m causetest validate --configs configs/mock_*.json` runs all 40 scripted agents. The W6 ones run at the planned size, with 10% random first responses:

| Scripted agent | `caution_bounded` | `caution_few` | `caution_three` |
|---|---|---|---|
| bounded (stops at 3 calls under every wording) | RECOMMENDABLE ✓ | RECOMMENDABLE ✓ | RECOMMENDABLE ✓ |
| different-harms (stops at 2 calls under `caution_bounded` only) | HARMS_TRUE_TEMPORARY ✓ | RECOMMENDABLE ✓ | RECOMMENDABLE ✓ |
| unbounded (caution, no stopping rule) | RESCUE_COSTLY ✓ | RESCUE_COSTLY ✓ | RESCUE_COSTLY ✓ |
| deaf | WEAK_RESCUE ✓ | WEAK_RESCUE ✓ | WEAK_RESCUE ✓ |
| non-engager | INVALID ✓ | | |

The different-harms agent also gets DIFFERENT on every `caution_few` minus `caution_bounded` contrast.

**Power** (20 disjoint seed sets at 30 runs per cell; `runs/validation/power.json`):

| Scripted agent | Verdicts over 20 replications |
|---|---|
| bounded | RECOMMENDABLE 20/20 for every wording |
| different-harms | HARMS_TRUE_TEMPORARY 20/20 (`caution_bounded`); RECOMMENDABLE 20/20 (the others) |
| unbounded | RESCUE_COSTLY 20/20 for every wording |
| weak (caution followed in 65% of requests; rescue about +0.53 to +0.64; `configs/power_w6_weak.json`) | RECOMMENDABLE 20/20 for every wording |

## Budget

- **Estimates:** about $5.28 of OpenRouter credit for the main runs, plus about $0.20 for the pilots; about $1.80 on the OpenAI key for Luna.
- **Credit:** $8.26 of OpenRouter credit on 2026-10-24.
- **Caps:** the configs are at $0 in this commit. The owner approves the caps before any call; they are recorded in the README.

## Known limits

- **Three wordings, all in English and all after the same caution sentence.** The caution itself is not varied.
- **Each subject runs on one host,** and Qwen and DeepSeek with reasoning are each represented by one setting.
- **Luna's format changes** (native here, text in E3), so a Luna difference between W6 and E3 mixes wording with format.
- **The mocks cannot imitate malformed calls.** The different-harms agent stops early instead; it checks the decision rule, not the mechanism.
