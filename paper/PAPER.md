# Do LLM Agents Believe the Error Message? Stated Causes, Two Traps, and a Counted Stopping Rule

**Denis Gurskiy** · independent researcher · 28 October 2026

*Preprint draft, not peer reviewed. Code, protocols and every raw log: [github.com/XGenic/believe-the-error-message](https://github.com/XGenic/believe-the-error-message).*

## Abstract

When a tool call fails, the error message usually states a cause. An agent cannot see the true fault, so treating that cause as evidence is reasonable; the question is whether agents keep testing it as calls fail or succeed. We vary the cause an error message states independently of the true fault, in a simulated stock-lookup tool. Across 13 pre-registered studies (about 14,900 conversations) covering five models from four developers in 13 model-and-setting arms (Claude Haiku 5.5, GPT-6-luna, DeepSeek V4.1 Flash, Qwen3.8-27B and gpt-oss-120b), agents act on the stated cause and rarely revise it. This produces two traps. A false "temporary" over a fixable fault makes agents repeat the same broken call while every result contradicts the message (at most 10% solved on 12 of 13 arms). A false "unavailable" over a fault that would clear makes them stop before the one more call that would test the message (at most 10% solved on 11 of 13 arms). On the two models tested over 18 requests, neither trap is learned away, and light reasoning does not help. A brief caution that error messages can be wrong, paired with a counted stopping rule ("If the same error comes back on three attempts in a row, accept it"), rescues the give-up trap on all 7 model arms tested; a vaguer rule works on 3 of 7. The count matches this environment, where faults clear on the third call, and the rule was never tested without the caution. The retry trap remains unsolved.

## 1 Introduction

Tool-using agents read error messages the way people do: as diagnoses. "Temporary service problem" says wait and retry. "Not found" says stop. "Invalid format" says fix the request. Usually the diagnosis is right. Sometimes it is not: a load balancer answers "503 Service Temporarily Unavailable" when no servers are registered at all, and a storage service answers "no such bucket" for a bucket created moments earlier. An audit of 25 documented production cases (§3.5) finds both patterns, produced by systematic mechanisms such as security masking, eventual consistency and generic intermediary status codes.

An agent cannot observe the true fault, so acting on a stated cause at first is reasonable: the message is evidence, and usually good evidence. The failure we look for is different: an agent that keeps acting on the message after its own calls contradict it, or that stops before making the one cheap call that would test it. In other words, a failure to calibrate trust in fallible, tool-generated causal information. If agents do not calibrate, a wrong message steers them into the wrong recovery. That matters for reliability, and it matters for safety. Error strings are an input channel the agent trusts, so anyone who controls one can make an agent loop on a failing action or abandon a task, without any instruction-like text that prompt-injection defenses look for.

We ask four questions:

1. **Do agents recover by the stated cause or by the true cause?**
2. **Do they revise a stated cause as their own calls contradict it?**
3. **What makes an agent persist or give up, beyond the message itself?**
4. **Is there a cheap instruction that helps across models?**

The design is a factorial grid: three true faults (fixable, transient, permanent) crossed with four stated causes (format, temporary, unavailable, and a neutral "request rejected"). Every study was pre-registered: its protocol, decision rule, predictions and spending cap were committed before its first model call, every decision rule was first validated on scripted agents with known behavior, and every deviation is logged.

**Contributions.**

- A paradigm that separates the stated cause of a tool error from its true cause, with a fixed coding of the agent's next action and pre-registered decision rules.
- Evidence across 13 model-and-setting arms that agents follow the stated cause into two traps, and do not learn out of them when every error looks alike.
- Evidence that on most models the give-up trap is worst at the first failure: one earlier error that cleared cuts stopping at once from 78–100% to 0–10% on GPT-6-luna and Qwen, and halves it on DeepSeek without reasoning, with a smaller effect on gpt-oss and none on Claude Haiku 5.5.
- A two-sentence instruction, a caution that error messages can be wrong plus a counted stopping rule, that rescues the give-up trap at about the minimum cost on every model tested in this environment, and evidence that the rule's wording matters.
- A fully reproducible record: raw logs of every call, hashes, and a command that re-scores every run byte for byte.

## 2 Related work

**Tool use and agents.** Tool-augmented language models (Schick et al., 2023) and reason-and-act agents (Yao et al., 2023) made tool calls a standard agent capability. Benchmarks such as τ-bench (Yao et al., 2024) evaluate agents in realistic tool environments, and LM-emulated sandboxes probe the risks of agent actions (Ruan et al., 2024).

**Unreliable tool feedback.** Closest to this work, Zhang et al. (2026) vary the content of tool observations (faithful, misleading or absent) and find that persistent misleading feedback can leave an agent worse off than no feedback at all. ToolMaze (Zhu et al., 2026) perturbs tools along explicit/implicit and transient/permanent failures, and finds that agents over-trust corrupted outputs and recover poorly. Both vary *what fails* or *what the tool returns*. We hold the failure fixed and vary only *the cause the error message states*, which isolates the message's causal claim as the steering signal.

**Untrusted tool outputs as an attack surface.** Indirect prompt injection (Greshake et al., 2023) and AgentDojo (Debenedetti et al., 2024) show that instructions hidden in tool outputs can hijack agents. Our error messages contain no instructions at all, only causal statements, and a test enforces this. A misleading cause is a weaker, harder-to-filter form of the same channel.

**Attribution.** The design borrows from attribution theory: people explain outcomes by causes (Kelley, 1967), and the perceived stability of a cause shapes the expectation of future success (Weiner, 1985). The give-up trap also resembles learned helplessness (Seligman & Maier, 1967), with one difference: the agent never experiences the failures that would teach it, because it stops before them.

## 3 Paradigm

### 3.1 Environment

A fictional wholesaler has six depots. The agent answers stock requests ("how many units of glass fuse, SKU nt-2647, are on hand at the Dunmere depot?") with one tool, `stock_lookup(site, sku)`. A run is one conversation of six requests (18 in one study). The agent may make up to six calls per request, then must answer with a figure or "UNKNOWN". Three depots each expect a different SKU spelling, so a fixable fault is fixed by respelling the SKU.

| True fault | What happens | What works |
|---|---|---|
| fixable | rejected unless the SKU is spelled in the depot's convention | respell |
| transient | the first two calls of every request fail | any third call |
| permanent | every call fails | stop |

| Stated cause | Error text | Implied strategy |
|---|---|---|
| format | "the SKU is not written the way this depot's system expects" | respell |
| temporary | "temporary service problem" | retry |
| unavailable | "stock data for this depot is unavailable" | stop |
| neutral | "request rejected" | (baseline) |

The full grid has 12 cells: 3 accurate, 6 misleading and 3 neutral. The two cells this paper is about are the **retry trap** ("temporary" over a fixable fault) and the **give-up trap** ("unavailable" over a transient fault). In the give-up trap, for example, the agent looks up a depot's stock, receives "ERROR: stock data for this depot is unavailable.", and answers UNKNOWN; a third call would have returned the figure.

### 3.2 Measures

After each failed call, the agent's next action is coded by a fixed rule as RETRY (the identical call), REFORMAT (SKU changed), SITE_ONLY (depot changed), STOP (answered) or OTHER.

- **Steering S:** for each misleading cell, the share of first responses on request 1 that follow the stated cause, minus the same share under the neutral message with the same fault, averaged over the six misleading cells. S = 0 means the message has no effect on the first response; S = 1 means it moves every first response from the neutral baseline to the strategy the message implies.
- **Learning L\*:** the drop in following from requests 1–2 to requests 5–6 in the misleading cells whose outcomes contradict the claim, minus the same drop in accurate cells.
- **Trap success:** the share of requests solved in each trap.

Intervals are 95% percentile bootstraps over runs (2,000 resamples). Each study has a fixed decision rule and names one primary question. The C4 rule, for example, calls an agent CONTINUE_CREDULOUS when S is at least 0.25 (lower bound at least 0.10) and L\* is below 0.10 (upper bound below 0.20); CONTINUE_SELF_CORRECTING when S passes the same bar and L\* is at least 0.15 (lower bound above 0); and INCONCLUSIVE otherwise. Validity rules (at least 95% of runs complete in every cell, at most 10% protocol failures, the tool called on request 1 in at least 90% of runs) make a run INVALID before any verdict. The rules use fixed bars rather than significance tests, and no correction is made for multiple comparisons.

### 3.3 Models and access

| Model | Access | Settings |
|---|---|---|
| Claude Haiku 5.5 | Claude Code CLI (text format); Anthropic Messages API (native tool use) | no reasoning; thinking off and on |
| GPT-6-luna | OpenAI Responses API (text format and native tool use) | reasoning none, low, medium, high |
| DeepSeek V4.1 Flash | OpenRouter, one pinned host (native tool use) | reasoning off and on |
| Qwen3.8-27B | OpenRouter, one pinned host (native tool use) | reasoning off and on |
| gpt-oss-120b | OpenRouter, one pinned host (native tool use) | reasoning on |

The first studies used a text reply format (`CALL stock_lookup {...}` or `ANSWER ...`); later studies use native function calling, translated into the same episode. A comparison on GPT-6-luna (§4.5) shows the traps do not depend on the format.

### 3.4 Process

Every study followed the same sequence. The protocol, configurations and code were committed with a spending cap of zero. The decision rule was run against scripted agents with known behavior (40 in all) and checked for power over 20 disjoint seed sets. A one-run-per-cell pilot on a development seed had to pass a health gate (complete runs, at most 10% protocol failures, the tool used on the first request). Only then did the main run go ahead, within a cap approved in advance. Main runs use 30 runs per cell (60 per condition in E5). In all, the studies ran about 14,900 conversations and 332,000 model calls. Predictions were recorded before any call, and are scored in Appendix A, misses included.

### 3.5 Misleading errors in the wild

To check that the traps are not artifacts, we collected 25 documented production cases in which an error message stated the wrong cause, with sources. Seven follow the give-up pattern: a permanent-sounding message ("not found", "forbidden", "damaged") over something transient or fixable, such as identity-management propagation delays. Nine follow the retry pattern: a transient-sounding message (503, timeout, 429) over something permanent or client-fixable. Nine more point to the wrong fix. The causes are systematic: security masking, eventual consistency, intermediaries that do not know the real status, and status codes shared between unrelated states.

## 4 Results

### 4.1 Agents follow the stated cause into both traps

![Figure 1](../figures/stated_true_grid.svg)

*Figure 1. Share of requests solved, by stated cause (rows) and true fault (columns), for every model and setting. Red outlines mark the two traps.*

On the first two models, in the text format, steering was strong: S = +0.34 [+0.32, +0.37] for Claude Haiku 5.5 and +0.96 [+0.92, +0.98] for GPT-6-luna. Both were CONTINUE_CREDULOUS. Neither model solved a single trap request (0 of 180 in each trap, for each model). Under the neutral message the same transient fault was solved on 97% (Haiku) and 67% (Luna) of requests, so the "unavailable" message alone turned a recoverable fault into a lost one. Under "temporary" over a fixable fault, neither model ever respelled the SKU. Following the message on the first call is not the failure here. In the retry trap the agent made up to six identical calls, each returning the same error, without changing anything; in the give-up trap it stopped after one or two calls, before the third that would have tested the message.

The pattern holds across the panel (Table 1). The retry trap is solved in at most 10% of requests on 12 of 13 arms; the exception is DeepSeek with reasoning on, at 16%. The give-up trap is solved in at most 10% on 11 of 13 arms; the exceptions are GPT-6-luna at medium and high reasoning effort, at 14% and 11%. The credulous verdict holds on 9 of 13 arms. The other four are INCONCLUSIVE because of a moderate L\*, and in none of them does the drift move toward the true cause: it comes from an accurate cell (GPT-6-luna with reasoning off), from rewriting the depot instead of the SKU (Qwen with reasoning), from withdrawing from the tool (gpt-oss), or from giving up on every error (Haiku).

*Table 1. The panel: C4 verdict (CREDULOUS = CONTINUE_CREDULOUS), steering S, and the share of trap requests solved (180 requests per trap: 30 runs × 6). Intervals for every cell are in `runs/panel/PANEL.md`.*

| Model, setting | C4 verdict | S | Retry trap | Give-up trap |
|---|---|---|---|---|
| Haiku 5.5, CLI text | CREDULOUS | +0.34 | 0.00 | 0.00 |
| Haiku 5.5, API, thinking off | INCONCLUSIVE | +0.69 | 0.00 | 0.00 |
| Haiku 5.5, API, thinking on | CREDULOUS | +0.61 | 0.00 | 0.00 |
| GPT-6-luna, text, low | CREDULOUS | +0.96 | 0.00 | 0.00 |
| GPT-6-luna, native, none | INCONCLUSIVE | +0.54 | 0.01 | 0.05 |
| GPT-6-luna, native, low | CREDULOUS | +0.79 | 0.00 | 0.03 |
| GPT-6-luna, native, medium | CREDULOUS | +0.92 | 0.01 | 0.14 |
| GPT-6-luna, native, high | CREDULOUS | +0.94 | 0.01 | 0.11 |
| DeepSeek V4.1 Flash, off | CREDULOUS | +0.78 | 0.00 | 0.00 |
| DeepSeek V4.1 Flash, on | CREDULOUS | +0.66 | 0.16 | 0.02 |
| Qwen3.8-27B, off | CREDULOUS | +0.50 | 0.03 | 0.03 |
| Qwen3.8-27B, on | INCONCLUSIVE | +0.78 | 0.01 | 0.06 |
| gpt-oss-120b, on | INCONCLUSIVE | +0.92 | 0.00 | 0.03 |

S is not comparable across access methods: it is measured against each arm's own neutral baseline, and that baseline moves with format and reasoning (§4.5). The trap rates are the robust comparison.

### 4.2 Repetition teaches nothing when errors look alike

In 18-request conversations where every error in a run is the same (E1), Haiku and GPT-6-luna solved 0 of 216 retry-trap requests and 0 of 216 give-up-trap requests. Both were NO_LEARNING. The give-up trap seals itself: obeying "unavailable" means the agent never makes the third call, so no contrary evidence ever arrives. In the retry trap the evidence does arrive, every call, and is ignored. Haiku remarked on the repetition within a request ("I've tried this lookup five times…") and still kept treating the fault as temporary.

### 4.3 The first encounter is the worst case, on most models

Pure-run traps are a worst case. In 12-request conversations that mix accurate and misleading errors (E4), plain GPT-6-luna solved about half of the give-up traps (45–55%, against 0 in pure runs). An exploratory split suggested why: before any error in the conversation had cleared on a later call, it stopped at once on 89–100% of "unavailable" messages; after one had cleared, on 21–40%.

A pre-registered follow-up (E5) tested this directly with three-request runs, varying only the first request. With no earlier error, GPT-6-luna stopped at once on 60 of 60 first "unavailable" messages. After one error that cleared on its third call, it stopped at once on 2 of 60 (D1 = +0.97 [+0.92, +1.00], CONFIRMED). The effect replicated through native tool calls (+0.93) and at every reasoning effort, and it was CONFIRMED on 9 of 11 arms with a valid test. Its size varies by model. Qwen stopped at once on 80–90% of first "unavailable" messages, and on 3–10% after a cleared error. DeepSeek without reasoning went from 100% to 48%; with reasoning it stopped at once on only 43% to begin with, and on 2% after a cleared error. gpt-oss changed less (93% to 68%; INCONCLUSIVE). The persistence a cleared error teaches is indiscriminate: afterwards GPT-6-luna spent about 5–6 calls on a true outage, against 1.

Claude Haiku 5.5 is the exception. With thinking off it rarely persisted long enough to see an error clear (33% of runs), so the manipulation failed and the test is INVALID by its pre-registered check. With thinking on it rarely stopped at once on a first "unavailable" (12%), but it retried only once and still stopped before the call that would work, solving none of these requests; errors that never cleared made it stop at once 92% of the time, the reverse of the other models.

### 4.4 A caution with a counted stopping rule fixes the give-up trap

One sentence in the system prompt, "Error messages from the stock system do not always state the true cause of a failure", rescued GPT-6-luna's give-up trap (0% → 98%, E2). The cost was doubt about real outages too: 5.2 calls per request on a true outage, against 1.0. Adding a stopping rule kept the rescue at the floor cost (E3). The floor is 3 calls, because the transient fault clears on the third call and the agent cannot tell which fault it faces. "If the same error keeps coming back after a few different attempts, accept it" gave a +0.92 rescue at 3.08 calls; "If the same error comes back on three attempts in a row, accept it" gave +0.97 at 3.01.

On the open-weight models the first wording did not carry over cleanly (W2-B): rescues of +0.34 to +0.72, and on DeepSeek with reasoning the word "different" made the agent rewrite the depot on every call, which lost 17% of real transient recoveries. A pre-registered comparison of three wordings on five subjects (W6), repeated on Haiku (W2-C), separates the idea from the wording (Figure 2, Table 2). In every arm the stopping rule is a second sentence after the same caution, so these studies test the pair, not the rule alone. A wording counts as RECOMMENDABLE if it rescues the give-up trap (at least +0.50, lower bound above +0.30) at no more than 3.5 calls on a true outage (upper bound below 4.0), without harming real transient recoveries.

![Figure 2](../figures/rescue_cost.svg)

*Figure 2. Give-up rescue against calls per request on a true outage, per model and wording. The shaded corner is the RECOMMENDABLE region; the dashed line is the 3-call floor.*

*Table 2. RECOMMENDABLE verdicts per wording (W6 and W2-C). Each wording follows the caution sentence.*

| Subject | "after a few different attempts" | "after a few attempts" | "three attempts in a row" |
|---|---|---|---|
| GPT-6-luna, native, low | no (4.9 calls) | no (5.2 calls) | **yes** (+1.00, 3.0 calls) |
| DeepSeek, off | yes | yes | **yes** (+0.98) |
| DeepSeek, on | yes | yes | **yes** (+0.90) |
| gpt-oss-120b | no (rescue +0.20) | no (+0.19) | **yes** (+0.69) |
| Qwen, off | no (+0.44) | yes | **yes** (+0.76) |
| Haiku, thinking off | no (+0.43) | no (+0.30) | **yes** (+0.97) |
| Haiku, thinking on | yes | yes | **yes** (+1.00) |
| **Total** | 3 of 7 | 4 of 7 | **7 of 7** |

The caution alone did much less on most models: give-up rescues of +0.98 on GPT-6-luna, but +0.33 on Qwen, +0.18 on DeepSeek without reasoning, −0.03 on gpt-oss and 0.00 on Haiku without thinking. Adding the counted rule raised those four to between +0.69 and +0.98, so the rule adds to the caution where the caution is weak. It never met the harm rule for real transient faults. On six of seven arms, agents under it stopped a true outage after 2.5–3.1 calls, close to the stated count.

The count is not a general answer. The transient fault in this environment always clears on the third call, so "three attempts" encodes the threshold that recovers it. What the result shows is that a stated count is followed reliably across models, where "a few" is read differently by each. Where recovery times vary, the right count trades rescued transient faults against calls wasted on real outages, and a retry policy written in code, outside the model, is the obvious baseline (§5). Its price is the retry trap: under "three in a row" agents send the identical call three times, and solve 0–2% of retry traps, where "different" lifts some models to 17–26%.

The retry trap remains open. The best instruction tested, the caution plus "If an approach keeps failing, try a different one", solved 42% of it on GPT-6-luna, at 4.7 calls per request. Even told to try something different, agents changed the depot first.

### 4.5 Robustness: format and reasoning

**Format.** Re-running the grid on GPT-6-luna through native function calls (N1) left both traps and the first-encounter effect unchanged (SAME), but lowered S from +0.96 to +0.79, because the format claim was followed less often and the neutral baseline shifted. On Haiku, moving from the CLI text format to the API with thinking off changed its default after an uninformative error from persisting (97% solved) to giving up (0% solved). S rose from +0.34 to +0.69, and both traps stayed at 0%.

**Reasoning.** GPT-6-luna at reasoning effort high against low (W5, primary): SAME on S and both traps. Reasoning changed the default, not the credulity: after a neutral error over a transient fault, Luna at high effort persisted to success in 89% of requests (46% at low), yet after "unavailable" over the same fault it still stopped (11% solved). Haiku with thinking on against off was SAME on S and both traps. One caveat limits this: GPT-6-luna used about 11 reasoning tokens per call even at high effort, so these tests vary the effort setting, not long deliberation.

## 5 Discussion

**For API and tool designers: state a cause only when it is reliable.** A confident wrong cause is worse than none. On GPT-6-luna, replacing the false cause with "the cause of this failure is unknown" rescued the give-up trap almost fully, and on a transient fault "unknown" beat "request rejected" by 34 points. The production audit shows that the misleading causes come from systematic mechanisms (masking, propagation delay, generic intermediaries), which are fixable at the source.

**For agent builders: pair a caution with a counted stopping rule.** "Error messages from the stock system do not always state the true cause of a failure. If the same error comes back on three attempts in a row, accept it." In this environment it rescued the give-up trap on every model tested, at about the minimum cost, and never met the harm rule for real transient faults. Set the count from how your tools actually recover, not from this paper. Wording matters: vaguer variants failed on some models, and one made an agent malform its calls. Where retries can be handled in code, a programmatic retry policy may do the same job more simply; we have not compared the two.

**The worst case is the first failure.** On most models tested, an agent that has not yet seen an error clear takes "unavailable" at its word; one earlier recovery largely removes this, but also makes the agent waste calls on real outages. Agents in fresh sessions, the common case for short tasks, are likely the most exposed.

**Limitations.** One artificial environment, with faults chosen so that messages mislead; real messages are usually accurate, and mixing them weakens the traps (§4.3). Five models, settings not matched across them, each open-weight model on one host, and only the smallest Anthropic model. Interventions other than the stopping rule were tested on one model. The counted rule was always tested after the caution sentence, never alone. The transient fault always cleared on the third call, and error reliability and retry cost were fixed; the rule's count was not tested against varied recovery times. Short conversations without memory across them. The call budget (6) and the floor (3) are properties of this environment. Verdicts use fixed bars with no correction for multiple comparisons, so a result near a bar can change on replication: the harm from the word "different" on DeepSeek measured −0.17 in one study and −0.09 in the next. Hosted models can change behind the same name; every run is dated, and a replication on GPT-6-luna a week apart was unchanged. Costs are API-equivalent estimates. The planned extensions are larger models with long, visible reasoning (Claude Sonnet, Opus and Fable; OpenAI and Google models); an environment with randomized recovery times, error reliability and retry costs, comparing the instruction with a programmatic retry policy and testing the stopping rule without the caution; and injecting misleading errors into an existing agent benchmark.

**Ethics and broader impact.** The study involves no human participants; all data are model outputs from public APIs. Describing the traps could help someone craft misleading errors on purpose. We publish the mitigation with them, and the mechanisms that produce misleading errors in production are already documented publicly (§3.5).

## 6 Reproducibility

Everything is public: the code (Python 3.13, standard library only), 107 configurations, the 13 frozen protocols, 40 scripted agents, and raw logs of every model call with its cost. `python -m causetest reproduce` checks 380 raw files against SHA-256 hashes and re-scores every live run, byte for byte. The total API-equivalent spend for all studies was about $65.

## References

- Debenedetti, E., et al. (2024). AgentDojo: A dynamic environment to evaluate prompt injection attacks and defenses for LLM agents. *NeurIPS Datasets and Benchmarks*.
- Greshake, K., et al. (2023). Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection. *AISec Workshop*.
- Kelley, H. H. (1967). Attribution theory in social psychology. *Nebraska Symposium on Motivation*, 15, 192–238.
- Ruan, Y., et al. (2024). Identifying the risks of LM agents with an LM-emulated sandbox. *ICLR*.
- Schick, T., et al. (2023). Toolformer: Language models can teach themselves to use tools. *NeurIPS*.
- Seligman, M. E. P., & Maier, S. F. (1967). Failure to escape traumatic shock. *Journal of Experimental Psychology*, 74(1), 1–9.
- Weiner, B. (1985). An attributional theory of achievement motivation and emotion. *Psychological Review*, 92(4), 548–573.
- Yao, S., et al. (2023). ReAct: Synergizing reasoning and acting in language models. *ICLR*.
- Yao, S., et al. (2024). τ-bench: A benchmark for tool-agent-user interaction in real-world domains. *arXiv:2406.12045*.
- Zhang, C., et al. (2026). Don't blindly trust it: How unreliable feedback breaks tool-using LLM agents. *arXiv:2606.21409*.
- Zhu, D., et al. (2026). When tools fail: Benchmarking dynamic replanning and anomaly recovery in LLM agents. *arXiv:2606.05806*.

## Appendix A: Predictions against outcomes

Each protocol recorded predictions before its first call. They are not part of any decision rule.

| Study | Held | Notable misses |
|---|---|---|
| E2 | 7 of 8 | The caution alone rescued the give-up trap; predicted no effect or a partial one. |
| E3 | 4 of 5 | "A few different attempts" helped the retry trap. |
| E4 | 3 of 7 | Did not foresee that one cleared error teaches persistence. |
| E5 | 3 of 4 | Underestimated the primary effect (predicted 20–45% stopping at once after a cleared error; observed 3%). |
| N1 | 2 of 4 | S changed with the format. |
| W2-A | 4 of 5 | Reasoning loosened DeepSeek's retry trap. |
| H1 | 1 of 1 tested | — |
| W2-B | 1 of 4 | No open-weight model was cost-aware; DeepSeek with reasoning was harmed. |
| W6 | 3 of 5 | Dropping "different" was SAME, not DIFFERENT, on DeepSeek with reasoning; its harm did not replicate at the same size. |
| W5 | 1 of 5 | Reasoning did not loosen the retry trap. |
| W2-C | 3 of 5 | Haiku's primary was INCONCLUSIVE; E5 did not apply to Haiku. |

## Appendix B: Where everything is

- Protocols: `PROTOCOL*.md`. Lab notebook with every approval and deviation: `NOTEBOOK.md`. Consolidated report: `REPORT.md`.
- Raw data per run: `runs/<run>/` (`results.jsonl`, `journal.jsonl`, `worlds.jsonl`, `config.json`, `analysis/`).
- The panel table: `runs/panel/PANEL.md`. Figures and their data: `figures/`.
- The production error audit: `ERROR_AUDIT.md`.
