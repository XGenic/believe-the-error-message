# C4 study P1 verdict: INVALID

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-p1-non_engager`; 6 requests per run, 30 runs per cell. Every cell has the transient fault (the first two calls fail).

- tool use on request 1 0.0 below 0.9 in some cell: agents did not engage
- unclassifiable responses None above 0.1

## Primary: does each rewording of "unavailable" lower success against the neutral message? **NOT_TESTABLE**

| Wording | Text | Success | Effect vs "request rejected" | Minus the original wording | Effect vs the second neutral sentence |
|---|---|---|---|---|---|
| original | ERROR: stock data for this depot is unavailable. | 0.00 | +0.000 [+0.000, +0.000] SAME |  | +0.000 [+0.000, +0.000] SAME |
| on_record | ERROR: this depot has no stock data on record. | 0.00 | +0.000 [+0.000, +0.000] SAME | +0.000 [+0.000, +0.000] SAME | +0.000 [+0.000, +0.000] SAME |
| not_available | ERROR: stock information is not available for this depot. | 0.00 | +0.000 [+0.000, +0.000] SAME | +0.000 [+0.000, +0.000] SAME | +0.000 [+0.000, +0.000] SAME |
| code_404 | ERROR 404: no stock data found for this depot. | 0.00 | +0.000 [+0.000, +0.000] SAME | +0.000 [+0.000, +0.000] SAME | +0.000 [+0.000, +0.000] SAME |

## Neutral messages

| Wording | Text | Success |
|---|---|---|
| original | ERROR: request rejected. | 0.00 |
| not_completed | ERROR: the request could not be completed. | 0.00 |

- Second neutral sentence minus the first: +0.000 [+0.000, +0.000] SAME

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| original / permanent / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| on_record / permanent / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| not_available / permanent / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| code_404 / permanent / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| original / neutral / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| not_completed / neutral / transient | 30 | 0.00 | 0.00 | 0/180 | 0/30 | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 0.0; unclassifiable None
- run statuses: {'complete': 180}
- cost: {'runs_recorded': 180, 'from_cache': 0, 'agent_calls': 1080, 'equiv_usd': 0.0}
