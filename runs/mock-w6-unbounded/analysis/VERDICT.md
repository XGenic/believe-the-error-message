# C4 study W6 verdict: VALID

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-w6-unbounded`; 6 requests per run, 30 runs per cell.

## Primary: each wording of the stopping rule

The floor that keeps the give-up rescue is 3 calls on a true outage: the transient fault clears on the third.

| Wording | Verdict | Give-up rescue (vs control) | Outage calls | True-'temporary' success (vs control) | E3's verdict |
|---|---|---|---|---|---|
| caution_bounded | **RESCUE_COSTLY** | +0.933 [+0.900, +0.967] | 4.95 [4.87, 5.02] | -0.028 [-0.067, +0.006] | RESCUE_ONLY |
| caution_few | **RESCUE_COSTLY** | +0.917 [+0.878, +0.956] | 4.90 [4.79, 5.00] | -0.006 [-0.039, +0.028] | RESCUE_ONLY |
| caution_three | **RESCUE_COSTLY** | +0.917 [+0.878, +0.956] | 5.02 [4.96, 5.07] | -0.017 [-0.050, +0.011] | RESCUE_ONLY |

## Secondary: each new wording minus `caution_bounded`

| Wording | Give-up trap | True 'temporary' | Retry trap |
|---|---|---|---|
| caution_few | SAME -0.017 [-0.056, +0.022] | SAME +0.022 [-0.017, +0.061] | SAME -0.006 [-0.033, +0.028] |
| caution_three | SAME -0.017 [-0.056, +0.022] | SAME +0.011 [-0.028, +0.050] | SAME -0.011 [-0.044, +0.022] |

## Reference and secondary (vs control)

| Arm | Give-up rescue | Outage calls | Outage calls vs plain caution | True-'temporary' success | Retry trap |
|---|---|---|---|---|---|
| caution | +0.928 [+0.889, +0.961] | 4.80 [4.68, 4.91] |  | -0.039 [-0.089, +0.006] | +0.939 [+0.906, +0.967] |
| caution_bounded | +0.933 [+0.900, +0.967] | 4.95 [4.87, 5.02] | +0.150 [+0.017, +0.294] | -0.028 [-0.067, +0.006] | +0.944 [+0.911, +0.972] |
| caution_few | +0.917 [+0.878, +0.956] | 4.90 [4.79, 5.00] | +0.100 [-0.061, +0.267] | -0.006 [-0.039, +0.028] | +0.939 [+0.906, +0.967] |
| caution_three | +0.917 [+0.878, +0.956] | 5.02 [4.96, 5.07] | +0.217 [+0.094, +0.350] | -0.017 [-0.050, +0.011] | +0.933 [+0.894, +0.967] |

## Descriptive: true 'temporary' requests in which every call differed from the earlier ones

- control: 5/180 requests, 0 of them failed
- caution: 164/180 requests, 0 of them failed
- caution_bounded: 167/180 requests, 0 of them failed
- caution_few: 169/180 requests, 0 of them failed
- caution_three: 167/180 requests, 0 of them failed

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| control / transient / fixable | 30 | 0.03 | 5.72 | 170/180 | 6/30 | {'RETRY': 26, 'REFORMAT': 1, 'STOP': 3} | 0.03 / 0.03 / 0.03 / 0.00 / 0.07 / 0.03 |
| control / transient / transient | 30 | 0.98 | 2.97 | 177/180 | 5/30 | {'RETRY': 30} | 1.00 / 1.00 / 0.97 / 1.00 / 0.97 / 0.97 |
| control / permanent / transient | 30 | 0.03 | 1.11 | 6/180 | 6/30 | {'STOP': 29, 'RETRY': 1} | 0.00 / 0.07 / 0.07 / 0.00 / 0.03 / 0.03 |
| control / permanent / permanent | 30 | 0.00 | 1.18 | 8/180 | 7/30 | {'STOP': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / fixable | 30 | 0.97 | 2.98 | 120/180 | 30/30 | {'REFORMAT': 30} | 1.00 / 1.00 / 0.97 / 0.93 / 0.97 / 0.97 |
| caution / transient / transient | 30 | 0.94 | 2.89 | 170/180 | 30/30 | {'REFORMAT': 28, 'STOP': 2} | 0.93 / 0.97 / 0.93 / 0.93 / 0.97 / 0.93 |
| caution / permanent / transient | 30 | 0.96 | 2.92 | 173/180 | 30/30 | {'REFORMAT': 30} | 1.00 / 1.00 / 0.93 / 0.93 / 0.93 / 0.97 |
| caution / permanent / permanent | 30 | 0.00 | 4.80 | 170/180 | 30/30 | {'REFORMAT': 29, 'RETRY': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_bounded / transient / fixable | 30 | 0.98 | 2.99 | 120/180 | 30/30 | {'REFORMAT': 30} | 1.00 / 1.00 / 0.93 / 1.00 / 1.00 / 0.93 |
| caution_bounded / transient / transient | 30 | 0.96 | 2.91 | 172/180 | 30/30 | {'REFORMAT': 26, 'STOP': 3, 'RETRY': 1} | 0.90 / 0.90 / 0.97 / 1.00 / 1.00 / 0.97 |
| caution_bounded / permanent / transient | 30 | 0.97 | 2.93 | 174/180 | 30/30 | {'REFORMAT': 30} | 1.00 / 0.93 / 1.00 / 0.93 / 0.93 / 1.00 |
| caution_bounded / permanent / permanent | 30 | 0.00 | 4.95 | 176/180 | 30/30 | {'REFORMAT': 29, 'STOP': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_few / transient / fixable | 30 | 0.97 | 3.00 | 119/180 | 30/30 | {'REFORMAT': 28, 'STOP': 1, 'RETRY': 1} | 0.97 / 0.97 / 1.00 / 1.00 / 0.93 / 0.97 |
| caution_few / transient / transient | 30 | 0.98 | 2.96 | 176/180 | 30/30 | {'REFORMAT': 28, 'STOP': 2} | 0.93 / 1.00 / 1.00 / 0.97 / 1.00 / 0.97 |
| caution_few / permanent / transient | 30 | 0.95 | 2.90 | 171/180 | 30/30 | {'REFORMAT': 27, 'RETRY': 2, 'STOP': 1} | 0.97 / 0.97 / 0.93 / 0.97 / 0.90 / 0.97 |
| caution_few / permanent / permanent | 30 | 0.00 | 4.90 | 173/180 | 30/30 | {'REFORMAT': 26, 'STOP': 2, 'RETRY': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / fixable | 30 | 0.97 | 2.97 | 116/180 | 30/30 | {'REFORMAT': 26, 'STOP': 1, 'RETRY': 3} | 0.97 / 0.93 / 0.97 / 1.00 / 0.93 / 1.00 |
| caution_three / transient / transient | 30 | 0.97 | 2.93 | 174/180 | 30/30 | {'REFORMAT': 27, 'RETRY': 3} | 1.00 / 0.97 / 0.93 / 0.93 / 1.00 / 0.97 |
| caution_three / permanent / transient | 30 | 0.95 | 2.90 | 171/180 | 30/30 | {'REFORMAT': 29, 'RETRY': 1} | 1.00 / 0.93 / 1.00 / 0.87 / 0.90 / 1.00 |
| caution_three / permanent / permanent | 30 | 0.00 | 5.02 | 179/180 | 30/30 | {'REFORMAT': 28, 'RETRY': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 600}
- cost: {'runs_recorded': 600, 'from_cache': 600, 'agent_calls': 15464, 'equiv_usd': 0.0}
