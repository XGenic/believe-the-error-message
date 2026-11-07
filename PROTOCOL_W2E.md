# C4 study W2-E: Claude Sonnet 5.5 and Gemini 3.8 Flash on C4 and E5 (frozen before any W2-E live call)

Status: **frozen**. This file, `configs/live_w2e_*.json` and their tests were committed before any W2-E live call, the pilots included. Changes after a W2-E live call must be logged in `NOTEBOOK.md` under "Deviations".

Sonnet is paid for by the owner personally, on the owner's Anthropic account. Gemini is paid for from OpenRouter credit.

## Question

The panel's only Anthropic model is its smallest, Google has no model in it, and no arm so far reasons at length: none averaged more than 35 reasoning tokens per call on C4. W2-E adds a larger Anthropic model and a fifth developer, and asks two things of each:

1. **Does the core pattern persist?** Credulity on the C4 grid and both traps.
2. **Does the first-encounter effect generalize?** E5.

## Design

Two designs, each exactly as already run through native tool calls:

| Design | Cells | Runs | Seeds (pilot) | Copied from |
|---|---|---|---|---|
| C4 grid | 12 (3 causes and non-diagnostic × 3 faults) | 30 per cell | 20261201 + r (20269201) | `live_n1_c4_native_low.json` (N1-A, W5, W2-C, W2-D) |
| E5 | 3 primes | 60 per cell | 20261701 + r (20269701) | `live_n1_e5_native_low.json` (N1-B, W5, W2-C, W2-D) |

Cells, seeds, decision rules and thresholds are copied from the configs named above; a test checks this. They were validated on scripted agents in their own studies, and neither their code nor their sample sizes change here.

**One setting per model, the model's own default, named in the request** so that a later change of default cannot alter it:

| Subject | Model | Transport | Setting | Output-token limit |
|---|---|---|---|---|
| Sonnet | `claude-sonnet-5-5` | `anthropic_messages_native`, as W2-C | adaptive thinking, effort `high` | 8,000 |
| Gemini | `google/gemini-3.8-flash` | `openrouter_chat_native`, as W2-A | reasoning effort `medium` | 16,000 |

The transports are unchanged. What differs by subject:

- **Sonnet:** no sampling parameter, and no server-side fallback, so a refusal stays a refusal and is never an answer from another model. A refusal is counted and reported. Each assistant turn goes back whole, thinking blocks included, as in W2-C.
- **Gemini:** pinned to Google AI Studio's flex tier (`google-ai-studio/flex`) at half the standard price, with no fallback to another host. Flex is the same model at a lower queue priority. No sampling parameter is sent. Reasoning cannot be turned off on this model. Reasoning details go back with each tool call, because Google requires its thought signatures in a tool loop. The output limit is above W2-A's 8,000 because one probe call at `high` reasoned for 7,678 tokens. Its wall-clock limit is 150 s, and timed-out calls are retried and counted as in W2-A.

W6 is not run. The counted stopping rule already held on 8 of 8 subject arms, R1 made a retry in code the main advice, and W6 would be about 60% of the cost.

## Cost probes before this protocol

**This study is registered before its first call on any misleading or non-diagnostic cell, but not before these models' first calls in this environment.** On 2026-11-06, with the owner's approval, seven small cost probes ran to estimate this study's budget (`NOTEBOOK.md`, Cost probes; `runs/probe/PROBE.md`). Each ran only the three accurate cells (`format|fixable`, `transient|transient`, `permanent|permanent`), 9 runs on development seeds 20262931–33, which W2-E does not use.

- **Settings:** this study's two (Sonnet's as frozen here; Gemini's at an 8,000-token limit), and five others: Sonnet with thinking off and at effort `max`, and Gemini at `low`, at `high`, and at `low` on flex.
- **Read before this protocol was written:** token use, cost, reasoning length, latency, stop reasons, refusals, calls per run, protocol failures and transport health.
- **Not read:** answers, success rates or next actions. The raw logs hold them for those three cells and were not analyzed for them.
- **No probe ran a trap, any other misleading cell, or a non-diagnostic cell,** so none shows how either model treats a false cause. Probe data enter no verdict, panel or comparison.

Any report of this study must disclose the probes.

## Decision rules

Each run gets the verdict of its own design, unchanged: C4's (CONTINUE_CREDULOUS, ...) and E5's (CONFIRMED, ...).

- **Primary: each subject's C4 verdict,** reported separately. There is no pooled verdict.
- **Secondary:**
  - Each subject's E5 verdict. An INVALID result is reported as such, as on Haiku with thinking off.
  - Each trap's success, against the non-diagnostic message over the same fault.
  - **Model:** Sonnet − Claude Haiku 5.5 with thinking on, by N1's comparison rule, for C4 (S and both traps) and E5 (D1), against W2-C's runs (same seeds). Descriptive: the runs are days apart, the two default efforts differ, and the models differ in more than size.
  - **Reasoning, descriptive:** the mean, median and 90th percentile of reasoning tokens per call on C4, overall, and on the call after an error in the give-up trap.

## Procedure

1. **Freeze:** protocol, configs at a $0 cap, tests.
2. **Approval:** the owner's approval and the caps, in a separate commit, before any call.
3. **Public registration, before any W2-E call:** the frozen protocol, configs and code, with the cost probes' configs and logs, are pushed to the public repository and published as a GitHub release (`w2e-protocol`), and the owner registers the same files on OSF. No pilot runs before both exist.
4. **Pilots:** one run per cell on the development seed, for each config. The W2 health gate applies: every run complete, protocol failures of 10% or less, the tool called on request 1 in at least 90% of runs, and the estimate within the cap.
5. **Main runs**, each only after its pilot passes the gate, C4 before E5 within a subject. A run whose pilot estimate exceeds its cap is not run, and is reported. Money left under one run's cap can move to another run only on the owner's word, logged as a deviation.
6. A run INVALID on completion through transport failures gets the W2-4 re-run (completed runs from the cache), logged as a deviation.
7. **If flex fails the health gate or stalls a main run,** Gemini stops and this is reported. Moving to the standard tier doubles its rates, so it needs the owner's word and new caps, logged as a deviation.

## Predictions (recorded before any W2-E call; not part of the decision rule)

- **Primary, Sonnet: CONTINUE_CREDULOUS,** with both traps solved in at most 10% of requests.
- **Primary, Gemini: CONTINUE_CREDULOUS,** with the give-up trap solved in at most 15% of requests and the retry trap in at most 25%. Longer reasoning may explore more; the highest retry trap so far is 16%, DeepSeek with reasoning on.
- **E5 CONFIRMED on both.** Haiku is the panel's exception, and Sonnet will behave more like the larger models.
- **Sonnet − Haiku:** SAME on both traps; D1 DIFFERENT, because Sonnet shows the first-encounter effect and Haiku did not.
- **Reasoning on C4:** Sonnet averages at most 30 tokens per call; Gemini averages at least 171, its accurate-cell figure in the probe.
- **Cost:** each main run falls within its estimate below.

## Budget

**Approved by the owner on 2026-11-06: $32.50 in all, pilots included: $16.50 for Sonnet and $16.00 for Gemini.** Each cap covers that config's pilot and main run. OpenRouter holds $14.47, so for Gemini that balance is the binding limit unless the owner adds credit. A run stopped by it is reported as stopped.

Estimates come from the probes, projected between the call volumes measured on Haiku (gives up early) and GPT-6.1 Sol (persists). Prices, read 2026-11-06: Sonnet $2 in, $2.50 cache write, $0.10 cache read, $10 out per million tokens (Anthropic's pricing page). Gemini on flex $0.375 in, $0.0375 cache read, $1.875 out (OpenRouter's listing; recorded cost is OpenRouter's billed figure).

| Config | Runs | Estimate | Cap |
|---|---|---|---|
| C4, Sonnet | 360 | $5.17–10.00 | $13.50 |
| E5, Sonnet | 180 | $1.11–1.49 | $3.00 |
| C4, Gemini | 360 | $4.93–10.36 | $13.50 |
| E5, Gemini | 180 | $0.99–1.34 | $2.50 |
| **Total** | 1,080 | **$12.20–23.19** | **$32.50** |

The caps sit above the estimates for two reasons: accurate cells understate reasoning, and the spend guard holds back each worker's worst-case call ($0.10 for Sonnet, $0.035 for Gemini; 10 workers). A backtest on finished C4 runs put this projection method at −4% to +13% of real cost on most models and about 35% over on Sol, at each model's real call volume.

## Known limits

- **One setting per model,** so W2-E cannot separate reasoning from the model. If Gemini differs from the panel, reasoning length is one possible reason among others.
- **The two subjects differ in setting and tier:** Sonnet's default barely reasons in this task (5 tokens per call in the probe), and Gemini's reasons more (171). Neither result stands for its model at other settings.
- **Replayed reasoning differs across the panel.** Anthropic and Gemini runs carry reasoning forward through the conversation; OpenAI and open-weight runs do not.
- **No stopping-rule results** for these models, because W6 is not run.
- **Flex is a price tier.** It has only been tried on 360 calls at 3 workers; the pilots try it at 10.
- **Still not run:** Claude Opus and Fable, Gemini 4 Argon, and any setting that makes Sonnet reason at length.
