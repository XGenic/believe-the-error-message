# C4 study W6 verdict: INVALID

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-w6-non_engager`; 6 requests per run, 30 runs per cell.

- tool use on request 1 0.0 below 0.9 in some cell: agents did not engage
- unclassifiable responses None above 0.1

## Primary: each wording of the stopping rule

The floor that keeps the give-up rescue is 3 calls on a true outage: the transient fault clears on the third.

| Wording | Verdict | Give-up rescue (vs control) | Outage calls | True-'temporary' success (vs control) | E3's verdict |
|---|---|---|---|---|---|
| caution_bounded | **WEAK_RESCUE** | +0.000 [+0.000, +0.000] | 0.00 [0.00, 0.00] | +0.000 [+0.000, +0.000] | NO_GAIN |
| caution_few | **WEAK_RESCUE** | +0.000 [+0.000, +0.000] | 0.00 [0.00, 0.00] | +0.000 [+0.000, +0.000] | NO_GAIN |
| caution_three | **WEAK_RESCUE** | +0.000 [+0.000, +0.000] | 0.00 [0.00, 0.00] | +0.000 [+0.000, +0.000] | NO_GAIN |

## Secondary: each new wording minus `caution_bounded`

| Wording | Give-up trap | True 'temporary' | Retry trap |
|---|---|---|---|
| caution_few | SAME +0.000 [+0.000, +0.000] | SAME +0.000 [+0.000, +0.000] | SAME +0.000 [+0.000, +0.000] |
| caution_three | SAME +0.000 [+0.000, +0.000] | SAME +0.000 [+0.000, +0.000] | SAME +0.000 [+0.000, +0.000] |

## Reference and secondary (vs control)

| Arm | Give-up rescue | Outage calls | Outage calls vs plain caution | True-'temporary' success | Retry trap |
|---|---|---|---|---|---|
| caution | +0.000 [+0.000, +0.000] | 0.00 [0.00, 0.00] |  | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| caution_bounded | +0.000 [+0.000, +0.000] | 0.00 [0.00, 0.00] | 0 [0, 0] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| caution_few | +0.000 [+0.000, +0.000] | 0.00 [0.00, 0.00] | 0 [0, 0] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| caution_three | +0.000 [+0.000, +0.000] | 0.00 [0.00, 0.00] | 0 [0, 0] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |

## Descriptive: true 'temporary' requests in which every call differed from the earlier ones

- control: 0/180 requests, 0 of them failed
- caution: 0/180 requests, 0 of them failed
- caution_bounded: 0/180 requests, 0 of them failed
- caution_few: 0/180 requests, 0 of them failed
- caution_three: 0/180 requests, 0 of them failed

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| control / transient / fixable | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / transient / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / permanent / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / permanent / permanent | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / fixable | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / permanent / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / permanent / permanent | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_bounded / transient / fixable | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_bounded / transient / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_bounded / permanent / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_bounded / permanent / permanent | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_few / transient / fixable | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_few / transient / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_few / permanent / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_few / permanent / permanent | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / fixable | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / permanent / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / permanent / permanent | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 0.0; unclassifiable None
- run statuses: {'complete': 600}
- cost: {'runs_recorded': 600, 'from_cache': 600, 'agent_calls': 3600, 'equiv_usd': 0.0}
