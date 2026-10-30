# C4 study P1 verdict: VALID

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-p1-generalizes`; 6 requests per run, 30 runs per cell. Every cell has the transient fault (the first two calls fail).

## Primary: does each rewording of "unavailable" lower success against the neutral message? **GENERALIZES**

| Wording | Text | Success | Effect vs "request rejected" | Minus the original wording | Effect vs the second neutral sentence |
|---|---|---|---|---|---|
| original | ERROR: stock data for this depot is unavailable. | 0.03 | -0.939 [-0.972, -0.900] DIFFERENT |  | -0.939 [-0.972, -0.906] DIFFERENT |
| on_record | ERROR: this depot has no stock data on record. | 0.04 | -0.928 [-0.961, -0.889] DIFFERENT | +0.011 [-0.022, +0.044] SAME | -0.928 [-0.961, -0.894] DIFFERENT |
| not_available | ERROR: stock information is not available for this depot. | 0.01 | -0.956 [-0.983, -0.922] DIFFERENT | -0.017 [-0.044, +0.011] SAME | -0.956 [-0.983, -0.922] DIFFERENT |
| code_404 | ERROR 404: no stock data found for this depot. | 0.04 | -0.922 [-0.956, -0.883] DIFFERENT | +0.017 [-0.017, +0.050] SAME | -0.922 [-0.956, -0.883] DIFFERENT |

## Neutral messages

| Wording | Text | Success |
|---|---|---|
| original | ERROR: request rejected. | 0.97 |
| not_completed | ERROR: the request could not be completed. | 0.97 |

- Second neutral sentence minus the first: +0.000 [-0.033, +0.039] SAME

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| original / permanent / transient | 30 | 0.03 | 1.07 | 5/180 | 5/30 | {'STOP': 29, 'RETRY': 1} | 0.00 / 0.03 / 0.03 / 0.07 / 0.00 / 0.03 |
| on_record / permanent / transient | 30 | 0.04 | 1.10 | 7/180 | 7/30 | {'STOP': 26, 'REFORMAT': 3, 'RETRY': 1} | 0.10 / 0.00 / 0.03 / 0.03 / 0.03 / 0.03 |
| not_available / permanent / transient | 30 | 0.01 | 1.04 | 2/180 | 2/30 | {'STOP': 29, 'RETRY': 1} | 0.00 / 0.03 / 0.00 / 0.00 / 0.00 / 0.03 |
| code_404 / permanent / transient | 30 | 0.04 | 1.13 | 8/180 | 8/30 | {'STOP': 30} | 0.00 / 0.03 / 0.03 / 0.13 / 0.03 / 0.03 |
| original / neutral / transient | 30 | 0.97 | 2.93 | 174/180 | 30/30 | {'REFORMAT': 24, 'RETRY': 5, 'STOP': 1} | 0.97 / 1.00 / 0.97 / 0.90 / 0.97 / 1.00 |
| not_completed / neutral / transient | 30 | 0.97 | 2.93 | 174/180 | 30/30 | {'REFORMAT': 25, 'RETRY': 3, 'STOP': 2} | 0.93 / 1.00 / 1.00 / 0.97 / 0.97 / 0.93 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 180}
- cost: {'runs_recorded': 180, 'from_cache': 0, 'agent_calls': 2916, 'equiv_usd': 0.0}
