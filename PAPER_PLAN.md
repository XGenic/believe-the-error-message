# Plan: from C4 to a submittable paper

> **Historical snapshot.** This plan was written on 2026-10-20 and is kept as it was then, with its spending figures of that date. It has not been updated since. Since then: W2 (the open-weight panel, and Claude Haiku 5.5 through the Anthropic API), W5 (reasoning effort) and W6 (wordings of the stopping rule) are done; W3 (benchmark injection) and the frontier models are not. For the current state see [`README.md`](README.md), [`REPORT.md`](REPORT.md) and [`NOTEBOOK.md`](NOTEBOOK.md).

**Status, 2026-10-20.** This is a plan, not a commitment. **Phase 1 (W0, W1, W4) is done; see §9.** Later phases have no budget yet. Each workstream that spends money needs its own approval, frozen protocol and pilot, as C4 and E1–E5 had. The current results are in [`REPORT.md`](REPORT.md).

## 1. The claim the paper would make

> LLM agents take the cause stated in a tool error as ground truth, and choose their recovery from it. This produces two failure modes:
> - **a retry trap:** endless identical retries of a request that needs fixing;
> - **a give-up trap:** stopping before a call that would work.
>
> Neither corrects itself when every error looks the same. Trust is set by experience within the conversation: before an agent has worked through any error, it takes "unavailable" at its word. After working through one error, even one that never cleared, it persists indiscriminately. A one-sentence caution with a stopping rule removes the first-encounter failure at close to the minimum cost.

This is useful to three groups:

- **API designers:** a wrong cause is worse than no cause, and "unknown" is better than "rejected".
- **Agent builders:** the bounded caution, and the first-encounter risk.
- **Evaluators:** benchmarks with homogeneous error conditions overstate or understate recovery.

## 2. What we have

| Study | Models | Size | Result |
|---|---|---|---|
| C4 kill test, 12 cells | Haiku 5.5, GPT-6-luna | 360 runs each | stated cause steers recovery (S +0.34 / +0.96) |
| E1, 18-request runs | both | 48 runs each | no learning when all errors are alike |
| E2, one-sentence fixes | Luna | 630 runs | caution rescues the give-up trap at a cost; retry trap resists |
| E3, stopping rule | Luna | 480 runs | rescue kept at the floor cost (COST_AWARE) |
| E4, mixed errors | Luna | 160 × 12-request runs | traps weaken in mixed conversations; caution's net gain about +4 points |
| E5, cleared-error test | Luna | 180 runs | one earlier error flips "give up" (100%) to "persist" (3%); mostly from effort, not payoff |

**Strengths to keep:**

- Every design was frozen before data, with $0 caps until approved.
- Scripted-agent validation and power analysis.
- Predictions recorded and scored: 17 of 24 held across E2–E5.
- Full logs of every call.

**Spend so far:** about $36.50.

## 3. What a reviewer will say, and the answer to each

| Objection | Severity | Answer, and the workstream that delivers it |
|---|---|---|
| "Two models, and the interventions only on one." | **high** | a panel of models (W2) |
| "Toy environment; the faults are engineered to mislead." | **high** | inject errors into an existing agent benchmark (W3); an audit of real misleading errors (W4) |
| "A made-up text reply format. Luna needed workarounds (L1, L2)." | **high** | native function calling (W1) |
| "Is this about reasoning?" (Luna ran with reasoning effort `low`, Haiku with none) | medium | a reasoning-effort sweep (W5) |
| "One wording per intervention." | medium | three wordings for each key intervention (W6) |
| "Many contrasts; separate verdicts per model." | medium | a hierarchical model across models, plus corrections for multiple primaries (W6) |
| "Results depend on run order." Bootstrap intervals shift slightly when mock runs are rebuilt from cache, because `results.jsonl` is written in thread-completion order. | low, but must fix | sort runs before the bootstrap (W0) |
| "Prior work already covers this." | medium | verify and position against the 2026 tool-unreliability papers listed in `PROTOCOL.md`. Those citations are unverified so far. (W7) |

## 4. Workstreams

### W0: reproducibility hygiene

*About 1 day, $0. Do first.*

- **Make analysis independent of row order:** sort runs by `run_id` and attempt in `analyze()` before the bootstrap.
  - Re-generate every report.
  - Log the change as a deviation that touches intervals only.
  - Point estimates do not change.
- **One script that re-runs every analysis** from the committed raw data, and checks a hash of each report.
- **A data card:** what each `results.jsonl` row holds, the licence, and a statement that there are no personal data or credentials.
- **Optional:** post the frozen protocols on OSF, to add an external timestamp to the git history.

**Done when** a fresh clone reproduces every number in the paper with one command.

### W1: native function calling

*About 2–3 days, under $5.*

- **A transport that uses each provider's tool-call API** instead of CALL/ANSWER text: the OpenAI Responses `tools`, Anthropic `tool_use`, and the equivalents for open-weight models.
  - The errors come back as tool results.
  - There is no L1 or L2, so Luna can run with reasoning off.
- **Equivalence check, pre-registered:**
  - Re-run the four core cells (the two traps and their accurate pairs) and the E5 prime test on Luna and Haiku.
  - Compare with the text-protocol results.
  - If behavior differs, that is itself a finding: format sensitivity.

**Done when** the core effects are measured through native tool calls on both current models.

### W2: a panel of models

*About 1–2 weeks, roughly $300–800.*

- **Six to eight models:** at least two from each of Anthropic, OpenAI and Google, plus two or three open-weight models, such as Qwen, Llama and DeepSeek.
  - Include each model's reasoning on/off variant where one exists.
- **A reduced core design per model:**
  1. **C4 core:** the two traps, their accurate cells, and the neutral baselines over the fixable and transient faults. About 6 cells × 30 runs.
  2. **E5:** the first-encounter test, 3 conditions × 60 runs. It is very cheap.
  3. **E3:** the bounded caution against control on the give-up trap and its accurate cell. 2 arms × 2 cells × 30 runs.
- **Analysis:** a mixed-effects logistic model with fixed effects for cell or condition, and random intercepts and slopes by model. Report the share of models showing each effect.
- **Cost driver:** frontier models. Use reduced grids for the most expensive ones, and API prompt caching where available.

**Done when** each headline effect has an estimate across the panel, with a between-model spread.

### W3: realism, by injecting errors into an existing benchmark

*About 1–2 weeks. Cheap models first, then $100–300.*

- **Choose one benchmark with stateful tools,** such as τ-bench (retail or airline) or AppWorld.
- **Wrap its tool layer.** On chosen calls, return an error whose stated cause is wrong, in the two trap patterns:
  - "temporary" over an argument error that the agent can fix;
  - "unavailable" over a fault that clears on retry.
- **Use matched accurate-error and no-error controls.**
- **Measure task success, calls and harmful actions,** for control against the bounded caution.
- **Realism checks:** errors injected at a low base rate (5–15%), the benchmark's own system prompts, and no other changes.

**Done when** there is a headline like "misleading errors cut success by X points, and the bounded caution recovers Y, at Z extra calls" on a benchmark others already use.

### W4: misleading errors in the wild

*About 3–5 days, $0.*

- **Collect 30–50 documented cases** where a production error message stated the wrong cause. Sources: API changelogs, GitHub issues, status-page post-mortems, and Stack Overflow.
  - Code each case's stated cause against its true cause, on the C4 axes: format, transient, permanent.
- **Purpose:** motivation and external validity.
  - It shows that both trap patterns occur, such as 503 "unavailable" for a malformed request, or "rate limited" for an authentication fault.
  - It gives a rough idea of which miscodings are common.

**Done when** there is a table of real cases, with sources, in an appendix.

### W5: does reasoning change anything?

*About 3–4 days, $20–50.*

- **Luna at reasoning effort none, low, medium and high** through native tools (W1), on the core cells and E5. If W2 shows reasoning on/off differences, add one Anthropic model with extended thinking.
- **For models that expose reasoning,** code a sample of traces for the cause the agent states. This is a pre-written rule plus a human check of about 100 items, with no LLM judge for primary measures. It addresses why the retry trap resists: does the agent blame the depot first?

### W6: robustness and statistics

*Runs alongside W2; mostly $0.*

- **Three wordings each** for the caution and the bounded caution; about $10 on cheap models.
- **Pre-specify one primary per study** and correct across them (Holm). Everything else is secondary.
- **Report effect sizes with intervals,** not only verdicts.
- **Fix the E1 bootstrap degeneracy** (zero-width intervals when every run follows): use a Wilson or Bayesian interval for proportions near 0 or 1.

### W7: writing

*About 1–2 weeks.*

**Title options:**

- "The error message is the diagnosis: LLM agents act on stated causes of tool failures"
- "Believing the error message: first-encounter credulity in LLM tool agents"

**Outline:**

1. Introduction: error messages as evidence; the two traps.
2. Related work: tool unreliability, fabrication after failure, misattribution and attribution theory.
3. Paradigm: stated cause × true cause; measures; pre-registration.
4. Results:
   - 4.1 credulity across models;
   - 4.2 no learning when errors are alike;
   - 4.3 first-encounter dynamics (E4, E5);
   - 4.4 interventions and their cost (E2, E3);
   - 4.5 benchmark injection (W3).
5. Discussion: advice for API designers and agent builders, limits.
6. Appendix: protocols, deviations, the error audit, scripted-agent validation, all prompts.

**Figures:**

1. The stated × true heatmap per model.
2. Learning curves (E1) beside the E5 prime effect.
3. Intervention rescue against outage-call cost, with the floor of 3 marked.
4. Benchmark success under injection.

## 5. Order and time

| Phase | Workstreams | Calendar (part-time) | Spend |
|---|---|---|---|
| 1 | W0, W1, W4 (**done**; $2.20) | about 1–2 weeks | under $5 |
| 2 | W2 with W6; W5 | about 2–3 weeks | $350–850 |
| 3 | W3 | about 2 weeks | $100–300 |
| 4 | W7 | about 1–2 weeks | $0 |

That is about 6–9 weeks part-time and about $450–1,150 API-equivalent. Most of the spend is frontier models in W2. A cheaper path, open-weight and small models only, would cost about $150–300 and weaken the panel.

## 6. Where to submit

- **arXiv preprint:** once phases 1–2 are done. A many-model study of the paradigm with native tool calls is a credible standalone preprint.
  - **Practical:** first-time submitters in cs.AI or cs.CL usually need an endorsement from an established author. Arrange this early.
- **Workshops:** agents, safety or trustworthy-ML workshops at ICLR, ICML or NeurIPS, with phases 1–2. These have a lower bar and give fast feedback.
- **Main-track or findings-track paper** (ACL, EMNLP or NAACL through ACL Rolling Review; or COLM): needs phase 3, the benchmark injection, to answer the realism objection.
- **Deadlines:** check the current calendars. I have not verified 2027 dates.

## 7. Risks

- **Effects vary across models.** That is still publishable: "credulity is model-dependent" is a finding. The E5 first-encounter effect is the most likely to generalize, and the cheapest to test.
- **Benchmark injection looks contrived.** The W4 audit should drive which miscodings are injected and at what rate.
- **Cost of frontier models.** Use reduced grids and caching. Drop to one model per provider if needed.
- **Model churn.** Record exact model IDs and dates, and keep raw logs. They are already kept.
- **Pricing is unverified.** Report costs as API-equivalent, with the source of the prices.

## 8. Decisions for the owner

1. Approve phase 1 (W0, W1, W4; under $5).
2. Choose the panel for W2, and its budget ceiling.
3. Choose the W3 benchmark: τ-bench or AppWorld.
4. Decide on authorship, endorsement and a target venue.

## 9. Phase 1 outcome (2026-10-20; spend $2.20 of the approved $5)

- **W0, done.**
  - Analysis no longer depends on row order.
  - Every derived file is written with LF.
  - `runs/MANIFEST.json` pins 97 raw files across 11 live runs.
  - `python -m causetest reproduce` passes, byte for byte.
  - Data card: [`DATA_CARD.md`](DATA_CARD.md).
  - Regenerating the reports moved interval bounds by at most 0.03, and changed no verdict (deviation W0-1).
- **W1, done for the OpenAI side (study N1).**
  - Native tool calls leave both traps and the E5 first-encounter effect unchanged.
  - They do change the *size* of S (0.96 → 0.79) and E5's secondary measure. Through native calls, errors that never cleared teach far less persistence (63% still stop at once, against 22%).
  - With reasoning off (newly possible), Luna's default after a neutral error is to give up, so S falls to 0.54. Neither trap moves.
- **W4, done:** [`ERROR_AUDIT.md`](ERROR_AUDIT.md). 25 documented misleading production errors, covering both trap patterns, plus 4 honest messages.

**What this changes for phase 2:**

1. **Run the model panel (W2) through native tool calls only.** The text format adds a model-specific confound: Luna needed L1 and L2. Native transports are needed for Anthropic, through the Messages API with an Anthropic key, and for Google and the open-weight models.
2. **Report S together with its neutral baseline.** S is a difference from the baseline, and the baseline (the agent's default after an uninformative error) varies with format and with reasoning. Trap success and first-response follow rates are more robust headline measures.
3. **Report E5's secondary measure (cleared against never-cleared) with its format,** and repeat it across the panel. The primary first-encounter effect is the robust one.
4. **Make reasoning effort a factor** (W5), not a nuisance. On Luna it changes the default stance after an uninformative error, from exploring to giving up.
## 10. Funding

**Anthropic External Researcher Access Program** ([program page](https://support.claude.com/en/articles/9125743-what-is-the-external-researcher-access-program); read on 2026-10-20):

- It gives free API credits, typically $1,000, for **AI safety and alignment research** on topics Anthropic considers high priority.
- It covers Anthropic models only, with no access to non-public models.
- Applications are reviewed on the first Monday of each month. Unsuccessful applicants hear nothing.
- **Fit for this project.** It plausibly qualifies as agent reliability and safety research: agents acting on false tool feedback, giving up or looping, and cheap mitigations. That fit is strongest if the application is framed around safety-relevant agent behavior, not around API error handling.
- **It would fund the Anthropic part of the W2 panel** (Haiku, Sonnet), including the Anthropic native transport. It would not fund OpenAI, Google or open-weight models.
- **Before applying:** make the repository public, or prepare a shareable summary (`REPORT.md`, `ERROR_AUDIT.md`), and choose a licence (see `DATA_CARD.md`).
