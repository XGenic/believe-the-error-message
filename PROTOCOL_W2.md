# C4 study W2-A: first open-weight models through OpenRouter (frozen before any W2 live call)

Status: **frozen 2026-10-22**, before any OpenRouter call that produces data. This file, the twelve configs named below, the OpenRouter transport and its tests were written before the probes and pilots. The folder is not a git repository, so this file has no commit timestamp. Changes after the first W2 call are logged in `README.md` under "Deviations".

W2-A is the first part of workstream W2 in [`PAPER_PLAN.md`](PAPER_PLAN.md), the panel of models.

## Owner's choice (2026-10-22)

**Models:** DeepSeek V4.1 Flash, Qwen3.8-27B and Gemma 4 31B, from the proposed open-weight panel (README, "Phase 2: proposed open-weight panel"). Each model runs both of its reasoning arms.

**Not run for now:** gpt-oss-120b, Mistral Small 4 and GLM-5.3. Their configs keep their $0 caps.

| Arm | Model | Pinned endpoint | Reasoning | C4 config | E5 config |
|---|---|---|---|---|---|
| DS-r0 | `deepseek/deepseek-v4.1-flash` | `deepinfra/fp8` | `effort: none` | `live_or_c4_deepseek_v4_1_flash_r0.json` | `live_or_e5_deepseek_v4_1_flash_r0.json` |
| DS-r1 | same | same | `effort: low` | `..._r1.json` | `..._r1.json` |
| QW-r0 | `qwen/qwen3.8-27b` | `deepinfra/bf16` | `effort: none` | `live_or_c4_qwen3_8_27b_r0.json` | `live_or_e5_qwen3_8_27b_r0.json` |
| QW-r1 | same | same | `effort: low` | `..._r1.json` | `..._r1.json` |
| GE-r0 | `google/gemma-4-31b-it` | `crusoe/bf16` | `enabled: false` | `live_or_c4_gemma_4_31b_r0.json` | `live_or_e5_gemma_4_31b_r0.json` |
| GE-r1 | same | same | `enabled: true` | `..._r1.json` | `..._r1.json` |

**Shared settings:**

- temperature 1.0;
- `max_tokens` 2,000 for r0 and 8,000 for r1;
- reasoning is not passed back;
- the native prompt of N1.

**Designs:**

- **C4:** the full grid, 12 cells × 30 runs, on seeds 20261201 + r, as N1-A.
- **E5:** 3 primes × 60 runs, on seeds 20261701 + r, as N1-B.

## Procedure

1. **Probe:** one request per arm, two calls at most, logged in `runs/w2-probes/`. The probe uses the development world and is never analyzed. It checks four things:
   - that OpenRouter accepts the endpoint tag;
   - that the response names the expected host;
   - whether reasoning is really off in r0;
   - that a tool result can be sent back without the model's reasoning.

   A probe failure stops that arm. The fix is logged as a deviation before its pilot.
2. **Pilot:** one run per cell on the design's development seed. It never enters an analysis.
3. **Health gate before each main run.** The pilot must show:
   - every run complete;
   - protocol failures of 10% or less;
   - the tool called on request 1 in at least 90% of runs;
   - an estimated main-run cost (cells × runs × the pilot's cost per run) within the config's cap.

   A config that fails the gate is not run, and is reported to the owner.
4. **Main run, in order of cost from the pilots, cheapest first.**

## Budget

- **Caps:** each config's cap is the one proposed in the README, at 3× the estimate before the pilot.
- **The binding limit is the account's credit:** $20 on 2026-10-22.
- **Before each main run,** the remaining credit is read from OpenRouter (`/api/v1/credits`). A main run starts only if 1.5× its pilot-based estimate fits within the remaining credit, less a $1 margin.
- Arms that do not fit wait for the owner. The skipped arms and their estimates are reported.

## Analysis (all rules already frozen)

- **Each run's verdict:**
  - C4 runs by C4's decision rule (`PROTOCOL.md`), on validity, S and L\*;
  - E5 runs by E5's rule (`PROTOCOL_E5.md`).
- **Headline measures per arm:**
  - S, reported with its neutral baseline (paper plan §9);
  - retry-trap success and give-up-trap success;
  - E5's D1.
- **Comparisons, by N1's rule** (`python -m causetest compare`; SAME, DIFFERENT or UNCLEAR):
  - each r0 C4 arm against Luna with reasoning off (N1-C, `runs/n1-c4-native-none-gpt-6-luna`);
  - each r1 C4 arm against Luna at reasoning low (N1-A, `runs/n1-c4-native-low-gpt-6-luna`);
  - r1 against r0 within each model, for the reasoning effect (paper plan W5);
  - each E5 arm against N1-B (`runs/n1-e5-native-low-gpt-6-luna`).

  These comparisons describe; they do not gate anything.
- **The cross-model mixed-effects analysis** (paper plan W2) waits for the complete panel.

## Predictions (recorded before any W2 call; not part of the decision rule)

- **Both traps hold for every arm:** retry-trap and give-up-trap success under 20%. Haiku and Luna both solved none.
- **S is positive for every valid arm**, with CONTINUE_CREDULOUS or CONTINUE on most. My confidence is lower for Gemma r0, which is the weakest agent on OpenRouter's agentic index.
- **E5's D1 is CONFIRMED for at least four of the six arms.**
- **r1 against r0 is SAME on both traps for every model,** as with Luna under N1-C.
- **Biggest risks:**
  - Gemma r0 may be INVALID on protocol failures;
  - reasoning-on arms may cost more than estimated, from long reasoning.

## Known limits

- **One host per model.** Results are for that host's serving of the weights: its quantization, chat template and tool parser. Another host is a different subject.
- **Reasoning is not passed back,** as in N1. Hosts that expect it in a tool loop may behave differently from production agents.
- **Temperature 1.0 for every model,** rather than each lab's recommended setting. Top-p and top-k are left at OpenRouter's defaults for each model.
