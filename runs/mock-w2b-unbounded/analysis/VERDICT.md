# C4 extension E3 verdict: VALID

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-w2b-unbounded`; 6 requests per run, 30 runs per cell.

## Primary: does the stopping rule keep the rescue and cut the cost?

| Arm | Verdict | Give-up rescue (vs control) | Outage calls vs plain caution | True-'temporary' success (vs control) |
|---|---|---|---|---|
| caution_bounded | **RESCUE_ONLY** | +0.922 [+0.872, +0.967] | -0.033 [-0.183, +0.111] | +0.000 [-0.039, +0.044] |

## Calls per request on a true outage ('unavailable' over a permanent fault)

The lowest cost that keeps the give-up rescue is 3 calls: the transient fault clears on the third.

- control: 1.14
- caution: 4.91
- caution_bounded: 4.88
- caution_three: n/a

## Reference and secondary (vs control)

| Arm | Give-up rescue | Outage calls | True-'temporary' success | Retry trap |
|---|---|---|---|---|
| caution | +0.917 [+0.872, +0.961] | +3.772 [+3.644, +3.883] | -0.011 [-0.050, +0.028] | +0.939 [+0.900, +0.972] |
| caution_bounded | +0.922 [+0.872, +0.967] | +3.739 [+3.589, +3.878] | +0.000 [-0.039, +0.044] | +0.956 [+0.917, +0.983] |

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| control / transient / fixable | 30 | 0.02 | 5.90 | 178/180 | 2/30 | {'RETRY': 27, 'REFORMAT': 1, 'STOP': 2} | 0.03 / 0.00 / 0.07 / 0.00 / 0.00 / 0.00 |
| control / transient / transient | 30 | 0.97 | 2.93 | 174/180 | 4/30 | {'RETRY': 29, 'STOP': 1} | 0.97 / 0.97 / 0.97 / 0.93 / 0.97 / 1.00 |
| control / permanent / transient | 30 | 0.04 | 1.13 | 7/180 | 6/30 | {'STOP': 29, 'RETRY': 1} | 0.00 / 0.07 / 0.03 / 0.00 / 0.03 / 0.10 |
| control / permanent / permanent | 30 | 0.00 | 1.14 | 7/180 | 7/30 | {'STOP': 26, 'RETRY': 2, 'REFORMAT': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / fixable | 30 | 0.96 | 2.96 | 118/180 | 30/30 | {'REFORMAT': 29, 'RETRY': 1} | 1.00 / 1.00 / 0.97 / 0.93 / 0.90 / 0.93 |
| caution / transient / transient | 30 | 0.96 | 2.91 | 172/180 | 30/30 | {'REFORMAT': 28, 'RETRY': 1, 'STOP': 1} | 0.97 / 1.00 / 1.00 / 1.00 / 0.83 / 0.93 |
| caution / permanent / transient | 30 | 0.96 | 2.91 | 172/180 | 30/30 | {'REFORMAT': 27, 'STOP': 2, 'RETRY': 1} | 0.93 / 1.00 / 0.97 / 0.97 / 0.93 / 0.93 |
| caution / permanent / permanent | 30 | 0.00 | 4.91 | 175/180 | 30/30 | {'REFORMAT': 28, 'RETRY': 1, 'STOP': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_bounded / transient / fixable | 30 | 0.97 | 2.94 | 116/180 | 30/30 | {'REFORMAT': 28, 'STOP': 2} | 0.93 / 1.00 / 0.97 / 1.00 / 0.93 / 1.00 |
| caution_bounded / transient / transient | 30 | 0.97 | 2.93 | 174/180 | 30/30 | {'REFORMAT': 29, 'STOP': 1} | 0.97 / 0.93 / 1.00 / 1.00 / 0.93 / 0.97 |
| caution_bounded / permanent / transient | 30 | 0.96 | 2.92 | 173/180 | 30/30 | {'REFORMAT': 25, 'STOP': 2, 'RETRY': 3} | 0.93 / 0.93 / 0.97 / 1.00 / 0.97 / 0.97 |
| caution_bounded / permanent / permanent | 30 | 0.00 | 4.88 | 172/180 | 30/30 | {'REFORMAT': 23, 'STOP': 4, 'RETRY': 3} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 360}
- cost: {'runs_recorded': 360, 'from_cache': 360, 'agent_calls': 9085, 'equiv_usd': 0.0}
