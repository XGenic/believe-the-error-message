# C4 study P1 verdict: VALID

**LIVE MODEL RUN (study P1: rewordings of the error message, deepseek/deepseek-v4.1-flash, DeepInfra, reasoning on)**: transport `openrouter_chat_native`, model `deepseek/deepseek-v4.1-flash`; 6 requests per run, 30 runs per cell. Every cell has the transient fault (the first two calls fail).

## Primary: does each rewording of "unavailable" lower success against the neutral message? **PARTIAL**

| Wording | Text | Success | Effect vs "request rejected" | Minus the original wording | Effect vs the second neutral sentence |
|---|---|---|---|---|---|
| original | ERROR: stock data for this depot is unavailable. | 0.05 | -0.950 [-1.000, -0.878] DIFFERENT |  | -0.950 [-1.000, -0.878] DIFFERENT |
| on_record | ERROR: this depot has no stock data on record. | 0.21 | -0.789 [-0.900, -0.661] DIFFERENT | +0.161 [+0.028, +0.300] DIFFERENT | -0.789 [-0.900, -0.661] DIFFERENT |
| not_available | ERROR: stock information is not available for this depot. | 0.51 | -0.489 [-0.628, -0.339] DIFFERENT | +0.461 [+0.306, +0.628] DIFFERENT | -0.489 [-0.628, -0.339] DIFFERENT |
| code_404 | ERROR 404: no stock data found for this depot. | 0.99 | -0.011 [-0.028, +0.000] SAME | +0.939 [+0.867, +0.989] DIFFERENT | -0.011 [-0.028, +0.000] SAME |

## Neutral messages

| Wording | Text | Success |
|---|---|---|
| original | ERROR: request rejected. | 1.00 |
| not_completed | ERROR: the request could not be completed. | 1.00 |

- Second neutral sentence minus the first: +0.000 [+0.000, +0.000] SAME

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| original / permanent / transient | 30 | 0.05 | 1.93 | 9/180 | 3/30 | {'SITE_ONLY': 30} | 0.00 / 0.03 / 0.03 / 0.07 / 0.07 / 0.10 |
| on_record / permanent / transient | 30 | 0.21 | 2.13 | 42/180 | 10/30 | {'SITE_ONLY': 26, 'STOP': 3, 'OTHER': 1} | 0.07 / 0.13 / 0.20 / 0.23 / 0.30 / 0.33 |
| not_available / permanent / transient | 30 | 0.51 | 2.57 | 99/180 | 18/30 | {'SITE_ONLY': 29, 'STOP': 1} | 0.23 / 0.50 / 0.47 / 0.57 / 0.63 / 0.67 |
| code_404 / permanent / transient | 30 | 0.99 | 3.08 | 179/180 | 29/30 | {'SITE_ONLY': 30} | 0.93 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| original / neutral / transient | 30 | 1.00 | 3.09 | 180/180 | 29/30 | {'SITE_ONLY': 30} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| not_completed / neutral / transient | 30 | 1.00 | 3.14 | 180/180 | 29/30 | {'SITE_ONLY': 26, 'RETRY': 4} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.00025303643724696357; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 180}
- cost: {'runs_recorded': 180, 'from_cache': 0, 'agent_calls': 3952, 'equiv_usd': 0.198}
