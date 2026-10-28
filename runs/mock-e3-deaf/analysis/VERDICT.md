# C4 extension E3 verdict: VALID

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-e3-deaf`; 6 requests per run, 30 runs per cell.

## Primary: does the stopping rule keep the rescue and cut the cost?

| Arm | Verdict | Give-up rescue (vs control) | Outage calls vs plain caution | True-'temporary' success (vs control) |
|---|---|---|---|---|
| caution_bounded | **NO_GAIN** | +0.000 [-0.039, +0.039] | -0.011 [-0.089, +0.056] | +0.011 [-0.022, +0.050] |
| caution_three | **NO_GAIN** | -0.017 [-0.056, +0.017] | +0.050 [-0.050, +0.144] | -0.022 [-0.061, +0.017] |

## Calls per request on a true outage ('unavailable' over a permanent fault)

The lowest cost that keeps the give-up rescue is 3 calls: the transient fault clears on the third.

- control: 1.14
- caution: 1.09
- caution_bounded: 1.08
- caution_three: 1.14

## Reference and secondary (vs control)

| Arm | Give-up rescue | Outage calls | True-'temporary' success | Retry trap |
|---|---|---|---|---|
| caution | -0.022 [-0.056, +0.011] | -0.044 [-0.139, +0.056] | +0.006 [-0.028, +0.044] | +0.028 [-0.011, +0.061] |
| caution_bounded | +0.000 [-0.039, +0.039] | -0.056 [-0.144, +0.033] | +0.011 [-0.022, +0.050] | +0.011 [-0.022, +0.039] |
| caution_three | -0.017 [-0.056, +0.017] | +0.006 [-0.106, +0.117] | -0.022 [-0.061, +0.017] | +0.006 [-0.028, +0.039] |

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| control / transient / fixable | 30 | 0.02 | 5.90 | 178/180 | 2/30 | {'RETRY': 27, 'REFORMAT': 1, 'STOP': 2} | 0.03 / 0.00 / 0.07 / 0.00 / 0.00 / 0.00 |
| control / transient / transient | 30 | 0.97 | 2.93 | 174/180 | 4/30 | {'RETRY': 29, 'STOP': 1} | 0.97 / 0.97 / 0.97 / 0.93 / 0.97 / 1.00 |
| control / permanent / transient | 30 | 0.04 | 1.13 | 7/180 | 6/30 | {'STOP': 29, 'RETRY': 1} | 0.00 / 0.07 / 0.03 / 0.00 / 0.03 / 0.10 |
| control / permanent / permanent | 30 | 0.00 | 1.14 | 7/180 | 7/30 | {'STOP': 26, 'RETRY': 2, 'REFORMAT': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / fixable | 30 | 0.04 | 5.69 | 171/180 | 8/30 | {'RETRY': 26, 'REFORMAT': 4} | 0.13 / 0.00 / 0.03 / 0.00 / 0.07 / 0.03 |
| caution / transient / transient | 30 | 0.97 | 2.94 | 175/180 | 7/30 | {'RETRY': 25, 'REFORMAT': 1, 'STOP': 4} | 0.87 / 1.00 / 1.00 / 1.00 / 0.97 / 1.00 |
| caution / permanent / transient | 30 | 0.02 | 1.06 | 3/180 | 3/30 | {'STOP': 29, 'RETRY': 1} | 0.00 / 0.00 / 0.00 / 0.03 / 0.03 / 0.03 |
| caution / permanent / permanent | 30 | 0.00 | 1.09 | 4/180 | 4/30 | {'STOP': 28, 'RETRY': 1, 'REFORMAT': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_bounded / transient / fixable | 30 | 0.03 | 5.84 | 176/180 | 5/30 | {'RETRY': 29, 'REFORMAT': 1} | 0.03 / 0.07 / 0.03 / 0.03 / 0.00 / 0.00 |
| caution_bounded / transient / transient | 30 | 0.98 | 2.96 | 176/180 | 3/30 | {'RETRY': 27, 'STOP': 1, 'REFORMAT': 2} | 0.97 / 0.97 / 0.97 / 1.00 / 0.97 / 1.00 |
| caution_bounded / permanent / transient | 30 | 0.04 | 1.10 | 7/180 | 7/30 | {'STOP': 27, 'REFORMAT': 2, 'RETRY': 1} | 0.07 / 0.07 / 0.00 / 0.00 / 0.03 / 0.07 |
| caution_bounded / permanent / permanent | 30 | 0.00 | 1.08 | 1/180 | 1/30 | {'STOP': 29, 'RETRY': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / fixable | 30 | 0.02 | 5.78 | 173/180 | 3/30 | {'RETRY': 27, 'REFORMAT': 2, 'STOP': 1} | 0.07 / 0.00 / 0.07 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / transient | 30 | 0.94 | 2.89 | 170/180 | 7/30 | {'RETRY': 28, 'STOP': 1, 'REFORMAT': 1} | 0.97 / 1.00 / 0.90 / 0.93 / 0.97 / 0.90 |
| caution_three / permanent / transient | 30 | 0.02 | 1.08 | 4/180 | 4/30 | {'STOP': 28, 'RETRY': 1, 'REFORMAT': 1} | 0.03 / 0.07 / 0.00 / 0.00 / 0.03 / 0.00 |
| caution_three / permanent / permanent | 30 | 0.00 | 1.14 | 5/180 | 5/30 | {'STOP': 27, 'RETRY': 2, 'REFORMAT': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 480}
- cost: {'runs_recorded': 480, 'from_cache': 0, 'agent_calls': 10758, 'equiv_usd': 0.0}
