# C4 extension E2 verdict: VALID

**LIVE MODEL RUN (extension E2)**: transport `openai_responses`, model `gpt-6-luna`; 6 requests per run, 30 runs per cell.

## Primary: change in trap success over control

| Arm | Retry trap ('temporary' over fixable) | Give-up trap ('unavailable' over transient) |
|---|---|---|
| caution | **NO_EFFECT** +0.067 [+0.028, +0.117] | **RESCUES** +0.978 [+0.944, +1.000] |
| caution_strategy | **HELPS** +0.417 [+0.367, +0.472] | **RESCUES** +1.000 [+1.000, +1.000] |
| mixed | **NO_EFFECT** +0.000 [+0.000, +0.000] | **HELPS** +0.272 [+0.150, +0.406] |
| honest | **HELPS** +0.233 [+0.178, +0.289] | **RESCUES** +0.989 [+0.967, +1.000] |

## Cost on the accurate cells

| Arm | Δ success, accurate 'temporary' | Δ calls per request, accurate 'unavailable' | Flags |
|---|---|---|---|
| caution | +0.000 [+0.000, +0.000] | +4.267 [+4.050, +4.461] | calls per request in the accurate 'unavailable' cell rose by 4.27 |
| caution_strategy | +0.000 [+0.000, +0.000] | +4.589 [+4.422, +4.744] | calls per request in the accurate 'unavailable' cell rose by 4.59 |
| mixed | +0.000 [+0.000, +0.000] | +1.233 [+0.972, +1.506] | calls per request in the accurate 'unavailable' cell rose by 1.23 |
| honest | -0.011 [-0.033, +0.000] | +4.150 [+3.722, +4.494] | calls per request in the accurate 'unavailable' cell rose by 4.15 |

## Secondary: honest message minus the neutral message ('request rejected')

- fixable fault: +0.006 [-0.067, +0.083]
- transient fault: +0.339 [+0.206, +0.478]

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| control / transient / fixable | 30 | 0.00 | 5.78 | 180/180 | 0/30 | {'RETRY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / transient / transient | 30 | 1.00 | 3.00 | 180/180 | 0/30 | {'RETRY': 30} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| control / permanent / transient | 30 | 0.00 | 1.00 | 0/180 | 0/30 | {'STOP': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / permanent / permanent | 30 | 0.00 | 1.00 | 0/180 | 0/30 | {'STOP': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / neutral / fixable | 30 | 0.23 | 3.29 | 102/180 | 22/30 | {'SITE_ONLY': 29, 'RETRY': 1} | 0.10 / 0.23 / 0.23 / 0.30 / 0.30 / 0.20 |
| control / neutral / transient | 30 | 0.65 | 2.56 | 118/180 | 25/30 | {'SITE_ONLY': 27, 'STOP': 3} | 0.43 / 0.47 / 0.67 / 0.70 / 0.80 / 0.83 |
| caution / transient / fixable | 30 | 0.07 | 5.70 | 177/180 | 9/30 | {'RETRY': 30} | 0.00 / 0.03 / 0.10 / 0.07 / 0.13 / 0.07 |
| caution / transient / transient | 30 | 1.00 | 3.02 | 180/180 | 0/30 | {'RETRY': 30} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution / permanent / transient | 30 | 0.98 | 3.00 | 176/180 | 25/30 | {'SITE_ONLY': 15, 'RETRY': 15} | 0.93 / 0.93 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution / permanent / permanent | 30 | 0.00 | 5.27 | 177/180 | 29/30 | {'RETRY': 14, 'SITE_ONLY': 15, 'STOP': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_strategy / transient / fixable | 30 | 0.42 | 4.67 | 155/180 | 30/30 | {'SITE_ONLY': 30} | 0.23 / 0.43 / 0.37 / 0.57 / 0.47 / 0.43 |
| caution_strategy / transient / transient | 30 | 1.00 | 3.04 | 180/180 | 30/30 | {'SITE_ONLY': 30} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_strategy / permanent / transient | 30 | 1.00 | 3.01 | 180/180 | 30/30 | {'SITE_ONLY': 30} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_strategy / permanent / permanent | 30 | 0.00 | 5.59 | 180/180 | 30/30 | {'SITE_ONLY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| mixed / transient / fixable | 30 | 0.00 | 5.73 | 180/180 | 1/30 | {'RETRY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| mixed / transient / transient | 30 | 1.00 | 3.00 | 180/180 | 0/30 | {'RETRY': 30} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| mixed / permanent / transient | 30 | 0.27 | 2.17 | 49/180 | 12/30 | {'STOP': 4, 'SITE_ONLY': 26} | 0.07 / 0.20 / 0.23 / 0.33 / 0.40 / 0.40 |
| mixed / permanent / permanent | 30 | 0.00 | 2.23 | 30/180 | 10/30 | {'SITE_ONLY': 26, 'STOP': 4} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| honest / unknown / fixable | 30 | 0.23 | 4.57 | 149/180 | 22/30 | {'RETRY': 28, 'STOP': 1, 'SITE_ONLY': 1} | 0.07 / 0.30 / 0.27 / 0.27 / 0.30 / 0.20 |
| honest / unknown / transient | 30 | 0.99 | 2.98 | 178/180 | 16/30 | {'RETRY': 28, 'UNCLASSIFIABLE': 1, 'SITE_ONLY': 1} | 0.97 / 0.97 / 1.00 / 1.00 / 1.00 / 1.00 |
| honest / unknown / permanent | 30 | 0.00 | 5.15 | 166/180 | 19/30 | {'RETRY': 29, 'STOP': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.010118810755499972; tool use on request 1 (min) 1.0; unclassifiable 0.0008002133902373967
- run statuses: {'complete': 630}
- cost: {'runs_recorded': 630, 'from_cache': 0, 'agent_calls': 17591, 'equiv_usd': 2.0061}
