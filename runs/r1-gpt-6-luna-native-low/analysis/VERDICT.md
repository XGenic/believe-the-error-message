# C4 study R1 verdict: VALID

**LIVE MODEL RUN (study R1: recovery times and a retry in code, gpt-6-luna, native tool calls, reasoning low)**: transport `openai_responses_native`, model `gpt-6-luna`; 6 requests per run, 30 runs per cell.

The transient fault clears after 1, 2, 3, 4 failed calls, drawn per request. A strict count of three recovers 0.48 of these requests. Calls are counted at the stock system, so the code retry's own retries are included.

## Primary: the instruction (`caution_three`) minus the same count in code (`code_retry`): **WORSE_THAN_CODE**

| Measure | Instruction | Code retry | Δ [95% interval] | Label |
|---|---|---|---|---|
| Success, give-up trap | 0.57 | 0.57 | +0.000 [-0.094, +0.094] | SAME |
| Success, true 'temporary' | 0.64 | 1.00 | -0.361 [-0.428, -0.300] | DIFFERENT |
| Calls per request, true outage | 3.04 | 3.02 | 0.03 [-0.02, 0.08] | SAME |

## Secondary: the rule without the caution (`three_only`) minus the instruction (`caution_three`)

| Measure | Rule alone | Instruction | Δ [95% interval] | Label |
|---|---|---|---|---|
| Success, give-up trap | 0.53 | 0.57 | -0.039 [-0.111, +0.033] | SAME |
| Success, true 'temporary' | 0.54 | 0.64 | -0.094 [-0.183, -0.006] | SAME |
| Calls per request, true outage | 3.00 | 3.04 | -0.04 [-0.09, 0.00] | SAME |

## Secondary: each arm against control (W6's measures)

W6's verdict is shown for reference only: its bars were set for a fault that always cleared on the third call.

| Arm | Give-up rescue | Calls on a true outage | True-'temporary' success | W6's verdict |
|---|---|---|---|---|
| caution | +0.956 [+0.900, +0.994] | 5.67 [5.44, 5.86] | +0.039 [-0.006, +0.106] | RESCUE_COSTLY |
| caution_three | +0.539 [+0.461, +0.611] | 3.04 [3.00, 3.09] | -0.317 [-0.400, -0.228] | HARMS_TRUE_TEMPORARY |
| three_only | +0.500 [+0.428, +0.567] | 3.00 [3.00, 3.00] | -0.411 [-0.483, -0.328] | HARMS_TRUE_TEMPORARY |
| code_retry | +0.539 [+0.450, +0.633] | 3.02 [3.00, 3.05] | +0.044 [+0.000, +0.111] | RECOMMENDABLE |

## Descriptive: by recovery time (failed calls before the fault clears)

Each entry: success / calls per request / share of requests past three calls.

| Arm, claim, fault | k = 1 | k = 2 | k = 3 | k = 4 |
|---|---|---|---|---|
| caution_three / permanent / transient | 1.00 / 2.02 / 0.00 | 1.00 / 3.02 / 0.02 | 0.20 / 3.25 / 0.20 | 0.16 / 3.44 / 0.24 |
| caution_three / transient / transient | 1.00 / 2.00 / 0.00 | 1.00 / 3.00 / 0.00 | 0.30 / 3.32 / 0.30 | 0.32 / 3.68 / 0.36 |
| caution / permanent / transient | 1.00 / 2.04 / 0.00 | 1.00 / 3.12 / 0.12 | 1.00 / 4.02 / 1.00 | 0.96 / 5.12 / 1.00 |
| caution / transient / transient | 1.00 / 2.00 / 0.00 | 1.00 / 3.00 / 0.00 | 1.00 / 4.07 / 1.00 | 0.98 / 5.04 / 1.00 |
| code_retry / permanent / transient | 0.93 / 2.07 / 0.00 | 0.98 / 3.00 / 0.00 | 0.18 / 3.18 / 0.18 | 0.26 / 3.56 / 0.26 |
| code_retry / transient / transient | 1.00 / 2.00 / 0.00 | 1.00 / 3.00 / 0.00 | 1.00 / 4.00 / 1.00 | 1.00 / 5.00 / 1.00 |
| control / permanent / transient | 0.00 / 1.00 / 0.00 | 0.05 / 1.15 / 0.00 | 0.05 / 1.16 / 0.05 | 0.04 / 1.20 / 0.04 |
| control / transient / transient | 1.00 / 2.07 / 0.00 | 0.98 / 2.98 / 0.00 | 0.93 / 3.98 / 0.93 | 0.92 / 4.94 / 0.92 |
| three_only / permanent / transient | 1.00 / 2.00 / 0.00 | 1.00 / 3.00 / 0.00 | 0.16 / 3.16 / 0.16 | 0.06 / 3.20 / 0.14 |
| three_only / transient / transient | 1.00 / 2.00 / 0.00 | 1.00 / 3.00 / 0.00 | 0.16 / 3.16 / 0.16 | 0.10 / 3.26 / 0.12 |

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls at the stock system | Agent calls | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|
| control / transient / transient | 30 | 0.96 | 3.54 | 3.54 | {'RETRY': 28, 'SITE_ONLY': 1, 'OTHER': 1} | 0.90 / 0.97 / 0.93 / 0.97 / 1.00 / 0.97 |
| control / permanent / transient | 30 | 0.03 | 1.13 | 1.13 | {'STOP': 30} | 0.00 / 0.00 / 0.03 / 0.03 / 0.07 / 0.07 |
| control / permanent / permanent | 30 | 0.00 | 1.11 | 1.11 | {'STOP': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / transient | 30 | 0.99 | 3.58 | 3.58 | {'SITE_ONLY': 2, 'RETRY': 28} | 1.00 / 1.00 / 1.00 / 0.97 / 1.00 / 1.00 |
| caution / permanent / transient | 30 | 0.99 | 3.63 | 3.63 | {'SITE_ONLY': 17, 'RETRY': 12, 'OTHER': 1} | 1.00 / 1.00 / 0.97 / 0.97 / 1.00 / 1.00 |
| caution / permanent / permanent | 30 | 0.00 | 5.67 | 5.67 | {'SITE_ONLY': 17, 'RETRY': 12, 'OTHER': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / transient | 30 | 0.64 | 3.02 | 3.02 | {'RETRY': 30} | 0.40 / 0.60 / 0.70 / 0.83 / 0.73 / 0.57 |
| caution_three / permanent / transient | 30 | 0.57 | 2.94 | 2.94 | {'RETRY': 30} | 0.40 / 0.53 / 0.50 / 0.70 / 0.60 / 0.70 |
| caution_three / permanent / permanent | 30 | 0.00 | 3.04 | 3.04 | {'RETRY': 28, 'SITE_ONLY': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| three_only / transient / transient | 30 | 0.54 | 2.86 | 2.86 | {'RETRY': 30} | 0.40 / 0.57 / 0.57 / 0.77 / 0.50 / 0.47 |
| three_only / permanent / transient | 30 | 0.53 | 2.84 | 2.84 | {'RETRY': 30} | 0.40 / 0.53 / 0.47 / 0.67 / 0.57 / 0.57 |
| three_only / permanent / permanent | 30 | 0.00 | 3.00 | 3.00 | {'RETRY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| code_retry / transient / transient | 30 | 1.00 | 3.55 | 1.52 | {'RETRY': 18} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| code_retry / permanent / transient | 30 | 0.57 | 2.97 | 1.12 | {'STOP': 20} | 0.33 / 0.50 / 0.57 / 0.67 / 0.67 / 0.70 |
| code_retry / permanent / permanent | 30 | 0.00 | 3.02 | 1.01 | {'STOP': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 450}
- cost: {'runs_recorded': 450, 'from_cache': 0, 'agent_calls': 9902, 'equiv_usd': 1.0283}
