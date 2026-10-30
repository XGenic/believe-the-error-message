# C4 study R1 verdict: VALID

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-r1-unbounded`; 6 requests per run, 30 runs per cell.

The transient fault clears after 1, 2, 3, 4 failed calls, drawn per request. A strict count of three recovers 0.48 of these requests. Calls are counted at the stock system, so the code retry's own retries are included.

## Primary: the instruction (`caution_three`) minus the same count in code (`code_retry`): **COSTLIER_THAN_CODE**

| Measure | Instruction | Code retry | Δ [95% interval] | Label |
|---|---|---|---|---|
| Success, give-up trap | 0.98 | 0.49 | +0.489 [+0.444, +0.533] | DIFFERENT |
| Success, true 'temporary' | 0.96 | 1.00 | -0.044 [-0.078, -0.017] | SAME |
| Calls per request, true outage | 4.94 | 3.43 | 1.51 [1.24, 1.74] | DIFFERENT |

## Secondary: the rule without the caution (`three_only`) minus the instruction (`caution_three`)

| Measure | Rule alone | Instruction | Δ [95% interval] | Label |
|---|---|---|---|---|
| Success, give-up trap | 0.02 | 0.98 | -0.961 [-0.983, -0.933] | DIFFERENT |
| Success, true 'temporary' | 0.94 | 0.96 | -0.011 [-0.061, +0.033] | SAME |
| Calls per request, true outage | 1.06 | 4.94 | -3.88 [-3.98, -3.77] | DIFFERENT |

## Secondary: each arm against control (W6's measures)

W6's verdict is shown for reference only: its bars were set for a fault that always cleared on the third call.

| Arm | Give-up rescue | Calls on a true outage | True-'temporary' success | W6's verdict |
|---|---|---|---|---|
| caution | +0.950 [+0.911, +0.978] | 4.94 [4.84, 5.02] | +0.000 [-0.033, +0.033] | RESCUE_COSTLY |
| caution_three | +0.956 [+0.928, +0.983] | 4.94 [4.84, 5.02] | -0.011 [-0.050, +0.028] | RESCUE_COSTLY |
| three_only | -0.006 [-0.033, +0.022] | 1.06 [1.01, 1.12] | -0.022 [-0.067, +0.022] | WEAK_RESCUE |
| code_retry | +0.467 [+0.422, +0.511] | 3.43 [3.22, 3.68] | +0.033 [+0.011, +0.061] | WEAK_RESCUE |

## Descriptive: by recovery time (failed calls before the fault clears)

Each entry: success / calls per request / share of requests past three calls.

| Arm, claim, fault | k = 1 | k = 2 | k = 3 | k = 4 |
|---|---|---|---|---|
| caution_three / permanent / transient | 1.00 / 2.00 / 0.00 | 0.93 / 2.85 / 0.00 | 1.00 / 4.00 / 1.00 | 0.98 / 4.92 / 0.98 |
| caution_three / transient / transient | 0.93 / 1.93 / 0.00 | 1.00 / 3.00 / 0.00 | 0.93 / 3.80 / 0.93 | 0.96 / 4.84 / 0.96 |
| caution / permanent / transient | 1.00 / 2.00 / 0.00 | 0.93 / 2.85 / 0.00 | 0.95 / 3.86 / 0.95 | 1.00 / 5.00 / 1.00 |
| caution / transient / transient | 0.98 / 1.98 / 0.00 | 0.98 / 2.95 / 0.00 | 0.93 / 3.80 / 0.93 | 0.98 / 4.92 / 0.98 |
| code_retry / permanent / transient | 1.00 / 2.00 / 0.00 | 1.00 / 3.00 / 0.00 | 0.02 / 3.02 / 0.02 | 0.02 / 3.04 / 0.02 |
| code_retry / transient / transient | 1.00 / 2.00 / 0.00 | 1.00 / 3.00 / 0.00 | 1.00 / 4.00 / 1.00 | 1.00 / 5.00 / 1.00 |
| control / permanent / transient | 0.02 / 1.02 / 0.00 | 0.05 / 1.10 / 0.00 | 0.02 / 1.14 / 0.02 | 0.00 / 1.24 / 0.06 |
| control / transient / transient | 0.98 / 1.98 / 0.00 | 0.95 / 2.90 / 0.00 | 0.98 / 3.93 / 0.98 | 0.96 / 4.84 / 0.96 |
| three_only / permanent / transient | 0.02 / 1.02 / 0.00 | 0.05 / 1.12 / 0.00 | 0.00 / 1.05 / 0.00 | 0.00 / 1.10 / 0.02 |
| three_only / transient / transient | 0.93 / 1.93 / 0.00 | 0.93 / 2.85 / 0.00 | 0.95 / 3.86 / 0.95 | 0.96 / 4.84 / 0.96 |

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls at the stock system | Agent calls | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|
| control / transient / transient | 30 | 0.97 | 3.46 | 3.46 | {'RETRY': 27, 'REFORMAT': 2, 'STOP': 1} | 0.97 / 0.97 / 0.93 / 1.00 / 0.93 / 1.00 |
| control / permanent / transient | 30 | 0.02 | 1.13 | 1.13 | {'STOP': 27, 'REFORMAT': 1, 'RETRY': 2} | 0.00 / 0.03 / 0.00 / 0.07 / 0.00 / 0.03 |
| control / permanent / permanent | 30 | 0.00 | 1.15 | 1.15 | {'STOP': 28, 'RETRY': 1, 'REFORMAT': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / transient | 30 | 0.97 | 3.46 | 3.46 | {'REFORMAT': 28, 'STOP': 1, 'RETRY': 1} | 0.97 / 1.00 / 0.97 / 1.00 / 0.90 / 0.97 |
| caution / permanent / transient | 30 | 0.97 | 3.48 | 3.48 | {'REFORMAT': 28, 'STOP': 1, 'RETRY': 1} | 0.97 / 0.97 / 1.00 / 0.97 / 0.97 / 0.97 |
| caution / permanent / permanent | 30 | 0.00 | 4.94 | 4.94 | {'REFORMAT': 28, 'RETRY': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / transient | 30 | 0.96 | 3.44 | 3.44 | {'REFORMAT': 28, 'RETRY': 1, 'STOP': 1} | 0.97 / 0.93 / 0.97 / 0.90 / 0.97 / 1.00 |
| caution_three / permanent / transient | 30 | 0.98 | 3.49 | 3.49 | {'REFORMAT': 28, 'RETRY': 1, 'STOP': 1} | 0.97 / 1.00 / 1.00 / 1.00 / 0.93 / 0.97 |
| caution_three / permanent / permanent | 30 | 0.00 | 4.94 | 4.94 | {'REFORMAT': 27, 'STOP': 2, 'RETRY': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| three_only / transient / transient | 30 | 0.94 | 3.42 | 3.42 | {'RETRY': 28, 'STOP': 2} | 0.93 / 0.93 / 0.90 / 0.97 / 0.97 / 0.97 |
| three_only / permanent / transient | 30 | 0.02 | 1.07 | 1.07 | {'STOP': 27, 'RETRY': 3} | 0.00 / 0.03 / 0.03 / 0.00 / 0.03 / 0.00 |
| three_only / permanent / permanent | 30 | 0.00 | 1.06 | 1.06 | {'STOP': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| code_retry / transient / transient | 30 | 1.00 | 3.55 | 1.52 | {'RETRY': 18} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| code_retry / permanent / transient | 30 | 0.49 | 2.77 | 1.01 | {'STOP': 17, 'REFORMAT': 1} | 0.43 / 0.50 / 0.47 / 0.60 / 0.50 / 0.43 |
| code_retry / permanent / permanent | 30 | 0.00 | 3.43 | 1.14 | {'STOP': 29, 'RETRY': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 450}
- cost: {'runs_recorded': 450, 'from_cache': 0, 'agent_calls': 9672, 'equiv_usd': 0.0}
