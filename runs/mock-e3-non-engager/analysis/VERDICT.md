# C4 extension E3 verdict: INVALID

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-e3-non-engager`; 6 requests per run, 30 runs per cell.

- tool use on request 1 0.0 below 0.9 in some cell: agents did not engage
- unclassifiable responses None above 0.1

## Primary: does the stopping rule keep the rescue and cut the cost?

| Arm | Verdict | Give-up rescue (vs control) | Outage calls vs plain caution | True-'temporary' success (vs control) |
|---|---|---|---|---|
| caution_bounded | **NO_GAIN** | +0.000 [+0.000, +0.000] | 0 [0, 0] | +0.000 [+0.000, +0.000] |
| caution_three | **NO_GAIN** | +0.000 [+0.000, +0.000] | 0 [0, 0] | +0.000 [+0.000, +0.000] |

## Calls per request on a true outage ('unavailable' over a permanent fault)

The lowest cost that keeps the give-up rescue is 3 calls: the transient fault clears on the third.

- control: 0.00
- caution: 0.00
- caution_bounded: 0.00
- caution_three: 0.00

## Reference and secondary (vs control)

| Arm | Give-up rescue | Outage calls | True-'temporary' success | Retry trap |
|---|---|---|---|---|
| caution | +0.000 [+0.000, +0.000] | 0 [0, 0] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| caution_bounded | +0.000 [+0.000, +0.000] | 0 [0, 0] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| caution_three | +0.000 [+0.000, +0.000] | 0 [0, 0] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |

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
| caution_three / transient / fixable | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / permanent / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / permanent / permanent | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 0.0; unclassifiable None
- run statuses: {'complete': 480}
- cost: {'runs_recorded': 480, 'from_cache': 0, 'agent_calls': 2880, 'equiv_usd': 0.0}
