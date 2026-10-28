# C4 study W6 verdict: VALID

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-w6-different_harms`; 6 requests per run, 30 runs per cell.

## Primary: each wording of the stopping rule

The floor that keeps the give-up rescue is 3 calls on a true outage: the transient fault clears on the third.

| Wording | Verdict | Give-up rescue (vs control) | Outage calls | True-'temporary' success (vs control) | E3's verdict |
|---|---|---|---|---|---|
| caution_bounded | **HARMS_TRUE_TEMPORARY** | -0.033 [-0.056, -0.011] | 1.96 [1.92, 1.98] | -0.983 [-1.000, -0.961] | HARMS_TRUE_TEMPORARY |
| caution_few | **RECOMMENDABLE** | +0.928 [+0.889, +0.961] | 2.98 [2.94, 3.00] | -0.006 [-0.039, +0.022] | COST_AWARE |
| caution_three | **RECOMMENDABLE** | +0.933 [+0.900, +0.967] | 2.93 [2.88, 2.99] | -0.006 [-0.033, +0.022] | COST_AWARE |

## Secondary: each new wording minus `caution_bounded`

| Wording | Give-up trap | True 'temporary' | Retry trap |
|---|---|---|---|
| caution_few | DIFFERENT +0.961 [+0.928, +0.989] | DIFFERENT +0.978 [+0.950, +1.000] | DIFFERENT +0.317 [+0.294, +0.339] |
| caution_three | DIFFERENT +0.967 [+0.944, +0.989] | DIFFERENT +0.978 [+0.956, +0.994] | DIFFERENT +0.311 [+0.283, +0.333] |

## Reference and secondary (vs control)

| Arm | Give-up rescue | Outage calls | Outage calls vs plain caution | True-'temporary' success | Retry trap |
|---|---|---|---|---|---|
| caution | +0.928 [+0.889, +0.961] | 4.80 [4.68, 4.91] |  | -0.039 [-0.089, +0.006] | +0.939 [+0.906, +0.967] |
| caution_bounded | -0.033 [-0.056, -0.011] | 1.96 [1.92, 1.98] | -2.844 [-2.956, -2.717] | -0.983 [-1.000, -0.961] | +0.294 [+0.267, +0.317] |
| caution_few | +0.928 [+0.889, +0.961] | 2.98 [2.94, 3.00] | -1.822 [-1.939, -1.689] | -0.006 [-0.039, +0.022] | +0.611 [+0.578, +0.644] |
| caution_three | +0.933 [+0.900, +0.967] | 2.93 [2.88, 2.99] | -1.867 [-1.989, -1.733] | -0.006 [-0.033, +0.022] | +0.606 [+0.572, +0.633] |

## Descriptive: true 'temporary' requests in which every call differed from the earlier ones

- control: 5/180 requests, 0 of them failed
- caution: 164/180 requests, 0 of them failed
- caution_bounded: 170/180 requests, 170 of them failed
- caution_few: 171/180 requests, 0 of them failed
- caution_three: 172/180 requests, 0 of them failed

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
| caution_bounded / transient / fixable | 30 | 0.33 | 1.98 | 0/180 | 30/30 | {'REFORMAT': 30} | 0.30 / 0.47 / 0.37 / 0.17 / 0.37 / 0.30 |
| caution_bounded / transient / transient | 30 | 0.00 | 1.97 | 0/180 | 30/30 | {'REFORMAT': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_bounded / permanent / transient | 30 | 0.00 | 1.96 | 0/180 | 30/30 | {'REFORMAT': 27, 'RETRY': 2, 'STOP': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_bounded / permanent / permanent | 30 | 0.00 | 1.96 | 0/180 | 30/30 | {'REFORMAT': 28, 'RETRY': 1, 'STOP': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_few / transient / fixable | 30 | 0.64 | 2.63 | 120/180 | 30/30 | {'RETRY': 1, 'REFORMAT': 25, 'STOP': 4} | 0.47 / 0.60 / 0.63 / 0.70 / 0.80 / 0.67 |
| caution_few / transient / transient | 30 | 0.98 | 2.96 | 176/180 | 30/30 | {'REFORMAT': 28, 'RETRY': 1, 'STOP': 1} | 0.97 / 1.00 / 1.00 / 0.97 / 0.97 / 0.97 |
| caution_few / permanent / transient | 30 | 0.96 | 2.92 | 173/180 | 30/30 | {'REFORMAT': 29, 'STOP': 1} | 0.97 / 0.97 / 0.97 / 0.93 / 1.00 / 0.93 |
| caution_few / permanent / permanent | 30 | 0.00 | 2.98 | 178/180 | 30/30 | {'REFORMAT': 28, 'RETRY': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / fixable | 30 | 0.64 | 2.64 | 119/180 | 30/30 | {'REFORMAT': 28, 'RETRY': 2} | 0.67 / 0.83 / 0.47 / 0.73 / 0.60 / 0.53 |
| caution_three / transient / transient | 30 | 0.98 | 2.96 | 176/180 | 30/30 | {'REFORMAT': 30} | 1.00 / 1.00 / 0.93 / 1.00 / 0.93 / 1.00 |
| caution_three / permanent / transient | 30 | 0.97 | 2.93 | 174/180 | 30/30 | {'REFORMAT': 29, 'STOP': 1} | 0.97 / 0.97 / 0.93 / 0.97 / 1.00 / 0.97 |
| caution_three / permanent / permanent | 30 | 0.00 | 2.93 | 174/180 | 30/30 | {'REFORMAT': 28, 'STOP': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 600}
- cost: {'runs_recorded': 600, 'from_cache': 600, 'agent_calls': 13566, 'equiv_usd': 0.0}
