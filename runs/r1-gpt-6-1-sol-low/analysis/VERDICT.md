# C4 study R1 verdict: VALID

**LIVE MODEL RUN (study R1: recovery times and a retry in code, gpt-6.1-sol, native tool calls, reasoning low)**: transport `openai_responses_native`, model `gpt-6.1-sol`; 6 requests per run, 30 runs per cell.

The transient fault clears after 1, 2, 3, 4 failed calls, drawn per request. A strict count of three recovers 0.48 of these requests. Calls are counted at the stock system, so the code retry's own retries are included.

## Primary: the instruction (`caution_three`) minus the same count in code (`code_retry`): **WORSE_THAN_CODE**

| Measure | Instruction | Code retry | Δ [95% interval] | Label |
|---|---|---|---|---|
| Success, give-up trap | 0.48 | 0.48 | +0.000 [-0.056, +0.061] | SAME |
| Success, true 'temporary' | 0.48 | 1.00 | -0.522 [-0.561, -0.483] | DIFFERENT |
| Calls per request, true outage | 3.00 | 3.00 | 0.00 [0.00, 0.00] | SAME |

## Secondary: the rule without the caution (`three_only`) minus the instruction (`caution_three`)

| Measure | Rule alone | Instruction | Δ [95% interval] | Label |
|---|---|---|---|---|
| Success, give-up trap | 0.48 | 0.48 | +0.000 [-0.056, +0.056] | SAME |
| Success, true 'temporary' | 0.48 | 0.48 | +0.000 [-0.056, +0.061] | SAME |
| Calls per request, true outage | 3.00 | 3.00 | 0.00 [0.00, 0.00] | SAME |

## Secondary: each arm against control (W6's measures)

W6's verdict is shown for reference only: its bars were set for a fault that always cleared on the third call.

| Arm | Give-up rescue | Calls on a true outage | True-'temporary' success | W6's verdict |
|---|---|---|---|---|
| caution | +0.944 [+0.889, +0.983] | 4.28 [3.93, 4.67] | +0.000 [+0.000, +0.000] | RESCUE_COSTLY |
| caution_three | +0.478 [+0.439, +0.517] | 3.00 [3.00, 3.00] | -0.522 [-0.561, -0.483] | HARMS_TRUE_TEMPORARY |
| three_only | +0.478 [+0.439, +0.517] | 3.00 [3.00, 3.00] | -0.522 [-0.561, -0.483] | HARMS_TRUE_TEMPORARY |
| code_retry | +0.478 [+0.439, +0.517] | 3.00 [3.00, 3.00] | +0.000 [+0.000, +0.000] | WEAK_RESCUE |

## Descriptive: by recovery time (failed calls before the fault clears)

Each entry: success / calls per request / share of requests past three calls.

| Arm, claim, fault | k = 1 | k = 2 | k = 3 | k = 4 |
|---|---|---|---|---|
| caution_three / permanent / transient | 1.00 / 2.00 / 0.00 | 1.00 / 3.00 / 0.00 | 0.00 / 3.00 / 0.00 | 0.00 / 3.00 / 0.00 |
| caution_three / transient / transient | 1.00 / 2.00 / 0.00 | 1.00 / 3.00 / 0.00 | 0.00 / 3.00 / 0.00 | 0.00 / 3.00 / 0.00 |
| caution / permanent / transient | 1.00 / 2.00 / 0.00 | 1.00 / 3.00 / 0.00 | 1.00 / 4.00 / 1.00 | 0.80 / 4.78 / 0.98 |
| caution / transient / transient | 1.00 / 2.00 / 0.00 | 1.00 / 3.00 / 0.00 | 1.00 / 4.00 / 1.00 | 1.00 / 5.00 / 1.00 |
| code_retry / permanent / transient | 1.00 / 2.00 / 0.00 | 1.00 / 3.00 / 0.00 | 0.00 / 3.00 / 0.00 | 0.00 / 3.00 / 0.00 |
| code_retry / transient / transient | 1.00 / 2.00 / 0.00 | 1.00 / 3.00 / 0.00 | 1.00 / 4.00 / 1.00 | 1.00 / 5.00 / 1.00 |
| control / permanent / transient | 0.00 / 1.00 / 0.00 | 0.00 / 1.00 / 0.00 | 0.00 / 1.00 / 0.00 | 0.00 / 1.00 / 0.00 |
| control / transient / transient | 1.00 / 2.00 / 0.00 | 1.00 / 3.00 / 0.00 | 1.00 / 4.00 / 1.00 | 1.00 / 5.00 / 1.00 |
| three_only / permanent / transient | 1.00 / 2.00 / 0.00 | 1.00 / 3.00 / 0.00 | 0.00 / 3.00 / 0.00 | 0.00 / 3.00 / 0.00 |
| three_only / transient / transient | 1.00 / 2.00 / 0.00 | 1.00 / 3.00 / 0.00 | 0.00 / 3.00 / 0.00 | 0.00 / 3.00 / 0.00 |

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls at the stock system | Agent calls | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|
| control / transient / transient | 30 | 1.00 | 3.55 | 3.55 | {'RETRY': 30} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| control / permanent / transient | 30 | 0.00 | 1.00 | 1.00 | {'STOP': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / permanent / permanent | 30 | 0.00 | 1.00 | 1.00 | {'STOP': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / transient | 30 | 1.00 | 3.55 | 3.55 | {'RETRY': 30} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution / permanent / transient | 30 | 0.94 | 3.49 | 3.49 | {'SITE_ONLY': 28, 'RETRY': 2} | 0.83 / 1.00 / 0.87 / 1.00 / 1.00 / 0.97 |
| caution / permanent / permanent | 30 | 0.00 | 4.28 | 4.28 | {'SITE_ONLY': 26, 'RETRY': 4} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / transient | 30 | 0.48 | 2.75 | 2.75 | {'RETRY': 30} | 0.40 / 0.50 / 0.47 / 0.60 / 0.47 / 0.43 |
| caution_three / permanent / transient | 30 | 0.48 | 2.75 | 2.75 | {'RETRY': 30} | 0.40 / 0.50 / 0.47 / 0.60 / 0.47 / 0.43 |
| caution_three / permanent / permanent | 30 | 0.00 | 3.00 | 3.00 | {'RETRY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| three_only / transient / transient | 30 | 0.48 | 2.75 | 2.75 | {'RETRY': 30} | 0.40 / 0.50 / 0.47 / 0.60 / 0.47 / 0.43 |
| three_only / permanent / transient | 30 | 0.48 | 2.75 | 2.75 | {'RETRY': 30} | 0.40 / 0.50 / 0.47 / 0.60 / 0.47 / 0.43 |
| three_only / permanent / permanent | 30 | 0.00 | 3.00 | 3.00 | {'RETRY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| code_retry / transient / transient | 30 | 1.00 | 3.55 | 1.52 | {'RETRY': 18} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| code_retry / permanent / transient | 30 | 0.48 | 2.75 | 1.00 | {'STOP': 18} | 0.40 / 0.50 / 0.47 / 0.60 / 0.47 / 0.43 |
| code_retry / permanent / permanent | 30 | 0.00 | 3.00 | 1.00 | {'STOP': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 450}
- cost: {'runs_recorded': 450, 'from_cache': 0, 'agent_calls': 9431, 'equiv_usd': 11.8597}
