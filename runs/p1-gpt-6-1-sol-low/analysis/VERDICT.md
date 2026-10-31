# C4 study P1 verdict: VALID

**LIVE MODEL RUN (study P1: rewordings of the error message, gpt-6.1-sol, native tool calls, reasoning low)**: transport `openai_responses_native`, model `gpt-6.1-sol`; 6 requests per run, 30 runs per cell. Every cell has the transient fault (the first two calls fail).

## Primary: does each rewording of "unavailable" lower success against the neutral message? **GENERALIZES**

| Wording | Text | Success | Effect vs "request rejected" | Minus the original wording | Effect vs the second neutral sentence |
|---|---|---|---|---|---|
| original | ERROR: stock data for this depot is unavailable. | 0.00 | -0.967 [-1.000, -0.900] DIFFERENT |  | -1.000 [-1.000, -1.000] DIFFERENT |
| on_record | ERROR: this depot has no stock data on record. | 0.00 | -0.967 [-1.000, -0.900] DIFFERENT | +0.000 [+0.000, +0.000] SAME | -1.000 [-1.000, -1.000] DIFFERENT |
| not_available | ERROR: stock information is not available for this depot. | 0.00 | -0.967 [-1.000, -0.900] DIFFERENT | +0.000 [+0.000, +0.000] SAME | -1.000 [-1.000, -1.000] DIFFERENT |
| code_404 | ERROR 404: no stock data found for this depot. | 0.00 | -0.967 [-1.000, -0.900] DIFFERENT | +0.000 [+0.000, +0.000] SAME | -1.000 [-1.000, -1.000] DIFFERENT |

## Neutral messages

| Wording | Text | Success |
|---|---|---|
| original | ERROR: request rejected. | 0.97 |
| not_completed | ERROR: the request could not be completed. | 1.00 |

- Second neutral sentence minus the first: +0.033 [+0.000, +0.100] SAME

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| original / permanent / transient | 30 | 0.00 | 1.00 | 0/180 | 0/30 | {'STOP': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| on_record / permanent / transient | 30 | 0.00 | 1.00 | 0/180 | 0/30 | {'STOP': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| not_available / permanent / transient | 30 | 0.00 | 1.00 | 0/180 | 0/30 | {'STOP': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| code_404 / permanent / transient | 30 | 0.00 | 1.66 | 0/180 | 0/30 | {'STOP': 13, 'SITE_ONLY': 17} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| original / neutral / transient | 30 | 0.97 | 2.96 | 174/180 | 23/30 | {'SITE_ONLY': 1, 'RETRY': 29} | 0.97 / 0.97 / 0.97 / 0.97 / 0.97 / 0.97 |
| not_completed / neutral / transient | 30 | 1.00 | 3.00 | 180/180 | 0/30 | {'RETRY': 30} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 180}
- cost: {'runs_recorded': 180, 'from_cache': 0, 'agent_calls': 2990, 'equiv_usd': 3.9861}
