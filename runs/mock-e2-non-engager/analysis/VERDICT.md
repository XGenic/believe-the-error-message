# C4 extension E2 verdict: INVALID

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-e2-non-engager`; 6 requests per run, 30 runs per cell.

- tool use on request 1 0.0 below 0.9 in some cell: agents did not engage
- unclassifiable responses None above 0.1

## Primary: change in trap success over control

| Arm | Retry trap ('temporary' over fixable) | Give-up trap ('unavailable' over transient) |
|---|---|---|
| caution | **NO_EFFECT** +0.000 [+0.000, +0.000] | **NO_EFFECT** +0.000 [+0.000, +0.000] |
| caution_strategy | **NO_EFFECT** +0.000 [+0.000, +0.000] | **NO_EFFECT** +0.000 [+0.000, +0.000] |
| mixed | **NO_EFFECT** +0.000 [+0.000, +0.000] | **NO_EFFECT** +0.000 [+0.000, +0.000] |
| honest | **NO_EFFECT** +0.000 [+0.000, +0.000] | **NO_EFFECT** +0.000 [+0.000, +0.000] |

## Cost on the accurate cells

| Arm | Δ success, accurate 'temporary' | Δ calls per request, accurate 'unavailable' | Flags |
|---|---|---|---|
| caution | +0.000 [+0.000, +0.000] | 0 [0, 0] | none |
| caution_strategy | +0.000 [+0.000, +0.000] | 0 [0, 0] | none |
| mixed | +0.000 [+0.000, +0.000] | 0 [0, 0] | none |
| honest | +0.000 [+0.000, +0.000] | 0 [0, 0] | none |

## Secondary: honest message minus the neutral message ('request rejected')

- fixable fault: +0.000 [+0.000, +0.000]
- transient fault: +0.000 [+0.000, +0.000]

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| control / transient / fixable | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / transient / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / permanent / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / permanent / permanent | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / neutral / fixable | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / neutral / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / fixable | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / permanent / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / permanent / permanent | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_strategy / transient / fixable | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_strategy / transient / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_strategy / permanent / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_strategy / permanent / permanent | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| mixed / transient / fixable | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| mixed / transient / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| mixed / permanent / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| mixed / permanent / permanent | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| honest / unknown / fixable | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| honest / unknown / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| honest / unknown / permanent | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 0.0; unclassifiable None
- run statuses: {'complete': 630}
- cost: {'runs_recorded': 630, 'from_cache': 0, 'agent_calls': 3780, 'equiv_usd': 0.0}
