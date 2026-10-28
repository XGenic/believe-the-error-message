# C4: Do agents believe error messages? (kill test)

> **This is the lab notebook,** in the order things happened: approvals, pilots, deviations and results, study by study. It was this folder's `README.md` until 2026-10-28, so protocols and reports written before then call it `README.md`. The overview is in [`README.md`](README.md), and the consolidated results in [`REPORT.md`](REPORT.md).

When a tool call fails, does an agent choose how to recover by the cause the error message *states*, or by the cause that is *true*? And does it learn to distrust a stated cause that keeps proving wrong?

The test crosses four error texts with three true faults. The error texts are:

- "the SKU is not written the way this depot's system expects";
- "temporary service problem";
- "stock data for this depot is unavailable";
- a neutral "request rejected".

The true faults are fixable (a spelling convention), transient (the first two calls fail) and permanent. That makes 12 cells. The test records what the agent does after each failure.

The old sources are the misattribution paradigm (Schachter & Singer 1962; Storms & Nisbett 1970) and Weiner's attribution dimensions (1979). C4 grew out of C3's tuning observations.

- Design handoff: [`ai_experiment_handoffs/claude_set/C4_stated_cause_vs_true_cause_in_tool_errors.md`](../ai_experiment_handoffs/claude_set/C4_stated_cause_vs_true_cause_in_tool_errors.md)
- Frozen design, measures and decision rule: [`PROTOCOL.md`](PROTOCOL.md)
- **Consolidated write-up of C4 and E1–E5: [`REPORT.md`](REPORT.md)**
- **Plan toward a submittable paper: [`PAPER_PLAN.md`](PAPER_PLAN.md)**

This folder holds everything for the experiment: code, configs, tests, mock validation and live runs. "Believes", "credulous" and "distrust" name behavioral patterns only.

## Resume here: public release and the Anthropic application (2026-10-28)

- **Public repository:** [github.com/XGenic/believe-the-error-message](https://github.com/XGenic/believe-the-error-message), made public on the owner's word on 2026-10-28. It holds this folder without the per-run caches, as one commit by Denis Gurskiy (GitHub no-reply address). Code under MIT, data and documents under CC BY 4.0. Tests and `reproduce` pass there.
- **Preprint draft:** [`paper/PAPER.md`](paper/PAPER.md).
- **Anthropic External Researcher Access:** a proposal for $1,000 to run Claude Sonnet 5.5, Opus 5.5 and Fable 5.1; the owner submits it before the November 2 review.
- **Keeping the two in step:** this folder is the source. Changes are made here, then copied to the public repository.

## Earlier note: study W2-C done (2026-10-28)

- **The Anthropic transport** (`anthropic_messages_native` in `causetest/transports.py`) works live: Claude models through the Messages API with native tool use.
- **Study W2-C is done** (Claude Haiku 5.5, thinking off and on; $2.65): both traps hold (0%), "three attempts in a row" is RECOMMENDABLE in both arms, and E5's mechanism does not apply to Haiku. See "W2-C results" and `REPORT.md` §4.13.
- **Its key** is `ANTHROPIC_API_KEY` in this folder's `.env` (gitignored, never printed).
- **Branch:** `c4-anthropic-native`, cut from main after PR #29. Pushed and merged to main on the owner's word, 2026-10-28.

## Earlier note: studies W6 and W5 done (2026-10-27)

- **Study W5 is done** (Luna's reasoning effort, under the owner's delegation): more reasoning does not get Luna out of either trap (primary SAME). See "W5 results" and `REPORT.md` §4.12.
- **Also done at $0:** the panel table (`python -m causetest panel`, [`runs/panel/PANEL.md`](runs/panel/PANEL.md)) and two paper figures in [`figures/`](figures/).
- **Branch:** `c4-w5-reasoning` (W6, W5, the panel table and the figures; it contains `c4-w6-wording`). Pushed and merged to main on the owner's word, 2026-10-27.

## Earlier note: study W6 done (2026-10-27)

- **Study W6 is done:** all five subjects valid. "Three attempts in a row" is ROBUST (RECOMMENDABLE on 5 of 5); neither "a few" wording is. See "W6 results" and `REPORT.md` §4.11. The runs are pinned in `runs/MANIFEST.json`.
- **Qwen r0** finished on 2026-10-27 after the W6-2 restarts.
- **Branch:** `c4-w6-wording`, cut from main after PR #28.
- **Owner's delegation (2026-10-27, in chat, before leaving the machine without remote access):** "I will delegate any follow ups to you to run (i.e. redoing a subset of runs or the like). You have permission to use up the remaining credits in openrouter if need be. If you need to do another Luna run, you can do that as well. Basically you can go ahead and work through any pending work short of us starting the big-boy test runs of the frontier models."
  - **Read as:** follow-up and re-runs for W6 within the frozen procedure; any remaining OpenRouter credit; Luna runs on the OpenAI key; and pending $0 work from `PAPER_PLAN.md`.
  - **Not covered:** frontier-model runs (the Anthropic and Google transports, the W2 frontier panel), pushing and merging.
  - Each new live study is still frozen and committed at $0 first, with its cap recorded here before any call.

## Earlier pause note (2026-10-24, before W6; superseded by the section above)

- **Done on 2026-10-24:**
  - gpt-oss-120b's C4 run (on a second host, W2-7) and its E5 run;
  - study H1 on Luna: NO_CARRYOVER. gpt-oss's H1 run stopped at the pilot health gate (owner's decision);
  - study W2-B: the bounded caution on all five open-weight arms, all valid, no COST_AWARE. See "W2-B results".
- **Branch:** `c4-h1-withdrawal` held H1 and W2-B. It was merged to main as PR #28 on 2026-10-24.
- **The W2-B runs are pinned:** `runs/MANIFEST.json` covers them, and `reproduce` passes.
- **OpenRouter credit:** $8.26 of $20.
- **Open options:**
  - W6, wording variants of the bounded caution. W2-B makes this more pressing: on DeepSeek r1 the word "different" made the agent malform its calls;
  - Anthropic and Google native transports (keys needed);
  - the W5 reasoning sweep, the cross-model analysis, and W3 benchmark injection.

## Earlier pause note (2026-10-23; superseded by the section above)

- **Done:**
  - all four DeepSeek V4.1 Flash runs, all valid after W2-4 and W2-5, with their Luna comparisons; see "Study W2-A: results so far";
  - the probes, and the pilots for DeepSeek and Qwen.
- **Done on 2026-10-23: the four Qwen3.8-27B main runs** (results in "Study W2-A: results so far"). They took about 1.5–2 hours, with no host stalls, and the credit check passed before each run. All six pre-registered Qwen comparisons are in `runs/w2-comparison/`.
- **Owner's go-ahead, recorded 2026-10-23 before any Qwen main-run call.** Start the four Qwen main runs under their existing caps and `w2_runner.py`'s credit rule. Credit at launch was $18.78; after the runs it was $13.88.
- **Next:**
  1. **Done 2026-10-23 (owner's go-ahead):** the W2 runs are pinned. `runs/MANIFEST.json` now covers 167 raw files across 19 live runs, and `reproduce` passes.
  2. **Decide on Gemma** (below), then the cross-model analysis of the panel (paper plan W2). Anthropic and Google native transports are still to be built.
- **Gemma 4 31B is dropped** (deviation W2-6, owner's decision 2026-10-23). **gpt-oss-120b is added in its place** (one arm, r1): probe, then pilots, then main runs, with caps $4 (C4) and $1 (E5).
- **The key** is read by `w2_runner.py` from `.env` or `.env.txt` in this folder. Both names are gitignored.

## Earlier pause note (2026-10-20; superseded by the section above)

- **Where things stand:**
  - C4, extensions E1–E5, and phase 1 of the paper plan (W0, W1/N1, W4) are complete and merged.
  - The consolidated results are in [`REPORT.md`](REPORT.md), and the road to a paper is in [`PAPER_PLAN.md`](PAPER_PLAN.md) (§9 has the phase-1 outcome).
  - Nothing is running, and no config has an open budget beyond what has already been spent.
  - Spend to date: about $38.70 API-equivalent ($29.73 on Haiku, $9.00 on Luna).
- **Check the repository is intact,** from this folder (no network):

  ```sh
  python -m unittest discover -s tests
  ```

  ```sh
  python -m causetest reproduce
  ```

  Expect 61 tests to pass, and `reproduce` to report `"passed": true` for all 11 live runs.
- **Next: phase 2 (the panel of models).** The owner decides:
  1. which models are in the panel;
  2. the budget ceiling;
  3. whether an Anthropic API key is available (Haiku and Sonnet need a native Messages-API transport);
  4. whether to apply for API credits (see "Funding" in `PAPER_PLAN.md`).
- **Phase 2's first engineering step:** native tool-call transports for Anthropic, Google and an open-weight provider, modelled on `OpenAINativeTransport` in `causetest/transports.py`. Then pre-register and run the reduced core design per model (`PAPER_PLAN.md`, W2).
  - **The OpenRouter transport is built and tested (2026-10-22, no live call).** It covers the open-weight models and can also serve Google's. See "Paper plan, phase 2: the OpenRouter transport" below. The Anthropic transport is not built.
  - **A proposed open-weight panel is waiting for approval:** 6 models, 10 reasoning arms and 20 configs with $0 caps, estimated at about $91 in total. See "Phase 2: proposed open-weight panel" below.
- **The working pattern used so far:**
  1. freeze the protocol and configs with a $0 cap, and commit;
  2. validate on scripted agents and run power checks;
  3. set the caps the owner approved;
  4. run a pilot, check its health, then the main run;
  5. write the results up in the README and `REPORT.md`;
  6. open a PR and merge it.
- **The API keys** are read from `.env` (`OPENAI_API_KEY`, `OPENROUTER_API_KEY` for OpenRouter runs, and `ANTHROPIC_API_KEY` for the Anthropic transport). It is gitignored and never committed. Launch live runs from this folder; a background shell may start elsewhere (see the N1 procedural note).

## Status

- **Instrument:** built and tested. All 79 unit tests pass (C4, extensions E1–E5, studies H1, W2-B, W2-C, W5 and W6, the panel table, the Anthropic transport, the Luna settings, reproducibility, native tool calling, and the OpenRouter transport).
  - Forty scripted agents give the expected verdicts at the planned sizes. See [`runs/validation/VALIDATION.md`](runs/validation/VALIDATION.md).
    - C4's six are credulous, credulous-superstitious, evidence learner, message-blind, non-engager and format violator.
    - E1's four are credulous, slow learner, entrencher and non-engager.
    - E2's four are deaf, prompt-responsive, instruction-follower and non-engager.
    - E3's five are bounded, unbounded, overcautious, deaf and non-engager.
    - E4's four are bounded, unbounded, deaf and non-engager.
    - E5's four are credulous, clear-learner, exposure-learner and non-engager.
    - H1's five are persistent, helpless, failure-counter, fatigue and non-engager.
    - W2-B's three are bounded, unbounded and deaf.
    - W6's five are bounded, different-harms, unbounded, deaf and non-engager.
  - This line said "eleven" and "C4's seven" before E2. The configs only ever held six C4 agents.
  - Power is in [`runs/validation/power.json`](runs/validation/power.json).
  - These runs are MOCK and are not evidence about any model.
- **Owner's choice, recorded 2026-10-20 before any live call:**
  - The development pilot is approved on Claude Haiku 5.5 (`configs/live_claude_haiku.json`), with a $1 API-equivalent cap that covers the pilot only (D1).
  - The kill test, and its cap, will be decided after the pilot has measured the per-call cost.
- **Development pilot (2026-10-20; not evidence; one run per cell on development seed 20269201):** [`runs/live-claude-haiku-5-5/pilot/PILOT.md`](runs/live-claude-haiku-5-5/pilot/PILOT.md).

  | Measure | Pilot result |
  |---|---|
  | Runs complete | 12 of 12 |
  | Agent calls | 296 (24.7 per run) |
  | API-equivalent cost | $0.49, so **$0.00166 per call** |
  | Protocol failures | 2.7% of turns |
  | Called the tool on request 1 | every run |
  | Latency per call | median 4.6 s; one stall of 272 s, under the 480 s timeout and over C3's old 240 s |

  - **The protocol failures** were CLI artifacts seen in C3, each answered by the reminder:
    - stray `<reasoning_effort>` and `<br>` lines;
    - one tool call written in the CLI's own `<invoke>` syntax;
    - one 13,098-character reply of blank lines.
  - **Kill-test estimate from the pilot:** 360 runs × 24.7 calls × $0.00166, about **$14.75 API-equivalent**, and about 75–90 minutes.
- **Kill test (owner's approval, recorded 2026-10-20 before any kill-test call):** Haiku 5.5 at 30 runs per cell, with a $22 API-equivalent cap covering the pilot and the kill test together (D2).
- **Kill test: run on 2026-10-20. [CONTINUE_CREDULOUS](runs/live-claude-haiku-5-5/analysis/VERDICT.md).**
  - **Size:** 360 of 360 runs completed, 100% in every cell.
  - **Interruption:** the run was interrupted once by a container restart and resumed (D3).
  - **Transport:** 2 CLI timeouts, both re-run cleanly.
  - **Protocol failures:** 1.4% of turns, all CLI artifacts.
  - **Every run called the tool on request 1.**
  - **Cost:** $16.39 API-equivalent, plus $0.49 for the pilot, against the $22 cap.

## Results: Haiku 5.5 (CONTINUE_CREDULOUS)

| Primary measure | Value | Rule |
|---|---|---|
| **Steering S** | **+0.344** [+0.322, +0.367] | CONTINUE needs at least 0.25, with a lower bound of at least 0.10 |
| **Learning L\*** | **−0.004** [−0.058, +0.052] | credulous: below 0.10, with an upper bound below 0.20 |

The error message's stated cause sets Haiku's recovery strategy, and nothing changes over six requests of contrary evidence.

**Success over all 180 requests of each cell, with mean calls per request in parentheses.** Rows are the message shown; columns are the true fault.

| Message ↓ / true fault → | fixable | transient | permanent |
|---|---|---|---|
| "the SKU is not written the way this depot's system expects" | **0.97** (2.7) | 1.00 (3.0) | 0.00 (3.1) |
| "temporary service problem" | **0.00** (5.4) | 1.00 (3.0) | 0.00 (5.3) |
| "stock data for this depot is unavailable" | **0.00** (1.8) | **0.00** (1.7) | 0.00 (1.8) |
| "request rejected" (neutral) | 0.10 (2.4) | 0.97 (3.0) | 0.00 (2.2) |

**What the table shows:**

- **A false "temporary" turns a fixable fault into a permanent failure.**
  - Over a spelling fault, Haiku retried the identical call 5.4 times per request and succeeded on 0 of 180 requests.
  - It never once changed the SKU's spelling, and every first response on requests 2–6 was RETRY.
  - Under the neutral message it at least sometimes explored, and solved 18 of 180.
- **A false "unavailable" makes Haiku give up on a fault that one more call would clear.**
  - Over a transient fault (the third call works), Haiku stopped after about 1.7 calls, and succeeded on 0 of 180 requests, against 97% under the neutral message.
  - Its stopping grew over the run: STOP as the first response rose from 3 of 30 runs on request 1 to 13 of 30 by request 6.
- **H4, talked out of a fixable fault, is confirmed.** Under "unavailable" over a fixable fault, Haiku never reformatted in 180 requests, and succeeded 0 times against the neutral message's 18.
- **The format claim helps when it is true and wastes calls when it is not.**
  - It solved 97% of fixable requests.
  - Under a permanent outage it kept reformatting, about 3 calls per request. It noticed ("every SKU I've tried at every depot has been rejected with the same error") without changing what it did. STOP rose only from 0 to 4 of 30 by request 6.
- **Why S is 0.34 and not higher.** On request 1, the first response to "temporary" and to "unavailable" is RETRY, which is also Haiku's neutral default, so those four Δ values are about 0. All of S comes from the format claim (Δ = 1.00 in both of its misleading cells). The two outage claims act on *how long* Haiku keeps trying, not on its first move. That is measured by H3:
- **H3 (Weiner's stability → expectancy) holds strongly.**
  - On requests 5–6, the stable "unavailable" claim gave fewer calls per request than the unstable "temporary" one, by 3.45 for fixable faults, 1.38 for transient and 3.35 for permanent.
  - Under the neutral message, Haiku's first responses diversified over the run (depot written differently, reformat). Under every specific claim they stayed locked.

**Checks:**

- **Pass split.** The first pass gave S 0.341 and L\* +0.003; the resumed pass gave S 0.350 and L\* −0.019. The interruption did not shift anything.
- **No fabrication.** There were 0 unsupported answers and 0 fabricated RESULT lines.
- **Superstition probe: null.** Under the format claim over a transient fault, 53% of later requests open with a changed spelling, against 55% under the neutral message (index −0.02). No claim-induced superstition beyond Haiku's own exploration.
- **Cause language was rare** (at most 24% of requests in any cell), mostly echoes of the error text.

**What this does not show:**

- whether other models behave the same (one model only);
- whether learning appears after more than six requests;
- how agents respond to messages that mix a cause with an instruction, as real services often do.

## Extension E1: longer runs (frozen; [`PROTOCOL_E1.md`](PROTOCOL_E1.md))

**Owner's request, 2026-10-20:** run the Haiku extension with longer runs.

**Design:**

- **Length:** 18 requests per run instead of 6.
- **Cells:** four. These are C4's two headline traps, "temporary" over a fixable fault and "unavailable" over a transient fault, each paired with the accurate cell for the same claim.
- **Size:** 12 runs per cell planned.
- **Measure:** whether following a misleading claim fades (LEARNS), stays (NO_LEARNING) or grows (ENTRENCHMENT) from requests 1–3 to 16–18, compared with the accurate cell.

**Budget.** Per-call cost grows with conversation length, so a run's cost grows roughly with the square of its length. The full grid at 18 requests would cost about $33–50; this four-cell design is projected at about $19.

- A pre-registered 4-run pilot measures the cost first.
- A fixed rule then caps runs per cell so that the estimate stays under $20.
- One $22 cap covers the pilot and the run, the same ceiling the owner approved for the C4 kill test (`configs/live_e1_claude_haiku.json`).

**Status:** run on 2026-10-20.

- **Pilot:** 4 runs, $1.28. The sizing rule kept 12 runs per cell.
- **Main run:** 48 of 48 runs complete, with no transport errors and protocol failures at 0.4% of turns. It cost $11.57 API-equivalent, so $12.85 in total against the $22 cap.

### E1 result: [NO_LEARNING](runs/e1-live-claude-haiku-5-5/analysis/VERDICT.md)

**L_E1 = +0.056 [−0.042, +0.167].** Three times the contrary evidence did not loosen Haiku's hold on a false stated cause. Its behavior on requests 16–18 matches requests 1–3.

| Cell | Follows the claim (requests 1–3 → 16–18) | Success, all 216 requests | Calls per request (start → end) | Requests reaching a 3rd call |
|---|---|---|---|---|
| "temporary" over a **fixable** fault (retry trap) | 1.00 → 1.00 | **0 / 216** | 5.6 → 4.8 | 214 / 216, all identical retries |
| "temporary" over a transient fault (accurate) | 1.00 → 1.00 | 216 / 216 | 3.0 → 3.0 | 216 / 216 |
| "unavailable" over a **transient** fault (give-up trap) | 0.19 → 0.25 | **0 / 216** | 1.8 → 1.8 | **0 / 216** |
| "unavailable" over a permanent fault (accurate) | 0.08 → 0.25 | 0 / 216 | 1.9 → 1.8 | 0 / 216 |

**The retry trap holds for all 18 requests.**

- No run ever changed the SKU's spelling: 0 of 12 runs reformatted.
- Haiku notices the repetition within a request but keeps framing it as temporary: "I've tried this lookup five times and the stock service returned 'temporary service problem' each time… I can't get the figure right now." The next request goes the same way.

**The give-up trap seals itself.**

- Under "unavailable", Haiku retries once and stops. It never reached the third call that would have succeeded: 0 of 216 requests.
- So no contrary evidence ever arrives, and its behavior is the same whether the claim is false (transient fault) or true (permanent fault).
- The +0.11 contrast for this claim reflects a difference in early stopping (0.19 against 0.08 on requests 1–3), not learning. Both cells end at 0.25.

**What "runs ever deviating 12/12" means in the "unavailable" cells:** the claim implies STOP, and Haiku's first response is usually one retry before stopping. That is Haiku's fixed habit, not a change over the run.

**Reading.** Within a conversation, Haiku 5.5 does not learn to distrust an error message's stated cause, even after 18 requests of contrary outcomes. A false "temporary" produces endless identical retries. A false "unavailable" produces early give-ups that never collect the evidence that would correct them.


## Replication on GPT-6-luna

**Owner's request and approval, recorded 2026-10-20 before any Luna call:**

- Replicate both designs on `gpt-6-luna`: the full 12-cell grid first, then E1.
- Each design starts with its pre-registered development pilot, under a $0.50 cap per design. The main-run caps will be set after the pilots have measured the per-call cost.

**Configs:** [`configs/live_gpt6luna.json`](configs/live_gpt6luna.json) and [`configs/live_e1_gpt6luna.json`](configs/live_e1_gpt6luna.json).

- They keep the Haiku runs' seeds, sizes, thresholds and agent-facing text.
- Only the model settings differ. Luna accepts `temperature` only with reasoning effort `none`, as recorded in C1 and C2, so both configs send `temperature: 1.0` with `reasoning: {effort: none}`.
- Prices are $0.10 input and $0.50 output per million tokens, from third-party listings.
- The transport bills all input at the uncached rate, so the recorded cost is an upper bound.

**Status:**

- **Full-grid pilot (2026-10-20; not evidence):** [`runs/live-gpt-6-luna/pilot-before-L1/PILOT.md`](runs/live-gpt-6-luna/pilot/PILOT.md).
  - All 12 runs completed: 204 calls, $0.0186, so $0.00009 per call.
  - **Protocol failures were 11.3% of turns**, above the 10% validity threshold. One run never called the tool on request 1.
- **What the failures are.** With reasoning off, Luna does not stop after a CALL line and wait for the result.
  - In 33 of its 132 replies that contain a call, it goes on to write `ANSWER UNKNOWN` after the call, before seeing the result.
  - Sometimes the call and the answer are on one line, or the call is written twice, or stray format tokens appear.
  - The parser acts on the first line, but the whole reply stays in the conversation history. Luna then usually acts on its own pre-written answer and stops after one call, even in the accurate cells.
  - So, as configured, the run would mostly measure this pre-written answer rather than the error message.
- **The owner's choice (2026-10-20): deviation L1, below.** Both pilots will be re-run with it, under the same $0.50 caps.

**Deviation L1 (Luna runs only; after the first full-grid pilot, before any other Luna call).**

- **What changes.** The conversation history keeps each Luna reply only up to and including its first CALL or ANSWER line, as a stop sequence would. The Responses API has no stop parameter, so the code does the cut itself (`history_cut_after_first_protocol_line` in both Luna configs).
- **What does not change.**
  - The agent-facing text, design, seeds and thresholds.
  - Parsing: the first protocol line already decided the action.
  - The recorded replies, which stay whole. Each call's record notes whether its reply was cut (`history_reply_cut`).
  - The Haiku configs and their results.
- **What it does not fix.** A call and an answer written on one line are not cut and still count as protocol failures.
- **Bookkeeping.**
  - The first pilot is kept, unchanged, in `runs/live-gpt-6-luna/pilot-before-L1/`.
  - Its $0.0186 is outside the spend guard's journal, so it is added by hand to the Luna totals.
  - The setting is part of the cache key only when it is on, so no earlier run's cache is affected.

**Full-grid pilot with L1 (2026-10-20; not evidence):** [`runs/live-gpt-6-luna/pilot-L1/PILOT.md`](runs/live-gpt-6-luna/pilot-L1/PILOT.md).

- All 12 runs completed: 208 calls, $0.016.
- **Protocol failures rose to 16.4% of turns.** Only 7 of 208 replies needed the cut. The failures are mostly on the first turn of a request:
  - two calls, or a call and `ANSWER UNKNOWN`, written on one line with no line break;
  - stray text that looks like Luna's own tool-calling channel, such as "assistant to=stock_lookup", or "A tool call was not actually issued since format text?";
  - every one is followed by the format reminder, which costs a turn.
- **Luna gives up after one failure in almost every cell.** It answered UNKNOWN after a single failed call even under the accurate "temporary" over a transient fault, and under the neutral message. Only "temporary" over a fixable or permanent fault drew retries. 11 of 12 cells had 0 successes.
- **Reading.** With reasoning off, the C4 text protocol does not work reliably on Luna, and L1 does not fix it. A Luna run under this protocol would measure Luna's format handling rather than its response to the stated cause.
- **The E1 pilot was not run.**
- **Luna spend so far:** $0.0186 + $0.0160 = **$0.035**, against $0.50 approved for the full-grid pilot.

**Deviation L2 (Luna runs only; owner's choice, recorded 2026-10-20 after the L1 pilot and before any further Luna call).**

- **What changes.** Both Luna configs use reasoning effort `low` instead of `none`.
  - `temperature` is dropped, because Luna accepts it only with reasoning off. Luna samples at its default.
  - `max_output_tokens` rises from 300 to 2,000, because reasoning tokens count toward it.
  - The worst-case reserve per call rises to $0.005.
- **What stays.** L1 stays on. Agent-facing text, design, seeds, thresholds and the $0.50 pilot caps are unchanged.
- **Why.** The leaked tool-channel text in both pilots points to the reasoning-off mode as the cause of the format failures.
- **Caveats.**
  - The Luna results are now from a reasoning model, unlike Haiku's no-reasoning runs. Comparisons with Haiku must say so.
  - Reasoning tokens are billed as output.
  - Request options are not part of the cache key, so the L2 pilot runs in a fresh `pilot/` folder.

**Full-grid pilot with L1 + L2 (2026-10-20; not evidence):** [`runs/live-gpt-6-luna/pilot/PILOT.md`](runs/live-gpt-6-luna/pilot/PILOT.md).

| Measure | Result |
|---|---|
| Runs complete | 12 of 12 |
| Agent calls | 304 |
| Cost | $0.035, so $0.00011 per call |
| Protocol failures | **3.9% of turns**, under the 10% threshold |
| Called the tool on request 1 | every run |
| Replies cut by L1 | 2 of 304 |
| Reasoning tokens per call | median 19, maximum 309 |

- The accurate cells now succeed: 18 of 18 requests in "temporary" over transient, format over transient and format over fixable.
- **Main-grid estimate: about $1.04.**

**E1 pilot with L1 + L2 (2026-10-20; not evidence):** [`runs/e1-live-gpt-6-luna/pilot/PILOT.md`](runs/e1-live-gpt-6-luna/pilot/PILOT.md).

- 4 of 4 runs completed: 271 calls, $0.057, so $0.00021 per call.
- Protocol failures were 0.4% of turns. Every run called the tool on request 1.
- **Main-run estimate: about $0.69.** The pre-registered sizing rule keeps 12 runs per cell.

**Luna spend so far:** $0.126 over four pilots.

**Main-run caps (budget only; owner's approval, recorded 2026-10-20 after the pilots and before any main-run call).**

- `max_equiv_usd` rose from $0.50 to $2.00 in both Luna configs, about 2× each estimate.
- Each cap covers that design's journaled pilot and main run together. The two pre-L2 pilots ($0.035) sit outside both journals.
- The full grid runs first, then E1. No design element, threshold or agent-facing text changed.

### Luna full grid: [CONTINUE_CREDULOUS](runs/live-gpt-6-luna/analysis/VERDICT.md)

**Run on 2026-10-20 with L1 + L2.**

- 360 of 360 runs completed, 9,337 calls, $1.04 API-equivalent.
- Protocol failures were 1.3% of turns. Every run called the tool on request 1, and no response was unclassifiable.

| Primary measure | GPT-6-luna | Haiku 5.5 (for reference) |
|---|---|---|
| **Steering S** | **+0.956** [+0.922, +0.983] | +0.344 [+0.322, +0.367] |
| **Learning L\*** | **+0.000** [−0.019, +0.020] | −0.004 [−0.058, +0.052] |

**Success over all 180 requests of each cell, with mean calls per request in parentheses.** Rows are the message shown; columns are the true fault.

| Message ↓ / true fault → | fixable | transient | permanent |
|---|---|---|---|
| "the SKU is not written the way this depot's system expects" | **0.96** (3.1) | 0.99 (3.0) | 0.00 (5.7) |
| "temporary service problem" | **0.00** (5.7) | 1.00 (3.0) | 0.00 (5.7) |
| "stock data for this depot is unavailable" | **0.00** (1.0) | **0.00** (1.0) | 0.00 (1.0) |
| "request rejected" (neutral) | 0.21 (3.3) | 0.67 (2.6) | 0.00 (4.0) |

**What the table shows:**

- **Luna does exactly what each message implies, on every request.**
  - Under the format claim it reformats, under "temporary" it retries the identical call, and under "unavailable" it stops after one call.
  - This holds in 30 of 30 runs on request 1 in most cells, and it does not change by requests 5–6.
- **A false "temporary" makes Luna retry until the call limit.** Over a fixable fault, it made 5.7 calls per request and never changed the spelling: 0 of 180 requests.
- **A false "unavailable" ends every request after one call.** Over a transient fault, Luna never reached the third call that would have worked: 0 of 180 requests. Under the neutral message it solved 121 of 180.
- **Why S is much higher than Haiku's.** Under the neutral message, Luna's first move is to write the depot differently. Haiku's was to retry.
  - So, unlike Haiku, "temporary" (retry) and "unavailable" (stop) each move Luna's first response away from its default.
  - Every misleading cell then gives a Δ of 0.90–1.00.
- **H3 (stability → expectancy) holds.** On requests 5–6, the stable "unavailable" claim gave fewer calls per request than the unstable "temporary" one: 4.68 fewer for fixable faults, 2.00 for transient and 4.58 for permanent.
- **H4 (talked out of a fixable fault) is confirmed.** Under "unavailable" over a fixable fault, Luna never reformatted, and succeeded on 0 of 180 requests, against the neutral message's 37.

**Checks:**

- **No fabrication.** There were 0 unsupported answers and 0 fabricated RESULT lines.
- **Superstition probe: none.** Under the format claim over a transient fault, 4% of later requests open with a changed spelling, against 30% under the neutral message (index −0.26). The claim narrowed Luna's exploration rather than adding superstitious reformatting.
- **Cause language** appeared in at most 1% of requests in any cell.

**Caveats:**

- These results are with reasoning effort `low` (L2), while Haiku's had no reasoning, and with L1's history cut.
- The Luna and Haiku numbers come from the same design, seeds and agent-facing text. They are not an exact match of model settings.

### Luna E1, longer runs: [NO_LEARNING](runs/e1-live-gpt-6-luna/analysis/VERDICT.md)

**Run on 2026-10-20 with L1 + L2.**

- 48 of 48 runs completed (12 per cell), 3,199 calls, $0.66 API-equivalent.
- Protocol failures were 1.1% of turns. Every run called the tool on request 1.

**L_E1 = +0.000 [+0.000, +0.000].** Luna followed the claim the same way on requests 16–18 as on requests 1–3, in every cell.

- The zero-width interval comes from following rates of 1.00 at both ends in almost every run. It is a degenerate bootstrap interval, not proof that the true change is exactly zero.

| Cell | Follows the claim (requests 1–3 → 16–18) | Success, all 216 requests | Calls per request (start → end) | Requests reaching a 3rd call |
|---|---|---|---|---|
| "temporary" over a **fixable** fault (retry trap) | 1.00 → 1.00 | **0 / 216** | 5.8 → 5.4 | 215 / 216, with no reformatting |
| "temporary" over a transient fault (accurate) | 1.00 → 1.00 | 216 / 216 | 3.0 → 3.0 | 216 / 216 |
| "unavailable" over a **transient** fault (give-up trap) | 1.00 → 1.00 | **0 / 216** | 1.0 → 1.0 | **0 / 216** |
| "unavailable" over a permanent fault (accurate) | 1.00 → 1.00 | 0 / 216 | 1.0 → 1.0 | 0 / 216 |

**Reading:**

- Both traps hold for all 18 requests, more rigidly than on Haiku.
- **The retry trap:** under a false "temporary", Luna retries the identical call until the limit on every request. It never tries another spelling, so it never solves the fixable fault.
- **The give-up trap:** under a false "unavailable", it stops after exactly one call every time. So it never collects the evidence, a third call that works, that could correct it.
  - Haiku's "unavailable" cells showed a habit of retrying once before stopping. Luna does not retry even once.

**Luna totals:** $0.126 for four pilots, plus $1.04 for the full grid and $0.66 for E1, so **$1.83 API-equivalent**. The approved caps were $0.50 per pilot and $2 per main run.

## Extension E2: what breaks the traps? (frozen; [`PROTOCOL_E2.md`](PROTOCOL_E2.md))

**Owner's request, 2026-10-20:** after the Luna replication, test fixes on Luna.

**Question.** Does one added sentence break the retry trap or the give-up trap, and does it matter whether the sentence goes in the agent's instructions or in the error message?

**Arms:**

- **control:** C4 as run.
- **caution:** the system prompt says error messages "do not always state the true cause of a failure".
- **caution_strategy:** the same, plus "If an approach keeps failing, try a different one."
- **mixed:** the error message keeps its false cause and adds "Check the request and try again."
- **honest:** the error message says "the cause of this failure is unknown".

**Design.**

- Each arm runs both traps and their accurate cells. The control arm also runs the neutral message.
- That makes 21 cells at 30 runs each, with six requests per run, on Luna with L1 + L2.
- The seeds are new, so the control arm also replicates the traps out of sample.

**Measures.**

- **Primary, per arm and trap:** the change in success over control. Each contrast gets one of RESCUES, HELPS, HARMS, NO_EFFECT or INCONCLUSIVE.
- **Cost, per arm:** success lost in the accurate "temporary" cell, and calls wasted in the accurate "unavailable" cell.

**Status: run on 2026-10-20 (VALID; results below).**

- All 33 unit tests pass.
- The four E2 scripted agents give the expected verdict on every contrast, and power runs reproduce them 20 of 20 times. See [`runs/validation/VALIDATION.md`](runs/validation/VALIDATION.md).
- The live config `configs/live_e2_gpt6luna.json` was committed with its cap at $0, before any E2 call.
- **Estimated cost:** about $1.86 API-equivalent with the pilot.
- **Owner's approval, recorded 2026-10-20 before any E2 call:** the E2 pilot may run under a $0.25 cap. The main-run cap is set after the pilot (budget only, no design change).
- **E2 pilot (2026-10-20; not evidence):** [`runs/e2-live-gpt-6-luna/pilot/PILOT.md`](runs/e2-live-gpt-6-luna/pilot/PILOT.md).
  - All 21 runs completed: 598 calls, $0.069, so $0.00012 per call.
  - Protocol failures were 0.8% of turns. Every run called the tool on request 1.
  - **Main-run estimate: $2.08.**
- **Main-run cap (budget only; owner's approval, recorded 2026-10-20 after the pilot and before any main-run call):** `max_equiv_usd` rose from $0.25 to $4.00, about 2× the estimate. It covers the pilot and the main run together.

### E2 result on GPT-6-luna: [VALID](runs/e2-live-gpt-6-luna/analysis/VERDICT.md). The give-up trap breaks easily; the retry trap mostly holds.

**Run:**

- 630 of 630 runs completed, 17,591 calls, $2.01, plus the $0.069 pilot, against the $4 cap.
- Protocol failures were 1.0% of turns, unclassifiable responses 0.1%. Every run called the tool on request 1.
- **The control arm replicated both traps on new seeds:** 0 of 180 requests solved in each.

**Primary: change in trap success over control, with 95% intervals.**

| Arm | Retry trap ("temporary" over a fixable fault) | Give-up trap ("unavailable" over a transient fault) |
|---|---|---|
| caution | **NO_EFFECT** +0.07 [+0.03, +0.12] | **RESCUES** +0.98 [+0.94, +1.00] |
| caution + strategy | **HELPS** +0.42 [+0.37, +0.47] | **RESCUES** +1.00 [+1.00, +1.00] |
| mixed ("…Check the request and try again.") | **NO_EFFECT** +0.00 | **HELPS** +0.27 [+0.15, +0.41] |
| honest ("the cause of this failure is unknown") | **HELPS** +0.23 [+0.18, +0.29] | **RESCUES** +0.99 [+0.97, +1.00] |

**Cost, measured on the accurate cells:**

| Arm | Δ success, true "temporary" | Δ calls per request, true "unavailable" (control: 1.0) | Cost flag |
|---|---|---|---|
| caution | +0.00 | **+4.27** | yes |
| caution + strategy | +0.00 | **+4.59** | yes |
| mixed | +0.00 | +1.23 | yes |
| honest | −0.01 | **+4.15** | yes |

**What E2 shows:**

- **One sentence in the instructions breaks the give-up trap.**
  - With only the caution, Luna stopped taking "unavailable" at its word. It kept trying and reached the third call that works on 176 of 180 requests, against 0 under control.
  - Fixing the message itself (honest) worked just as well.
- **But Luna then doubts a true outage too.** Every arm that broke the give-up trap made Luna spend about 5 calls per request on a real outage, against 1 under control.
  - The sentence did not teach Luna to tell true outages from false ones. It swapped belief for doubt.
  - In this design some extra calls are the price of checking. Luna pays nearly the whole six-call budget.
- **The retry trap is harder.** It is not only credulity.
  - The caution alone barely moved it. The +0.07 is small but its interval excludes 0; the rule calls it NO_EFFECT because it is under 0.10.
  - **Caution + strategy** made every run try other spellings, yet it solved only 42%. Its first move after a failure was always to rewrite the depot (30 of 30 runs). Most failed requests hit the six-call limit having tried only two SKU spellings.
  - **The honest message** did no better than the neutral "request rejected" over the fixable fault (difference +0.01 [−0.07, +0.08]). With no stated cause, Luna's default is to blame the depot, not the SKU.
- **A generic "try again" is the weakest fix.**
  - Over the fixable fault, "temporary… Check the request and try again" still produced identical retries: 0 of 180 solved.
  - Under "unavailable… try again", Luna tried once more and stopped. It reached a third call on only 49 of 180 requests.
- **Saying "unknown" beats saying nothing on transient faults:** the honest message minus "request rejected" was +0.34 [+0.21, +0.48]. On fixable faults there was no difference.
- **No arm hurt the true "temporary" cell.** Luna still retried and succeeded every time.

**Predictions (PROTOCOL_E2.md): 7 of 8 matched.** The exception was the caution alone on the give-up trap, which RESCUED where NO_EFFECT or HELPS was predicted.

**Limits:**

- one model, with light reasoning (L2);
- one wording per arm;
- the six-call limit shapes the retry-trap result: with more calls, caution + strategy would probably find the spelling more often.

## Extension E3: a caution with a stopping rule (frozen; [`PROTOCOL_E3.md`](PROTOCOL_E3.md))

**Owner's request, 2026-10-20:** the cost-aware caution, next after E2.

**Question.** E2's caution rescued the give-up trap but made Luna spend 5.3 calls per request on a true outage, against 1.0 under control. Does a stopping rule added to the caution keep the rescue and cut that cost?

- The floor is 3 calls, because the transient fault clears on the third.

**Arms:** control, E2's caution, and two cautions with stopping rules:

- **caution_bounded:** "…If the same error keeps coming back after a few different attempts, accept it."
- **caution_three:** "…If the same error comes back on three attempts in a row, accept it." This is fitted to this environment, so it is a best case.

**Design:** both traps and their accurate cells in every arm: 16 cells × 30 runs, on Luna with L1 + L2, on new seeds.

**Verdict per bounded arm:**

- **COST_AWARE:** keeps the rescue and saves at least 1 call per outage request against the plain caution.
- **RESCUE_ONLY**, **LOSES_RESCUE**, **NO_GAIN**, or **HARMS_TRUE_TEMPORARY** if it breaks a retry that works.

**Status: run on 2026-10-20 (VALID; results below).**

- The five E3 scripted agents give the expected verdicts.
- Power reproduces COST_AWARE and RESCUE_ONLY 20 of 20 times. An effect at the threshold splits between them, as it should.
- The live config `configs/live_e3_gpt6luna.json` was committed with its cap at $0, before any E3 call.
- **Estimated cost:** about $1.67 API-equivalent with the pilot.
- **Owner's approval (budget only), recorded 2026-10-20 before any E3 call:**
  - The pilot may run under a $0.25 cap.
  - If the pilot is healthy, the cap rises to $3.50 and the main run follows without another check-in. Healthy means: protocol failures below 10%, every run calls the tool on request 1, and the projected main-run cost below $3.
  - Otherwise the work stops and is reported.
- **E3 pilot (2026-10-20; not evidence):** [`runs/e3-live-gpt-6-luna/pilot/PILOT.md`](runs/e3-live-gpt-6-luna/pilot/PILOT.md).
  - All 16 runs completed: 421 calls, $0.045.
  - Protocol failures were 1.2%. Every run called the tool on request 1.
  - Main-run estimate: $1.35.
  - **Healthy on all three conditions, so `max_equiv_usd` rose from $0.25 to $3.50 as approved.**
- **Procedural note (no deviation).** The commit that set the pilot cap (`d8bcb92`) was made while one unit test failed: the E3 gating test still expected a $0 cap to block live calls.
  - The test was fixed before the main run. It now checks that `--live` and a cap above $0 are both required.
  - No design element or agent-facing text was involved.

### E3 result on GPT-6-luna: [VALID](runs/e3-live-gpt-6-luna/analysis/VERDICT.md). Both stopping rules are COST_AWARE.

**Run:** 480 of 480 runs completed, 12,438 calls, $1.31, plus the $0.045 pilot, against the $3.50 cap. Protocol failures were 1.1% of turns. Every run called the tool on request 1.

| Arm | Verdict | Give-up rescue (vs control) | Calls per request on a true outage | Saving vs plain caution | True-"temporary" success (vs control) |
|---|---|---|---|---|---|
| control | | | 1.00 | | |
| caution (E2's) | | +0.98 [+0.96, +0.99] | 5.24 | | +0.00 |
| caution_bounded ("…after a few different attempts, accept it") | **COST_AWARE** | +0.92 [+0.83, +0.97] | **3.08** | −2.17 [−2.52, −1.79] | −0.03 [−0.08, +0.00] |
| caution_three ("…three attempts in a row, accept it") | **COST_AWARE** | +0.97 [+0.94, +0.99] | **3.01** | −2.23 [−2.56, −1.88] | −0.04 [−0.07, −0.02] |

**What E3 shows:**

- **A stopping rule keeps the rescue at the lowest possible cost.**
  - Both bounded cautions rescued the give-up trap almost as well as the plain caution.
  - They cut outage calls from 5.2 to about 3.0, the floor for this environment: the transient fault needs a third call, and Luna cannot know which fault it faces.
  - The vague wording, "a few", worked as well as the number. Luna read it as three attempts.
- **The plain caution replicated E2 on new seeds:** rescue +0.98 and 5.24 outage calls, against +0.98 and 5.27 in E2.
- **A small cost on a true "temporary", below the harm threshold.**
  - Under caution_three, 7 of 180 requests stopped before the third call that would have worked. Success fell by 0.04, and the interval excludes 0.
  - Under caution_bounded the fall was 0.03, and the interval reaches 0.
  - Both are well inside the 0.15 harm threshold, but the counting is not perfectly reliable.
- **The two wordings change *how* Luna explores. This was not predicted.**
  - Under "three attempts in a row", Luna sent the identical call three times: no run ever respelled the SKU. So it gained nothing on the retry trap (+0.00).
  - Under "a few *different* attempts", Luna varied its calls: 28 of 30 runs respelled. It solved 29% of retry-trap requests, against 2% for the plain caution, in 3.4 calls per request.
  - E2's caution + strategy solved 42%, but needed 4.7 calls per request.

**Predictions (PROTOCOL_E3.md): 4 of 5 held.**

- Both arms were COST_AWARE, with outage calls near 3.
- Neither harmed the true "temporary".
- The plain caution replicated E2.
- **The miss:** I predicted neither stopping rule would help the retry trap. "A few different attempts" did (+0.29), because the word "different" made Luna vary the SKU.

**Taken together (E2 + E3), for this model and environment:**

- **"Error messages do not always state the true cause. If the same error keeps coming back after a few different attempts, accept it."**
- This one sentence pair rescues the give-up trap (0% to 92%), recovers part of the retry trap (0% to 29%), and costs about 2 extra calls on a real outage, the minimum possible.
- It barely affects success when the message is true.

**Limits:**

- one model, with light reasoning (L2);
- one wording per rule;
- the floor of 3 calls is a property of this environment;
- six requests per run.

## Extension E4: mixed accurate and misleading errors (frozen; [`PROTOCOL_E4.md`](PROTOCOL_E4.md))

**Owner's request, 2026-10-20:** after the write-up ([`REPORT.md`](REPORT.md)), run the mixed-errors experiment.

**Question.** Does E3's bounded caution still pay off when most error messages are accurate? And does a higher share of false messages make the agent trust them less?

**Design:**

- 12-request runs mix five request types: true "unavailable", the give-up trap, true "temporary", the retry trap and true "format".
- Each message type appears 4 times per run. Two mixes vary how many of those are false:
  - `rare`: 2 of 12 requests are misleading (17%);
  - `common`: 4 of 12 are misleading (33%).
- Arms: control and E3's bounded caution, so 4 cells × 40 runs on Luna with L1 + L2.

**Verdict per mix:**

- **HOLDS:** the rescue is kept, at about the floor cost.
- **RESCUE_ONLY** or **FADES** otherwise.
- **Harm flags** for true "temporary" and true "format". The format flag is new: a three-attempt habit can stop the spelling search too early.
- The net effect over all requests is reported without a verdict.

**Status: run on 2026-10-20 (VALID; results below).**

- The four E4 scripted agents give the expected verdicts, and power reproduces them 20 of 20 times.
- The live config was committed with its cap at $0, before any E4 call.
- **Budget (owner's instruction, 2026-10-20, to run E4 after a quoted $2–4; recorded before any E4 call):**
  - The pilot may run under a $0.25 cap.
  - If the pilot is healthy, the cap rises to $4.00 and the main run follows without another check-in. Healthy means: protocol failures below 10%, every run calls the tool on request 1, and the projected main-run cost below $3.50.
  - Otherwise the work stops and is reported.
- **E4 pilot (2026-10-20; not evidence):** [`runs/e4-live-gpt-6-luna/pilot/PILOT.md`](runs/e4-live-gpt-6-luna/pilot/PILOT.md).
  - All 4 runs completed: 214 calls, $0.036.
  - Protocol failures were 2.3%. Every run called the tool on request 1.
  - Main-run estimate: $1.42.
  - **Healthy on all three conditions, so `max_equiv_usd` rose from $0.25 to $4.00 as approved.**
- **Estimated cost:** about $1.48 with the pilot.

### E4 result on GPT-6-luna: [VALID](runs/e4-live-gpt-6-luna/analysis/VERDICT.md). Mixing message types weakens the traps by itself.

**Run:** 160 of 160 runs completed, 8,260 calls, $1.32, plus the $0.036 pilot, against the $4 cap. Protocol failures were 0.8% of turns. Every run called the tool on request 1.

**Success, and calls per request, by request type.** The pure-run figures are from C4 and E3, where every request in a run had the same message and fault.

| Request type | Control, pure runs | Control, `rare` | Control, `common` | Bounded caution, `rare` | Bounded caution, `common` |
|---|---|---|---|---|---|
| give-up trap | 0.00 | **0.45** | **0.55** | 0.97 | 0.90 |
| true "unavailable" (calls) | 1.0 | **3.1** | **3.5** | 3.7 | 3.8 |
| retry trap | 0.00 | **0.25** | **0.46** | 0.45 | 0.57 |
| true "temporary" | 1.00 | 1.00 | 1.00 | 1.00 | 0.99 |
| true "format" | 0.96 | 0.93 | 0.94 | 0.86 | 0.83 |
| all 12 requests | | 0.62 | 0.65 | 0.65 | 0.69 |

**Pre-registered verdicts for the bounded caution, against control:**

| Mix | Verdict | Give-up rescue | Extra calls, true "unavailable" | Δ success, all requests | Harm flags |
|---|---|---|---|---|---|
| `rare` | **HOLDS** | +0.53 [+0.38, +0.68] | +0.62 [−0.10, +1.40] | +0.035 [+0.002, +0.069] | none (true "format" −0.08 [−0.14, −0.01], under the 0.15 threshold) |
| `common` | **FADES** | +0.35 [+0.19, +0.51] | +0.29 [−0.44, +1.03] | +0.040 [−0.015, +0.096] | none (true "format" −0.11 [−0.19, −0.02]) |

**What E4 shows:**

- **The control arm changed most.**
  - In mixed runs, plain Luna solved about half the give-up traps and a quarter to a half of the retry traps. It spent about 3 calls on true outages. In pure runs those figures were 0, 0 and 1.0.
  - **The common-mix FADES is about the control, not the caution.** The bounded caution still solved 90% of give-up traps there. Control rose to 55%, so the gap fell below the pre-registered 0.50.
- **Why (exploratory; not pre-registered).** The deciding factor was whether Luna had already seen an error clear in the same conversation, for example a "temporary" failure that worked on the third call.
  - Before any error had cleared, control stopped at once on 89–100% of "unavailable" messages, as in the pure runs.
  - After one had cleared, it stopped at once on only 21–40%.
  - When request 1 itself was an "unavailable" message, control stopped after one call in 31 of 31 runs.
  - So Luna does learn, but not which message to distrust. It learns that errors can clear, and applies that to every message.
- **Pre-registered adaptation measures.**
  - The share of false messages did not change trust: common minus rare was −0.11 and −0.05, with intervals spanning 0.
  - Within a run, control's trust fell. Following "temporary" dropped by 0.20 [−0.32, −0.09] from requests 1–6 to 7–12 in the common mix. That meets the rule for reporting adaptation as found.
  - Smaller drops, −0.08 to −0.12, appeared for "unavailable". Their intervals exclude 0, but they are under the 0.15 rule.
  - The bounded caution never stopped at the first failure: 0 of 320 "unavailable" requests.
- **The caution's marginal cost almost disappears in mixed runs.** Control already persists, so the caution adds only +0.3 to +0.6 calls on true outages, and both intervals include 0.
  - It costs a small but real share of true-"format" successes (−0.08 to −0.11). That is under the harm threshold.
  - Its net effect over all requests is small and positive: +0.035 and +0.040.

**Predictions (PROTOCOL_E4.md): 3 of 7 held.**

- **Held:**
  - no base-rate effect in control;
  - no harm on true "temporary";
  - no adaptation under the caution.
- **Missed:**
  - "control stays trapped";
  - HOLDS in both mixes;
  - a format harm flag (the format loss was real but under the threshold);
  - a clearly positive net in `common`.

All four misses come from one thing I did not foresee: a cleared error teaches plain Luna to persist.

**What this changes:**

- **The traps in C4–E3 are worst-case conditions:** conversations in which the agent has never seen an error clear.
- **In mixed conversations,** plain Luna recovers about half of what it lost. The bounded caution's advantage shrinks to the first requests and to the agent's first move.
- **The caution remains the safer default:** it never gives up at the first failure, and it costs little. But the case for it is now insurance against early or isolated failures, not a large average gain.

## Extension E5: does one cleared error make a plain agent persist? (frozen; [`PROTOCOL_E5.md`](PROTOCOL_E5.md))

**Owner's request, 2026-10-20:** run the pre-registered test of E4's exploratory finding.

**Design.** Three-request runs on plain Luna. Only request 1, the prime, varies:

- `none`: no error at all;
- `cleared`: "temporary", which clears on the third call;
- `not_cleared`: "temporary" over a permanent fault.

Request 2 is always the give-up trap, and request 3 a true outage. 60 runs per condition, on paired seeds.

**Measures:**

- **Primary:** how often the agent stops at once on the target's "unavailable", `none` minus `cleared`.
- **Secondary:** `not_cleared` minus `cleared`, which separates the clearing from the persisting.
- **Manipulation check:** each prime must have done its job in at least 80% of runs.

**Status: run on 2026-10-20 (CONFIRMED; results below).**

- The four E5 scripted agents give the expected verdicts.
- Power: 20 of 20 for full-strength learners, and 19 of 20 for the credulous agent.
- The live config was committed with its cap at $0, before any E5 call.
- **Budget (owner's instruction, 2026-10-20, to run E5 after a quoted $1–2; recorded before any E5 call):**
  - The pilot may run under a $0.10 cap.
  - If the pilot is healthy, the cap rises to $1.00 and the main run follows. Healthy means: protocol failures below 10%, every run calls the tool on request 1, and the projected main-run cost below $0.75.
- **E5 pilot (2026-10-20; not evidence):** 3 of 3 runs completed, 32 calls, $0.002. There were no protocol failures, and every run called the tool on request 1. Main-run estimate: $0.13. **Healthy, so `max_equiv_usd` rose to $1.00 as approved.**
- **Estimated cost:** about $0.16.

### E5 result on GPT-6-luna: [CONFIRMED](runs/e5-live-gpt-6-luna/analysis/VERDICT.md). One earlier error makes plain Luna persist.

**Run:** 180 of 180 runs completed, 2,278 calls, $0.169, plus the $0.002 pilot, against the $1 cap. Protocol failures were 1.4% of turns. Every run called the tool on request 1. The manipulation check held in 100% of runs in every condition.

| Request 1 (prime) | Stopped at once on the next "unavailable" | Give-up trap solved | Calls on the target | Calls on the later true outage |
|---|---|---|---|---|
| `none`: no error | **1.00** (60/60) | 0.00 | 1.0 | 1.0 |
| `cleared`: an error that cleared on the third call | **0.03** (2/60) | 0.97 | 2.9 | 5.9 |
| `not_cleared`: errors that never cleared | **0.22** | 0.78 | 2.6 | 5.2 |

**Verdicts:**

- **Primary: CONFIRMED.** `none` minus `cleared` = +0.97 [+0.92, +1.00].
- **Secondary: INCONCLUSIVE.** `not_cleared` minus `cleared` = +0.18 [+0.07, +0.30]. That is above 0 but under the 0.30 bar for CLEARING_SPECIFIC.

**What E5 shows:**

- **Luna's trust in "unavailable" depends almost entirely on whether it has already worked through an error in this conversation.**
  - With no earlier error, it stopped at once every time.
  - After one error that cleared, it almost never did.
- **Persisting is learned mostly from the effort, not the payoff.** Errors that never cleared still cut stopping at once from 100% to 22%; `none` minus `not_cleared` = +0.78 [+0.68, +0.88]. Seeing the error clear adds 18 points on top. I had predicted it was the clearing that mattered.
- **The learned persistence is indiscriminate.** After either prime, Luna spent 5.2–5.9 calls on the true outage that followed, against 1.0 after `none`. That is the same cost as E2's caution, picked up from experience rather than instruction.
- **It is not message-specific.** The prime used "temporary" and the target "unavailable", so the effect transfers across message types.

**Predictions (PROTOCOL_E5.md): 3 of 4 held.**

- **Held:**
  - the manipulation check passed;
  - the primary was CONFIRMED;
  - calls on the later outage rose.
- **Missed:** CLEARING_SPECIFIC.
- **Magnitudes:** I also underestimated the effect. I expected 20–45% stopping at once after `cleared`, and it was 3%.

**What this changes.** The give-up trap is a first-encounter effect. A plain agent's stance toward "unavailable" is set by whether it has already worked through any error in the conversation. That is a habit of persistence, not an assessment of the message.

## Paper plan, phase 1 (owner's approval, 2026-10-20: phase 1, under $5)

### W0: reproducibility (done)

- **The analysis no longer depends on row order.** `analyze()` sorts runs by `run_id` and attempt before the bootstrap. Before this, rebuilding a run from its cache could shift interval bounds in the third decimal.
- **Every derived file is written with LF** on every platform. Raw files keep their bytes: `.gitattributes` sets `* -text`, and the Luna runs made on Windows are CRLF.
- **`runs/MANIFEST.json`** pins the SHA-256 of all 73 raw files of the 8 live runs.
- **`python -m causetest reproduce`** checks those hashes, re-scores every live run into a scratch folder, and compares the result with the committed `analysis/` byte for byte. It passes for all 8 runs.
- **Data card:** [`DATA_CARD.md`](DATA_CARD.md).
- **Deviation W0-1 (analysis only; no raw data and no verdict changed).** All live and scripted-agent reports were regenerated with the order-independent analysis.
  - Point estimates are identical.
  - Interval bounds moved by at most 0.03. E4's unstable ratio of extra calls per extra success moved more; it has no verdict.
  - Every verdict is unchanged. The Haiku kill test's L\* interval is now [−0.057, +0.051], against [−0.058, +0.052] before.
  - The per-run sections above keep their original intervals as a historical record. `REPORT.md` uses the regenerated ones.
  - `runs/validation/power.json` was produced before W0. Its verdict counts are not re-run.

### W1: native tool calling, study N1 (frozen; [`PROTOCOL_N1.md`](PROTOCOL_N1.md))

- **The new transport** `openai_responses_native` gives the model a real `stock_lookup` function. Its calls are translated to and from the unchanged episode. One sentence of the instructions changes: "To use the tool, call stock_lookup. Make one call at a time; its result comes back to you." The history cut (L1) is not needed.
- **N1-A:** the C4 grid through native calls, reasoning `low`, against the text-format C4 run.
- **N1-B:** E5 through native calls, against the text-format E5 run.
- **N1-C (secondary):** the C4 grid through native calls with reasoning `none`, against N1-A.
- **Verdict per measure:** SAME, DIFFERENT or UNCLEAR, on S and both traps' success for the grid, and on D1 for E5.
- **Status: run on 2026-10-20 (results below).** The three configs were committed with their caps at $0.
- **Estimated cost:** about $2.00.
- **Caps (budget only; under the owner's phase-1 approval of under $5; recorded before any N1 call):** N1-A $2.00, N1-B $0.50 and N1-C $1.50, so $4.00 in all. Each cap covers its study's pilot and main run. Each pilot must show protocol failures below 10% and tool use on request 1 in every run, or that study's main run stops and is reported.
- **N1 pilots (2026-10-20; not evidence):** all healthy, each with **0% protocol failures** and tool use on request 1 in every run. That includes N1-C with reasoning off, where the text format failed on 11–16% of turns.
  - N1-A: 12 runs, $0.036; main-run estimate $1.08.
  - N1-B: 3 runs, $0.003; estimate $0.15.
  - N1-C: 12 runs, $0.030; estimate $0.90.
- **Procedural note (no deviation; no spend).** The first background launch of the three main runs could not load `.env`: the shell started outside the experiment folder. Every run failed before any request, and no run files were written. The runs were relaunched from a script that sets the folder and checks the key first.

#### N1 results: [comparisons](runs/n1-comparison/)

**Runs:**

| Run | Runs | Calls | Protocol failures | Own verdict | Cost |
|---|---|---|---|---|---|
| N1-A, grid | 360 of 360 | 8,862 | 0.0% | CONTINUE_CREDULOUS | $1.00 |
| N1-B, E5 | 180 of 180 | 2,082 | 0.0% | CONFIRMED; secondary **CLEARING_SPECIFIC** | $0.16 |
| N1-C, grid | 360 of 360 | 8,630 | 0.0% | **INCONCLUSIVE** | $0.97 |

**Comparisons:**

| Comparison | Overall | S | Retry trap | Give-up trap | E5 D1 |
|---|---|---|---|---|---|
| **N1-A:** native minus text (reasoning `low`) | **DIFFERENT** | **−0.17** [−0.23, −0.10] (0.79 against 0.96) | SAME (0.00 against 0.00) | SAME (0.03 against 0.00) | |
| **N1-B:** native minus text (E5) | **SAME** | | | | −0.03 [−0.12, +0.05] (0.93 against 0.97) |
| **N1-C:** reasoning `none` minus `low` (native) | **DIFFERENT** | **−0.24** [−0.32, −0.16] (0.54 against 0.79) | SAME | SAME | |

**What N1 shows:**

- **The traps and the first-encounter effect do not depend on the reply format.**
  - Through native calls, "temporary" over a fixable fault still drew an identical retry in 30 of 30 runs, and 0 of 180 requests were solved.
  - "Unavailable" over a transient fault still drew a stop in 30 of 30 runs, with 0.03 solved.
  - E5's primary effect replicated: 100% stopped at once with no earlier error, against 7% after a cleared one.
- **The size of steering S does depend on the format.** It fell from 0.96 to 0.79. Two things cause this:
  - the format claim was followed less often on request 1 (Δ 0.53–0.73, against 0.97–1.00);
  - under the neutral message, native-call Luna stopped at once more often (6–7 of 30 runs, against 1–3), which shrinks the measured steering of "unavailable".
  - The verdict stays CONTINUE_CREDULOUS.
- **E5's secondary result depends on the format.**
  - With native calls, errors that never cleared left Luna stopping at once **63%** of the time, against **22%** in the text format.
  - The native run's own E5 verdict is CLEARING_SPECIFIC: never-cleared minus cleared = +0.57 [+0.43, +0.70].
  - So "persistence is learned mostly from the effort" (E5) holds only in the text format. Through native calls, seeing an error clear is what matters.
- **With reasoning off,** native calls make Luna usable: 0% protocol failures, against 11–16% in the text format. But its default changes: after a neutral failure it stopped at once in 24–27 of 30 runs, against 6–7 with reasoning `low`.
  - That high stopping baseline lowers S (0.54) without making Luna less credulous: under "unavailable" it still stopped 30 of 30 times.
  - Its INCONCLUSIVE verdict comes from L\* = +0.12 [+0.06, +0.19], which is driven by an *accurate* cell: more reformatting over time under a true format claim. It is not driven by learning to distrust false claims. Neither trap moved: 0.05 and 0.01 solved.

**Predictions (PROTOCOL_N1.md): 2 of 4 held.**

- **Held:**
  - N1-B SAME;
  - N1-C valid.
- **Missed:**
  - N1-A SAME: it was DIFFERENT on S, though the traps matched;
  - N1-C SAME against N1-A: it was DIFFERENT on S.

**Spend:** $2.20 for N1 including pilots, within the $4 in caps and the $5 phase-1 approval.

### W4: misleading errors in the wild (done; [`ERROR_AUDIT.md`](ERROR_AUDIT.md))

- **25 documented cases** of production error messages that misstate the cause, plus **4 honest messages**, each with its source. 9 of the misleading cases are backed by official documentation.
- **Both C4 traps occur in the wild:**
  - give-up pattern, 7 cases: for example, GitHub's 404 for an authentication problem, Azure's `PrincipalNotFound` during replication, and IAM propagation;
  - retry pattern, 9 cases: for example, a load balancer's or ingress's "503 Temporarily Unavailable" for a missing backend, OpenAI's 429 for billing, and a 500 for invalid input.
  - Another 9 cases point to the wrong fix.
- **The causes are systematic:** security masking, eventual consistency, generic intermediary statuses, missing validation, shared error codes, and local causes reported as remote. Some of these are deliberate and will not go away.
- **Honest two-cause messages exist,** for example Docker's "repository does not exist or may require 'docker login'". E2's honest arm is therefore realistic.
- **A targeted search, not a sample:** it shows that the patterns exist, not how often they occur.

## Paper plan, phase 2: the OpenRouter transport (built 2026-10-22; no live call, $0)

Transport `openrouter_chat_native`, in `causetest/transports.py`. It is for the open-weight part of the W2 panel, and it can also serve Google's models.

- **Same translation as N1.** It uses OpenRouter's OpenAI-compatible Chat Completions API with one `stock_lookup` function. It does not send `parallel_tool_calls` (see below).
  - A tool call reaches the unchanged episode as `CALL stock_lookup {...}`. The harness's next message goes back as that call's `tool` message.
  - The instructions are N1's native prompt.
  - As in N1, text sent alongside a call and the model's reasoning are not passed back. The exception is `pass_reasoning_back: true`, for models whose hosts require reasoning in a tool loop; choose it per model before any live call.
  - Unlike N1, the tool schema is not sent in strict mode, because most open-model hosts do not implement it.
- **One host per model.** OpenRouter otherwise routes a model to any of its hosts. They differ in quantization (DeepSeek V4 Flash has 15 hosts, from fp4 to fp8), chat template and tool-call parser.
  - The config's `provider` must name exactly one host in `order`. The transport always sends `allow_fallbacks: false` and `require_parameters: true`, and refuses a config that asks otherwise. `quantizations` is passed through.
  - Every response's serving host is recorded in `meta.host`.
  - A response from any other host fails the run, and the failure is kept, not retried away. Its billed cost still counts against the cap and in the journal (`BilledTransportError`; the episode now settles a failed call with the cost the error carries).
  - The host is part of the cache key, so a run on another host never reuses cached runs.
- **Billed cost.** `meta.cost_usd` is OpenRouter's `usage.cost`, with `meta.cost_source: "billed"`. If a response lacks it, the transport falls back to the config's prices and marks the cost `"price_estimate"`. Each response's `generation_id` is kept for audit against OpenRouter's records.
- **Errors.** An HTTP error, or an error object inside an HTTP 200 response, fails the run, which is then re-run once as before. A missing or malformed `OPENROUTER_API_KEY` stops the call before anything is sent.
- **Tests (8, all offline against a fake server):**
  - translation both ways, including the call closed by "No tool calls remain…";
  - the host pin and its validation;
  - billed and estimated cost;
  - errors inside a 200 response;
  - the missing key;
  - reasoning passed back only when set;
  - gating;
  - a whole run through the runner: host and cost in the records, the journal's spend, cache reuse, a new host bypassing the cache, and a wrong host failing while its cost counts.
- **Before a live run, for each model:**
  1. choose the host from OpenRouter's endpoints listing (`/api/v1/models/<model>/endpoints`), preferring the lab's own host or a bf16 or fp8 one;
  2. set temperature and reasoning explicitly, because hosts' defaults differ;
  3. freeze the config with a $0 cap, then set the approved cap;
  4. run the development pilot, and check its protocol-failure rate, which is where a host's broken tool-call parsing would show.
- **Two changes made with the panel (2026-10-22, still no live call):**
  - **No `parallel_tool_calls`.** No open-model host on OpenRouter lists that parameter, and with `require_parameters` it could block routing. A model that makes several calls at once gets the extra ones answered "Not run: make one call at a time.", and `native_calls` records it. A config can still add the parameter in `request_options`.
  - **Endpoint tags.** A pin may name an endpoint tag such as `deepinfra/fp8`, because one host can list several versions of a model at different precisions. The config's `expected_host` is the name responses give, such as `DeepInfra`. The check ignores case and punctuation, and also accepts the tag's host part.
  - The draft config `live_or_draft_deepseek_v4_flash.json` was removed. Its `"effort": "low"` is not a setting that DeepSeek V4 Flash (0423) accepts.

## Phase 2: proposed open-weight panel (2026-10-22; awaiting the owner's approval)

All 20 configs are `configs/live_or_<design>_<model>_<arm>.json`. Each has a **$0 cap**, so `--live` is refused until the owner sets one. A test checks that every config is gated and well formed, and that it builds a transport. Nothing has been sent.

**Design per arm: N1's designs, not the paper plan's reduced grid.**

- Each model-reasoning arm runs two designs:
  - the full C4 grid, 12 cells × 30 runs, which is N1-A's design;
  - E5, 3 primes × 60 runs, which is N1-B's design.
- `python -m causetest compare` can then put each arm against Luna's N1 runs directly.
- The plan's 6-cell reduction (`PAPER_PLAN.md`, W2) would leave S undefined. S averages over all six misleading cells, each against its neutral baseline.
- At open-model prices the full grid costs about $1.30–$37 per arm, so the reduction saves little. E3 is left for later.
- If approved, this is a change to the paper plan's W2 design, made before any W2 call.

**Panel: six labs, one model each.** Each model has its pinned endpoint, read from OpenRouter's endpoints listing on 2026-10-22.

| Model (OpenRouter ID) | Lab | Pinned endpoint (`expected_host`) | Precision | $/Mtok in / out | Reasoning arms | Estimate C4 + E5 | Proposed caps C4 / E5 |
|---|---|---|---|---|---|---|---|
| `deepseek/deepseek-v4.1-flash` | DeepSeek | `deepinfra/fp8` (DeepInfra) | fp8 | 0.14 / 0.42 | r0 `effort: none`; r1 `effort: low` | r0 $2.0; r1 $4.3 | r0 $6 / $1; r1 $11 / $3 |
| `qwen/qwen3.8-27b` | Alibaba (Qwen) | `deepinfra/bf16` (DeepInfra) | bf16 | 0.15 / 1.88 | r0 `none`; r1 `low` | r0 $3.7; r1 $14.3 | r0 $10 / $2; r1 $36 / $8 |
| `google/gemma-4-31b-it` | Google | `crusoe/bf16` (Crusoe) | bf16 | 0.14 / 0.40 | r0 `enabled: false`; r1 `enabled: true` | r0 $2.0; r1 $4.2 | r0 $6 / $1; r1 $11 / $3 |
| `mistralai/mistral-small-2603` (Mistral Small 4) | Mistral | `mistral` (Mistral, first party) | not listed | 0.15 / 0.60 | r0 `none`; r1 `high` (its only "on" setting) | r0 $2.3; r1 $11.8 | r0 $6 / $2; r1 $29 / $7 |
| `openai/gpt-oss-120b` | OpenAI | `deepinfra/bf16` (DeepInfra) | bf16 | 0.04 / 0.17 | r1 `low` only (reasoning cannot be turned off) | $1.6 | $4 / $1 |
| `z-ai/glm-5.3` | Z.ai | `z-ai/fp8` (Z.AI, first party) | fp8 | 1.40 / 4.40 | r1 `low` only (reasoning cannot be turned off) | $44.8 | $112 / $23 |
| **Total** | | | | | **10 arms, 20 configs** | **about $91** | **$282 if every cap were used** |

**Settings shared by every config:**

- temperature 1.0, as in N1-C. Other sampling settings are left at OpenRouter's or the host's defaults.
- `max_tokens` is 2,000 with reasoning off and 8,000 with it on, because reasoning counts toward the limit.
- Reasoning is not passed back, as in N1.
- Seeds, cells, thresholds and the instructions are N1's.

**Reasoning arms:**

- **r0** turns reasoning off.
- **r1** is the lowest "on" setting the model offers.
- gpt-oss and GLM-5.3 cannot turn reasoning off, so they have r1 only. They also cover W5's question, whether reasoning changes anything, across labs.

**How the estimates were made, and how far to trust them:**

- **Measured (from Luna's N1 runs):**
  - calls per run: 24.6 for C4 and 11.6 for E5;
  - input tokens per call: 1,020 for C4 and 650 for E5.
- **Guessed:** output tokens per call, at 100 with reasoning off, 600 at low and 1,500 at high. Reasoning models can produce much more; this guess is the biggest uncertainty.
- **Caps:** each proposed cap is 3× its estimate, rounded up, with a minimum of $1. A pilot costs about 3% of a config's run and measures the real figure. The cap can be cut after it, as was done for Haiku.

**Alternatives and models left out:**

- **GLM-5.3 on Novita** (fp8, $0.63 / $1.98) would cost about $20 instead of $45, but loses the first-party host.
- **Kimi K3** (Moonshot, 2.8T parameters): the largest open model. At about $3 / $15 per Mtok, it would be roughly $100–150 for one reasoning arm.
- **Llama 3.3 70B:** a non-reasoning, widely cited but dated baseline. About $10 on CoreWeave fp16.
- **DeepSeek V4.1 Flash 1017:** released on 2026-10-17, too new to have settled hosts.
- **Qwen Max and Plus:** closed weights.

**What only the first pilot can check.** Each of these would show within the first few calls, at a cost of cents:

1. that OpenRouter accepts an endpoint tag in `provider.order`;
2. that the response names the host as `expected_host` says;
3. that `effort: none` or `enabled: false` really turns reasoning off (`reasoning_chars` absent, and few output tokens);
4. that no host rejects a tool loop without its reasoning passed back. Some thinking-mode tool loops require it; the fix would be `pass_reasoning_back: true`, decided before the main run.

**Suggested order:**

1. The cheapest arms first, which also test the transport: gpt-oss-120b, then DeepSeek r0 and Gemma r0.
2. The rest of r0 and r1.
3. GLM-5.3 last.

## Study W2-A: results so far (2026-10-23; DeepSeek and Qwen done, Gemma held back)

The frozen design is in [`PROTOCOL_W2.md`](PROTOCOL_W2.md), and deviations W2-1 to W2-5 are listed under "Deviations". OpenRouter credit used to date: $6.12 ($20.00 → $13.88 on 2026-10-23), probes and pilots included. The four Qwen main runs cost $4.90 against a pilot-based estimate of $5.10.

| Run | Verdict | Key numbers |
|---|---|---|
| DeepSeek V4.1 Flash r0, C4 | **CONTINUE_CREDULOUS** | S +0.78 [+0.72, +0.84]; L\* +0.03 [−0.02, +0.07]. Retry trap 0/180 solved, give-up trap 0/180. Completion ≥ 0.97 in every cell. |
| DeepSeek V4.1 Flash r1, C4 | pass 1 **INVALID** (completion 0.933); after the W2-5 re-run, **CONTINUE_CREDULOUS** | S +0.66 [+0.64, +0.68]; L\* −0.01 [−0.08, +0.06]. 360/360 complete. The retry trap is partly broken: 16% of requests solved, against 0% at r0. The give-up trap holds: 2% solved. |
| DeepSeek V4.1 Flash r0, E5 | **CONFIRMED**, secondary CLEARING_SPECIFIC | D1 (stops at once, no error minus cleared) +0.52 [+0.40, +0.64]. |
| DeepSeek V4.1 Flash r1, E5 | pass 1 **INVALID** (completion 0.55); after the W2-4 re-run, **CONFIRMED**, secondary EXPOSURE_GENERAL | D1 +0.42 [+0.30, +0.55]. With reasoning on, either kind of earlier error makes the agent persist: 62% and 55% of targets solved, against 0% with no prior error. |
| Qwen3.8-27B r0, C4 | **CONTINUE_CREDULOUS** | S +0.50 [+0.43, +0.57]; L\* +0.08 [−0.01, +0.15]. Retry trap 5/180 solved, give-up trap 6/180. 360/360 complete; protocol failures 0.03%. $1.78. |
| Qwen3.8-27B r1, C4 | **INCONCLUSIVE** | S +0.78 [+0.72, +0.84]; L\* +0.13 [+0.06, +0.19], between the credulous and self-correcting bars. Retry trap 2/180, give-up trap 11/180. 360/360 complete; protocol failures 1.3%. $2.32. |
| Qwen3.8-27B r0, E5 | **CONFIRMED**, secondary INCONCLUSIVE | D1 +0.87 [+0.77, +0.95]. Stops at once: 90% with no prior error, 3% after a cleared one, 13% after uncleared ones. $0.33. |
| Qwen3.8-27B r1, E5 | **CONFIRMED**, secondary INCONCLUSIVE | D1 +0.70 [+0.57, +0.82]. Stops at once: 80%, 10% and 25%. $0.47. |
| gpt-oss-120b r1, E5 (added by W2-6) | **INCONCLUSIVE** | D1 +0.25 [+0.12, +0.40]: above 0, but under the 0.30 bar. Stops at once: 93% with no prior error, 68% after a cleared one, 98% after uncleared ones. Protocol failures 2.6%. The cleared prime worked in exactly 80% of runs, the minimum allowed. $0.04. |
| gpt-oss-120b r1, C4 (DeepInfra) | **not run:** failed the pilot health gate (12.2% protocol failures; W2-6) | |
| gpt-oss-120b r1, C4 (Crusoe, W2-7) | **INCONCLUSIVE** | S +0.92 [+0.88, +0.96], the highest of the open models. L\* +0.14 [+0.03, +0.25], driven by withdrawal (see below). Retry trap 0/180, give-up trap 6/180. 360/360 complete, after 4 transport failures were re-run once. Protocol failures 6.7%. $0.42. |

**Comparisons, by N1's rule** (`runs/w2-comparison/`; Δ = A − B, with 95% intervals):

| A vs B | S | Retry trap | Give-up trap | E5 D1 | Overall |
|---|---|---|---|---|---|
| DeepSeek r0 vs Luna, reasoning none (C4) | +0.24 [+0.16, +0.32] DIFFERENT | −0.01 SAME | −0.05 SAME | | DIFFERENT |
| DeepSeek r1 vs Luna, reasoning low (C4) | −0.13 [−0.18, −0.07] SAME | +0.16 [+0.10, +0.23] DIFFERENT | −0.01 SAME | | DIFFERENT |
| DeepSeek r1 vs r0 (C4) | −0.12 [−0.18, −0.06] SAME | +0.16 [+0.09, +0.23] DIFFERENT | +0.02 SAME | | DIFFERENT |
| DeepSeek r0 vs Luna (E5) | | | | −0.42 [−0.55, −0.26] DIFFERENT | DIFFERENT |
| DeepSeek r1 vs Luna (E5) | | | | −0.52 [−0.65, −0.37] DIFFERENT | DIFFERENT |
| DeepSeek r1 vs r0 (E5) | | | | −0.10 [−0.27, +0.08] UNCLEAR | UNCLEAR |
| Qwen r0 vs Luna, reasoning none (C4) | −0.04 [−0.14, +0.06] SAME | +0.02 SAME | −0.02 SAME | | SAME |
| Qwen r1 vs Luna, reasoning low (C4) | −0.01 [−0.09, +0.08] SAME | +0.01 SAME | +0.03 SAME | | SAME |
| Qwen r1 vs r0 (C4) | +0.28 [+0.19, +0.38] DIFFERENT | −0.02 SAME | +0.03 SAME | | DIFFERENT |
| Qwen r0 vs Luna (E5) | | | | −0.07 [−0.17, +0.03] SAME | SAME |
| Qwen r1 vs Luna (E5) | | | | −0.23 [−0.38, −0.10] DIFFERENT | DIFFERENT |
| Qwen r1 vs r0 (E5) | | | | −0.17 [−0.32, −0.02] DIFFERENT | DIFFERENT |

**Reading so far (two open-weight models plus Luna; the panel is not complete):**

- **The C4 credulity verdict generalizes to DeepSeek at both reasoning settings.** S is large and there is no learning.
- **The give-up trap is robust:** solved at most 2% of the time, on every arm and model so far.
- **The retry trap is the one reasoning loosens.** With reasoning on, DeepSeek solves 16% of retry-trap requests; Luna at low reasoning solved none. This is the first model-and-reasoning difference on a trap in the study.
- **E5's first-encounter effect holds, but is about half Luna's size.** D1 is +0.42 to +0.52, against +0.93.
  - With reasoning off, the prime effect is specific to errors that cleared.
  - With reasoning on, any earlier error makes the agent persist.
- **Qwen3.8-27B looks like Luna.** All four primary C4 measures are SAME as Luna at the matching reasoning setting, and its E5 effect with reasoning off is SAME as Luna's (D1 +0.87).
- **Both traps hold for Qwen at both settings:** at most 6% of trap requests solved. So across three models and five arms, the give-up trap is never solved more than 6% of the time. Only DeepSeek with reasoning on loosens the retry trap (16%).
- **Reasoning raises Qwen's steering** (S +0.50 → +0.78). Its C4 r1 verdict is INCONCLUSIVE because L\* = +0.13. Unlike Luna's INCONCLUSIVE (N1-C), this one comes from the *misleading* cells:
  - over the run, Qwen with reasoning on stops repeating identical calls under a false "temporary";
  - its late first moves shift toward rewriting the depot (19 of 60 in the retry trap).
  - That is partial learning, but toward the wrong fix: retry-trap success stays at 2/180. This is the same "depot first" exploration Luna showed in E2 and E3.
- **Reasoning weakens the first-encounter effect for Qwen** (D1 +0.87 → +0.70). With reasoning on, more agents persist even with no prior error (20% against 10%), and fewer persist after errors that never cleared (25% stop at once against 13%).
- **gpt-oss-120b (E5 only) is the most "unavailable"-credulous model so far.** One cleared error moved it only a little: from 93% to 68% stopping at once. It is the first E5 arm that is not CONFIRMED. So the first-encounter effect is not universal: its size runs from about +0.25 (gpt-oss) to +0.93 (Luna).
- **gpt-oss-120b withdraws from the tool as a run goes on.** No other model did this.
  - By request 6, 124 of its 360 C4 runs answered without calling the tool at all. On requests 4–6 it gave 268 such answers, against at most 1 for Luna, Qwen or DeepSeek.
  - Withdrawal is strongest under "temporary" (103 of 270 late requests) and weakest under the format message (14 of 270). It also happens under the neutral message (72).
  - **Its positive L\* comes from this withdrawal,** not from learning to distrust false claims. Following falls in the *accurate* cells too (true "temporary" +0.44, true "unavailable" +0.36).
  - It resembles the helplessness pattern studied in C3 more than learning.
- **For gpt-oss, a true "temporary" is worse than no cause.** Under the neutral message it solved the transient fault 30/30 on every request. Under the true "temporary" it solved only about 14/30: it often stopped or wandered before the third call.
- **The traps hold for gpt-oss too:** retry trap 0/180, give-up trap 6/180. Its C4 primary measures are SAME as Luna's at reasoning low.
- **E5's secondary result is INCONCLUSIVE for both Qwen arms.** Cleared and never-cleared errors differ by only 0.10–0.15. Combined with DeepSeek (CLEARING_SPECIFIC at r0, EXPOSURE_GENERAL at r1) and Luna (CLEARING_SPECIFIC under native calls), this distinction is not stable across models and should not be a headline claim.

**W2 predictions (`PROTOCOL_W2.md`), scored for the arms run so far (DeepSeek and Qwen):**

- **Held:**
  - both traps under 20% solved on every arm: yes, except DeepSeek r1's retry trap at 16%, which is still under 20%;
  - S positive on every valid arm: yes;
  - E5 D1 CONFIRMED: 4 of 4 arms so far;
  - r1 against r0 SAME on both traps: yes for Qwen.
- **Missed:** r1 against r0 SAME on both traps for DeepSeek, whose retry trap was DIFFERENT (+0.16).
- **gpt-oss-120b (W2-6):**
  - **Held:**
    - both traps under 20%: 0% and 3%;
    - S positive, with C4 INCONCLUSIVE, which was one of the two predicted verdicts.
  - **Missed:** E5 D1 CONFIRMED; it was INCONCLUSIVE.
  - **The flagged risk** (protocol failures through the host) occurred on DeepInfra, and was cleared on Crusoe (W2-7).
- **Gemma's predictions are open,** since its arms have not been run.

## Study H1: does tool withdrawal carry over to a tool that works? (frozen; [`PROTOCOL_H1.md`](PROTOCOL_H1.md))

**Owner's request, 2026-10-24:** follow up W2-7's finding that gpt-oss-120b increasingly answers without calling the tool.

**Design.** Each run is 12 requests: a training block of 8, then a test block of 4 in which every call works. The training conditions are:

- no failure;
- **controllable:** the format message over a fixable fault;
- **uncontrollable:** the same format message over a permanent fault;
- **uncontrollable with "temporary".**

The subjects are gpt-oss-120b (Crusoe, reasoning `low`) and Luna as a reference model, at 30 runs per condition each.

**Measures:**

- **Primary:** the share of test-block requests answered without a call, `uncontrollable` minus `no_failure`. The verdict is CARRYOVER, NO_CARRYOVER or INCONCLUSIVE.
- **Secondary,** only after CARRYOVER: uncontrollable minus controllable, giving CONTROLLABILITY_MATTERS or FAILURE_GENERAL.

**Status: built and validated (MOCK); not run.**

- The five H1 scripted agents give the expected verdicts. A fatigue agent, which withdraws with conversation length alone, is correctly judged NO_CARRYOVER.
- Power: CARRYOVER 20 of 20 even for a weakly helpless agent.
- Both live configs are at $0.
- **Estimated cost:** gpt-oss about $0.37 (OpenRouter), Luna about $0.93 (OpenAI).
- **Proposed caps:** gpt-oss $0.10 for the pilot, then $1; Luna $0.15, then $2.50.
- **Owner's approval, recorded 2026-10-24 before any H1 call:**
  - the pilots under caps of $0.10 (gpt-oss) and $0.15 (Luna);
  - each main run under $1.00 (gpt-oss) and $2.50 (Luna), once its pilot passes the W2 health gate. That gate is: every run complete, protocol failures of 10% or less, the tool called on request 1 in at least 90% of runs, and the estimate within the cap.
- **H1 pilots (2026-10-24; not evidence):**
  - **Luna passes the health gate:** 4 of 4 runs complete, 0% protocol failures, the tool called on request 1 in every run, estimate $0.96. Its cap rises to $2.50 as approved, and the main run follows.
  - **gpt-oss-120b fails the health gate:** 15.7% protocol failures against the 10% gate. **Its main run is not started**, and the result is reported to the owner.
    - All 22 failures are empty ANSWER lines: `ANSWER`, then leaked reasoning ("We need to output the figure…"), then the real `ANSWER 122`.
    - 9 of them come after *successful* calls in the no-failure condition, so they reflect gpt-oss's own formatting, not the conditions. It is the artifact seen on DeepInfra and Crusoe in W2-6 and W2-7.
    - H1's runs have more answers to give than C4's, because more requests succeed, so the artifact weighs more here.
  - **Owner's decision (2026-10-24): gpt-oss's H1 main run is not run**, as the gate requires. H1 is reported for Luna only, and gpt-oss's withdrawal stays a descriptive W2-7 finding. The gpt-oss pilot data stay on record.

### H1 result on GPT-6-luna: [NO_CARRYOVER](runs/h1-gpt-6-luna-native-low/analysis/VERDICT.md)

**Run:** 120 of 120 runs complete, 5,692 calls, $0.97. Protocol failures were 0%.

| Training condition | Training success | Failed calls in training | No-call, test block | Test success |
|---|---|---|---|---|
| no failure | 1.00 | 0.0 | 0.00 | 1.00 |
| controllable | 0.94 | 19.5 | 0.00 | 1.00 |
| uncontrollable | 0.00 | 46.3 | 0.00 | 1.00 |
| uncontrollable + "temporary" | 0.00 | 44.4 | 0.00 | 1.00 |

- **Luna never answered a request without calling the tool:** 0 of 1,440 requests, in training or in the test block. That held even after about 46 failed calls of uncontrollable failure.
- The intervals are degenerate (all zeros), so they show no variation at all, not an exact zero effect.
- **The controllable condition worked as intended:** 94% training success.
- **The result matches C3's Haiku finding** (KILL_NO_CARRYOVER) and the prediction.
- **gpt-oss's withdrawal (W2-7) remains a single-model observation.** Its own H1 test could not run, because its answer-formatting habit failed the pilot health gate.
- **Predictions (PROTOCOL_H1.md):** the Luna prediction held. The gpt-oss predictions are untested.

## Study W2-B: the bounded caution on the open-weight panel (frozen; [`PROTOCOL_W2B.md`](PROTOCOL_W2B.md))

**Owner's request, 2026-10-24.** E3's bounded caution, the paper's main practical recommendation, was tested only on Luna. W2-B runs E3's design on every open-weight arm:

- the arms are control, the plain caution and the bounded caution;
- the cells are the two traps and their accurate pairs: 360 runs per subject, on E3's seeds;
- the subjects are DeepSeek r0 and r1, Qwen r0 and r1, and gpt-oss r1;
- the decision rule is E3's: COST_AWARE, RESCUE_ONLY, LOSES_RESCUE, NO_GAIN or HARMS_TRUE_TEMPORARY.

**Status: done (2026-10-24); results below.**

- The three-arm design gives the expected verdicts on scripted agents (bounded, unbounded and deaf).
- The configs are at $0.
- **Estimates:** about $6.65 in all: DeepSeek r0 $0.35, r1 $0.70; gpt-oss $0.51; Qwen r0 $2.21, r1 $2.88. That is from $13.40 of OpenRouter credit.
- **Proposed caps, at about 3× the estimates:** $1, $2, $1.50, $6.50 and $8.50.
- **Owner's approval, recorded 2026-10-24 before any W2-B call:** the caps as proposed, each covering that subject's pilot and main run. Each main run starts only after its pilot passes the W2 health gate and the credit rule; a subject that fails the gate is stopped and reported.
- **W2-B pilots (2026-10-24; not evidence): all five pass the health gate.** Every run complete and the tool called on request 1 in every run:

  | Subject | Protocol failures | Main-run estimate |
  |---|---|---|
  | DeepSeek r0 | 1.1% | $0.31 |
  | gpt-oss | 6.2% | $0.34 |
  | DeepSeek r1 | 0.3% | $0.46 |
  | Qwen r0 | 0.0% | $1.86 |
  | Qwen r1 | 0.4% | $1.92 |

  The pilots cost $0.16 in all. The main runs follow, cheapest first.

### W2-B results: the rescue carries over in part; the cost saving does not

**Runs (2026-10-24):** all five main runs are VALID. Each has 360 of 360 runs complete; gpt-oss had 12 transport failures, each re-run once. Protocol failures were 0.0–7.7%, and the tool was called on request 1 in every run.

- **Cost:** $4.97 for the main runs (DeepSeek r0 $0.31, gpt-oss $0.34, DeepSeek r1 $0.46, Qwen r0 $1.76, Qwen r1 $2.09), against a pilot-based estimate of $4.89. With the pilots, W2-B cost $5.13.
- **OpenRouter credit:** $13.40 → $8.26.

Verdicts for `caution_bounded` by E3's rule (bars: rescue ≥ 0.50 with lower bound > 0.30; saving ≤ −1 call with upper bound < 0; harm ≤ −0.15 with upper bound < 0). Reports: `runs/w2b-*/analysis/VERDICT.md`.

| Subject | Verdict | Give-up rescue (bounded) | Plain caution's rescue | Outage calls: control / caution / bounded | Saving vs plain caution | True-"temporary" success vs control | Retry trap vs control |
|---|---|---|---|---|---|---|---|
| DeepSeek r0 | NO_GAIN | +0.45 [+0.30, +0.59] | +0.24 | 1.04 / 1.69 / 2.57 | +0.88 [+0.70, +1.07] | −0.03 [−0.13, +0.06] | +0.12 |
| DeepSeek r1 | **HARMS_TRUE_TEMPORARY** | +0.59 [+0.42, +0.77] | +0.91 | 1.93 / 3.99 / 2.56 | −1.43 [−1.69, −1.18] | **−0.17 [−0.29, −0.06]** | +0.11 |
| gpt-oss-120b r1 | NO_GAIN | +0.34 [+0.18, +0.49] | +0.07 | 1.01 / 1.21 / 1.27 | +0.06 [−0.07, +0.18] | +0.28 [+0.08, +0.48] | +0.01 |
| Qwen r0 | RESCUE_ONLY | +0.72 [+0.56, +0.87] | +0.57 | 1.89 / 2.64 / 2.82 | +0.17 [−0.43, +0.72] | +0.00 | +0.09 |
| Qwen r1 | RESCUE_ONLY | +0.56 [+0.38, +0.74] | +0.57 | 1.21 / 2.54 / 2.13 | −0.41 [−0.78, −0.04] | −0.01 [−0.02, +0.00] | +0.07 |
| *Luna, text, low (E3)* | *COST_AWARE* | *+0.92 [+0.83, +0.97]* | *+0.98* | *1.00 / 5.24 / 3.08* | *−2.17 [−2.51, −1.76]* | *−0.03 [−0.08, +0.00]* | *+0.29* |

The retry-trap and plain-caution columns are point estimates; their intervals are in each VERDICT.md. No interval was computed for the bounded caution against the plain caution's rescue.

**Reading:**

- **No subject is COST_AWARE.** E3's main result, the full rescue at about the floor cost, is so far a Luna result.
- **The rescue carries over in direction, not in size.**
  - The bounded caution raised give-up-trap success on all five subjects, by +0.34 to +0.72, and every interval excludes 0.
  - It cleared E3's bar on three: DeepSeek r1 and both Qwen arms. Luna's rescue was +0.92.
  - Even the best open arm (Qwen r0) leaves 28% of give-up traps unsolved.
- **The cost saving does not carry over, mostly because there was little cost to save.**
  - E3 measures the saving against the plain caution, which on Luna spent 5.2 calls on a true outage.
  - On the open models the plain caution spent 1.2–4.0 calls, below or near the floor of 3 on four of five, because it rescued less.
  - Only DeepSeek r1 had a costly plain caution, and there the bound did cut 1.4 calls.
- **On the three weaker subjects the bounded caution acts as the stronger cue** (DeepSeek r0, gpt-oss, Qwen r0). It rescued more than the plain caution and spent more calls (descriptive). "After a few different attempts" seems to work as an instruction to keep trying, not only as a stopping rule.
- **DeepSeek r1: the wording costs real successes (HARMS_TRUE_TEMPORARY).**
  - On a true "temporary" fault, success fell from 1.00 to 0.83.
  - In all 30 lost requests, DeepSeek changed the call on every attempt, rewriting the depot: for example "Corran", then "73", then "Corran (site 73)". The third call, the one on which the fault clears, was therefore itself malformed, and the agent then accepted the error.
  - It read "different attempts" literally. Without the bound (the plain caution), DeepSeek r1 rescued more (+0.91), at 4.0 calls.
- **gpt-oss: the cautions also help on a true "temporary".** Its control solved only 57% of those requests: it gave up early, or answered without calling the tool (18 of 180). Both cautions raised this (+0.37, +0.28), so its harm check is positive. Its give-up rescue was the weakest (+0.34).
- **The retry trap:** small gains everywhere (+0.01 to +0.12), against +0.29 on Luna.
- **For the paper:** the practical recommendation has to narrow. The bounded caution helps against the give-up trap on every model tested, but its size and cost depend on the model, and on one model its wording caused a measurable harm. W6 (wording variants) becomes more important.

**Predictions (PROTOCOL_W2B.md): 1 of 4 held.**

- COST_AWARE for at least 3 of 5: **missed** (0 of 5).
- The give-up rescue weakest for gpt-oss: **held** (+0.34). Its verdict was NO_GAIN, not the RESCUE_ONLY or LOSES_RESCUE I called plausible.
- No HARMS_TRUE_TEMPORARY: **missed** (DeepSeek r1).
- DeepSeek r1 gains most on the retry trap: **missed**, narrowly (DeepSeek r0 +0.12, r1 +0.11).

## Study W6: does the bounded caution depend on its wording? (done; [`PROTOCOL_W6.md`](PROTOCOL_W6.md))

**Owner's request, 2026-10-24.** W2-B weakened the paper's practical recommendation: no open-weight arm was COST_AWARE, and on DeepSeek r1 the bounded caution's wording ("a few *different* attempts") made the agent malform its calls. W6 tests three wordings side by side:

- `caution_bounded`, "…after a few different attempts, accept it" (E3, W2-B);
- `caution_few`, the same sentence without "different" (new; a minimal pair);
- `caution_three`, "…comes back on three attempts in a row, accept it" (E3).

Each follows the E2 caution, and runs against control and the plain caution. That is 5 arms × 4 cells × 30 runs = 600 runs per subject, on new seeds (20262001 + r).

- **Subjects:** DeepSeek r0 and r1, gpt-oss r1, Qwen r0 (OpenRouter, settings and hosts as in W2-A), and Luna through native calls with reasoning low (as N1-A).
- **Decision rule per subject and wording:** HARMS_TRUE_TEMPORARY, WEAK_RESCUE, RECOMMENDABLE (rescue with at most 3.5 outage calls, upper bound < 4.0) or RESCUE_COSTLY. Outage calls are absolute, not relative to the plain caution, because W2-B showed the plain caution is rarely costly on these models.
- **Primary question:** is any wording ROBUST, meaning RECOMMENDABLE on at least 4 of 5 subjects?
- **Secondary:** does dropping "different" remove DeepSeek r1's harm? Does that harm replicate?

**Status: done (2026-10-27).**

**Build and validation (MOCK, before any W6 call):**

- The five W6 scripted agents give the expected verdicts, and power reproduces them 20 of 20 times, including a weak agent near the rescue bar.
- **Shared code changed for W6 only:** a new arm (`caution_few`) in `causetest/e2.py`, the mock's stopping rule keyed by wording, and design `W6` in the runner. E3's arm list is unchanged. Every earlier mock verdict and every live report re-scores identically (`validate` 40/40, `reproduce` passes).
- The configs are at $0.
- **Estimates:** OpenRouter about $5.28 for the main runs plus about $0.20 for pilots, from $8.26 of credit. Luna about $1.80 on the OpenAI key.
- **Proposed caps, at about 3× the estimates where the credit allows:**

  | Subject | Estimate | Proposed cap |
  |---|---|---|
  | DeepSeek r0 | $0.57 | $1.50 |
  | gpt-oss r1 | $0.63 | $1.75 |
  | DeepSeek r1 | $0.85 | $2.25 |
  | Qwen r0 | $3.23 | $6.00 |
  | Luna, native, low | $1.80 | $5.00 |

- **Credit rule:** Qwen r0 runs last, and fits with little room. If its pilot estimate comes in higher, it waits for the owner (a top-up, or dropping it).
- **Owner's approval, recorded 2026-10-24 before any W6 call:** the caps as proposed, each covering that subject's pilot and main run. Each main run starts only after its pilot passes the W2 health gate (and, for the OpenRouter subjects, the credit rule). A subject that fails either is stopped and reported.
- **W6 pilots (2026-10-24; not evidence): all five pass the health gate.** Every run complete and the tool called on request 1 in every run:

  | Subject | Protocol failures | Main-run estimate |
  |---|---|---|
  | DeepSeek r0 | 0.4% | $0.56 |
  | gpt-oss r1 | 7.4% | $0.65 |
  | DeepSeek r1 | 0.8% | $0.71 |
  | Qwen r0 | 0.0% | $3.23 |
  | Luna, native, low | 0.0% | $1.97 |

  - gpt-oss had one transport failure: a 502 from Crusoe on one run, which was re-run once and completed. It is the same kind of failure as in W2-B.
  - The pilots cost $0.24 in all ($0.17 OpenRouter, $0.07 OpenAI). OpenRouter credit after them: $8.08, enough for Qwen under the credit rule. The main runs follow: the OpenRouter subjects cheapest first, and Luna in parallel on the OpenAI key.

### W6 results: "three attempts in a row" is ROBUST; the two "a few" wordings are not

All five subjects are VALID, 600 of 600 runs each. gpt-oss needed the W6-1 re-run (its first pass was INVALID, 0.933 completion in one cell), and Qwen r0 the W6-2 restarts. Reports: [Luna](runs/w6-gpt6luna-native-low/analysis/VERDICT.md), [DeepSeek r0](runs/w6-deepseek-v4-1-flash-r0/analysis/VERDICT.md), [DeepSeek r1](runs/w6-deepseek-v4-1-flash-r1/analysis/VERDICT.md), [gpt-oss](runs/w6-gpt-oss-120b-r1/analysis/VERDICT.md), [Qwen r0](runs/w6-qwen3-8-27b-r0/analysis/VERDICT.md).

**Per subject and wording:** verdict, give-up rescue against control, and calls per request on a true outage. The floor that keeps the rescue is 3 calls.

| Subject | Plain caution | `caution_bounded` ("a few different") | `caution_few` ("a few") | `caution_three` ("three in a row") |
|---|---|---|---|---|
| Luna, native, low | +0.98, 5.71 | RESCUE_COSTLY: +0.93, 4.94 | RESCUE_COSTLY: +1.00, 5.18 | **RECOMMENDABLE: +1.00, 3.01** |
| DeepSeek r0 | +0.18, 1.71 | RECOMMENDABLE: +0.53, 2.49 | RECOMMENDABLE: +0.85, 2.69 | **RECOMMENDABLE: +0.98, 2.98** |
| DeepSeek r1 | +0.94, 3.57 | RECOMMENDABLE: +0.76, 2.56 | RECOMMENDABLE: +0.60, 2.39 | **RECOMMENDABLE: +0.90, 3.06** |
| gpt-oss-120b r1 | −0.03, 1.21 | WEAK_RESCUE: +0.20, 1.32 | WEAK_RESCUE: +0.19, 1.26 | **RECOMMENDABLE: +0.69, 1.74** |
| Qwen r0 | +0.33, 3.07 | WEAK_RESCUE: +0.44, 2.73 | RECOMMENDABLE: +0.56, 2.79 | **RECOMMENDABLE: +0.76, 3.00** |
| **RECOMMENDABLE on** | | 2 of 5 | 3 of 5 | **5 of 5: ROBUST** |

Intervals are in each subject's report. `caution_three`'s rescue has its lower bound at +0.56 or above on every subject.

- **Q1 (primary): `caution_three` is ROBUST,** RECOMMENDABLE on all five subjects. It brought give-up-trap success to 0.81–1.00 on every subject, at 1.7–3.1 calls on a true outage. Neither "a few" wording is ROBUST.
  - E3's own verdicts for `caution_three`: COST_AWARE on Luna, RESCUE_ONLY on the other four (their plain caution was rarely costly).
- **Naming the count is what helps.** Against `caution_bounded`, `caution_three` rescued DIFFERENT and more on DeepSeek r0 (+0.45), gpt-oss (+0.49) and Qwen (+0.32), and UNCLEAR or SAME on the other two, which were near the ceiling.
- **Its cost: no help on the retry trap.** `caution_three` solved 0–2% of retry traps on every subject. `caution_bounded` solved 3–26%, and "different" is why (on Luna, `caution_few` 2% against `caution_bounded` 26%: DIFFERENT, −0.23). The retry trap stays unsolved by any wording.
- **Q2 ("different" on true "temporary"): SAME on all five subjects.** On DeepSeek r1 the mechanism recurred: under `caution_bounded` it varied its call on every attempt in 165 of 180 true-"temporary" requests, and 17 of those failed. Without "different" that fell to 55, with none failing. The gain from dropping the word, +0.09 [+0.01, +0.20], is under the 0.15 bar for DIFFERENT.
- **Q3 (replication): DeepSeek r1 is not HARMS_TRUE_TEMPORARY this time.** Its loss under `caution_bounded` was −0.09 [−0.20, −0.01], against −0.17 in W2-B: the same direction and mechanism, a smaller size, over the −0.15 bar.
- **On Luna, the bounded caution was not cost-aware through native calls:** 4.94 outage calls, against 3.08 in E3's text format. Only "three in a row" kept Luna at the floor (3.01). This mixes wording with format (a known limit).
- **Descriptive, varied-every-call requests in true "temporary"** (`caution_bounded` / `caution_few` / `caution_three`): Luna 154 / 6 / 0, DeepSeek r0 116 / 5 / 0, DeepSeek r1 165 / 55 / 3, gpt-oss 76 / 10 / 0, Qwen 94 / 47 / 19.

**Predictions (`PROTOCOL_W6.md`): 3 of 5 held.**

| Prediction | Outcome |
|---|---|
| `caution_three` ROBUST, `caution_bounded` not | **held** (5 of 5; 2 of 5) |
| DeepSeek r1: `caution_few` − `caution_bounded` on true "temporary" DIFFERENT and positive; SAME elsewhere | **missed** for DeepSeek r1 (SAME, +0.09); SAME elsewhere held |
| Luna's retry trap: `caution_bounded` beats `caution_few` | **held** (DIFFERENT, −0.23) |
| DeepSeek r1 HARMS_TRUE_TEMPORARY again | **missed** (−0.09) |
| gpt-oss weakest under every wording, WEAK_RESCUE under at least two | **held** (weakest under all three; WEAK_RESCUE under two) |

**Spend:** OpenRouter $4.91 (pilots $0.17, main runs $4.74, the W6-1 re-run and both W6-2 passes included); OpenAI $2.02 for Luna (pilot $0.07, main run $1.96). Total $6.93.

## Study W5: does reasoning effort change the traps? (done; [`PROTOCOL_W5.md`](PROTOCOL_W5.md))

**Under the owner's delegation of 2026-10-27** (Luna runs on the OpenAI key; see "Resume here"). Workstream W5 of `PAPER_PLAN.md`, Luna part only: the Anthropic model with extended thinking is a frontier run and waits for the owner.

**Why now.** At reasoning `low`, Luna hardly reasons in this task: 1.3 reasoning tokens per call on average in N1-A, 0.4 in W6. So N1-C (`none` against `low`) did not test reasoning. W5 runs `medium` and `high`.

- **Runs:** the C4 grid (12 cells × 30) at `low`, `medium` and `high`, and E5 (3 primes × 60) at `none`, `low`, `medium` and `high`. All through native calls, on N1's seeds, with every other setting as N1. `medium` and `high` get an 8,000-token output limit, because reasoning counts against it (at `low` the 2,000 limit never bound: the longest reply in N1-A was 191 tokens).
- **The `low` runs repeat N1-A and N1-B** in the same days as the new efforts, so effort is compared within one week, and drift since N1 is measured.
- **Primary:** C4 `high` − `low`, by N1's comparison rule (SAME, DIFFERENT or UNCLEAR on S and both traps). Everything else is secondary or a drift check.
- **No code changes.** `TestStudyW5` checks that the configs differ from N1's only in effort (and the output limit).

**Status: frozen; caps set (below).** Estimates and caps (about 2.5–3× the estimates, because the reasoning-token cost is a guess until the pilots):

| Run | Estimate | Proposed cap |
|---|---|---|
| C4, low | $1.00 | $2.50 |
| C4, medium | ~$2 | $6.00 |
| C4, high | ~$4 | $12.00 |
| E5, none | $0.15 | $0.50 |
| E5, low | $0.16 | $0.50 |
| E5, medium | ~$0.40 | $1.50 |
| E5, high | ~$1.00 | $3.00 |
| **Total** | **about $9** | **$26** |

- **Caps set, 2026-10-27, before any W5 call:** as proposed, each covering that run's pilot and main run, under the owner's delegation of the same day (Luna runs on the OpenAI key). Each main run starts only after its pilot passes the W2 health gate; a run that fails the gate is not run and is reported to the owner.
- **W5 pilots (2026-10-27; not evidence): all seven pass the health gate.** Every run complete, no protocol failures, and the tool called on request 1 in every run. No reply reached its output limit.

  | Run | Reasoning tokens per call | Longest reply (tokens) | Main-run estimate |
  |---|---|---|---|
  | E5, none | 0.0 | 27 | $0.19 |
  | E5, low | 1.1 | 41 | $0.14 |
  | E5, medium | 1.4 | 42 | $0.19 |
  | E5, high | 9.4 | 173 | $0.25 |
  | C4, low | 1.2 | 102 | $0.97 |
  | C4, medium | 6.3 | 181 | $1.24 |
  | C4, high | 9.1 | 202 | $1.26 |

  - **Even at `high`, Luna reasons very little in this task:** about 9 tokens per call. The effort setting is a request, not a guarantee. W5 therefore tests the effort setting as a user would set it, and its reasoning-token counts are reported with the results.
  - The pilots cost $0.13. The main runs follow: E5 and C4 in two parallel streams, each in the order of the table.

### W5 results: more reasoning does not get Luna out of the traps

All seven runs are VALID: complete in every cell, no protocol failures, no reply at its output limit. Comparisons: [`runs/w5-comparison/`](runs/w5-comparison/).

| Effort | Reasoning tokens per call | C4 verdict | S | Retry trap solved | Give-up trap solved | Neutral error over a transient fault, solved | E5: stop at once, no earlier error / after a cleared one | E5 verdict |
|---|---|---|---|---|---|---|---|---|
| none | 0 | *(N1-C: INCONCLUSIVE)* | *+0.54* | *1%* | *5%* | *25%* | 98% / 10% | CONFIRMED |
| low | 1.4 | CONTINUE_CREDULOUS | +0.79 | 1% | 2% | 46% | 97% / 3% | CONFIRMED |
| medium | 6.7 | CONTINUE_CREDULOUS | +0.92 | 1% | 14% | 81% | 90% / 2% | CONFIRMED |
| high | 11.0 | CONTINUE_CREDULOUS | +0.94 | 1% | 11% | 89% | 78% / 0% | CONFIRMED |

The `none` row's C4 figures are N1-C's (2026-10-20); W5 ran E5 only at `none`.

- **Primary: C4 `high` − `low` is SAME** on all three measures: S +0.14 [+0.08, +0.21], retry trap +0.00 [−0.03, +0.03], give-up trap +0.08 [+0.00, +0.18]. `medium` − `low` is SAME too.
- **What reasoning changes is the default, not the credulity.** After an uninformative ("neutral") error over a transient fault, Luna at `high` retried until it worked in 89% of requests, against 46% at `low` (DIFFERENT, +0.43). Told "unavailable" over the same fault, it still stopped: 11% solved. Steering S rises because the stated cause now overrides a more persistent default.
- **E5: the first-encounter effect is CONFIRMED at every effort,** but weaker at `high`: D1 +0.78 against +0.93 at `low` (DIFFERENT, −0.15 [−0.27, −0.03]). With no earlier error, Luna at `high` stopped at once on 78% of first "unavailable" messages, against 97%. `medium` and `none` are SAME as `low`.
- **Drift checks: SAME.** W5's `low` runs reproduce N1-A (S +0.794 against +0.789) and N1-B (D1 +0.93 against +0.93) a week later.
- **Luna reasons little in this task at any effort:** 11 reasoning tokens per call at `high`.

**Predictions (`PROTOCOL_W5.md`): 1 of 5 held.**

| Prediction | Outcome |
|---|---|
| Primary not SAME, through the retry trap (15–40% solved at `high`) | **missed:** SAME; the retry trap stayed at 1% |
| The give-up trap holds at every effort (under 10%) | **missed,** narrowly: 14% at `medium`, 11% at `high` |
| E5: D1 SAME at every effort, CONFIRMED in each | **missed** at `high` (DIFFERENT, −0.15); CONFIRMED in each held |
| `medium` between `low` and `high` | **missed** on the give-up trap (14% against 11%); held on S and D1 |
| Drift checks SAME | **held** |

**Spend:** $4.26 on the OpenAI key (pilots $0.13; main runs $4.13: C4 $3.42, E5 $0.71), against $26 of caps.

## Study W2-C: Claude Haiku 5.5 through native tool use (done; [`PROTOCOL_W2C.md`](PROTOCOL_W2C.md))

**Owner's request, 2026-10-28:** run Haiku 5.5 now, since it is cheap, so the Anthropic side has native-call coverage beside Luna's. The larger Claude models wait for the owner's research-credits application.

- **Designs:** the C4 grid, E5 and W6, each exactly as already run on the other models (same cells, seeds and decision rules).
- **Arms:** thinking off (`t0`) and on (`t1`, adaptive), both at the default effort.
- **Transport:** `anthropic_messages_native`. It sends each assistant turn back whole and uses automatic prompt caching; neither changes what the model sees.
- **Primary:** the C4 verdict with thinking off. Secondary: E5, W6's wordings, thinking on against off, and native against the earlier text-format Haiku run.

**Status: frozen; caps set (below).** Estimates and caps, within the owner's $10:

| Config | Estimate | Proposed cap |
|---|---|---|
| C4, thinking off | $1.20 | $1.40 |
| E5, thinking off | $0.19 | $0.30 |
| W6, thinking off | $2.35 | $2.70 |
| C4, thinking on | $1.65 | $1.85 |
| E5, thinking on | $0.27 | $0.40 |
| W6, thinking on | $3.20 | $3.35 |
| **Total** | **$8.86** | **$10.00** |

- **Owner's approval, 2026-10-28, before any W2-C call:** "approved, freeze it at $10 and run the pilots". The caps are as proposed, each covering that config's pilot and main run. **The main runs wait for the owner's word** after the pilots.
- **W2-C pilots (2026-10-28; not evidence): all six pass the health gate.** Every run complete, no protocol failures, the tool called on request 1 in every run, and no reply at its output limit. They were also the transport's first live calls; the first transcripts read cleanly.

  | Config | Output tokens per call | Calls with thinking | Share of input from the cache | Main-run estimate | Cap |
  |---|---|---|---|---|---|
  | E5, thinking off | 51 | 0 of 20 | 81% | $0.07 | $0.30 |
  | E5, thinking on | 89 | 8 of 25 | 83% | $0.12 | $0.40 |
  | C4, thinking off | 53 | 0 of 165 | 92% | $0.26 | $1.40 |
  | C4, thinking on | 83 | 49 of 236 | 93% | $0.54 | $1.85 |
  | W6, thinking off | 59 | 0 of 366 | 93% | $0.65 | $2.70 |
  | W6, thinking on | 76 | 73 of 446 | 94% | $0.96 | $3.35 |

  - **Caching cut the cost to about a third of the estimate:** about $2.60 for all six main runs, against $8.86 planned.
  - With thinking on, Haiku thought on about a fifth of its calls (the model decides).
  - The pilots cost $0.08.
- **Owner's word on the main runs, 2026-10-28, before any main-run call:** "approved, run the main runs". They run in two parallel streams (thinking off, thinking on), each E5, then C4, then W6.

### W2-C results: both traps hold on Haiku, and "three attempts in a row" works; E5's mechanism does not apply

All six runs completed (600 of 600 in W6 with thinking on, after the runner's single re-run of 5 runs whose connection was reset). Reports: `runs/w2c-<design>-claude-haiku-5-5-<t0|t1>/analysis/VERDICT.md`; comparisons in [`runs/w2c-comparison/`](runs/w2c-comparison/).

| | Thinking off (`t0`) | Thinking on (`t1`) |
|---|---|---|
| C4 verdict | INCONCLUSIVE (S +0.69 [+0.66, +0.73]; L\* +0.11 [+0.06, +0.16]) | CONTINUE_CREDULOUS (S +0.61; L\* +0.04) |
| Retry trap / give-up trap solved | 0% / 0% | 0% / 0% |
| Neutral error over a transient fault, solved | 0% | 47% |
| E5 | **INVALID** (manipulation check 0.33) | NOT_CONFIRMED (D1 +0.03) |
| W6: "a few different" / "a few" / "three in a row" | WEAK_RESCUE / WEAK_RESCUE / **RECOMMENDABLE** | RECOMMENDABLE / RECOMMENDABLE / **RECOMMENDABLE** |
| "Three in a row": give-up rescue, outage calls | +0.97, 2.53 | +1.00, 2.82 |

- **Primary (C4, thinking off): INCONCLUSIVE.** Haiku follows the stated cause (S +0.69) and solves neither trap. L\* is +0.11, between the credulous bar (0.10) and the self-correcting bar (0.15), because over a run Haiku drifts toward stopping at once on every error: the drift is toward giving up, not toward the true cause.
- **Through the API with thinking off, Haiku gives up after any error it cannot read.** After a neutral error over a transient fault it never persisted to the call that works (0%, against 97% through the CLI in the text format, DIFFERENT). That moves S from +0.34 to +0.69 (DIFFERENT); both traps are SAME (0%).
- **E5 cannot be tested on Haiku with thinking off.** The cleared-error prime needs the agent to persist to the third call, and Haiku did in only 33% of runs: the run is INVALID by the frozen rule. With thinking on the prime works, but Haiku did not stop at once on a first "unavailable" (12%), so there is no first-encounter effect to remove (NOT_CONFIRMED). After errors that never cleared, it stopped at once 92% of the time: the opposite of Luna's pattern. (Correction, 2026-10-28: an earlier version of this note and of PR #30 called the first-encounter effect Luna-specific. It is CONFIRMED on Luna, DeepSeek and Qwen; Haiku is the exception.)
- **"Three attempts in a row" is RECOMMENDABLE in both arms,** and with thinking off it is the only wording that rescues (+0.97, against +0.43 and +0.30 for the "a few" wordings). Across W6's five subjects and Haiku's two arms it is now RECOMMENDABLE on 7 of 7.
- **With thinking off, any caution also rescues accurate "temporary" errors:** control solved only 30% of them; every caution arm solved 90–100% (+0.60 to +0.70).
- **Thinking on against off: SAME** on S and both traps (C4), and on D1 (E5, descriptive, since `t0` is INVALID). Thinking changes the default after a neutral error (0% → 47% persisted).

**Predictions (`PROTOCOL_W2C.md`): 3 of 5 held.**

| Prediction | Outcome |
|---|---|
| Primary: `t0` CONTINUE_CREDULOUS, both traps at most 10% | **missed:** traps 0%, but INCONCLUSIVE (L\* +0.11) |
| E5 CONFIRMED in both arms | **missed:** INVALID (`t0`), NOT_CONFIRMED (`t1`) |
| "Three in a row" RECOMMENDABLE in both arms | **held** |
| `t1` − `t0` SAME on both traps | **held** (SAME on all three primary measures) |
| Format: S DIFFERENT from the text-format run, traps SAME | **held** (+0.35) |

**Spend:** $2.65 on the Anthropic key (pilots $0.08, main runs $2.57), against the $10 approved. Prompt caching supplied 87–95% of input tokens.

## Decisions for the owner

0. **Next steps toward a paper are in [`PAPER_PLAN.md`](PAPER_PLAN.md).** Phase 1 (reproducibility fixes, native tool calling and an audit of real misleading errors) costs under $5 and is ready for approval. E5 (above) has confirmed the E4 mechanism. The items below are kept for reference.
   - **A pre-registered test of E4's exploratory finding:** does one cleared error, placed before the first "unavailable", make a plain agent persist? This is cheap on Luna, and it would turn the E4 mechanism into a confirmed result.
   - **The bounded caution on Haiku 5.5 (no reasoning).** Is the E2 + E3 fix specific to a reasoning model? Haiku's default after a neutral failure was to retry, not to rewrite the depot.
   - **A retry-trap probe** with a larger call budget, to separate "does not explore" from "explores the wrong thing first". E3 suggests the second: the word "different" alone raised retry-trap success from 2% to 29%.
   - **A second wording of the bounded caution,** to check that the result is not tied to one phrasing.
1. **Whether to replicate on a further model.** The GPT-6-luna replication is done (above), and both designs gave the same verdicts as on Haiku.
   - **Sonnet 5.5:** about 15× Haiku's per-call cost, so roughly $250 API-equivalent for the full grid.
   - **GPT-4.1-mini:** the OpenAI key now works, and Luna's measured costs suggest the earlier $13 estimate is high. It needs its own pilot.
   - **Luna with reasoning off** cannot be run on the current text protocol. See the L1 pilot.
   - A smaller targeted replication could keep only the cells that carry the effect, for example "temporary" and "unavailable" over fixable and transient faults, plus their neutral baselines.
2. **Whether to extend on Haiku:** see item 0 for E2 on Haiku.

## Commands (run and passing on 2026-10-20)

From this folder, using Python 3.13 and the standard library only:

```sh
python3 -m unittest discover -s tests -v
python3 -m causetest plan --config configs/live_claude_haiku.json
python3 -m causetest validate --configs configs/mock_*.json            # MOCK validation, about 10 s
python3 -m causetest power --config configs/power_weak_credulous.json --replications 20 --runs-per-cell 30   # MOCK
python3 -m causetest plan --config configs/live_e2_gpt6luna.json        # E2 cost estimate, no network
python3 -m causetest power --config configs/power_e2_weak_cues.json --replications 20 --runs-per-cell 30     # MOCK, E2
python3 -m causetest plan --config configs/live_e3_gpt6luna.json        # E3 cost estimate, no network
python3 -m causetest power --config configs/power_e3_half_bounded.json --replications 20 --runs-per-cell 30  # MOCK, E3
python3 -m causetest plan --config configs/live_e4_gpt6luna.json        # E4 cost estimate, no network
python3 -m causetest plan --config configs/live_e5_gpt6luna.json        # E5 cost estimate, no network
python3 -m causetest plan --config configs/live_or_c4_deepseek_v4_1_flash_r0.json   # OpenRouter panel config, no network
python3 -m causetest reproduce                                          # raw-data hashes + byte-identical re-scoring of every live run
python3 -m causetest compare --a runs/<A> --b runs/<B> --design C4 --out runs/n1-comparison/<name>.md   # study N1
```

Live runs, each of which needs the owner's go-ahead and a cap above $0 in the config:

```sh
python3 -m causetest pilot --config configs/live_claude_haiku.json --live   # development seed; measures cost
python3 -m causetest run   --config configs/live_claude_haiku.json --live   # the kill test
python3 -m causetest analyze --run-dir runs/<run>                           # re-score without new calls
python3 -m causetest combine --run-dirs runs/<run-a> runs/<run-b> --out runs/overall
```

A run writes the following to `runs/<run_name>/`:

| File | Contents |
|---|---|
| `config.json` | config snapshot |
| `worlds.jsonl` | ground truth for the 30 worlds |
| `pilot/` | development-pilot runs and `PILOT.md` |
| `results.jsonl` | one row per agent run: every request's turns, replies, parsed actions, tool results and coded responses |
| `journal.jsonl` | every request, response cost and error |
| `cache/` | completed runs, used to resume (a cached run is marked and is not a new sample) |
| `analysis/` | `summary.json` and `VERDICT.md` |

## Layout

| Path | Purpose |
|---|---|
| `causetest/env.py` | worlds, depot conventions, the three true faults, the four error texts, cells |
| `causetest/protocol.py` | system prompt, reply parsing, answer normalization, response coding, cause-language rules |
| `causetest/episode.py` | one run through six requests, with call and format limits and per-request summaries |
| `causetest/transports.py` | Claude CLI, OpenAI Responses (text and native), OpenRouter native, Anthropic Messages native and MOCK transports; spend guard (from C3) |
| `causetest/mocks.py` | scripted agents |
| `causetest/score.py` | S, L\*, bootstrap, secondary measures, decision rule |
| `causetest/runner.py` | plan, pilot, run (with one re-run of transport failures), analyze, combine, validate, power |
| `causetest/extension.py` | extension E1: L_E1, its bootstrap, decision rule and report |
| `causetest/e2.py` | extensions E2 and E3: the intervention texts, arms and cells; E2 contrasts, cost flags, decision rule and report |
| `causetest/e3.py` | extension E3: the stopping-rule contrasts, decision rule and report |
| `causetest/e4.py` | extension E4: mixed-request schedules, the per-request environment, contrasts, decision rule and report |
| `causetest/e5.py` | extension E5: primed three-request runs, the no-fault prime, manipulation check, contrasts, decision rule and report |
| `causetest/h1.py` | study H1: training and test schedules, the scheduled environment, withdrawal measures, decision rule and report |
| `causetest/w6.py` | study W6: wording contrasts, the per-wording decision rule, the varied-call count and report |
| `causetest/panel.py` | the panel table: every model and setting side by side, from committed summaries (descriptive; `python -m causetest panel`) |
| `causetest/compare.py` | study N1: one run minus another for the same design, with bootstrap intervals and fixed verdicts |
| `figures/stated_true_grid.py` | paper figure: share of requests solved by stated cause × true fault, one grid per model and setting; writes `stated_true_grid.svg` and `.csv` |
| `figures/rescue_cost.py` | paper figure: give-up rescue against outage-call cost per model and wording (E3, W6); writes `rescue_cost.svg` and its data `rescue_cost.csv` |

## Deviations

Pre-freeze differences from the handoff are listed at the end of `PROTOCOL.md`.

- **D1 (budget only, before any live call).** `configs/live_claude_haiku.json` `max_equiv_usd` was raised from 0 to 1.0, with the owner's approval, for the development pilot. The pilot's estimate is about $0.50. The kill test needs a new cap, set from the pilot's measured cost. No design element, threshold or agent-facing text changed.
- **D2 (budget only, after the pilot, before any kill-test call).** `max_equiv_usd` in `configs/live_claude_haiku.json` was raised from 1.0 to 22.0, with the owner's approval. That is about 1.5× the pilot-based estimate of $14.75. No design element, threshold or agent-facing text changed.
- **D3 (interruption and resume, during the kill test).** The session's container restarted partway through. By then 234 of 360 runs had completed, 2 had failed on CLI timeouts, and 10 were mid-conversation. The run was resumed with the same command and config:
  - the 234 completed runs were reused from the cache; they were completed earlier in this same kill test, so they are not new samples;
  - the 10 interrupted runs and the 2 failed runs started again from the beginning;
  - the remaining 114 runs were run for the first time.

  The first pass's results are kept as `runs/live-claude-haiku-5-5/results.pass1.jsonl`. Every call from both passes is in `journal.jsonl` and counts against the cap, including the interrupted runs' partial calls. The pre-registered single re-run of transport failures applies within the resumed pass: the two first-pass failures get their fresh start there, and any further failure in that pass gets one re-run, which is reported.
- **E1, procedural note (no deviation).** The first background launch of the E1 run failed at import, "No module named causetest", before any call. It was relaunched with an explicit `PYTHONPATH`. No spend, no data.
- **W2-1 (transport, after the probes and before any W2 pilot).** In the probes (`runs/w2-probes/probe.jsonl`), Gemma 4 31B returned HTTP 429. The message was "temporarily rate-limited upstream", from the host's shared pool, on Crusoe and on Novita alike.
  - The OpenRouter transport now retries an HTTP 429 up to six times, with waits of 2, 4, 8, 16, 30 and 30 seconds.
  - Each call records its retry count in `meta.rate_limit_retries`.
  - A 429 comes before the model runs. It is not billed, and it does not depend on the conversation, so the retry changes nothing the agent sees.
  - Any other HTTP error, or a 429 after six retries, fails the run as before, and the run is re-run once.
  - A test covers the change.
  - No design element, threshold or agent-facing text changed.
- **W2-2 (scope, before any W2 pilot).** Gemma 4 31B is held back.
  - Even single requests needed 2–4 retries on Crusoe.
  - Six parallel requests on Novita, the alternative bf16 host, failed after six retries.
  - At the pilot's 10 parallel workers, most runs would fail on rate limits rather than on anything the agent did.
  - The DeepSeek and Qwen arms proceed as frozen. Gemma's four configs keep their caps, but are not run until the owner decides how to proceed.
- **W2, probe results (no deviation).** One request per arm, two calls at most, costing about $0.002 in total. They confirmed four things:
  - OpenRouter accepts endpoint tags in `provider.order`;
  - responses name the expected host (DeepInfra, Crusoe, Novita);
  - the cost comes back billed;
  - r0 produced 0 reasoning tokens on every model, and tool results go back without the model's reasoning.
- **W2-3 (transport, owner's approval 2026-10-22, between main runs).** The first two main runs (DeepSeek r0 and r1, E5) hit DeepInfra stalls.
  - **The stalls:** a call hung for about 300 s and then returned a 504 "Provider timed out".
    - The transport's 180 s socket timeout never fired, because OpenRouter keeps a waiting request open with keep-alive whitespace.
    - Each stall tied up a worker for 5 minutes and failed the whole run.
    - Under the old transport, DeepSeek r0 E5 lost 4 of 182 attempts, and DeepSeek r1 E5 lost 98 of its 180 first attempts.
    - The stalls came in waves; the successful calls' latency had a median of 0.9 s and a maximum of 13 s.
  - **The change, approved by the owner:**
    - a wall-clock deadline of 60 s per call (`deadline_seconds`, default 60);
    - a host timeout is retried like a rate limit: up to six retries, with waits of 2, 4, 8, 16, 30 and 30 seconds. A host timeout is an HTTP 504, a 504 error inside a 200 response, or no complete response within the deadline.
    - Each call records its count in `meta.timeout_retries`.
  - **Why this is safe:** a stalled call returns nothing and is not billed, so the agent never saw it, and the retry sends the identical conversation.
  - **One risk:** a call that would legitimately take more than 60 s is cut and re-sampled. No successful call has come near that.
  - **Scope:**
    - Every other error still fails the run, which then gets its single re-run.
    - The two E5 DeepSeek runs already finished keep their old-transport results as recorded.
    - The batch was stopped after DeepSeek r1 E5 ended. The remaining six main runs use the new transport.
    - Any partial calls of the next config before the stop are in its journal and count against its cap.
  - Tests cover each timeout path, the cap on the socket timeout, and that other errors are not retried.
  - No design element, threshold or agent-facing text changed.
- **W2-4 (re-run, owner's approval 2026-10-22, before the re-run).** DeepSeek r1 E5 (`runs/or-e5-deepseek-v4-1-flash-r1`) was INVALID on completion: 55–58% per cell, against the frozen 95%.
  - **Why:** every failed run failed on a DeepInfra stall of the kind W2-3 fixed, on its first attempt and again on its single re-run. 78 of 180 runs never completed. Protocol failures in the completed runs were 0.08%.
  - **The re-run:**
    - It runs the same config again on the fixed transport.
    - The 102 completed runs come from the cache and are not new samples.
    - The 78 failed runs start fresh, which is their third attempt.
    - Any run that fails in this pass gets the usual single re-run.
  - **Kept on record:**
    - the first pass's rows, as `results.pass1.jsonl`;
    - its reports, as `analysis.pass1/`;
    - every call from all passes, in `journal.jsonl`, all counting against the cap.
  - **Bias risk.** The stalls happened before any reply, did not depend on what the agent had done, and came in time waves. A third attempt should therefore not select runs by behavior.
  - **How to read the verdict:** the re-run decides whether the arm is valid at all, and then gives its E5 verdict. Both the pass-1 INVALID and the final verdict are reported.
  - No design element, threshold or agent-facing text changed.
- **W2-5 (re-run, owner's approval 2026-10-22, before the re-run).** DeepSeek r1 C4 (`runs/or-c4-deepseek-v4-1-flash-r1`) was INVALID on completion: 0.933 in two cells, against the frozen 0.95.
  - **Why:** 354 of 360 runs completed. The other 6 failed twice, each time on DeepInfra outages long enough to use up all seven tries of the W2-3 transport. No run failed for any other reason.
  - **The re-run:** the same procedure as W2-4. The same config runs again, the completed runs come from the cache, the 6 failed runs start fresh as their third attempt, and any failure in this pass gets the single re-run.
  - **Kept on record:** `results.pass1.jsonl`, `analysis.pass1/`, and every call in `journal.jsonl`.
  - **How to read the verdict:** both the pass-1 INVALID and the final verdict are reported.
  - No design element, threshold or agent-facing text changed.
- **W2-6 (scope, owner's decision 2026-10-23, after the DeepSeek and Qwen runs, before any gpt-oss call).**
  - **Gemma 4 31B is dropped from W2-A.** Its four configs keep their caps but are not run. The reason is W2-2: every bf16 host rate-limits it from a shared pool, so at 10 workers most runs would fail on rate limits rather than on the agent. Google is to be covered through a native Gemini transport instead.
  - **gpt-oss-120b (`openai/gpt-oss-120b`, pinned to `deepinfra/bf16`) is added** as the fourth open-weight family. It has one arm, r1, with reasoning effort `low`, because its reasoning cannot be turned off.
    - **Configs:** `live_or_c4_gpt_oss_120b_r1.json` and `live_or_e5_gpt_oss_120b_r1.json`, unchanged from their frozen versions except for the caps.
    - **Caps:** the proposed $4 (C4) and $1 (E5), against a $1.60 estimate.
    - **Procedure:** the same as the other W2 arms. One probe, then each pilot and its health check, then each main run under `w2_runner.py`'s credit rule. The comparisons are r1 against N1-A (Luna, native, low) for C4, and against N1-B for E5.
  - **Predictions for gpt-oss-120b,** recorded before any call; not part of the decision rule:
    - both traps solved under 20%;
    - S positive, with C4 CONTINUE_CREDULOUS or INCONCLUSIVE;
    - E5 D1 CONFIRMED.
    - **The main risk:** protocol failures from tool-call formatting through the host's parser.
  - No design element, threshold or agent-facing text changed.
- **W2-6, probe and pilots (2026-10-23; no deviation).**
  - **Probe:** passed. DeepInfra served it, and two native calls parsed cleanly.
  - **E5 pilot: passes the health gate.** 3 of 3 runs complete, protocol failures 4.2%, the tool called on request 1 in every run, estimate $0.04 against a $1 cap.
  - **C4 pilot: fails the health gate on protocol failures,** 12.2% of turns against the 10% gate.
    - 24 of the 33 failures are empty ANSWER lines. The reply starts with `ANSWER` and non-breaking spaces, then text that looks like leaked reasoning ("We need to output ANSWER UNKNOWN…"), and only then a valid `ANSWER UNKNOWN`. The parser takes the first ANSWER line, finds it empty, and counts a failure.
    - The rest are 5 malformed calls and 4 over-budget replies.
    - **Under the frozen gate, the C4 config is not run, and is reported to the owner.**
- **W2-7 (host, owner's decision 2026-10-24, before any call to the new host).** gpt-oss-120b's C4 arm moves to a second host. The owner rejected a parser rule for this arm alone, because it would score one model by a different rule.
  - **The new config** is `live_or_c4_gpt_oss_120b_r1_crusoe.json`, pinned to `crusoe/bf16`: the same precision as DeepInfra's bf16, and one of the cheaper bf16 hosts. Its run folder is `runs/or-c4-gpt-oss-120b-r1-crusoe`.
    - **Everything else is unchanged from the DeepInfra config:** model, reasoning `low`, temperature, token limit, seeds, cells, thresholds, the $4 cap, and every scoring rule.
    - The DeepInfra C4 config and its failed pilot stay on record. E5's valid run stays on DeepInfra, so gpt-oss's C4 and E5 results come from different hosts.
  - **Procedure:**
    1. a probe, then the pilot and the same health gate;
    2. if the gate passes, the main run under `w2_runner.py`'s credit rule, then the comparison with N1-A;
    3. **if the gate fails, gpt-oss stays E5-only.** That is the owner's fallback, and no further host is tried.
  - **The predictions are those of W2-6.** In addition: whether the empty-ANSWER failures came from DeepInfra's handling of the reply is exactly what this pilot tests.
  - **Probe and pilot (2026-10-24):** the probe passed (two clean native calls on Crusoe). The pilot **passes the health gate**: 12 of 12 runs complete, protocol failures 7.8% (against 12.2% on DeepInfra), the tool called on request 1 in every run, estimate $0.39 against the $4 cap. The main run follows.
  - No design element, threshold or agent-facing text changed.
- **W6-1 (re-run, owner's approval 2026-10-24, before the re-run).** gpt-oss-120b's W6 run (`runs/w6-gpt-oss-120b-r1`) was INVALID on completion: 0.933 in one cell (`caution_three` over the retry trap, 28 of 30), against the frozen 0.95.
  - **Why:** 598 of 600 runs completed. The other 2 failed twice on HTTP 502s from Crusoe: the host's tool-call parser rejected a call into which gpt-oss had leaked reasoning text ("unexpected tokens remaining in message header"). The other 20 runs that failed this way completed on their single re-run.
  - **The re-run:** the same procedure as W2-4 and W2-5. The same config runs again, the 598 completed runs come from the cache, the 2 failed runs start fresh as their third attempt, and a failure in this pass gets the single re-run. Cost: about $0.01.
  - **Kept on record:** the first pass's rows as `results.pass1.jsonl`, its reports as `analysis.pass1/`, and every call from both passes in `journal.jsonl`, all counting against the cap.
  - **Bias risk, higher than in W2-4 and W2-5.** Those failures were host stalls, unrelated to the agent. These come from gpt-oss's own output, so a third attempt selects runs by behavior. Two points limit the effect:
    - only 2 of 600 runs are involved;
    - the affected cell (the retry trap) enters no primary W6 measure, only the retry-trap contrasts. The primary verdicts were already computed in pass 1 and cannot change except through the validity label.
  - **How to read the verdict:** both the pass-1 INVALID and the final verdict are reported.
  - **Outcome:** both runs completed on their third attempt, and the run is VALID (600 of 600). The three primary verdicts are unchanged from pass 1 (WEAK_RESCUE, WEAK_RESCUE, RECOMMENDABLE); the intervals moved by at most 0.006.
  - No design element, threshold or agent-facing text changed.
- **W6-2 (stop and later restart, owner's approval 2026-10-24, before the restart).** Qwen3.8-27B r0's W6 main run (`runs/w6-qwen3-8-27b-r0`) was stopped at 17:45, 75 minutes in, with 19 of 600 runs complete.
  - **Why:** DeepInfra (bf16) served about 9 requests a minute, against about 340 in W2-B on the same host and settings. 9 runs had failed on client timeouts (60 s, six retries each). At that pace the run would take more than a day, and the single re-run of failed runs at the end would likely meet the same stalls, leaving the run INVALID on completion.
  - **The restart:** the same procedure as W2-4, W2-5 and W6-1. The same config runs again once the host is back to its usual speed. The 19 completed runs come from the cache. The 9 failed runs and the unfinished ones start fresh, and a failure gets the single re-run.
  - **Stop rule for the restart, fixed now:** if the restarted run serves fewer than 100 requests a minute over its first 10 minutes, it is stopped again and reported to the owner.
  - **The credit rule is checked again at the restart,** against the pilot estimate as before.
  - **Kept on record:** the stopped pass's rows as `results.pass1.jsonl`, and every call from both passes in `journal.jsonl`, all counting against the cap. The stopped pass spent about $0.15.
  - **Bias risk: low.** The failures were host timeouts with no reply, unrelated to the agent's output, as in W2-4 and W2-5.
  - **The restart (18:09), stopped again by the stop rule.** OpenRouter showed DeepInfra's endpoint as degraded (status −2) at the stop and normal (0) at 18:09. The restarted run served 41 requests a minute over its first 10 minutes (413 requests, no failures), below 100, so it was stopped at 18:19 and reported to the owner. By then 30 of 600 runs were complete, the 9 that had failed included. Its rows are kept as `results.pass2.jsonl`. Spend on Qwen so far: about $0.23.
  - **Second restart (owner's approval 2026-10-27, before the restart): the speed rule is dropped.** The owner accepts a slow run of 6 hours or more. DeepInfra bf16 showed status 0 and 100% uptime over the last day at 11:33. The same config runs again, and the 30 completed runs come from the cache. **The only stop rule left is for failures:** if more than 5% of the new runs fail (once at least 40 new runs have finished), the run is stopped and reported to the owner. Speed alone no longer stops it.
  - **Outcome:** the run finished at 12:37 on 2026-10-27, VALID, 600 of 600 complete, with no failures in this pass (DeepInfra served 120–220 requests a minute). Its rows: `results.pass1.jsonl` (stopped 2026-10-24), `results.pass2.jsonl` (stopped by the speed rule), `results.jsonl` (final). Qwen's W6 spend was $2.98 (pilot $0.11, all main passes $2.87).
  - No design element, threshold or agent-facing text changed.
