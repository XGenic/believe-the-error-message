# C4 study W2-C: Claude Haiku 5.5 through native tool use (frozen before any W2-C live call)

Status: **frozen**. This file, `configs/live_w2c_*.json`, the Anthropic transport (`anthropic_messages_native` in `causetest/transports.py`) and their tests were committed before any W2-C live call, the pilots included. Changes after a W2-C live call must be logged in `README.md` under "Deviations".

W2-C is the first Anthropic arm of the paper plan's model panel (W2). The owner approved it on 2026-10-28, with $10 for the whole study.

## Question

Claude Haiku 5.5 is the only Anthropic model run so far, and only through the Claude Code command-line tool in the text format (C4 and E1, 2026-10-20). Every other arm of the panel now runs through native tool calls. W2-C puts Haiku on the same footing:

1. **Does Haiku 5.5 show the core pattern through native tool use?** Credulity on the C4 grid, both traps, and E5's first-encounter effect.
2. **Does the stopping rule that was ROBUST in W6 ("three attempts in a row") also work on Haiku?**
3. **Does thinking change anything?** Haiku runs with thinking off and on.

## Design

Three designs, each exactly as already run on the other models, in two arms:

| Design | Cells | Runs | Seeds (pilot) | Same as |
|---|---|---|---|---|
| C4 grid | 12 (3 causes and neutral × 3 faults) | 30 per cell | 20261201 + r (20269201) | C4, N1-A, W2-A |
| E5 | 3 primes | 60 per cell | 20261701 + r (20269701) | E5, N1-B, W2-A |
| W6 | 5 arms × 4 cells | 30 per cell | 20262001 + r (20262901) | W6 |

| Arm | Thinking | Output-token limit |
|---|---|---|
| `t0` | off (`thinking: disabled`) | 2,000 |
| `t1` | on (`thinking: adaptive`) | 8,000 |

Both arms use the model's default effort (`medium`), so they differ only in thinking (and the output limit thinking needs). Cells, seeds, decision rules and thresholds are copied from the configs named above; a test checks this.

**The transport** (`anthropic_messages_native`): the Messages API, API version 2026-10-21, raw HTTP. The instructions are the native-call prompt every native transport uses. The tool is declared with `strict: true`, and parallel tool use is off. Two properties differ from the OpenAI and OpenRouter transports, and are fixed here:

- **Each assistant turn goes back whole,** thinking blocks and any text beside a call included. The API requires it once thinking is on, and both arms get the same history.
- **Automatic prompt caching is on** (`cache_control: ephemeral`). It reuses identical prompt prefixes: the model sees the same input, and the cost falls.

No sampling parameter is sent; API version 2026-10-21 rejects them.

## Decision rules

Each run gets the verdict of its own design, unchanged: C4's (CONTINUE_CREDULOUS, ...), E5's (CONFIRMED, ...) and W6's per wording (RECOMMENDABLE, ...).

- **Primary: the C4 verdict of `t0`.** It answers question 1 for Haiku as the panel runs every model.
- **Secondary:**
  - E5's verdict in each arm.
  - W6's three wording verdicts in each arm. Haiku is reported beside W6's five subjects; W6's own ROBUST count stays as frozen (5 subjects).
  - `t1` − `t0` by N1's comparison rule, for C4 (S and both traps) and E5 (D1).
  - **Format:** `t0` against the text-format Haiku C4 run (`runs/live-claude-haiku-5-5`), by the same rule. This mixes format with transport (the command-line tool against the Messages API) and is descriptive.

## Procedure

As every earlier study:

1. **Pilots:** one run per cell on the development seed, for all six configs. The W2 health gate applies: every run complete, protocol failures of 10% or less, the tool called on request 1 in at least 90% of runs, and the estimate within the cap.
2. **Main runs** only after the owner's word, each only after its pilot passes the gate. A run that fails is not run, and is reported.
3. A run INVALID on completion through transport failures gets the W2-4 re-run (completed runs from the cache), logged as a deviation.

## Predictions (recorded before any W2-C call; not part of the decision rule)

- **Primary: `t0` is CONTINUE_CREDULOUS,** with both traps solved in at most 10% of requests.
- **E5 CONFIRMED in both arms.**
- **"Three attempts in a row" is RECOMMENDABLE in both arms.**
- **`t1` − `t0`: SAME on both traps;** S may differ.
- **Format: S DIFFERENT from the text-format run** (+0.34 there, where Haiku's default after a neutral error was to retry), traps SAME.

## Budget

Approved by the owner on 2026-10-28: **$10 for the whole study, pilots included.** Estimates are Luna's measured cost per run at the same list prices ($0.10 / $0.50 per million tokens), × 1.2 for tokenizer differences and × 1.4 more for thinking in `t1`, before any saving from caching:

| Config | Estimate | Cap |
|---|---|---|
| C4, `t0` | $1.20 | $1.40 |
| E5, `t0` | $0.19 | $0.30 |
| W6, `t0` | $2.35 | $2.70 |
| C4, `t1` | $1.65 | $1.85 |
| E5, `t1` | $0.27 | $0.40 |
| W6, `t1` | $3.20 | $3.35 |
| **Total** | **$8.86** | **$10.00** |

Recorded cost is priced from each response's usage at the list prices, cache writes and reads included.

## Known limits

- **One Anthropic model.** Sonnet, Opus and Fable wait for the owner's decision (and possibly research credits).
- **The format comparison is not clean:** the earlier Haiku run went through the Claude Code tool, whose own context and settings differ from a bare API call.
- **Thinking is adaptive:** the model decides how much to think, and its thinking is not visible (`display` is left at its default, `omitted`). Thinking tokens are counted in the output.
