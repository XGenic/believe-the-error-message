# C4 extension E2 verdict: VALID

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-e2-instruction-follower`; 6 requests per run, 30 runs per cell.

## Primary: change in trap success over control

| Arm | Retry trap ('temporary' over fixable) | Give-up trap ('unavailable' over transient) |
|---|---|---|
| caution | **NO_EFFECT** +0.017 [-0.022, +0.056] | **NO_EFFECT** +0.011 [-0.028, +0.044] |
| caution_strategy | **NO_EFFECT** +0.011 [-0.022, +0.050] | **NO_EFFECT** +0.028 [-0.011, +0.067] |
| mixed | **RESCUES** +0.928 [+0.889, +0.961] | **RESCUES** +0.928 [+0.883, +0.961] |
| honest | **RESCUES** +0.950 [+0.922, +0.978] | **RESCUES** +0.933 [+0.894, +0.972] |

## Cost on the accurate cells

| Arm | Δ success, accurate 'temporary' | Δ calls per request, accurate 'unavailable' | Flags |
|---|---|---|---|
| caution | +0.006 [-0.039, +0.050] | +0.072 [-0.028, +0.183] | none |
| caution_strategy | +0.000 [-0.039, +0.039] | +0.128 [+0.017, +0.267] | none |
| mixed | +0.011 [-0.022, +0.050] | +3.878 [+3.767, +3.972] | calls per request in the accurate 'unavailable' cell rose by 3.88 |
| honest | -0.006 [-0.050, +0.033] | +3.806 [+3.683, +3.917] | calls per request in the accurate 'unavailable' cell rose by 3.81 |

## Secondary: honest message minus the neutral message ('request rejected')

- fixable fault: +0.006 [-0.022, +0.033]
- transient fault: -0.017 [-0.056, +0.022]

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| control / transient / fixable | 30 | 0.03 | 5.77 | 172/180 | 5/30 | {'RETRY': 29, 'REFORMAT': 1} | 0.03 / 0.03 / 0.00 / 0.03 / 0.07 / 0.00 |
| control / transient / transient | 30 | 0.96 | 2.92 | 173/180 | 5/30 | {'RETRY': 29, 'STOP': 1} | 0.97 / 0.97 / 0.97 / 0.90 / 1.00 / 0.97 |
| control / permanent / transient | 30 | 0.02 | 1.08 | 4/180 | 3/30 | {'STOP': 27, 'REFORMAT': 2, 'RETRY': 1} | 0.07 / 0.03 / 0.00 / 0.00 / 0.00 / 0.03 |
| control / permanent / permanent | 30 | 0.00 | 1.07 | 1/180 | 1/30 | {'STOP': 29, 'RETRY': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / neutral / fixable | 30 | 0.97 | 3.00 | 120/180 | 30/30 | {'REFORMAT': 28, 'RETRY': 2} | 1.00 / 0.97 / 1.00 / 0.97 / 0.97 / 0.93 |
| control / neutral / transient | 30 | 0.97 | 2.94 | 175/180 | 30/30 | {'REFORMAT': 28, 'STOP': 1, 'RETRY': 1} | 0.97 / 0.97 / 1.00 / 0.97 / 0.93 / 1.00 |
| caution / transient / fixable | 30 | 0.04 | 5.76 | 174/180 | 7/30 | {'RETRY': 29, 'REFORMAT': 1} | 0.03 / 0.00 / 0.03 / 0.07 / 0.00 / 0.13 |
| caution / transient / transient | 30 | 0.97 | 2.93 | 174/180 | 6/30 | {'REFORMAT': 2, 'RETRY': 27, 'STOP': 1} | 0.97 / 0.97 / 1.00 / 0.93 / 0.97 / 0.97 |
| caution / permanent / transient | 30 | 0.03 | 1.11 | 6/180 | 6/30 | {'STOP': 26, 'REFORMAT': 3, 'RETRY': 1} | 0.10 / 0.00 / 0.00 / 0.00 / 0.03 / 0.07 |
| caution / permanent / permanent | 30 | 0.00 | 1.14 | 8/180 | 7/30 | {'STOP': 29, 'REFORMAT': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_strategy / transient / fixable | 30 | 0.04 | 5.69 | 171/180 | 6/30 | {'RETRY': 27, 'STOP': 2, 'REFORMAT': 1} | 0.03 / 0.00 / 0.10 / 0.03 / 0.03 / 0.03 |
| caution_strategy / transient / transient | 30 | 0.96 | 2.92 | 173/180 | 3/30 | {'RETRY': 30} | 1.00 / 1.00 / 0.90 / 0.97 / 0.97 / 0.93 |
| caution_strategy / permanent / transient | 30 | 0.05 | 1.13 | 9/180 | 9/30 | {'STOP': 29, 'REFORMAT': 1} | 0.03 / 0.03 / 0.07 / 0.03 / 0.03 / 0.10 |
| caution_strategy / permanent / permanent | 30 | 0.00 | 1.20 | 10/180 | 7/30 | {'RETRY': 2, 'REFORMAT': 1, 'STOP': 27} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| mixed / transient / fixable | 30 | 0.96 | 2.96 | 115/180 | 30/30 | {'REFORMAT': 28, 'RETRY': 1, 'STOP': 1} | 0.97 / 0.93 / 0.93 / 0.97 / 1.00 / 0.93 |
| mixed / transient / transient | 30 | 0.97 | 2.94 | 175/180 | 30/30 | {'REFORMAT': 28, 'RETRY': 2} | 1.00 / 0.97 / 1.00 / 1.00 / 0.97 / 0.90 |
| mixed / permanent / transient | 30 | 0.95 | 2.90 | 171/180 | 30/30 | {'REFORMAT': 29, 'RETRY': 1} | 1.00 / 0.87 / 1.00 / 0.93 / 0.93 / 0.97 |
| mixed / permanent / permanent | 30 | 0.00 | 4.95 | 175/180 | 30/30 | {'REFORMAT': 26, 'RETRY': 2, 'STOP': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| honest / unknown / fixable | 30 | 0.98 | 2.99 | 119/180 | 30/30 | {'REFORMAT': 28, 'RETRY': 2} | 1.00 / 1.00 / 0.97 / 1.00 / 0.97 / 0.93 |
| honest / unknown / transient | 30 | 0.96 | 2.91 | 172/180 | 30/30 | {'REFORMAT': 28, 'STOP': 2} | 0.93 / 0.97 / 1.00 / 0.90 / 0.97 / 0.97 |
| honest / unknown / permanent | 30 | 0.00 | 4.88 | 173/180 | 30/30 | {'REFORMAT': 26, 'STOP': 3, 'RETRY': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 630}
- cost: {'runs_recorded': 630, 'from_cache': 0, 'agent_calls': 15158, 'equiv_usd': 0.0}
