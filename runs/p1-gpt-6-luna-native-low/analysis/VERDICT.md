# C4 study P1 verdict: VALID

**LIVE MODEL RUN (study P1: rewordings of the error message, gpt-6-luna, native tool calls, reasoning low)**: transport `openai_responses_native`, model `gpt-6-luna`; 6 requests per run, 30 runs per cell. Every cell has the transient fault (the first two calls fail).

## Primary: does each rewording of "unavailable" lower success against the neutral message? **GENERALIZES**

| Wording | Text | Success | Effect vs "request rejected" | Minus the original wording | Effect vs the second neutral sentence |
|---|---|---|---|---|---|
| original | ERROR: stock data for this depot is unavailable. | 0.02 | -0.594 [-0.756, -0.406] DIFFERENT |  | -0.844 [-0.939, -0.722] DIFFERENT |
| on_record | ERROR: this depot has no stock data on record. | 0.00 | -0.611 [-0.767, -0.439] DIFFERENT | -0.017 [-0.050, +0.000] SAME | -0.861 [-0.956, -0.744] DIFFERENT |
| not_available | ERROR: stock information is not available for this depot. | 0.06 | -0.556 [-0.728, -0.361] DIFFERENT | +0.039 [-0.033, +0.133] SAME | -0.806 [-0.922, -0.667] DIFFERENT |
| code_404 | ERROR 404: no stock data found for this depot. | 0.03 | -0.583 [-0.750, -0.406] DIFFERENT | +0.011 [-0.039, +0.061] SAME | -0.833 [-0.933, -0.711] DIFFERENT |

## Neutral messages

| Wording | Text | Success |
|---|---|---|
| original | ERROR: request rejected. | 0.61 |
| not_completed | ERROR: the request could not be completed. | 0.86 |

- Second neutral sentence minus the first: +0.250 [+0.050, +0.444] DIFFERENT

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| original / permanent / transient | 30 | 0.02 | 1.04 | 3/180 | 1/30 | {'STOP': 30} | 0.00 / 0.00 / 0.00 / 0.03 / 0.03 / 0.03 |
| on_record / permanent / transient | 30 | 0.00 | 1.01 | 0/180 | 0/30 | {'STOP': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| not_available / permanent / transient | 30 | 0.06 | 1.18 | 10/180 | 2/30 | {'STOP': 26, 'SITE_ONLY': 4} | 0.03 / 0.03 / 0.07 / 0.07 / 0.07 / 0.07 |
| code_404 / permanent / transient | 30 | 0.03 | 1.06 | 5/180 | 2/30 | {'STOP': 30} | 0.00 / 0.00 / 0.00 / 0.03 / 0.07 / 0.07 |
| original / neutral / transient | 30 | 0.61 | 2.57 | 129/180 | 20/30 | {'SITE_ONLY': 23, 'STOP': 7} | 0.53 / 0.53 / 0.60 / 0.67 / 0.67 / 0.67 |
| not_completed / neutral / transient | 30 | 0.86 | 2.88 | 162/180 | 21/30 | {'SITE_ONLY': 15, 'RETRY': 9, 'STOP': 5, 'OTHER': 1} | 0.77 / 0.83 / 0.83 / 0.87 / 0.93 / 0.93 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 180}
- cost: {'runs_recorded': 180, 'from_cache': 0, 'agent_calls': 2833, 'equiv_usd': 0.2397}
