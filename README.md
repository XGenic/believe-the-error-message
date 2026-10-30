# Do LLM agents believe the error message?

When a tool call fails, the error message usually states a cause: "invalid format", "temporarily unavailable", "not found". An agent cannot see the true fault, so treating that cause as evidence is reasonable. This project tests whether LLM agents keep testing it: whether they revise a **stated** cause when their own calls contradict it, or recover by it regardless of the **true** one. It varies the two independently in a small simulated stock-lookup tool.

**Short answer: they act on the stated cause and rarely revise it, and two traps follow.** A brief caution paired with a counted stopping rule fixes the worse of the two on every model tested, in this environment; for read-only calls, retrying in the tool's client does the same without giving up on real transient faults.

Results to 2026-10-30: 15 pre-specified studies on 6 models from 4 developers (15 model-and-setting arms), about $124 of API spend. The two latest, W2-D and R1, were registered publicly before their first call. **Paper draft:** [`paper/PAPER.md`](paper/PAPER.md) (preprint draft, not peer reviewed). The consolidated write-up is [`REPORT.md`](REPORT.md).

## The two traps

| Trap | The message says | The truth | What agents do |
|---|---|---|---|
| **Retry trap** | "temporary service problem" | the request is malformed, and fixable | repeat the same broken call until the call budget runs out |
| **Give-up trap** | "data unavailable" | a transient fault that clears on the third call | stop after one or two calls, before the call that would work |

Both patterns occur in production systems: [`ERROR_AUDIT.md`](ERROR_AUDIT.md) documents 25 real cases.

## Key findings

![Share of requests solved by stated cause and true fault, one grid per model](figures/stated_true_grid.svg)

| Finding | Evidence |
|---|---|
| Agents act on the stated cause | Credulous verdict on 11 of 15 arms; steering S from +0.34 to +0.96 |
| The retry trap holds, but is only partly the message's doing | At most 10% solved on 14 of 15 arms (highest 16%); most models seldom fix that fault under a neutral message either (12 points higher on average) |
| The give-up trap holds, and is the message's doing | At most 10% solved on 13 of 15 arms (highest 14%): 64 points below a neutral message over the same fault, on average |
| Repeated identical errors do not change behavior | 0 of 216 trap requests solved in 18-request conversations (Haiku, Luna) |
| A caution plus a counted stopping rule fixes the give-up trap | "Error messages … do not always state the true cause of a failure. If the same error comes back on three attempts in a row, accept it." passed the pre-set bar on 8 of 8 model arms: 81–100% success, at no more than 3.1 calls on a real outage. The rule was always tested after the caution, and its count matches this environment, where faults clear on the third call |
| The wording matters | "After a few different attempts" passed on 4 of 8, and made one model send malformed calls |
| A retry in code does it better | When faults took 2–5 calls to clear (R1, four models), retrying three times in the tool's client rescued the give-up trap as well as the instruction, and kept the accurate "temporary" recoveries the instruction gave up on (1.00 against 0.42–0.64). This holds for read-only calls; retries can be unsafe where calls have side effects. The caution sentence added no substantial benefit to the count |
| The first failure is the worst case, on some models | GPT-6-luna stopped at once on 60 of 60 first "unavailable" messages, and on 2 of 60 after one earlier error had cleared (GPT-6.1 Sol: 60 of 60 and 0 of 60); Claude Haiku 5.5 shows no such effect |
| Light reasoning does not help | Luna and Sol at high reasoning effort, and Haiku with thinking on: the same traps |

The retry trap is not solved by any instruction tested; the best sentence solved 42% of it on Luna, at 4.7 calls per request.

![Give-up rescue against its cost on a true outage, per model and wording](figures/rescue_cost.svg)

The numbers come from [`runs/panel/PANEL.md`](runs/panel/PANEL.md), which puts every model and setting side by side.

## Models

| Model | Access | Settings |
|---|---|---|
| Claude Haiku 5.5 | Claude Code CLI (text format); Anthropic Messages API (native tool use) | no reasoning; thinking off and on |
| GPT-6-luna | OpenAI Responses API (text format and native tool use) | reasoning none, low, medium, high |
| GPT-6.1 Sol | OpenAI Responses API (native tool use) | reasoning low, high |
| DeepSeek V4.1 Flash | OpenRouter, one pinned host (native tool use) | reasoning off and on |
| Qwen3.8-27B | OpenRouter, one pinned host (native tool use) | reasoning off and on |
| gpt-oss-120b | OpenRouter, one pinned host (native tool use) | reasoning on |

## Studies

Each study's protocol, decision rule and predictions were committed before its first model call, in the author's private working repository. This repository is an export of that work made on 2026-10-28, so its history cannot independently confirm that timing: the studies are pre-specified, not independently timestamped pre-registrations, and that is what "pre-registered" means in the older documents here. From W2-D on, studies are registered publicly, as a tagged release and on OSF, before any call. Deviations are logged in [`NOTEBOOK.md`](NOTEBOOK.md), and every prediction is scored in `REPORT.md` §5, misses included.

| Study | Question | Models | Protocol | Result |
|---|---|---|---|---|
| C4 | Does the stated cause steer recovery, and does the agent learn otherwise? | Haiku, Luna | [`PROTOCOL.md`](PROTOCOL.md) | Both credulous |
| E1 | Does it learn over 18 requests? | Haiku, Luna | [`PROTOCOL_E1.md`](PROTOCOL_E1.md) | No learning |
| E2 | What breaks the traps? | Luna | [`PROTOCOL_E2.md`](PROTOCOL_E2.md) | One caution sentence breaks the give-up trap, at a cost |
| E3 | Can a stopping rule cut that cost? | Luna | [`PROTOCOL_E3.md`](PROTOCOL_E3.md) | Yes: the rescue at about the minimum cost |
| E4 | Do mixed accurate and misleading errors change things? | Luna | [`PROTOCOL_E4.md`](PROTOCOL_E4.md) | Mixing weakens the traps |
| E5 | Does one earlier error make an agent persist? | Luna | [`PROTOCOL_E5.md`](PROTOCOL_E5.md) | Confirmed |
| N1 | Do native tool calls change the results? | Luna | [`PROTOCOL_N1.md`](PROTOCOL_N1.md) | Traps unchanged; steering size changes |
| H1 | Does tool withdrawal carry over? | Luna | [`PROTOCOL_H1.md`](PROTOCOL_H1.md) | No carry-over |
| W2-A | Do open-weight models show the same pattern? | DeepSeek, Qwen, gpt-oss | [`PROTOCOL_W2.md`](PROTOCOL_W2.md) | Yes |
| W2-B | Does the stopping rule carry over to them? | DeepSeek, Qwen, gpt-oss | [`PROTOCOL_W2B.md`](PROTOCOL_W2B.md) | Partly; never at Luna's cost |
| W6 | Does the stopping rule depend on its wording? | Luna, DeepSeek, Qwen, gpt-oss | [`PROTOCOL_W6.md`](PROTOCOL_W6.md) | "Three attempts in a row" works on 5 of 5 |
| W5 | Does more reasoning help? | Luna | [`PROTOCOL_W5.md`](PROTOCOL_W5.md) | No |
| W2-C | Claude Haiku 5.5 through native tool use | Haiku | [`PROTOCOL_W2C.md`](PROTOCOL_W2C.md) | Traps hold; "three in a row" works; no first-encounter effect |
| W2-D | A larger OpenAI model, at two reasoning efforts | Sol | [`PROTOCOL_W2D.md`](PROTOCOL_W2D.md) ([OSF](https://osf.io/z2pwa)) | Credulous; traps hold (0%); every stopping-rule wording works |
| R1 | Does the stopping rule hold when recovery times vary, and how does it compare with a retry in code? | Sol, Luna, Haiku, DeepSeek | [`PROTOCOL_R1.md`](PROTOCOL_R1.md) ([OSF](https://osf.io/d64ju)) | Code is better on 4 of 4; the caution adds no substantial benefit to the count |

## Reproduce

Python 3.13, standard library only. From this folder:

```sh
python -m unittest discover -s tests                          # 88 tests
python -m causetest validate --configs configs/mock_*.json   # 45 scripted agents with known behaviour
python -m causetest reproduce                                 # raw-data hashes + byte-identical re-scoring of every live run
python -m causetest panel                                     # the cross-model table in runs/panel/
```

`reproduce` checks every raw file against [`runs/MANIFEST.json`](runs/MANIFEST.json) (SHA-256) and re-scores every live run from its raw logs. No API key is needed for any of these. Running a model needs a key in `.env` and an approved spending cap in the config: every live config here is capped.

## Repository map

| Path | What it holds |
|---|---|
| `causetest/` | environment, episode, transports (Claude CLI, OpenAI, OpenRouter, Anthropic), scoring and every study's decision rule |
| `configs/` | one config per run: live runs and scripted agents (mocks) |
| `runs/<run>/` | raw data per live run: `results.jsonl` (every turn), `journal.jsonl` (every call and its cost), `worlds.jsonl`, `config.json`, and `analysis/` (the verdict report) |
| `tests/` | unit tests |
| `figures/` | the two figures above, with their data as CSV and the scripts that draw them |
| `PROTOCOL*.md` | the frozen protocols |
| `paper/PAPER.md` | the preprint draft |
| `REPORT.md`, `NOTEBOOK.md`, `DATA_CARD.md`, `ERROR_AUDIT.md` | the write-up, the lab notebook, the data card, the audit of real errors |

The per-run response caches used while the runs were in progress are left out of this release: `results.jsonl` holds the same rows. So is `PAPER_PLAN.md`, the author's private planning document. Older files link to it and name workstreams (W1–W6) after it; those links do not resolve here, and each workstream's protocol states its full design.

## Licence

Code under the MIT licence ([`LICENSE`](LICENSE)); data, reports and figures under CC BY 4.0 ([`LICENSE-DATA.md`](LICENSE-DATA.md)).

## Citation

Denis Gurskiy. *Do LLM agents believe the error message?* 2026. https://github.com/XGenic/believe-the-error-message
