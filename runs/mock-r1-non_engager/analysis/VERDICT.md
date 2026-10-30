# C4 study R1 verdict: INVALID

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-r1-non_engager`; 6 requests per run, 30 runs per cell.

- tool use on request 1 0.0 below 0.9 in some cell: agents did not engage
- unclassifiable responses None above 0.1

The transient fault clears after 1, 2, 3, 4 failed calls, drawn per request. A strict count of three recovers 0.48 of these requests. Calls are counted at the stock system, so the code retry's own retries are included.

## Primary: the instruction (`caution_three`) minus the same count in code (`code_retry`): **MATCHES_CODE**

| Measure | Instruction | Code retry | Δ [95% interval] | Label |
|---|---|---|---|---|
| Success, give-up trap | 0.00 | 0.00 | +0.000 [+0.000, +0.000] | SAME |
| Success, true 'temporary' | 0.00 | 0.00 | +0.000 [+0.000, +0.000] | SAME |
| Calls per request, true outage | 0.00 | 0.00 | 0.00 [0.00, 0.00] | SAME |

## Secondary: the rule without the caution (`three_only`) minus the instruction (`caution_three`)

| Measure | Rule alone | Instruction | Δ [95% interval] | Label |
|---|---|---|---|---|
| Success, give-up trap | 0.00 | 0.00 | +0.000 [+0.000, +0.000] | SAME |
| Success, true 'temporary' | 0.00 | 0.00 | +0.000 [+0.000, +0.000] | SAME |
| Calls per request, true outage | 0.00 | 0.00 | 0.00 [0.00, 0.00] | SAME |

## Secondary: each arm against control (W6's measures)

W6's verdict is shown for reference only: its bars were set for a fault that always cleared on the third call.

| Arm | Give-up rescue | Calls on a true outage | True-'temporary' success | W6's verdict |
|---|---|---|---|---|
| caution | +0.000 [+0.000, +0.000] | 0.00 [0.00, 0.00] | +0.000 [+0.000, +0.000] | WEAK_RESCUE |
| caution_three | +0.000 [+0.000, +0.000] | 0.00 [0.00, 0.00] | +0.000 [+0.000, +0.000] | WEAK_RESCUE |
| three_only | +0.000 [+0.000, +0.000] | 0.00 [0.00, 0.00] | +0.000 [+0.000, +0.000] | WEAK_RESCUE |
| code_retry | +0.000 [+0.000, +0.000] | 0.00 [0.00, 0.00] | +0.000 [+0.000, +0.000] | WEAK_RESCUE |

## Descriptive: by recovery time (failed calls before the fault clears)

Each entry: success / calls per request / share of requests past three calls.

| Arm, claim, fault | k = 1 | k = 2 | k = 3 | k = 4 |
|---|---|---|---|---|
| caution_three / permanent / transient | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 |
| caution_three / transient / transient | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 |
| caution / permanent / transient | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 |
| caution / transient / transient | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 |
| code_retry / permanent / transient | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 |
| code_retry / transient / transient | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 |
| control / permanent / transient | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 |
| control / transient / transient | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 |
| three_only / permanent / transient | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 |
| three_only / transient / transient | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 |

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls at the stock system | Agent calls | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|
| control / transient / transient | 30 | 0.00 | 0.00 | 0.00 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / permanent / transient | 30 | 0.00 | 0.00 | 0.00 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / permanent / permanent | 30 | 0.00 | 0.00 | 0.00 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / transient | 30 | 0.00 | 0.00 | 0.00 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / permanent / transient | 30 | 0.00 | 0.00 | 0.00 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / permanent / permanent | 30 | 0.00 | 0.00 | 0.00 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / transient | 30 | 0.00 | 0.00 | 0.00 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / permanent / transient | 30 | 0.00 | 0.00 | 0.00 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / permanent / permanent | 30 | 0.00 | 0.00 | 0.00 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| three_only / transient / transient | 30 | 0.00 | 0.00 | 0.00 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| three_only / permanent / transient | 30 | 0.00 | 0.00 | 0.00 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| three_only / permanent / permanent | 30 | 0.00 | 0.00 | 0.00 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| code_retry / transient / transient | 30 | 0.00 | 0.00 | 0.00 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| code_retry / permanent / transient | 30 | 0.00 | 0.00 | 0.00 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| code_retry / permanent / permanent | 30 | 0.00 | 0.00 | 0.00 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 0.0; unclassifiable None
- run statuses: {'complete': 450}
- cost: {'runs_recorded': 450, 'from_cache': 0, 'agent_calls': 2700, 'equiv_usd': 0.0}
