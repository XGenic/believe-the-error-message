# C4 study W6 verdict: VALID

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-w6-deaf`; 6 requests per run, 30 runs per cell.

## Primary: each wording of the stopping rule

The floor that keeps the give-up rescue is 3 calls on a true outage: the transient fault clears on the third.

| Wording | Verdict | Give-up rescue (vs control) | Outage calls | True-'temporary' success (vs control) | E3's verdict |
|---|---|---|---|---|---|
| caution_bounded | **WEAK_RESCUE** | +0.011 [-0.028, +0.050] | 1.07 [1.03, 1.11] | -0.033 [-0.078, +0.006] | NO_GAIN |
| caution_few | **WEAK_RESCUE** | -0.006 [-0.039, +0.028] | 1.15 [1.08, 1.23] | -0.006 [-0.033, +0.022] | NO_GAIN |
| caution_three | **WEAK_RESCUE** | -0.017 [-0.044, +0.011] | 1.07 [1.02, 1.12] | -0.033 [-0.067, +0.000] | NO_GAIN |

## Secondary: each new wording minus `caution_bounded`

| Wording | Give-up trap | True 'temporary' | Retry trap |
|---|---|---|---|
| caution_few | SAME -0.017 [-0.056, +0.017] | SAME +0.028 [-0.011, +0.072] | SAME -0.022 [-0.050, +0.006] |
| caution_three | SAME -0.028 [-0.067, +0.006] | SAME +0.000 [-0.050, +0.050] | SAME -0.011 [-0.044, +0.022] |

## Reference and secondary (vs control)

| Arm | Give-up rescue | Outage calls | Outage calls vs plain caution | True-'temporary' success | Retry trap |
|---|---|---|---|---|---|
| caution | -0.022 [-0.050, +0.006] | 1.12 [1.06, 1.18] |  | -0.022 [-0.061, +0.011] | +0.028 [-0.022, +0.078] |
| caution_bounded | +0.011 [-0.028, +0.050] | 1.07 [1.03, 1.11] | -0.050 [-0.122, +0.022] | -0.033 [-0.078, +0.006] | +0.000 [-0.033, +0.033] |
| caution_few | -0.006 [-0.039, +0.028] | 1.15 [1.08, 1.23] | +0.033 [-0.056, +0.128] | -0.006 [-0.033, +0.022] | -0.022 [-0.050, +0.006] |
| caution_three | -0.017 [-0.044, +0.011] | 1.07 [1.02, 1.12] | -0.050 [-0.128, +0.028] | -0.033 [-0.067, +0.000] | -0.011 [-0.039, +0.022] |

## Descriptive: true 'temporary' requests in which every call differed from the earlier ones

- control: 5/180 requests, 0 of them failed
- caution: 5/180 requests, 0 of them failed
- caution_bounded: 4/180 requests, 0 of them failed
- caution_few: 7/180 requests, 0 of them failed
- caution_three: 7/180 requests, 0 of them failed

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| control / transient / fixable | 30 | 0.03 | 5.72 | 170/180 | 6/30 | {'RETRY': 26, 'REFORMAT': 1, 'STOP': 3} | 0.03 / 0.03 / 0.03 / 0.00 / 0.07 / 0.03 |
| control / transient / transient | 30 | 0.98 | 2.97 | 177/180 | 5/30 | {'RETRY': 30} | 1.00 / 1.00 / 0.97 / 1.00 / 0.97 / 0.97 |
| control / permanent / transient | 30 | 0.03 | 1.11 | 6/180 | 6/30 | {'STOP': 29, 'RETRY': 1} | 0.00 / 0.07 / 0.07 / 0.00 / 0.03 / 0.03 |
| control / permanent / permanent | 30 | 0.00 | 1.18 | 8/180 | 7/30 | {'STOP': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / fixable | 30 | 0.06 | 5.63 | 168/180 | 7/30 | {'RETRY': 27, 'STOP': 1, 'REFORMAT': 2} | 0.07 / 0.10 / 0.03 / 0.07 / 0.03 / 0.07 |
| caution / transient / transient | 30 | 0.96 | 2.92 | 173/180 | 4/30 | {'RETRY': 28, 'STOP': 2} | 0.93 / 1.00 / 0.93 / 0.93 / 1.00 / 0.97 |
| caution / permanent / transient | 30 | 0.01 | 1.06 | 2/180 | 2/30 | {'STOP': 28, 'RETRY': 2} | 0.00 / 0.03 / 0.00 / 0.00 / 0.00 / 0.03 |
| caution / permanent / permanent | 30 | 0.00 | 1.12 | 4/180 | 4/30 | {'STOP': 24, 'RETRY': 4, 'REFORMAT': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_bounded / transient / fixable | 30 | 0.03 | 5.77 | 171/180 | 6/30 | {'RETRY': 28, 'STOP': 2} | 0.00 / 0.07 / 0.07 / 0.03 / 0.03 / 0.00 |
| caution_bounded / transient / transient | 30 | 0.95 | 2.90 | 171/180 | 4/30 | {'RETRY': 28, 'REFORMAT': 1, 'STOP': 1} | 0.97 / 1.00 / 0.93 / 0.90 / 0.93 / 0.97 |
| caution_bounded / permanent / transient | 30 | 0.04 | 1.13 | 8/180 | 7/30 | {'STOP': 28, 'RETRY': 1, 'REFORMAT': 1} | 0.03 / 0.03 / 0.00 / 0.07 / 0.07 / 0.07 |
| caution_bounded / permanent / permanent | 30 | 0.00 | 1.07 | 1/180 | 1/30 | {'STOP': 28, 'RETRY': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_few / transient / fixable | 30 | 0.01 | 5.81 | 174/180 | 2/30 | {'RETRY': 29, 'REFORMAT': 1} | 0.03 / 0.00 / 0.00 / 0.03 / 0.00 / 0.00 |
| caution_few / transient / transient | 30 | 0.98 | 2.96 | 176/180 | 5/30 | {'RETRY': 29, 'REFORMAT': 1} | 1.00 / 0.97 / 1.00 / 1.00 / 0.93 / 0.97 |
| caution_few / permanent / transient | 30 | 0.03 | 1.07 | 5/180 | 5/30 | {'STOP': 29, 'REFORMAT': 1} | 0.03 / 0.10 / 0.00 / 0.03 / 0.00 / 0.00 |
| caution_few / permanent / permanent | 30 | 0.00 | 1.15 | 5/180 | 5/30 | {'STOP': 28, 'RETRY': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / fixable | 30 | 0.02 | 5.79 | 174/180 | 4/30 | {'RETRY': 27, 'REFORMAT': 2, 'STOP': 1} | 0.07 / 0.03 / 0.03 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / transient | 30 | 0.95 | 2.90 | 171/180 | 6/30 | {'RETRY': 27, 'STOP': 3} | 0.90 / 1.00 / 0.97 / 0.97 / 0.93 / 0.93 |
| caution_three / permanent / transient | 30 | 0.02 | 1.05 | 3/180 | 3/30 | {'STOP': 28, 'RETRY': 1, 'REFORMAT': 1} | 0.03 / 0.00 / 0.00 / 0.03 / 0.00 / 0.03 |
| caution_three / permanent / permanent | 30 | 0.00 | 1.07 | 3/180 | 3/30 | {'STOP': 28, 'REFORMAT': 1, 'RETRY': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 600}
- cost: {'runs_recorded': 600, 'from_cache': 600, 'agent_calls': 13384, 'equiv_usd': 0.0}
