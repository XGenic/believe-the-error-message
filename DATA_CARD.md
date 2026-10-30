# C4 data card

This card describes the raw records of every C4 live run, as of 2026-10-30: the kill test, extensions E1–E5, and studies N1, H1, R1, W2-A, W2-B, W2-C, W2-D, W5 and W6. That is 54 run folders and about 18,400 runs. The results are in [`REPORT.md`](REPORT.md).

## What the data are

The data are complete conversations between a language-model agent and a simulated stock-lookup tool. They record every turn, every call and its cost, and the hidden ground truth.

- **The world is fictional.** It is a wholesaler with six depots and generated SKUs.
- **No human subjects were involved,** and there is **no personal data**.
- **No credentials.** API keys were supplied to the run process through the environment and never written to any file. Every run folder was scanned for key-shaped strings before commit; the only `sk-` matches are SKUs such as `sk-3924`.

## Live runs

| Folder | Study | Model | Transport | Runs | Raw size |
|---|---|---|---|---|---|
| `runs/e1-live-claude-haiku-5-5/` | E1 | claude-haiku-5-5 | claude_cli | 48 | 7 MB |
| `runs/e1-live-gpt-6-luna/` | E1 | gpt-6-luna | openai_responses | 48 | 4 MB |
| `runs/e2-live-gpt-6-luna/` | E2 | gpt-6-luna | openai_responses | 630 | 21 MB |
| `runs/e3-live-gpt-6-luna/` | E3 | gpt-6-luna | openai_responses | 480 | 15 MB |
| `runs/e4-live-gpt-6-luna/` | E4 | gpt-6-luna | openai_responses | 160 | 10 MB |
| `runs/e5-live-gpt-6-luna/` | E5 | gpt-6-luna | openai_responses | 180 | 3 MB |
| `runs/h1-gpt-6-luna-native-low/` | H1 | gpt-6-luna | openai_responses_native | 120 | 7 MB |
| `runs/live-claude-haiku-5-5/` | C4 kill test | claude-haiku-5-5 | claude_cli | 360 | 28 MB |
| `runs/live-gpt-6-luna/` | C4 kill test | gpt-6-luna | openai_responses | 360 | 11 MB |
| `runs/n1-c4-native-low-gpt-6-luna/` | N1-A | gpt-6-luna | openai_responses_native | 360 | 10 MB |
| `runs/n1-c4-native-none-gpt-6-luna/` | N1-C | gpt-6-luna | openai_responses_native | 360 | 10 MB |
| `runs/n1-e5-native-low-gpt-6-luna/` | N1-B | gpt-6-luna | openai_responses_native | 180 | 3 MB |
| `runs/or-c4-deepseek-v4-1-flash-r0/` | W2-A, C4 grid | deepseek/deepseek-v4.1-flash | openrouter_chat_native | 369 | 14 MB |
| `runs/or-c4-deepseek-v4-1-flash-r1/` | W2-A, C4 grid | deepseek/deepseek-v4.1-flash | openrouter_chat_native | 360 | 31 MB |
| `runs/or-c4-gpt-oss-120b-r1-crusoe/` | W2-A, C4 grid | openai/gpt-oss-120b | openrouter_chat_native | 364 | 12 MB |
| `runs/or-c4-qwen3-8-27b-r0/` | W2-A, C4 grid | qwen/qwen3.8-27b | openrouter_chat_native | 360 | 16 MB |
| `runs/or-c4-qwen3-8-27b-r1/` | W2-A, C4 grid | qwen/qwen3.8-27b | openrouter_chat_native | 360 | 15 MB |
| `runs/or-e5-deepseek-v4-1-flash-r0/` | W2-A, E5 | deepseek/deepseek-v4.1-flash | openrouter_chat_native | 182 | 3 MB |
| `runs/or-e5-deepseek-v4-1-flash-r1/` | W2-A, E5 | deepseek/deepseek-v4.1-flash | openrouter_chat_native | 180 | 6 MB |
| `runs/or-e5-gpt-oss-120b-r1/` | W2-A, E5 | openai/gpt-oss-120b | openrouter_chat_native | 180 | 3 MB |
| `runs/or-e5-qwen3-8-27b-r0/` | W2-A, E5 | qwen/qwen3.8-27b | openrouter_chat_native | 180 | 4 MB |
| `runs/or-e5-qwen3-8-27b-r1/` | W2-A, E5 | qwen/qwen3.8-27b | openrouter_chat_native | 180 | 4 MB |
| `runs/r1-claude-haiku-5-5-t0/` | R1 | claude-haiku-5-5 | anthropic_messages_native | 450 | 13 MB |
| `runs/r1-deepseek-v4-1-flash-r0/` | R1 | deepseek/deepseek-v4.1-flash | openrouter_chat_native | 450 | 16 MB |
| `runs/r1-gpt-6-1-sol-low/` | R1 | gpt-6.1-sol | openai_responses_native | 450 | 13 MB |
| `runs/r1-gpt-6-luna-native-low/` | R1 | gpt-6-luna | openai_responses_native | 450 | 12 MB |
| `runs/w2b-deepseek-v4-1-flash-r0/` | W2-B | deepseek/deepseek-v4.1-flash | openrouter_chat_native | 360 | 14 MB |
| `runs/w2b-deepseek-v4-1-flash-r1/` | W2-B | deepseek/deepseek-v4.1-flash | openrouter_chat_native | 360 | 16 MB |
| `runs/w2b-gpt-oss-120b-r1/` | W2-B | openai/gpt-oss-120b | openrouter_chat_native | 372 | 12 MB |
| `runs/w2b-qwen3-8-27b-r0/` | W2-B | qwen/qwen3.8-27b | openrouter_chat_native | 360 | 15 MB |
| `runs/w2b-qwen3-8-27b-r1/` | W2-B | qwen/qwen3.8-27b | openrouter_chat_native | 360 | 15 MB |
| `runs/w2c-c4-claude-haiku-5-5-t0/` | W2-C, C4 grid | claude-haiku-5-5 | anthropic_messages_native | 360 | 9 MB |
| `runs/w2c-c4-claude-haiku-5-5-t1/` | W2-C, C4 grid | claude-haiku-5-5 | anthropic_messages_native | 360 | 12 MB |
| `runs/w2c-e5-claude-haiku-5-5-t0/` | W2-C, E5 | claude-haiku-5-5 | anthropic_messages_native | 180 | 2 MB |
| `runs/w2c-e5-claude-haiku-5-5-t1/` | W2-C, E5 | claude-haiku-5-5 | anthropic_messages_native | 180 | 3 MB |
| `runs/w2c-w6-claude-haiku-5-5-t0/` | W2-C, W6 design | claude-haiku-5-5 | anthropic_messages_native | 600 | 19 MB |
| `runs/w2c-w6-claude-haiku-5-5-t1/` | W2-C, W6 design | claude-haiku-5-5 | anthropic_messages_native | 605 | 23 MB |
| `runs/w2d-c4-gpt-6-1-sol-high/` | W2-D, C4 grid | gpt-6.1-sol | openai_responses_native | 360 | 12 MB |
| `runs/w2d-c4-gpt-6-1-sol-low/` | W2-D, C4 grid | gpt-6.1-sol | openai_responses_native | 360 | 12 MB |
| `runs/w2d-e5-gpt-6-1-sol-high/` | W2-D, E5 | gpt-6.1-sol | openai_responses_native | 180 | 2 MB |
| `runs/w2d-e5-gpt-6-1-sol-low/` | W2-D, E5 | gpt-6.1-sol | openai_responses_native | 180 | 2 MB |
| `runs/w2d-w6-gpt-6-1-sol-low/` | W2-D, W6 design | gpt-6.1-sol | openai_responses_native | 600 | 20 MB |
| `runs/w5-c4-high-gpt-6-luna/` | W5, C4 grid | gpt-6-luna | openai_responses_native | 360 | 12 MB |
| `runs/w5-c4-low-gpt-6-luna/` | W5, C4 grid | gpt-6-luna | openai_responses_native | 360 | 10 MB |
| `runs/w5-c4-medium-gpt-6-luna/` | W5, C4 grid | gpt-6-luna | openai_responses_native | 360 | 11 MB |
| `runs/w5-e5-high-gpt-6-luna/` | W5, E5 | gpt-6-luna | openai_responses_native | 180 | 3 MB |
| `runs/w5-e5-low-gpt-6-luna/` | W5, E5 | gpt-6-luna | openai_responses_native | 180 | 3 MB |
| `runs/w5-e5-medium-gpt-6-luna/` | W5, E5 | gpt-6-luna | openai_responses_native | 180 | 3 MB |
| `runs/w5-e5-none-gpt-6-luna/` | W5, E5 | gpt-6-luna | openai_responses_native | 180 | 3 MB |
| `runs/w6-deepseek-v4-1-flash-r0/` | W6 | deepseek/deepseek-v4.1-flash | openrouter_chat_native | 600 | 24 MB |
| `runs/w6-deepseek-v4-1-flash-r1/` | W6 | deepseek/deepseek-v4.1-flash | openrouter_chat_native | 600 | 26 MB |
| `runs/w6-gpt-oss-120b-r1/` | W6 | openai/gpt-oss-120b | openrouter_chat_native | 600 | 36 MB |
| `runs/w6-gpt6luna-native-low/` | W6 | gpt-6-luna | openai_responses_native | 600 | 20 MB |
| `runs/w6-qwen3-8-27b-r0/` | W6 | qwen/qwen3.8-27b | openrouter_chat_native | 600 | 28 MB |

Raw size counts the pinned files (`config.json`, `worlds.jsonl`, `results*.jsonl`, `journal.jsonl` and pilots). Runs is the main run's recorded runs, including any single re-run of a transport failure.

Development pilots are kept in each run's `pilot*/` folders. They never enter an analysis. The `runs/mock-*` folders are scripted-agent validation runs, not model data; only their `analysis/` folders are committed.

## Files in a run folder

| File | Contents |
|---|---|
| `config.json` | the full configuration, as run: seeds, cells, thresholds, model, request options, prices, caps |
| `worlds.jsonl` | one line per world seed: the depots, items, stock, each depot's SKU convention, and the requests. This is the ground truth. |
| `results.jsonl` | one line per agent run (below) |
| `journal.jsonl` | one line per event: `run_start`, `request`, `response` (with `cost_usd`), transport errors, spend-cap stops, `run_end` |
| `results.pass1.jsonl`, `results.pass2.jsonl` | earlier passes of a run that was interrupted or re-run (the Haiku kill test, deviation D3; W2-4, W2-5, W6-1 and W6-2), kept on record |
| `pilot/`, `pilot-*/` | the development pilots' own `results.jsonl`, `journal.jsonl`, `pilot.json` and `PILOT.md` |
| `cache/` | one JSON file per completed run, used to resume an interrupted run; the same records as the completed rows in `results.jsonl`. Kept in the author's working repository, and **left out of the public release**. Nothing in the analysis or in `reproduce` reads it. |
| `analysis/` | derived: `summary.json` and `VERDICT.md`, regenerated by `python -m causetest analyze` |

### A `results.jsonl` row (one agent run)

**Run-level fields:**

| Field | Meaning |
|---|---|
| `run_id` | `claim\|fault\|seed`, or `arm\|claim\|fault\|seed` in E2–E5 |
| `arm` | E2–E5, W6 and R1 |
| `claim`, `fault` | the cell. In E4 they are `mixed` and the mix; in E5, `primed` and the prime. |
| `seed`, `model`, `transport` | the world seed, the model and the transport |
| `status` | `complete`, `failed` or `stopped` |
| `attempt` | 1, or 2 for the single re-run of a transport failure |
| `cached` | whether the row was read back from the resume cache |

**`tasks`:** one entry per request.

| Field | Meaning |
|---|---|
| `index`, `text`, `truth`, `depot` | the request and its true answer |
| `claim`, `fault`, `kind` | E4 and E5 only: the per-request cell |
| `recovery_failures` | R1 only: failed calls before this request's transient fault clears (1–4) |
| `turns` | the conversation for this request (below) |
| `summary` | the coded outcome (below) |

**Each turn:**

| Field | Meaning |
|---|---|
| `user` | what the harness sent |
| `reply` | the agent's full raw reply |
| `action` | the parsed CALL or ANSWER, or the reason it was invalid |
| `tool` | the arguments, success, the result text shown, and hidden bookkeeping such as whether the spelling convention was met. In R1 the bookkeeping also counts the calls that reached the stock system (`service_calls`, with the code retry's own attempts) and those before it in the request (`service_calls_before`) |
| `meta` | cost, token usage, latency; for text-format Luna, whether the history cut L1 applied; for native runs, the number of native calls in the reply (`native_calls`) and any text sent with a call (`text_with_call`); for OpenRouter runs, also the host that served the call (`host`), whether the cost is OpenRouter's billed figure or a price estimate (`cost_source`), the generation id (`generation_id`), the finish reasons, and the length of any reasoning text (`reasoning_chars`) |

**`summary`:**

| Field | Meaning |
|---|---|
| `calls`, `failures`, `success`, `failures_before_success` | call counts and the outcome |
| `responses`, `first_response` | the coded response after each failure: RETRY, REFORMAT, SITE_ONLY, STOP, OTHER or UNCLASSIFIABLE |
| `answer`, `answer_norm`, `correct`, `unknown`, `unsupported` | the answer and how it was scored |
| `format_errors`, `over_budget`, `extra_protocol_lines`, `fabricated_result_lines` | protocol counts |
| `self_cause_language`, `service_cause_language` | causal language in the agent's own words |
| `first_call_spelling` | which spelling the request's first call used |

## Integrity and reproduction

- **`runs/MANIFEST.json`** pins the SHA-256 of every raw file of every live run: 452 files across 54 run folders. That is everything except `analysis/` and `cache/`.
- **`python -m causetest reproduce`** checks those hashes. It then re-scores every live run from its raw records into a scratch folder and compares the result with the committed `analysis/` byte for byte. As of 2026-10-30 it passes for every run, in the working repository and in the public release.
- **Raw files are kept exactly as written,** because `.gitattributes` sets `* -text`. Runs made on Windows (everything after the two Haiku CLI runs) have CRLF line endings; the Haiku CLI runs, made on Linux, have LF. JSON parsing ignores the difference, and the manifest pins the bytes as they are.
- **Analysis output is written with LF on every platform,** and runs are sorted before the bootstrap. Both since paper plan W0.

## Known caveats

- **Costs are API-equivalent estimates.**
  - Haiku's come from the Claude CLI's usage report.
  - Luna's are computed from third-party price listings that have not been checked against an invoice. All input is billed at the uncached rate, so they are an upper bound.
  - OpenRouter's (DeepSeek, Qwen, gpt-oss) are OpenRouter's billed figures, read from each response.
  - The Anthropic API runs (W2-C) are priced from each response's usage at Anthropic's list prices, with cache writes and reads at their own rates.
  - The GPT-6.1 Sol runs (W2-D, R1) are priced the same way, at OpenAI's list prices for Sol, with cached input and cache writes at their own rates.
  - R1's other subjects are priced as in their earlier runs: Luna at the uncached rate, Haiku at Anthropic's list prices, DeepSeek by OpenRouter's billed figures.
- **Settings differ between the models.** The text-format Luna runs use deviations L1 (history cut) and L2 (reasoning effort `low`); see `NOTEBOOK.md`. Each model's settings are in its runs' `config.json`.
- **`from_cache` in a summary** records how rows were produced (fresh or read back from the resume cache). It is bookkeeping, not an outcome.

## Licence

Chosen by the owner on 2026-10-28: code under MIT ([`LICENSE`](LICENSE)), data and documents under CC BY 4.0 ([`LICENSE-DATA.md`](LICENSE-DATA.md)).
