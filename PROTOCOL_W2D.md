# C4 study W2-D: GPT-6.1 Sol through native tool calls (frozen before any W2-D live call)

Status: **frozen**. This file, `configs/live_w2d_*.json`, the change to the OpenAI transport (cached-input pricing and retries, in `causetest/transports.py`) and their tests were committed before any W2-D live call, the pilots included. Changes after a W2-D live call must be logged in `NOTEBOOK.md` under "Deviations".

W2-D is the first frontier arm of the model panel (W2), and the first study **registered publicly before its first call** (see Procedure). It is paid for by OpenAI API credit that comes with the owner's Pro subscription: $77 this month.

## Question

GPT-6-luna is the only OpenAI model run so far. Every result on it comes from a small model that reasons very little in this task: about 11 reasoning tokens per call even at high effort (W5). GPT-6.1 Sol is OpenAI's larger model, through the same API and transport. W2-D asks:

1. **Does Sol show the core pattern?** Credulity on the C4 grid, both traps, and E5's first-encounter effect.
2. **Does the stopping rule that was RECOMMENDABLE on 7 of 7 arms ("three attempts in a row") also work on Sol?**
3. **Does more reasoning change anything?** Sol runs at reasoning effort `low` and `high`.

## Design

Three designs, each exactly as already run on Luna through native tool calls:

| Design | Cells | Runs | Seeds (pilot) | Copied from |
|---|---|---|---|---|
| C4 grid | 12 (3 causes and neutral × 3 faults) | 30 per cell | 20261201 + r (20269201) | `live_n1_c4_native_low.json` (N1-A, W5) |
| E5 | 3 primes | 60 per cell | 20261701 + r (20269701) | `live_n1_e5_native_low.json` (N1-B, W5) |
| W6 | 5 arms × 4 cells | 30 per cell | 20262001 + r (20262901) | `live_w6_gpt6luna_native_low.json` (W6) |

| Arm | Reasoning effort | Output-token limit | Designs |
|---|---|---|---|
| `low` | `low` | 2,000 | C4, E5, W6 |
| `high` | `high` | 8,000 | C4, E5 |

`low` is the setting of every Luna arm in the panel; `high` and its output limit are W5's. Sol has no `none` effort; its default is `medium`. W6 runs at `low` only, for budget. Cells, seeds, decision rules and thresholds are copied from the configs named above; a test checks this.

**The transport** (`openai_responses_native`) is unchanged in what the model sees: the Responses API, the native-call instructions every native transport uses, the tool declared with `strict: true`, parallel tool calls off, `store: false`, and no sampling parameter. As in every Luna run, **reasoning items are not passed back** between turns. Two changes, neither visible to the model:

- **Cost is priced by cache use.** OpenAI caches repeated prompt prefixes automatically. Each response's cached input is priced at $0.10 and its cache writes at $2.50 per million tokens, the rest of the input at $2.00, and output at $10.00 (OpenAI's model page, read 2026-10-28). Earlier OpenAI runs priced all input at the uncached rate, an upper bound; their configs, which list no cache-write price, are priced as before.
- **Unbilled failures are retried**, as in the Anthropic transport: rate limits (429), server errors (5xx) and socket timeouts, with backoff, and counted in each turn's record. A 429 for exhausted quota is not retried.

## Decision rules

Each run gets the verdict of its own design, unchanged: C4's (CONTINUE_CREDULOUS, ...), E5's (CONFIRMED, ...) and W6's per wording (RECOMMENDABLE, ...).

- **Primary: the C4 verdict of `low`.** It answers question 1 for Sol as the panel runs every model.
- **Secondary:**
  - E5's verdict in each arm.
  - W6's three wording verdicts at `low`. Sol is reported beside the earlier subjects; W6's own ROBUST count stays as frozen (5 subjects).
  - `high` − `low` by N1's comparison rule, for C4 (S and both traps) and E5 (D1).
  - **Model:** Sol − Luna at `low`, by the same rule, against W5's `low` runs (C4 and E5, same seeds) and W6's Luna run. Descriptive: the runs are a day or more apart, and the two models differ in more than size.
  - Reasoning tokens per call in each arm, against Luna's in W5.

## Procedure

1. **Freeze** (this commit): protocol, configs at a $0 cap, transport change, tests.
2. **Approval:** the owner's approval and the caps, in a separate commit, before any call.
3. **Public registration, before any call:** the frozen protocol, configs and code are pushed to the public repository and published as a GitHub release (`w2d-protocol`), and the owner registers the same files on OSF. The release and the OSF registration carry their own timestamps. No pilot runs before both exist.
4. **Pilots:** one run per cell on the development seed, for each of the five configs. The W2 health gate applies: every run complete, protocol failures of 10% or less, the tool called on request 1 in at least 90% of runs, and the estimate within the cap.
5. **Main runs**, each only after its pilot passes the gate, **in this order of priority:** C4 `low`, E5 `low`, W6 `low`, C4 `high`, E5 `high`. A run whose pilot estimate exceeds its cap is not run, and is reported; money left under one run's cap can move to a later run only on the owner's word, logged as a deviation.
6. A run INVALID on completion through transport failures gets the W2-4 re-run (completed runs from the cache), logged as a deviation.

## Predictions (recorded before any W2-D call; not part of the decision rule)

- **Primary: `low` is CONTINUE_CREDULOUS,** with both traps solved in at most 10% of requests.
- **E5 CONFIRMED at `low`.**
- **"Three attempts in a row" is RECOMMENDABLE at `low`.**
- **`high` − `low`: SAME on both traps;** S may differ.
- **Sol reasons more than Luna:** a median of more than 11 reasoning tokens per call at `high` (Luna's W5 figure).

## Budget

Approved by the owner on 2026-10-28: **$80 for the whole study, pilots included**, within about $82 of credit that lapses on November 9. (The frozen draft proposed $75.) Each cap covers that config's pilot and main run. Estimates are Luna's measured tokens per run in the matching run, cache use included, at Sol's list prices, × 1.3 at `low` and × 2.0 at `high` for more reasoning:

| Config | Runs | Luna-based cost per run | Estimate | Cap |
|---|---|---|---|---|
| C4, `low` | 360 | $0.029 | $13.40 | $15 |
| E5, `low` | 180 | $0.018 | $4.19 | $6 |
| W6, `low` | 600 | $0.031 | $24.54 | $28 |
| C4, `high` | 360 | $0.034 | $24.47 | $23 |
| E5, `high` | 180 | $0.021 | $7.55 | $8 |
| **Total** | 1,680 | | **$74.15** | **$80** |

The cap is tighter than the estimate for C4 `high`. The pilots measure Sol's real cost; if a run would not fit its cap, the order of priority decides what runs.

## Known limits

- **One larger OpenAI model.** GPT-6 Astra waits for later credit.
- **Reasoning items are not passed back** between turns, as in every Luna run, so each call reasons afresh. OpenAI recommends passing them back; this keeps Sol comparable with Luna instead.
- **W6 at `low` only.** Whether more reasoning changes the stopping rule's effect is not tested.
- **The credit is monthly** and lapses on November 9. If it lapses before the main runs finish, the runs not yet made are reported as not run, and none is paid for otherwise without the owner's word.
