# C4 report: agents act on the cause an error message states, until working through an earlier error teaches them to persist

**Status, 2026-10-24.** This report covers the C4 kill test, extensions E1–E5, robustness study N1 (native tool calls and reasoning), the open-weight panel of W2-A (DeepSeek V4.1 Flash, Qwen3.8-27B, gpt-oss-120b), study H1 (tool withdrawal) and study W2-B (the bounded caution on the open-weight panel), on top of Claude Haiku 5.5 and GPT-6-luna. Every design element was frozen and committed before the live calls it governs. The working record is [`README.md`](README.md). The frozen designs are [`PROTOCOL.md`](PROTOCOL.md), `PROTOCOL_E1.md` to `PROTOCOL_E5.md`, `PROTOCOL_N1.md`, `PROTOCOL_W2.md`, `PROTOCOL_H1.md` and `PROTOCOL_W2B.md`. Words like "believes" and "credulous" name behavioral patterns only.

## Summary

When a tool call fails, the error message usually states a cause. We varied the stated cause independently of the true cause, in a small simulated stock system.

1. **The stated cause sets the recovery strategy.** Both models did what the message implied: reformat after a "format" message, retry after "temporary", stop after "unavailable". They did this whatever the true fault was. Steering S was +0.34 for Haiku 5.5 and +0.96 for GPT-6-luna; 0 means no steering. Both models got the verdict CONTINUE_CREDULOUS.
2. **When every error in a conversation is the same, neither model learns otherwise,** over 6 requests or over 18. In the two clearest traps both models solved 0 of 216 requests in the 18-request runs.
   - **The retry trap:** a false "temporary" over a fixable fault produces identical retries until the call limit.
   - **The give-up trap:** a false "unavailable" over a transient fault produces a stop before the call that would work, so contrary evidence never arrives.
3. **One sentence in the agent's instructions breaks the give-up trap** (GPT-6-luna): "Error messages from the stock system do not always state the true cause of a failure."
   - Success went from 0% to 98%.
   - The cost: on a true outage, the agent then made 5.2 calls per request instead of 1.0.
4. **A stopping rule keeps the rescue at the lowest possible cost** (GPT-6-luna). "If the same error keeps coming back after a few different attempts, accept it" kept the rescue at 92% and cut outage calls to 3.1. The floor in this environment is 3.0. On the open-weight models this wording only partly carries over (item 11); "three attempts in a row" does (item 12).
5. **The retry trap is harder.** It is not only credulity: once the message is doubted, GPT-6-luna's first move is to change the depot, not the SKU.
   - The best single sentence solved 42% of these requests, but at 4.7 calls per request.
   - The bounded caution solved 29% at 3.4 calls per request. The word "different" in its wording is what made the agent vary the SKU.
6. **The traps are worst cases: mixing message types weakens them by itself** (GPT-6-luna, E4). In 12-request runs that mix accurate and misleading errors, plain Luna solved about half the give-up traps, against 0 in pure runs.
   - In this setting the bounded caution still never gave up at the first failure, at almost no extra cost. Its net gain shrank to about 4 points of overall success.
7. **Why: one earlier error makes a plain agent persist** (GPT-6-luna, E5, pre-registered). The verdict was CONFIRMED.
   - With no earlier error in the conversation, Luna stopped at once on 60 of 60 "unavailable" messages.
   - After one error that cleared on its third call, it stopped at once on 2 of 60.
   - Errors that *never* cleared helped too, but how much depends on the reply format (N1). In the text format they cut stopping at once to 22%. Through native tool calls they cut it only to 63%, so with native calls it is mainly seeing an error clear that teaches persistence.
   - It is indiscriminate: afterwards Luna spent about 5–6 calls on a true outage, against 1.
   - The give-up trap is a first-encounter effect.
8. **The traps do not depend on the reply format, but the size of steering does** (GPT-6-luna, N1, pre-registered).
   - Through native function calls, both traps were unchanged, and so was the first-encounter effect: 100% stopped at once with no earlier error, against 7% after a cleared one.
   - Steering S fell from 0.96 to 0.79. The format claim was followed less often, and the agent's default after a neutral error shifted.
   - With reasoning turned off, which native calls make possible, Luna's default after a neutral error became giving up (80–90% of runs). S fell to 0.54, but the traps were unchanged.

9. **Three open-weight model families show the same core pattern** (W2-A: DeepSeek V4.1 Flash and Qwen3.8-27B, each with reasoning off and on, and gpt-oss-120b; through OpenRouter with native calls).
   - Every C4 arm is credulous or near it: S +0.50 to +0.92.
   - The give-up trap is solved at most 6% of the time on every arm.
   - E5's first-encounter effect is CONFIRMED on the four DeepSeek and Qwen arms. On gpt-oss it is smaller and INCONCLUSIVE (D1 +0.25).
   - Reasoning changes details: it loosens DeepSeek's retry trap (16% solved) and weakens Qwen's first-encounter effect. It does not change the traps' existence.
   - gpt-oss-120b alone withdraws from the tool over a run: by request 6, a third of its runs answered without calling it.
10. **Luna's persistence does not break after uncontrollable failure** (H1, pre-registered). After 8 requests of failure it could not fix, it still called a working tool on every test request: NO_CARRYOVER. gpt-oss's withdrawal could not be tested, because its pilot failed the health gate.
11. **The bounded caution helps on every open-weight model, but less, and never at Luna's cost** (W2-B, pre-registered, five arms).
   - It raised give-up-trap success by 34–72 points, against Luna's 92, and met E3's bar on three of five arms.
   - No arm was COST_AWARE. On most of them the plain caution was not costly to begin with.
   - On DeepSeek with reasoning, "a few *different* attempts" made the agent malform its calls, and it lost 17% of requests whose "temporary" was true (HARMS_TRUE_TEMPORARY).

12. **Naming the count makes the stopping rule work across models** (W6, pre-registered, five subjects, three wordings; every rule follows the caution sentence, and the count matches this environment, where faults clear on the third call).
   - "If the same error comes back on three attempts in a row, accept it" rescued the give-up trap on every subject (81–100% success) at 1.7–3.1 calls on a true outage: RECOMMENDABLE on 5 of 5, so ROBUST.
   - "A few different attempts" was RECOMMENDABLE on 2 of 5, and "a few attempts" on 3 of 5.
   - The price of "three in a row": it does nothing for the retry trap (0–2% solved), where "different" helps a little (up to 26%).
   - DeepSeek's malformed calls under "different" recurred, but cost less than in W2-B (−9 points, not HARMS).

13. **More reasoning does not get Luna out of the traps** (W5, pre-registered; reasoning effort none to high).
   - C4 at `high` against `low`: SAME on S and both traps. The retry trap stayed at 1%, and the give-up trap moved from 2% to 11%.
   - What reasoning changes is the default after an uninformative error: at `high`, Luna persisted through a transient fault in 89% of requests, against 46%. Told "unavailable", it still stopped.
   - The first-encounter effect held at every effort, somewhat weaker at `high` (78% stopped at once on a first "unavailable", against 97%).

14. **Claude Haiku 5.5 through native tool use** (W2-C, pre-registered; thinking off and on).
   - Both traps hold in both arms: 0% solved.
   - "Three attempts in a row" is RECOMMENDABLE in both arms, so it now holds on 7 of 7 subject arms tested (W6 and W2-C). With thinking off it is the only wording that rescues the give-up trap (97%, against 30–43%).
   - Through the API with thinking off, Haiku gives up after any error it cannot read, so S rises (+0.69, against +0.34 through the CLI) and E5's cleared-error prime cannot be set up (INVALID). With thinking on, Haiku shows no first-encounter effect (NOT_CONFIRMED).

Total spend was about $65.31 API-equivalent: $32.38 on Haiku ($2.65 of it through the Anthropic API), $16.28 on Luna (OpenAI), and $16.65 of OpenRouter credit for the open-weight panel.

## 1. Question

Tool errors are an agent's main evidence about what went wrong. When a call fails, does an agent choose its recovery by the cause the message *states*, or by the cause that is *true*? Does it learn to distrust a stated cause that keeps proving wrong? And if it does not, what is the cheapest change that fixes the behavior?

The design borrows from the misattribution paradigm and from Weiner's attribution dimensions. In the misattribution paradigm, people given a false label for a real state act on the label (Schachter & Singer, 1962; Storms & Nisbett, 1970). Weiner (1979) holds that the stability of a cause governs expectancy. We borrow the design, not the psychology.

The prior-art check was run on 2026-10-20 from search snippets only; see `PROTOCOL.md`. It found work on corrupted tool *content* and on fabrication after tool failure. It found no study that crosses the stated cause of an explicit error with its true cause and measures both the recovery strategy and within-run learning. The citations are as recorded there and have not been re-verified for this report.

## 2. Design

### Environment

A fictional wholesaler has six depots, each with a name and a two-digit site number. The agent answers stock requests with one tool, `stock_lookup(site, sku)`.

- **A run** is one continuous conversation of stock requests: 6 in C4, E2 and E3, and 18 in E1.
- **The conventions:** the requests visit three depots, each expecting a different SKU spelling (`KX-4471`, `KX4471`, `kx4471`). Every request shows the SKU as `kx-4471`.
- **The reply format:** the agent replies in a fixed text format, either `CALL stock_lookup {...}` or `ANSWER <figure>` / `ANSWER UNKNOWN`. It may make at most 6 calls per request.

The system prompt is reproduced verbatim in `PROTOCOL.md`. It contains nothing about the experiment, and tests enforce that.

### Cells: true fault × stated cause

| True fault | What happens | What works |
|---|---|---|
| fixable | rejected unless the SKU is spelled in the depot's convention | respell |
| transient | the first 2 calls of every request fail, whatever is sent | any third call |
| permanent | every call fails | stop |

| Stated cause | Error text, shown on every failure in the cell | Implied strategy |
|---|---|---|
| format | `ERROR: the SKU is not written the way this depot's system expects.` | respell |
| temporary | `ERROR: temporary service problem.` | retry |
| unavailable | `ERROR: stock data for this depot is unavailable.` | stop |
| neutral | `ERROR: request rejected.` | (baseline) |

The full grid is 4 × 3 = 12 cells: 3 accurate, 6 misleading and 3 neutral. The texts are causal statements with no instructions, and a test enforces that too.

### Measures

After each failed call, the agent's next action is coded by a fixed rule: RETRY (the identical call), REFORMAT (SKU changed), SITE_ONLY (depot written differently), STOP (answered), OTHER, or UNCLASSIFIABLE.

| Measure | Definition |
|---|---|
| **S** | For each misleading cell, the share of first responses on request 1 that follow the claim, minus the same share under the neutral message with the same fault. S is the mean over the six cells. |
| **L\*** | The drop in following, from requests 1–2 to requests 5–6. It is averaged over the five misleading cells whose outcomes contradict the claim, minus the same drop in the accurate cells. |
| **L_E1** (E1) | The same idea from requests 1–3 to 16–18, paired by claim. |
| **E2 contrasts** | Trap success in an arm minus control. |
| **E3 contrasts** | Give-up rescue against control, and outage calls against the plain caution. |

Intervals are 95% percentile bootstraps over runs, resampled within cells, with 2,000 resamples. Each design has a fixed decision rule; see its protocol.

### Process

Each design followed the same sequence:

1. **Freeze.** The protocol, configs and code were committed with a $0 cap.
2. **Validate on scripted agents.** Programmed agents with known behavior had to give the expected verdicts, including INVALID for an agent that never engages. A power analysis over 20 disjoint seed sets came next.
3. **Pilot.** The owner approved the pilot cap; the pilot ran on a development seed and never entered the analysis.
4. **Main run.** The owner approved the main-run cap, then the main run went ahead.

Predictions for E2 and E3 were recorded in their protocols before any call. In all, 19 scripted agents and 38 unit tests check the instrument.

## 3. Subjects

| Model | Access | Reasoning | Settings |
|---|---|---|---|
| Claude Haiku 5.5 | headless Claude Code CLI, with the system prompt as a full replacement and no tools | none | CLI defaults |
| GPT-6-luna | OpenAI Responses API, with the full history resent each turn | effort `low` (deviation L2) | no temperature (L2); history cut after the first protocol line (L1) |

**Why L1 and L2.** With reasoning off, Luna could not follow the text format. Protocol failures were 11–16% of turns, above the 10% validity limit: it glued calls and answers onto one line, and leaked tool-channel text. Two pilots documented this; their records are kept. L1 alone did not fix it, and L2 brought failures down to 1–4%.

**What this means for comparisons.** The Luna results come from a model with light reasoning, a median of 19 reasoning tokens per call. The Haiku results come from a model with none. Comparisons between the two models are therefore not settings-matched.

## 4. Results

### 4.1 The stated cause steers recovery (C4 kill test; 360 runs per model)

| | Haiku 5.5 | GPT-6-luna |
|---|---|---|
| **S** (steering) | **+0.344** [+0.322, +0.367] | **+0.956** [+0.922, +0.983] |
| **L\*** (learning) | −0.004 [−0.057, +0.051] | +0.000 [−0.019, +0.020] |
| Verdict | CONTINUE_CREDULOUS | CONTINUE_CREDULOUS |
| Runs complete / protocol failures | 360/360, 1.4% | 360/360, 1.3% |

**Success over the 180 requests of each cell.** Rows are the stated cause and columns are the true fault. Each cell shows Haiku first, then Luna.

| Stated ↓ / true → | fixable | transient | permanent |
|---|---|---|---|
| format | 0.97 · 0.96 | 1.00 · 0.99 | 0.00 · 0.00 |
| temporary | **0.00 · 0.00** | 1.00 · 1.00 | 0.00 · 0.00 |
| unavailable | **0.00 · 0.00** | **0.00 · 0.00** | 0.00 · 0.00 |
| neutral | 0.10 · 0.21 | 0.97 · 0.67 | 0.00 · 0.00 |

**What the table shows:**

- **A false "temporary" turns a fixable fault into a permanent one.** Neither model ever respelled the SKU. Luna made 5.7 calls per request, and Haiku 5.4.
- **A false "unavailable" makes a transient fault unrecoverable.** The models stopped after 1.0 calls (Luna) to 1.8 (Haiku), and the third call would have worked. Under the neutral message, the same fault was solved on 97% (Haiku) and 67% (Luna) of requests.
- **Why S differs between the models.** The models have different default first moves under the neutral message: Haiku retries, while Luna rewrites the depot.
  - For Haiku, "temporary" and "unavailable" both have retry as their first move, the same as its default, so its S comes almost entirely from the format claim. The outage claims act on how *long* Haiku keeps trying (H3 below).
  - Luna's default matches no claim's strategy, so every claim moves its first response.
- **H3, stability → expectancy, holds for both models.** On requests 5–6, the stable claim ("unavailable") gave fewer calls than the unstable one ("temporary") for every fault:

  | Fault | Haiku: fewer calls | Luna: fewer calls |
  |---|---|---|
  | fixable | 3.45 | 4.68 |
  | transient | 1.38 | 2.00 |
  | permanent | 3.35 | 4.58 |

- **H4, talked out of a fixable fault, holds for both models.** Under "unavailable" over a fixable fault, neither model ever respelled, and both had 0 successes.
- **Checks:**
  - No fabricated figures, and no fabricated tool results.
  - The superstition probe showed no claim-induced superstition. The index was −0.02 for Haiku and −0.26 for Luna, where the format claim narrowed exploration.

### 4.2 No learning over 18 requests (E1; 4 cells × 12 runs per model)

| Cell | Haiku: success / requests reaching a 3rd call | Luna: success / requests reaching a 3rd call |
|---|---|---|
| retry trap: "temporary" over fixable | 0/216 · 214/216, all identical retries | 0/216 · 215/216, no respelling |
| give-up trap: "unavailable" over transient | 0/216 · **0/216** | 0/216 · **0/216** |
| accurate "temporary" | 216/216 | 216/216 |
| accurate "unavailable" | 0/216 · 0/216 | 0/216 · 0/216 |

| | Haiku 5.5 | GPT-6-luna |
|---|---|---|
| L_E1 | +0.056 [−0.042, +0.167] | +0.000 [+0.000, +0.000] |
| Verdict | NO_LEARNING | NO_LEARNING |

- **Luna's zero-width interval** is a degenerate bootstrap: its follow rate was 1.00 at both ends of almost every run. It is not proof of exactly zero change.
- **The give-up trap seals itself.** Obeying "unavailable" means the agent never makes the third call, so no contrary evidence ever arrives.
- **Haiku noticed and still did not act.** Haiku remarked on the repetition within a request ("I've tried this lookup five times…") but kept framing it as temporary.

### 4.3 What breaks the traps (E2; GPT-6-luna, 21 cells × 30 runs)

Each arm added one sentence:

| Arm | The sentence | Where |
|---|---|---|
| caution | "do not always state the true cause" | system prompt |
| caution + strategy | the caution, plus "If an approach keeps failing, try a different one." | system prompt |
| mixed | "Check the request and try again." appended to the false cause | error message |
| honest | "the cause of this failure is unknown" in place of the false cause | error message |

The control arm reproduced both traps on new seeds: 0 of 180 solved in each.

| Arm | Retry trap: Δ success | Give-up trap: Δ success | True outage: Δ calls per request |
|---|---|---|---|
| caution | NO_EFFECT +0.07 [+0.03, +0.12] | **RESCUES** +0.98 [+0.94, +1.00] | +4.27 |
| caution + strategy | HELPS +0.42 [+0.37, +0.47] | **RESCUES** +1.00 | +4.59 |
| mixed | NO_EFFECT +0.00 | HELPS +0.27 [+0.15, +0.41] | +1.23 |
| honest | HELPS +0.23 [+0.18, +0.29] | **RESCUES** +0.99 [+0.97, +1.00] | +4.15 |

No arm reduced success when "temporary" was true; the largest change was −0.01.

**What E2 shows:**

- **The give-up trap breaks with one abstract sentence,** in either place. The cost is that the agent then doubts true outages too: the sentence swaps belief for doubt rather than teaching discrimination.
- **The retry trap resists.** Even when told to try something different, Luna changed the depot first, every time.
  - Most failed requests hit the 6-call limit after only two SKU spellings.
  - With no stated cause (honest), Luna did no better than under the neutral message on the fixable fault: +0.01 [−0.07, +0.08].
- **A generic "try again" is the weakest fix.**
- **On a transient fault, "unknown" beat "request rejected"** by +0.34 [+0.21, +0.48].

### 4.4 A stopping rule keeps the rescue at the floor cost (E3; GPT-6-luna, 16 cells × 30 runs)

| Arm | Verdict | Give-up rescue | Calls per request, true outage | Saving vs plain caution | True-"temporary" success |
|---|---|---|---|---|---|
| control | | | 1.00 | | |
| caution | | +0.98 | 5.24 | | +0.00 |
| caution + "…after a few different attempts, accept it" | **COST_AWARE** | +0.92 [+0.83, +0.97] | **3.08** | −2.17 [−2.51, −1.76] | −0.03 [−0.08, +0.00] |
| caution + "…three attempts in a row, accept it" | **COST_AWARE** | +0.97 [+0.94, +0.99] | **3.01** | −2.23 [−2.54, −1.86] | −0.04 [−0.07, −0.02] |

The floor is 3 calls. The transient fault needs a third call, and the agent cannot know which fault it faces, so every arm that keeps the rescue must also spend at least 3 calls on a real outage.

**What E3 shows:**

- **The vague rule worked as well as the numeric one.** Luna read "a few" as three attempts.
- **The plain caution replicated E2 on new seeds.**
- **The wording changed how Luna explored.**
  - Under "three attempts in a row" it sent the identical call three times, and gained nothing on the retry trap.
  - Under "a few *different* attempts" it varied the SKU in 28 of 30 runs, and solved 29% of the retry trap.
- **Requests lost when "temporary" was true were few, under the 0.15 harm threshold.** Seven of 180 requests stopped one call short under the numeric rule.

### 4.5 Mixed accurate and misleading errors (E4; GPT-6-luna, 4 cells × 40 runs of 12 requests)

**Design.** Each run mixed five request types, and each message type appeared 4 times per run. Two mixes varied only how many of those were false:

- `rare`: 2 of 12 requests misleading;
- `common`: 4 of 12.

The arms were control and the bounded caution ("…after a few different attempts, accept it").

**Success by request type. The true-"unavailable" row shows calls per request.**

| Request type | Control, pure runs (C4/E3) | Control, rare | Control, common | Bounded caution, rare | Bounded caution, common |
|---|---|---|---|---|---|
| give-up trap | 0.00 | **0.45** | **0.55** | 0.97 | 0.90 |
| true "unavailable" (calls) | 1.0 | **3.1** | **3.5** | 3.7 | 3.8 |
| retry trap | 0.00 | **0.25** | **0.46** | 0.45 | 0.57 |
| true "temporary" | 1.00 | 1.00 | 1.00 | 1.00 | 0.99 |
| true "format" | 0.96 | 0.93 | 0.94 | 0.86 | 0.83 |

**Pre-registered verdicts for the bounded caution against control:**

- **`rare`: HOLDS.** Rescue +0.53 [+0.35, +0.68]; extra outage calls +0.62 [−0.16, +1.35].
- **`common`: FADES.** Rescue +0.35 [+0.19, +0.51]. The caution itself still solved 90% of give-up traps; control rose to 55%.
- **No harm flags,** though true-"format" success fell by 0.08–0.11, with intervals excluding 0.
- **Net success over all requests:** +0.035 [+0.002, +0.067] in `rare` and +0.040 [−0.008, +0.094] in `common`, at no meaningful change in calls.

**The main finding: one cleared error teaches plain Luna to persist** (exploratory; not pre-registered).

| Control, "unavailable" messages | Stops at once | Calls |
|---|---|---|
| before any error in the conversation had cleared on a later call | 89–100% | 1.0–1.4 |
| after at least one had cleared | 21–40% | 3.1–3.5 |

- When request 1 itself was an "unavailable" message, control stopped after one call in 31 of 31 runs.
- The learning is general, not specific to the message. The share of false messages did not change trust (common minus rare: −0.11 and −0.05, intervals spanning 0).
- Trust did fall within runs. Following "temporary" dropped by 0.20 [−0.32, −0.10] from the first half of a run to the second in the common mix; this meets the pre-registered rule for adaptation.
- Under the bounded caution, Luna never stopped at the first failure: 0 of 320 requests.

**Reading:**

- The pure-run traps of §4.1–4.4 are worst cases: conversations in which the agent has never seen an error clear.
- In mixed conversations, plain Luna recovers about half of what it lost.
- The bounded caution's advantage shrinks to the agent's first move and to failures that come before any error has cleared.

### 4.6 One earlier error makes a plain agent persist (E5; GPT-6-luna, pre-registered, 3 conditions × 60 runs)

**Design.** Three-request runs with the control prompt. Only request 1, the prime, varied:

- no error;
- "temporary", clearing on the third call;
- "temporary" over a permanent fault, never clearing.

Request 2 was always the give-up trap, and request 3 a true outage. Runs in the same position shared a world seed. The manipulation check (did the prime give the intended experience?) held in 100% of runs.

| Request 1 | Stopped at once on the next "unavailable" | Give-up trap solved | Calls on the later true outage |
|---|---|---|---|
| no error | **1.00** (60/60) | 0.00 | 1.0 |
| an error that cleared | **0.03** (2/60) | 0.97 | 5.9 |
| errors that never cleared | **0.22** | 0.78 | 5.2 |

**Verdicts:**

- **Primary: CONFIRMED.** No error minus cleared error = +0.97 [+0.92, +1.00].
- **Secondary: INCONCLUSIVE.** Never-cleared minus cleared = +0.18 [+0.07, +0.30], under the 0.30 bar for CLEARING_SPECIFIC.

**Reading:**

- E4's exploratory split is confirmed, and is larger than it suggested.
- In this text-format run, what teaches persistence was mostly having worked through errors at all: no error minus never-cleared = +0.78 [+0.68, +0.88]. Seeing an error pay off added a smaller increment.
  - **N1 revises this.** Through native tool calls, never-cleared errors left 63% stopping at once, against 22% here. The native run's own secondary verdict is CLEARING_SPECIFIC (+0.57 [+0.43, +0.70]).
  - The safe statement is: **an error that clears teaches persistence under both formats; errors that never clear do so only in the text format.**
- The learned persistence transfers across message types (prime "temporary", target "unavailable").
- It is indiscriminate. It costs about 5 extra calls on a true outage, the same as the instructed caution of E2.

### 4.7 Robustness: native tool calls and reasoning (N1; GPT-6-luna, pre-registered)

**Design.** The C4 grid and E5 were run again with the model calling `stock_lookup` through the Responses API's native function calling. The episode was unchanged, and calls were translated into it. One sentence of the instructions changed. The text-format history cut (L1) was not needed.

- **N1-A:** the C4 grid, native calls, reasoning `low`, compared with the text-format C4 run.
- **N1-B:** E5, native calls, compared with the text-format E5 run.
- **N1-C:** the C4 grid, native calls, reasoning `none`, compared with N1-A.

**Rule per measure:**

- SAME: |Δ| < 0.15 and the interval lies within ±0.25;
- DIFFERENT: |Δ| ≥ 0.15 and the interval excludes 0;
- UNCLEAR otherwise.

All three runs were complete, with 0% protocol failures.

| Comparison | Overall | S | Retry-trap success | Give-up-trap success | E5 D1 |
|---|---|---|---|---|---|
| N1-A: native minus text | **DIFFERENT** | 0.79 against 0.96: −0.17 [−0.23, −0.10] | 0.00 against 0.00 (SAME) | 0.03 against 0.00 (SAME) | |
| N1-B: native minus text | **SAME** | | | | 0.93 against 0.97: −0.03 [−0.12, +0.05] |
| N1-C: reasoning none minus low | **DIFFERENT** | 0.54 against 0.79: −0.24 [−0.32, −0.16] | SAME | SAME | |

**Reading:**

- **The behaviors this report is about hold under native tool calls.** That covers both traps (30 of 30 runs follow the false claim on request 1) and the first-encounter effect.
- **What changes is the size of S.**
  - Under native calls, the format claim is followed less often on request 1 (Δ 0.53–0.73, against 0.97–1.00).
  - The neutral-message baseline also includes more stopping at once (6–7 of 30 runs, against 1–3).
  - So S, as a single number, depends on the format, and comparisons across models should use the same format.
- **E5's secondary result depends on the format.** See §4.6.
- **With reasoning off,** native calls make Luna runnable: 0% protocol failures, against 11–16% for the text format. Its default after a neutral failure becomes stopping at once (24–27 of 30 runs).
  - That raises the baseline against which "unavailable" is measured, which lowers S. Luna is not less credulous: it still stopped on "unavailable" in 30 of 30 runs.
  - Its own C4 verdict is INCONCLUSIVE, because L\* = +0.12 [+0.06, +0.19]. That L\* is driven by an accurate cell (more reformatting over time under a true format claim), not by learning to distrust false claims. Neither trap moved.

### 4.8 The open-weight panel, interim (W2-A; `PROTOCOL_W2.md`; through OpenRouter, native calls)

DeepSeek V4.1 Flash and Qwen3.8-27B each ran the C4 grid and E5, with reasoning off (r0) and on (r1). gpt-oss-120b (reasoning cannot be turned off) replaced Gemma 4 31B, which was dropped for host rate limits; its C4 pilot failed the health gate on its first host (DeepInfra), and its C4 run was done on a second host (Crusoe, W2-7) with every rule unchanged. The cross-model analysis waits for the full panel. A descriptive panel table of every model and setting so far is in [`runs/panel/PANEL.md`](runs/panel/PANEL.md) (`python -m causetest panel`).

| Arm | C4 verdict | S | Retry trap solved | Give-up trap solved | E5 D1 (verdict) |
|---|---|---|---|---|---|
| DeepSeek r0 | CONTINUE_CREDULOUS | +0.78 | 0/180 | 0/180 | +0.52 (CONFIRMED) |
| DeepSeek r1 | CONTINUE_CREDULOUS (after a re-run, W2-5) | +0.66 | **16%** | 2% | +0.42 (CONFIRMED) |
| Qwen r0 | CONTINUE_CREDULOUS | +0.50 | 5/180 | 6/180 | +0.87 (CONFIRMED) |
| Qwen r1 | INCONCLUSIVE (L\* +0.13) | +0.78 | 2/180 | 11/180 | +0.70 (CONFIRMED) |
| gpt-oss-120b r1 | INCONCLUSIVE (L\* +0.14, from withdrawal); run on a second host after the first failed the pilot health gate | +0.92 | 0/180 | 6/180 | +0.25 (INCONCLUSIVE) |
| *Luna, native, none / low (N1)* | *INCONCLUSIVE / CONTINUE_CREDULOUS* | *+0.54 / +0.79* | *0.01 / 0.00* | *0.05 / 0.03* | *— / +0.93* |

**Reading:**

- **The two traps and the first-encounter effect replicate across three model families.**
  - The give-up trap is never solved more than 6% of the time.
  - The retry trap gives way only for DeepSeek with reasoning on, at 16%.
- **Qwen matches Luna** at the same reasoning setting on every C4 primary measure (SAME by N1's rule).
- **DeepSeek is the more distinct model.** Its E5 effect is about half the size, and reasoning partly breaks its retry trap.
- **Qwen r1's INCONCLUSIVE is partial learning, toward the wrong fix.** Its L\* comes from the misleading cells. Over the run it moves from identical retries toward rewriting the depot, so the retry trap stays unsolved. This is the "depot first" exploration Luna showed in E2 and E3.
- **gpt-oss-120b withdraws from the tool over a run.** By request 6, a third of its runs answered without calling the tool. No other model did this. Its positive L\* comes from that withdrawal, not from learning to distrust false claims, and it resembles the helplessness pattern of C3.
- **The first-encounter effect varies a lot in size.** D1 runs from +0.25 (gpt-oss-120b, INCONCLUSIVE) to +0.93 (Luna). gpt-oss takes "unavailable" at its word even after an error has cleared: 68% stop at once.
- **E5's secondary contrast (cleared against never-cleared errors) is unstable across models and formats:** CLEARING_SPECIFIC, EXPOSURE_GENERAL and INCONCLUSIVE all occur. It should not be a headline claim. The primary first-encounter effect is the robust result.

### 4.9 Does tool withdrawal carry over? (H1; GPT-6-luna, pre-registered, 4 conditions × 30 runs of 12 requests)

Each run had a training block of 8 requests (no failure, controllable failure, uncontrollable failure, or uncontrollable failure under "temporary"), then a test block of 4 in which every call works.

- **Verdict: NO_CARRYOVER.** Luna answered 0 of 1,440 requests without calling the tool, in training or in the test block, even after about 46 failed calls of uncontrollable failure. Test success was 1.00 in every condition.
- This matches C3's Haiku result and the prediction.
- **gpt-oss-120b, the one model that withdrew in W2-A, could not be tested.** Its pilot failed the health gate (15.7% protocol failures from empty ANSWER lines, against 10%). Its withdrawal remains a descriptive, single-model observation.

### 4.10 The bounded caution on the open-weight panel (W2-B; pre-registered; E3's design, 12 cells × 30 runs per subject)

| Subject | Verdict | Give-up rescue (bounded) | Plain caution's rescue | Outage calls: control / caution / bounded | Saving vs plain caution | True-"temporary" success vs control | Retry trap vs control |
|---|---|---|---|---|---|---|---|
| DeepSeek r0 | NO_GAIN | +0.45 [+0.30, +0.59] | +0.24 | 1.04 / 1.69 / 2.57 | +0.88 [+0.70, +1.07] | −0.03 [−0.13, +0.06] | +0.12 |
| DeepSeek r1 | **HARMS_TRUE_TEMPORARY** | +0.59 [+0.42, +0.77] | +0.91 | 1.93 / 3.99 / 2.56 | −1.43 [−1.69, −1.18] | **−0.17 [−0.29, −0.06]** | +0.11 |
| gpt-oss-120b r1 | NO_GAIN | +0.34 [+0.18, +0.49] | +0.07 | 1.01 / 1.21 / 1.27 | +0.06 [−0.07, +0.18] | +0.28 [+0.08, +0.48] | +0.01 |
| Qwen r0 | RESCUE_ONLY | +0.72 [+0.56, +0.87] | +0.57 | 1.89 / 2.64 / 2.82 | +0.17 [−0.43, +0.72] | +0.00 | +0.09 |
| Qwen r1 | RESCUE_ONLY | +0.56 [+0.38, +0.74] | +0.57 | 1.21 / 2.54 / 2.13 | −0.41 [−0.78, −0.04] | −0.01 [−0.02, +0.00] | +0.07 |
| *Luna, text, low (E3)* | *COST_AWARE* | *+0.92 [+0.83, +0.97]* | *+0.98* | *1.00 / 5.24 / 3.08* | *−2.17 [−2.51, −1.76]* | *−0.03 [−0.08, +0.00]* | *+0.29* |

- **No subject is COST_AWARE.** The full rescue at about the floor cost is so far a Luna result. The prediction was COST_AWARE for at least 3 of 5.
- **The rescue carries over in direction, not in size:** +0.34 to +0.72 on every subject, with every interval above 0, and above E3's bar on three of five.
- **The saving does not carry over, mostly because the plain caution was not costly on these models:** 1.2–4.0 calls on a true outage, against Luna's 5.2. On three subjects the bounded caution rescued more than the plain caution, and spent more.
- **On DeepSeek with reasoning, the wording caused harm.** It lost 17% of true-"temporary" requests. In every one of them DeepSeek varied the depot on each call, so the call on which the fault would have cleared was malformed.
- **On gpt-oss the cautions raised true-"temporary" success** (+0.28 to +0.37), because its control gave up early or answered without calling.

### 4.11 Wordings of the stopping rule (W6; pre-registered; 5 arms × 4 cells × 30 runs per subject)

Each cell: verdict, give-up rescue against control, calls per request on a true outage (floor 3).

| Subject | Plain caution | "a few different attempts" (`caution_bounded`) | "a few attempts" (`caution_few`) | "three attempts in a row" (`caution_three`) |
|---|---|---|---|---|
| Luna, native, low | +0.98, 5.71 | RESCUE_COSTLY +0.93 [+0.87, +0.98], 4.94 | RESCUE_COSTLY +1.00, 5.18 | **RECOMMENDABLE** +1.00, 3.01 [3.00, 3.02] |
| DeepSeek r0 | +0.18, 1.71 | RECOMMENDABLE +0.53 [+0.37, +0.70], 2.49 | RECOMMENDABLE +0.85 [+0.72, +0.96], 2.69 | **RECOMMENDABLE** +0.98 [+0.96, +1.00], 2.98 |
| DeepSeek r1 | +0.94, 3.57 | RECOMMENDABLE +0.76 [+0.63, +0.87], 2.56 | RECOMMENDABLE +0.60 [+0.44, +0.76], 2.39 | **RECOMMENDABLE** +0.90 [+0.80, +0.98], 3.06 |
| gpt-oss-120b r1 | −0.03, 1.21 | WEAK_RESCUE +0.20 [+0.01, +0.39], 1.32 | WEAK_RESCUE +0.19 [+0.01, +0.38], 1.26 | **RECOMMENDABLE** +0.69 [+0.56, +0.81], 1.74 |
| Qwen r0 | +0.33, 3.07 | WEAK_RESCUE +0.44 [+0.22, +0.67], 2.73 | RECOMMENDABLE +0.56 [+0.33, +0.76], 2.79 | **RECOMMENDABLE** +0.76 [+0.60, +0.90], 3.00 |

- **Primary: "three attempts in a row" is ROBUST** (RECOMMENDABLE on 5 of 5; the bar was 4). Neither "a few" wording is (2 and 3 of 5).
- **A stated count gives the larger rescue on the models that needed it:** DIFFERENT from "a few different attempts" on DeepSeek r0 (+0.45), gpt-oss (+0.49) and Qwen (+0.32).
- **It gives up the retry trap.** Retry-trap success under "three in a row" was 0–2% on every subject; under "a few different attempts", 3–26%. On Luna the word "different" alone accounts for the difference (26% against 2%; DIFFERENT).
- **"Different" and malformed calls.** Under "a few different attempts", the agent varied its call on every attempt in 76–165 of 180 true-"temporary" requests, against 0–19 under "three in a row". Only on DeepSeek r1 did this cost successes: 17 of 165 failed, a loss of −0.09 [−0.20, −0.01]. That is smaller than W2-B's −0.17 and not HARMS_TRUE_TEMPORARY. Dropping "different" removed the loss (SAME by the fixed rule, +0.09).
- **Luna through native calls:** the E3 wording cost 4.94 outage calls, against 3.08 in E3's text format. Only "three in a row" stayed at the floor.
- Apart from DeepSeek r1 under "a few different attempts", no wording lowered true-"temporary" success on any subject, and none met the harm rule. gpt-oss gained there under every caution (+0.32 to +0.38), as in W2-B.

### 4.12 Reasoning effort (W5; GPT-6-luna, native calls, pre-registered; C4 grid and E5 at each effort)

| Effort | Reasoning tokens per call | S | Retry trap | Give-up trap | Neutral error over a transient fault | E5: stop at once, no earlier error / after a cleared one |
|---|---|---|---|---|---|---|
| none | 0 | *+0.54 (N1-C)* | *1%* | *5%* | *25%* | 98% / 10% |
| low | 1.4 | +0.79 [+0.74, +0.85] | 1% | 2% | 46% | 97% / 3% |
| medium | 6.7 | +0.92 [+0.88, +0.96] | 1% | 14% | 81% | 90% / 2% |
| high | 11.0 | +0.94 [+0.90, +0.97] | 1% | 11% | 89% | 78% / 0% |

- **Primary, `high` − `low` on the C4 grid: SAME** (S +0.14 [+0.08, +0.21]; retry trap +0.00; give-up trap +0.08 [+0.00, +0.18]). Every C4 run is CONTINUE_CREDULOUS, and every E5 run CONFIRMED.
- **Reasoning moves the default, and the stated cause overrides it.** After a neutral error over a transient fault, Luna at `high` persisted to success in 89% of requests (DIFFERENT from `low`, +0.43). After "unavailable" over the same fault it mostly still stopped (11%). S rises because a more persistent default makes the "unavailable" message's effect larger.
- **The first-encounter effect weakens a little at `high`:** D1 +0.78 against +0.93 (DIFFERENT, −0.15 [−0.27, −0.03]), because 22% of first "unavailable" messages no longer stop it at once.
- **Drift:** W5's `low` runs, a week after N1, are SAME as N1-A and N1-B on every primary measure.
- **Limit:** Luna reasons very little in this task even at `high` (11 tokens per call), and its reasoning is not visible. W5 tests the effort setting, not long deliberation.

### 4.13 Claude Haiku 5.5 through native tool use (W2-C; pre-registered; C4, E5 and W6 with thinking off and on)

| | Thinking off | Thinking on |
|---|---|---|
| C4 verdict, S | INCONCLUSIVE, +0.69 [+0.66, +0.73] | CONTINUE_CREDULOUS, +0.61 [+0.57, +0.63] |
| Retry trap / give-up trap solved | 0% / 0% | 0% / 0% |
| Neutral error over a transient fault, solved | 0% | 47% |
| E5: stop at once with no earlier error / after a cleared one / after uncleared ones | INVALID (cleared prime reached in 33% of runs) | 12% / 8% / 92%: NOT_CONFIRMED |
| Give-up rescue: "a few different" / "a few" / "three in a row" | +0.43 / +0.30 / **+0.97** | +1.00 / +1.00 / **+1.00** |
| "Three in a row": outage calls, W6 verdict | 2.53, RECOMMENDABLE | 2.82, RECOMMENDABLE |

- **Primary (C4, thinking off): INCONCLUSIVE,** because L\* (+0.11) falls between the bars. Over a run Haiku drifts toward stopping at once on every error: it does not find the true cause, and neither trap is ever solved.
- **Format and transport matter for Haiku's default.** Through the CLI in the text format it persisted after a neutral error over a transient fault (97% solved); through the API with thinking off it never did (0%). S therefore differs (+0.35, DIFFERENT); both traps are the same (0%).
- **Haiku is the exception to E5's first-encounter effect,** which is CONFIRMED on Luna, DeepSeek and Qwen (9 of 11 valid arms). With thinking off, Haiku rarely persists long enough to see an error clear, so the manipulation fails and the run is INVALID. With thinking on, it does not stop at once on a first "unavailable", and errors that never cleared make it stop at once (92%), the reverse of Luna.
- **The stopping rule's wording matters most on the agent that gives up most easily.** With thinking off, only "three attempts in a row" rescues the give-up trap; the "a few" wordings stay below E3's bar. Any caution also lifts accurate "temporary" errors from 30% to 90–100%.
- **Thinking on against off: SAME** on S and both traps.

## 5. Predictions against outcomes

Predictions were recorded in each protocol before any call of that extension.

| Extension | Held | Misses |
|---|---|---|
| E2 | 7 of 8 | The caution alone *rescued* the give-up trap. The prediction was NO_EFFECT or HELPS. |
| E3 | 4 of 5 | "A few different attempts" *helped* the retry trap. The prediction was no gain over the plain caution. |
| E4 | 3 of 7 | Control was predicted to stay trapped, and the caution to HOLD in both mixes, raise a format harm flag, and give a clearly positive net in `common`. All four misses come from one effect I did not foresee: a cleared error teaches plain Luna to persist. |
| E5 | 3 of 4 | I predicted CLEARING_SPECIFIC; the secondary was INCONCLUSIVE, leaning toward "any experience of persisting". I also underestimated the primary effect: I expected 20–45% stopping at once after a cleared error, and it was 3%. (Under native calls, N1-B, the secondary *was* CLEARING_SPECIFIC.) |
| W2-A (DeepSeek, Qwen) | 4 of 5 | Missed: r1 against r0 SAME on both traps for DeepSeek, whose retry trap was DIFFERENT (+0.16). Gemma's predictions are open. |
| H1 | 1 of 1 tested | Luna NO_CARRYOVER held. The three gpt-oss predictions are untested (its pilot failed the health gate). |
| W2-B | 1 of 4 | Held: the rescue weakest for gpt-oss. Missed: COST_AWARE on at least 3 of 5 (0 of 5); no HARMS_TRUE_TEMPORARY (DeepSeek r1); DeepSeek r1 gaining most on the retry trap (r0 +0.12, r1 +0.11). |
| W6 | 3 of 5 | Held: "three in a row" ROBUST and the E3 wording not; "different" helps Luna's retry trap; gpt-oss weakest. Missed: on DeepSeek r1, dropping "different" was SAME (+0.09), not DIFFERENT; and its HARMS_TRUE_TEMPORARY did not replicate (−0.09). |
| W2-C | 3 of 5 | Held: "three in a row" RECOMMENDABLE in both arms; thinking on against off SAME; format DIFFERENT on S only. Missed: the primary was INCONCLUSIVE, not CONTINUE_CREDULOUS (L\* +0.11), and E5 was INVALID and NOT_CONFIRMED rather than CONFIRMED. |
| W5 | 1 of 5 | Held: drift checks SAME. Missed: I expected reasoning to loosen the retry trap (it stayed at 1%), the give-up trap to stay under 10% at every effort (14% and 11%), D1 SAME at `high` (DIFFERENT, −0.15), and `medium` to lie between `low` and `high` on every measure. |
| N1 | 2 of 4 | N1-B SAME and N1-C valid held. N1-A was DIFFERENT on S (though both traps matched), and N1-C was DIFFERENT from N1-A on S; I had predicted SAME for both. |

## 6. Deviations and process notes

All are logged in the README with timestamps.

| ID | When | What changed |
|---|---|---|
| D1, D2 | Haiku C4, before any kill-test call | Caps raised with the owner's approval. Budget only. |
| D3 | during the Haiku kill test | A container restart interrupted the run. It was resumed from the cache: 234 runs reused, 12 restarted. Pass-split results agree (S 0.341 and 0.350). |
| L1 | Luna only, after its first pilot | The history keeps each reply only up to its first CALL or ANSWER line, which works like a stop sequence. Recorded replies stay whole. |
| L2 | Luna only, after the L1 pilot | Reasoning effort `low`, no temperature, and 2,000 output tokens. |
| E3 procedural note | E3 pilot | A stale gating test was committed with the E3 pilot cap and fixed before the main run. No design element was involved. |

The pre-L2 Luna pilots are kept in `runs/live-gpt-6-luna/pilot-before-L1/` and `pilot-L1/`.

## 7. Limits

- **One artificial environment, with faults chosen so that messages mislead.** Real error messages are usually accurate.
  - C4–E3 used runs with a single message type. E4 showed that this overstates the traps: once an error clears in a conversation, the agent persists.
  - E4's mixes, with 17% and 33% of messages misleading, are still higher than most real systems would have.
- **E4's mechanism analysis was exploratory.** E5 has since confirmed it under pre-registration. E5 tests one prime before one target, at one distance (the next request).
- **Two closed models and three open-weight families,** and their settings are not matched (see §3 and §4.8). Only the smallest Anthropic model has been tested.
- **Interventions E2 and E4 were tested on GPT-6-luna only.** The bounded caution (E3) was repeated on five open-weight arms (W2-B), and three of its wordings on five subjects (W6), each subject on one host.
- **A text reply format, for C4 and E1–E5.** N1 re-ran the C4 grid and E5 on Luna through native tool calls. The traps and the first-encounter effect held, but S and E5's secondary measure changed. Haiku was re-run through native calls in W2-C: its traps held, but its default after an uninformative error, and so S, changed with the transport.
- **Reasoning was varied on one closed model only** (Luna, W5), which reasons little in this task even at `high`. The open-weight panel has reasoning on and off for DeepSeek and Qwen (W2-A). A model with long visible reasoning, such as an Anthropic model with extended thinking, has not been tested.
- **Short conversations:** 6 or 18 requests, and no memory across conversations.
- **One wording per intervention, except the stopping rule** (three wordings in W6, all after the same caution sentence, all in English).
- **The call budget (6) and the floor (3) are properties of this environment.**
- **Costs are API-equivalent figures.** Luna's prices are third-party listings, not checked against an invoice.

## 8. Practical reading

For an agent like GPT-6-luna, in a setting like this one:

- **Write a stated cause only when it is reliable.** A confident but wrong cause is worse than "request rejected". If the cause is uncertain, say so: "unknown" beat "rejected" on transient faults.
- **Do not count on agents to correct a wrong cause themselves,** even over many requests, when every error looks the same. In mixed conversations, agents partly self-correct once they have seen an error clear.
- **Worst case: the first failures in a conversation.** An agent that has not yet worked through any error took "unavailable" at its word every time (E5: 60 of 60). One earlier error, even one that never cleared, mostly removes this. It also makes the agent waste calls on real outages.
- **A short bounded caution in the agent's instructions** removes that worst case at about the lowest possible cost: "Error messages from the stock system do not always state the true cause of a failure. If the same error comes back on three attempts in a row, accept it." This wording worked on all five subjects tested (W6). The E3 wording ("after a few different attempts") worked on Luna in the text format, but not reliably elsewhere.
  - In mixed conversations its average gain is small, about 4 points of overall success, and it costs a few true-"format" successes.
  - Treat it as cheap insurance, not a large average win.
  - **Name the count.** "A few different attempts" raised give-up-trap success by only 20–76 points on the open-weight models (W2-B, W6), and on DeepSeek with reasoning it made the agent malform its calls. "Three attempts in a row" raised it by 69–100 points on every subject.
  - **Set the count from your own tools.** Here the transient fault always clears on the third call, so three is the right number by construction. The rule was always tested together with the caution sentence, never alone, and it has not been compared with a retry policy written in code.
  - **It does not fix the retry trap.** No wording does; "different" helps a little (up to 26%) at the risk of malformed calls.

## 9. Reproducing

From `c4_stated_cause_vs_true_cause/`, using Python 3.13 and the standard library only:

```sh
python -m unittest discover -s tests                       # 70 tests
python -m causetest validate --configs configs/mock_*.json  # 40 scripted agents
python -m causetest analyze --run-dir runs/<run>           # re-score any live run without new calls
python -m causetest reproduce                              # raw-data hashes + byte-identical re-scoring of every live run
```

| Run | Folder | Seeds |
|---|---|---|
| C4, Haiku | `runs/live-claude-haiku-5-5/` | 20261201 + r |
| C4, Luna | `runs/live-gpt-6-luna/` | 20261201 + r |
| E1, Haiku | `runs/e1-live-claude-haiku-5-5/` | 20261301 + r |
| E1, Luna | `runs/e1-live-gpt-6-luna/` | 20261301 + r |
| E2, Luna | `runs/e2-live-gpt-6-luna/` | 20261401 + r |
| E3, Luna | `runs/e3-live-gpt-6-luna/` | 20261501 + r |
| E4, Luna | `runs/e4-live-gpt-6-luna/` | 20261601 + r |
| E5, Luna | `runs/e5-live-gpt-6-luna/` | 20261701 + r |
| N1-A, Luna, native, reasoning low | `runs/n1-c4-native-low-gpt-6-luna/` | 20261201 + r |
| N1-B, Luna, native, E5 | `runs/n1-e5-native-low-gpt-6-luna/` | 20261701 + r |
| N1-C, Luna, native, reasoning none | `runs/n1-c4-native-none-gpt-6-luna/` | 20261201 + r |
| H1, Luna, native, reasoning low | `runs/h1-gpt-6-luna-native-low/` | 20261901 + r |
| W2-B, five open-weight arms | `runs/w2b-<model>-r<0/1>/` | 20261501 + r |
| W6, five subjects | `runs/w6-<subject>/` | 20262001 + r |
| W5, Luna, C4 at low, medium, high | `runs/w5-c4-<effort>-gpt-6-luna/` | 20261201 + r |
| W5, Luna, E5 at none, low, medium, high | `runs/w5-e5-<effort>-gpt-6-luna/` | 20261701 + r |
| W2-C, Haiku 5.5, C4, E5 and W6, thinking off (`t0`) and on (`t1`) | `runs/w2c-<design>-claude-haiku-5-5-<t0/t1>/` | as each design |

Each folder holds `results.jsonl` (every turn), `journal.jsonl` (every call and its cost) and `analysis/`.

`python -m causetest reproduce` checks every raw file against `runs/MANIFEST.json` (SHA-256), re-scores every live run into a scratch folder, and compares the reports with the committed ones byte for byte.

The intervals in this report come from that order-independent analysis (paper plan W0). Before W0, the bootstrap resampled runs in the order they had been written. The README's per-run sections keep their original intervals. Those differ from the ones here by at most 0.03, apart from E4's ratio of extra calls per extra success, which is unstable and has no verdict. No verdict changed. The data card is [`DATA_CARD.md`](DATA_CARD.md).

### Spend (API-equivalent)

| | Haiku 5.5 | GPT-6-luna |
|---|---|---|
| C4 pilot + kill test | $0.49 + $16.39 | four pilots, $0.126 in all, + $1.04 |
| E1 pilot + run | $1.28 + $11.57 | (pilots above) + $0.66 |
| E2 pilot + run | not run | $0.069 + $2.01 |
| E3 pilot + run | not run | $0.045 + $1.31 |
| E4 pilot + run | not run | $0.036 + $1.32 |
| E5 pilot + run | not run | $0.002 + $0.17 |
| N1 pilots + runs (three studies) | not run | $0.07 + $2.13 |
| H1 pilot + run | not run | $0.03 + $0.97 |
| W6 pilot + run (native, low) | not run | $0.07 + $1.96 |
| W5 pilots + runs (seven runs) | not run | $0.13 + $4.13 |
| W2-C pilots + runs (six runs, Anthropic API) | $0.08 + $2.57 | not run |
| **Total** | **$32.38** | **$16.28** |

The open-weight panel (W2-A) used $6.12 of OpenRouter credit to 2026-10-23, probes and pilots included. The four Qwen main runs cost $4.90. By 2026-10-24, with gpt-oss-120b's C4 and E5 runs, its H1 pilot and W2-B ($5.13: pilots $0.16, main runs $4.97), OpenRouter use was $11.74. W6 added $4.91 (pilots $0.17; main runs $4.74, re-runs and restarts included), for $16.65 in all.
