# C4 study P1 verdict: VALID

**LIVE MODEL RUN (study P1: rewordings of the error message, claude-haiku-5-5, native tool use, thinking on)**: transport `anthropic_messages_native`, model `claude-haiku-5-5`; 6 requests per run, 30 runs per cell. Every cell has the transient fault (the first two calls fail).

## Primary: does each rewording of "unavailable" lower success against the neutral message? **GENERALIZES**

| Wording | Text | Success | Effect vs "request rejected" | Minus the original wording | Effect vs the second neutral sentence |
|---|---|---|---|---|---|
| original | ERROR: stock data for this depot is unavailable. | 0.00 | -0.394 [-0.567, -0.228] DIFFERENT |  | -0.900 [-1.000, -0.767] DIFFERENT |
| on_record | ERROR: this depot has no stock data on record. | 0.00 | -0.394 [-0.567, -0.228] DIFFERENT | +0.000 [+0.000, +0.000] SAME | -0.900 [-1.000, -0.767] DIFFERENT |
| not_available | ERROR: stock information is not available for this depot. | 0.00 | -0.394 [-0.567, -0.228] DIFFERENT | +0.000 [+0.000, +0.000] SAME | -0.900 [-1.000, -0.767] DIFFERENT |
| code_404 | ERROR 404: no stock data found for this depot. | 0.00 | -0.394 [-0.567, -0.228] DIFFERENT | +0.000 [+0.000, +0.000] SAME | -0.900 [-1.000, -0.767] DIFFERENT |

## Neutral messages

| Wording | Text | Success |
|---|---|---|
| original | ERROR: request rejected. | 0.39 |
| not_completed | ERROR: the request could not be completed. | 0.90 |

- Second neutral sentence minus the first: +0.506 [+0.278, +0.706] DIFFERENT

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| original / permanent / transient | 30 | 0.00 | 1.54 | 0/180 | 0/30 | {'RETRY': 16, 'STOP': 1, 'SITE_ONLY': 13} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| on_record / permanent / transient | 30 | 0.00 | 1.32 | 0/180 | 0/30 | {'STOP': 16, 'SITE_ONLY': 14} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| not_available / permanent / transient | 30 | 0.00 | 1.54 | 0/180 | 0/30 | {'SITE_ONLY': 24, 'STOP': 5, 'RETRY': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| code_404 / permanent / transient | 30 | 0.00 | 1.63 | 0/180 | 0/30 | {'SITE_ONLY': 26, 'STOP': 4} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| original / neutral / transient | 30 | 0.39 | 2.35 | 71/180 | 10/30 | {'SITE_ONLY': 27, 'RETRY': 3} | 0.40 / 0.40 / 0.37 / 0.40 / 0.40 / 0.40 |
| not_completed / neutral / transient | 30 | 0.90 | 2.91 | 162/180 | 4/30 | {'RETRY': 25, 'SITE_ONLY': 5} | 0.90 / 0.90 / 0.90 / 0.90 / 0.90 / 0.90 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 180}
- cost: {'runs_recorded': 180, 'from_cache': 0, 'agent_calls': 3112, 'equiv_usd': 0.2337}
