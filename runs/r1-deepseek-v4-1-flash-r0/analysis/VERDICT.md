# C4 study R1 verdict: VALID

**LIVE MODEL RUN (study R1: recovery times and a retry in code, deepseek/deepseek-v4.1-flash, DeepInfra, reasoning off)**: transport `openrouter_chat_native`, model `deepseek/deepseek-v4.1-flash`; 6 requests per run, 30 runs per cell.

The transient fault clears after 1, 2, 3, 4 failed calls, drawn per request. A strict count of three recovers 0.48 of these requests. Calls are counted at the stock system, so the code retry's own retries are included.

## Primary: the instruction (`caution_three`) minus the same count in code (`code_retry`): **WORSE_THAN_CODE**

| Measure | Instruction | Code retry | Δ [95% interval] | Label |
|---|---|---|---|---|
| Success, give-up trap | 0.49 | 0.56 | -0.067 [-0.161, +0.022] | SAME |
| Success, true 'temporary' | 0.49 | 1.00 | -0.506 [-0.544, -0.467] | DIFFERENT |
| Calls per request, true outage | 3.01 | 3.10 | -0.09 [-0.16, -0.02] | SAME |

## Secondary: the rule without the caution (`three_only`) minus the instruction (`caution_three`)

| Measure | Rule alone | Instruction | Δ [95% interval] | Label |
|---|---|---|---|---|
| Success, give-up trap | 0.48 | 0.49 | -0.006 [-0.067, +0.056] | SAME |
| Success, true 'temporary' | 0.48 | 0.49 | -0.011 [-0.078, +0.056] | SAME |
| Calls per request, true outage | 3.01 | 3.01 | -0.01 [-0.04, 0.03] | SAME |

## Secondary: each arm against control (W6's measures)

W6's verdict is shown for reference only: its bars were set for a fault that always cleared on the third call.

| Arm | Give-up rescue | Calls on a true outage | True-'temporary' success | W6's verdict |
|---|---|---|---|---|
| caution | +0.394 [+0.289, +0.500] | 1.70 [1.53, 1.86] | -0.078 [-0.167, +0.011] | WEAK_RESCUE |
| caution_three | +0.483 [+0.433, +0.539] | 3.01 [3.00, 3.03] | -0.411 [-0.472, -0.344] | HARMS_TRUE_TEMPORARY |
| three_only | +0.478 [+0.439, +0.517] | 3.01 [2.97, 3.04] | -0.422 [-0.494, -0.344] | HARMS_TRUE_TEMPORARY |
| code_retry | +0.550 [+0.483, +0.628] | 3.10 [3.03, 3.17] | +0.094 [+0.044, +0.150] | RECOMMENDABLE |

## Descriptive: by recovery time (failed calls before the fault clears)

Each entry: success / calls per request / share of requests past three calls.

| Arm, claim, fault | k = 1 | k = 2 | k = 3 | k = 4 |
|---|---|---|---|---|
| caution_three / permanent / transient | 1.00 / 2.00 / 0.00 | 0.98 / 2.98 / 0.00 | 0.07 / 3.07 / 0.07 | 0.00 / 3.08 / 0.08 |
| caution_three / transient / transient | 1.00 / 2.00 / 0.00 | 1.00 / 3.00 / 0.00 | 0.07 / 3.07 / 0.07 | 0.00 / 3.04 / 0.04 |
| caution / permanent / transient | 0.84 / 1.84 / 0.00 | 0.49 / 2.39 / 0.02 | 0.18 / 2.61 / 0.20 | 0.12 / 2.58 / 0.22 |
| caution / transient / transient | 1.00 / 2.00 / 0.00 | 0.95 / 3.05 / 0.05 | 0.75 / 3.84 / 0.75 | 0.64 / 4.68 / 0.90 |
| code_retry / permanent / transient | 1.00 / 2.00 / 0.00 | 1.00 / 3.00 / 0.00 | 0.14 / 3.14 / 0.14 | 0.16 / 3.32 / 0.16 |
| code_retry / transient / transient | 1.00 / 2.00 / 0.00 | 1.00 / 3.00 / 0.00 | 1.00 / 4.00 / 1.00 | 1.00 / 5.00 / 1.00 |
| control / permanent / transient | 0.02 / 1.02 / 0.00 | 0.00 / 1.05 / 0.00 | 0.00 / 1.07 / 0.00 | 0.00 / 1.02 / 0.00 |
| control / transient / transient | 1.00 / 2.00 / 0.00 | 0.98 / 2.98 / 0.00 | 0.91 / 3.89 / 0.91 | 0.76 / 4.50 / 0.80 |
| three_only / permanent / transient | 1.00 / 2.00 / 0.00 | 0.98 / 2.98 / 0.00 | 0.05 / 3.05 / 0.05 | 0.00 / 3.06 / 0.06 |
| three_only / transient / transient | 0.96 / 2.04 / 0.00 | 0.98 / 3.00 / 0.00 | 0.09 / 3.09 / 0.09 | 0.00 / 3.08 / 0.10 |

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls at the stock system | Agent calls | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|
| control / transient / transient | 30 | 0.91 | 3.38 | 3.38 | {'RETRY': 30} | 0.87 / 0.93 / 0.87 / 0.93 / 0.97 / 0.87 |
| control / permanent / transient | 30 | 0.01 | 1.04 | 1.04 | {'STOP': 27, 'SITE_ONLY': 2, 'RETRY': 1} | 0.03 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / permanent / permanent | 30 | 0.00 | 1.02 | 1.02 | {'STOP': 27, 'RETRY': 2, 'OTHER': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / transient | 30 | 0.83 | 3.43 | 3.43 | {'RETRY': 28, 'SITE_ONLY': 2} | 0.80 / 0.83 / 0.83 / 0.83 / 0.83 / 0.83 |
| caution / permanent / transient | 30 | 0.40 | 2.36 | 2.36 | {'SITE_ONLY': 13, 'RETRY': 15, 'STOP': 2} | 0.27 / 0.50 / 0.43 / 0.40 / 0.40 / 0.40 |
| caution / permanent / permanent | 30 | 0.00 | 1.70 | 1.70 | {'RETRY': 8, 'SITE_ONLY': 16, 'STOP': 4, 'OTHER': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / transient | 30 | 0.49 | 2.78 | 2.78 | {'RETRY': 30} | 0.40 / 0.50 / 0.47 / 0.60 / 0.53 / 0.47 |
| caution_three / permanent / transient | 30 | 0.49 | 2.78 | 2.78 | {'RETRY': 27, 'SITE_ONLY': 3} | 0.40 / 0.50 / 0.47 / 0.63 / 0.47 / 0.47 |
| caution_three / permanent / permanent | 30 | 0.00 | 3.01 | 3.01 | {'RETRY': 29, 'SITE_ONLY': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| three_only / transient / transient | 30 | 0.48 | 2.81 | 2.81 | {'RETRY': 29, 'OTHER': 1} | 0.40 / 0.57 / 0.43 / 0.57 / 0.53 / 0.40 |
| three_only / permanent / transient | 30 | 0.48 | 2.77 | 2.77 | {'RETRY': 30} | 0.40 / 0.50 / 0.47 / 0.63 / 0.43 / 0.47 |
| three_only / permanent / permanent | 30 | 0.00 | 3.01 | 3.01 | {'RETRY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| code_retry / transient / transient | 30 | 1.00 | 3.55 | 1.52 | {'RETRY': 18} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| code_retry / permanent / transient | 30 | 0.56 | 2.87 | 1.08 | {'STOP': 14, 'SITE_ONLY': 3, 'RETRY': 1} | 0.53 / 0.57 / 0.57 / 0.60 / 0.57 / 0.50 |
| code_retry / permanent / permanent | 30 | 0.00 | 3.10 | 1.03 | {'REFORMAT': 1, 'STOP': 24, 'RETRY': 2, 'SITE_ONLY': 3} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 450}
- cost: {'runs_recorded': 450, 'from_cache': 0, 'agent_calls': 8770, 'equiv_usd': 0.3179}
