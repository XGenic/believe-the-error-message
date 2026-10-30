# C4 study R1 verdict: VALID

**LIVE MODEL RUN (study R1: recovery times and a retry in code, claude-haiku-5-5, native tool use, thinking off)**: transport `anthropic_messages_native`, model `claude-haiku-5-5`; 6 requests per run, 30 runs per cell.

The transient fault clears after 1, 2, 3, 4 failed calls, drawn per request. A strict count of three recovers 0.48 of these requests. Calls are counted at the stock system, so the code retry's own retries are included.

## Primary: the instruction (`caution_three`) minus the same count in code (`code_retry`): **WORSE_THAN_CODE**

| Measure | Instruction | Code retry | Δ [95% interval] | Label |
|---|---|---|---|---|
| Success, give-up trap | 0.39 | 0.48 | -0.083 [-0.172, +0.006] | SAME |
| Success, true 'temporary' | 0.42 | 1.00 | -0.578 [-0.656, -0.511] | DIFFERENT |
| Calls per request, true outage | 2.26 | 3.00 | -0.74 [-0.99, -0.50] | DIFFERENT |

## Secondary: the rule without the caution (`three_only`) minus the instruction (`caution_three`)

| Measure | Rule alone | Instruction | Δ [95% interval] | Label |
|---|---|---|---|---|
| Success, give-up trap | 0.33 | 0.39 | -0.067 [-0.178, +0.050] | SAME |
| Success, true 'temporary' | 0.46 | 0.42 | +0.039 [-0.044, +0.128] | SAME |
| Calls per request, true outage | 2.05 | 2.26 | -0.21 [-0.62, 0.17] | SAME |

## Secondary: each arm against control (W6's measures)

W6's verdict is shown for reference only: its bars were set for a fault that always cleared on the third call.

| Arm | Give-up rescue | Calls on a true outage | True-'temporary' success | W6's verdict |
|---|---|---|---|---|
| caution | +0.133 [+0.072, +0.206] | 1.45 [1.33, 1.58] | +0.206 [+0.089, +0.322] | WEAK_RESCUE |
| caution_three | +0.383 [+0.300, +0.461] | 2.26 [2.01, 2.50] | +0.178 [+0.061, +0.289] | WEAK_RESCUE |
| three_only | +0.317 [+0.228, +0.400] | 2.05 [1.73, 2.36] | +0.217 [+0.111, +0.322] | WEAK_RESCUE |
| code_retry | +0.467 [+0.417, +0.511] | 3.00 [3.00, 3.00] | +0.756 [+0.667, +0.844] | WEAK_RESCUE |

## Descriptive: by recovery time (failed calls before the fault clears)

Each entry: success / calls per request / share of requests past three calls.

| Arm, claim, fault | k = 1 | k = 2 | k = 3 | k = 4 |
|---|---|---|---|---|
| caution_three / permanent / transient | 0.82 / 1.82 / 0.00 | 0.83 / 2.66 / 0.00 | 0.00 / 2.61 / 0.00 | 0.00 / 2.62 / 0.00 |
| caution_three / transient / transient | 0.89 / 1.89 / 0.00 | 0.88 / 2.78 / 0.00 | 0.00 / 2.82 / 0.00 | 0.00 / 2.80 / 0.00 |
| caution / permanent / transient | 0.51 / 1.51 / 0.00 | 0.07 / 1.68 / 0.00 | 0.00 / 1.75 / 0.00 | 0.00 / 1.72 / 0.00 |
| caution / transient / transient | 0.91 / 1.91 / 0.00 | 0.83 / 2.78 / 0.00 | 0.05 / 2.84 / 0.05 | 0.08 / 2.96 / 0.08 |
| code_retry / permanent / transient | 1.00 / 2.00 / 0.00 | 1.00 / 3.00 / 0.00 | 0.00 / 3.00 / 0.00 | 0.00 / 3.00 / 0.00 |
| code_retry / transient / transient | 1.00 / 2.00 / 0.00 | 1.00 / 3.00 / 0.00 | 1.00 / 4.00 / 1.00 | 1.00 / 5.00 / 1.00 |
| control / permanent / transient | 0.04 / 1.04 / 0.00 | 0.00 / 1.02 / 0.00 | 0.00 / 1.02 / 0.00 | 0.00 / 1.04 / 0.00 |
| control / transient / transient | 0.56 / 1.56 / 0.00 | 0.46 / 2.07 / 0.00 | 0.00 / 2.11 / 0.00 | 0.00 / 2.24 / 0.00 |
| three_only / permanent / transient | 0.62 / 1.62 / 0.00 | 0.76 / 2.51 / 0.00 | 0.00 / 2.34 / 0.00 | 0.00 / 2.40 / 0.00 |
| three_only / transient / transient | 0.98 / 1.98 / 0.00 | 0.95 / 2.90 / 0.00 | 0.00 / 2.91 / 0.00 | 0.00 / 2.96 / 0.00 |

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls at the stock system | Agent calls | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|
| control / transient / transient | 30 | 0.24 | 2.00 | 2.00 | {'RETRY': 30} | 0.33 / 0.27 / 0.23 / 0.23 / 0.23 / 0.17 |
| control / permanent / transient | 30 | 0.01 | 1.03 | 1.03 | {'STOP': 29, 'RETRY': 1} | 0.03 / 0.00 / 0.00 / 0.00 / 0.03 / 0.00 |
| control / permanent / permanent | 30 | 0.00 | 1.00 | 1.00 | {'STOP': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / transient | 30 | 0.45 | 2.63 | 2.63 | {'RETRY': 25, 'SITE_ONLY': 5} | 0.37 / 0.50 / 0.40 / 0.57 / 0.47 / 0.40 |
| caution / permanent / transient | 30 | 0.14 | 1.67 | 1.67 | {'RETRY': 27, 'SITE_ONLY': 3} | 0.20 / 0.20 / 0.13 / 0.13 / 0.13 / 0.07 |
| caution / permanent / permanent | 30 | 0.00 | 1.45 | 1.45 | {'RETRY': 25, 'SITE_ONLY': 5} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / transient | 30 | 0.42 | 2.57 | 2.57 | {'RETRY': 30} | 0.40 / 0.43 / 0.47 / 0.47 / 0.37 / 0.40 |
| caution_three / permanent / transient | 30 | 0.39 | 2.43 | 2.43 | {'RETRY': 28, 'SITE_ONLY': 1, 'STOP': 1} | 0.37 / 0.40 / 0.37 / 0.43 / 0.43 / 0.37 |
| caution_three / permanent / permanent | 30 | 0.00 | 2.26 | 2.26 | {'RETRY': 27, 'STOP': 2, 'SITE_ONLY': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| three_only / transient / transient | 30 | 0.46 | 2.69 | 2.69 | {'RETRY': 30} | 0.40 / 0.50 / 0.43 / 0.57 / 0.43 / 0.43 |
| three_only / permanent / transient | 30 | 0.33 | 2.22 | 2.22 | {'STOP': 7, 'RETRY': 22, 'SITE_ONLY': 1} | 0.33 / 0.27 / 0.30 / 0.43 / 0.30 / 0.33 |
| three_only / permanent / permanent | 30 | 0.00 | 2.05 | 2.05 | {'STOP': 10, 'RETRY': 20} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| code_retry / transient / transient | 30 | 1.00 | 3.55 | 1.52 | {'RETRY': 18} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| code_retry / permanent / transient | 30 | 0.48 | 2.75 | 1.00 | {'STOP': 18} | 0.40 / 0.50 / 0.47 / 0.60 / 0.47 / 0.43 |
| code_retry / permanent / permanent | 30 | 0.00 | 3.00 | 1.00 | {'STOP': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 450}
- cost: {'runs_recorded': 450, 'from_cache': 0, 'agent_calls': 7653, 'equiv_usd': 0.4324}
