# C4 extension E3 verdict: VALID

**LIVE MODEL RUN (extension E3)**: transport `openai_responses`, model `gpt-6-luna`; 6 requests per run, 30 runs per cell.

## Primary: does the stopping rule keep the rescue and cut the cost?

| Arm | Verdict | Give-up rescue (vs control) | Outage calls vs plain caution | True-'temporary' success (vs control) |
|---|---|---|---|---|
| caution_bounded | **COST_AWARE** | +0.917 [+0.833, +0.972] | -2.167 [-2.506, -1.761] | -0.033 [-0.083, +0.000] |
| caution_three | **COST_AWARE** | +0.967 [+0.944, +0.989] | -2.233 [-2.544, -1.856] | -0.039 [-0.067, -0.017] |

## Calls per request on a true outage ('unavailable' over a permanent fault)

The lowest cost that keeps the give-up rescue is 3 calls: the transient fault clears on the third.

- control: 1.00
- caution: 5.24
- caution_bounded: 3.08
- caution_three: 3.01

## Reference and secondary (vs control)

| Arm | Give-up rescue | Outage calls | True-'temporary' success | Retry trap |
|---|---|---|---|---|
| caution | +0.978 [+0.956, +0.994] | +4.244 [+3.861, +4.567] | +0.000 [+0.000, +0.000] | +0.022 [+0.000, +0.056] |
| caution_bounded | +0.917 [+0.833, +0.972] | +2.078 [+1.978, +2.194] | -0.033 [-0.083, +0.000] | +0.289 [+0.244, +0.333] |
| caution_three | +0.967 [+0.944, +0.989] | +2.011 [+1.983, +2.039] | -0.039 [-0.067, -0.017] | +0.000 [+0.000, +0.000] |

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| control / transient / fixable | 30 | 0.00 | 5.84 | 179/180 | 0/30 | {'RETRY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / transient / transient | 30 | 1.00 | 3.00 | 180/180 | 0/30 | {'RETRY': 30} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| control / permanent / transient | 30 | 0.00 | 1.01 | 0/180 | 0/30 | {'STOP': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / permanent / permanent | 30 | 0.00 | 1.00 | 0/180 | 0/30 | {'STOP': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / fixable | 30 | 0.02 | 5.82 | 179/180 | 2/30 | {'RETRY': 30} | 0.00 / 0.00 / 0.07 / 0.00 / 0.03 / 0.03 |
| caution / transient / transient | 30 | 1.00 | 3.03 | 180/180 | 1/30 | {'RETRY': 30} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution / permanent / transient | 30 | 0.98 | 2.98 | 176/180 | 25/30 | {'SITE_ONLY': 16, 'RETRY': 11, 'STOP': 3} | 0.87 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution / permanent / permanent | 30 | 0.00 | 5.24 | 167/180 | 28/30 | {'SITE_ONLY': 17, 'RETRY': 11, 'STOP': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_bounded / transient / fixable | 30 | 0.29 | 3.41 | 175/180 | 28/30 | {'SITE_ONLY': 25, 'RETRY': 5} | 0.27 / 0.13 / 0.33 / 0.33 / 0.43 / 0.23 |
| caution_bounded / transient / transient | 30 | 0.97 | 3.00 | 178/180 | 30/30 | {'RETRY': 10, 'SITE_ONLY': 20} | 0.93 / 0.97 / 0.97 / 0.93 / 1.00 / 1.00 |
| caution_bounded / permanent / transient | 30 | 0.92 | 2.92 | 166/180 | 28/30 | {'SITE_ONLY': 30} | 0.77 / 0.87 / 0.97 / 0.97 / 0.97 / 0.97 |
| caution_bounded / permanent / permanent | 30 | 0.00 | 3.08 | 172/180 | 29/30 | {'SITE_ONLY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / fixable | 30 | 0.00 | 3.03 | 180/180 | 0/30 | {'RETRY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / transient | 30 | 0.96 | 2.97 | 173/180 | 0/30 | {'RETRY': 30} | 0.97 / 1.00 / 0.90 / 0.90 / 1.00 / 1.00 |
| caution_three / permanent / transient | 30 | 0.97 | 2.97 | 174/180 | 0/30 | {'RETRY': 29, 'UNCLASSIFIABLE': 1} | 0.93 / 1.00 / 0.93 / 0.97 / 0.97 / 1.00 |
| caution_three / permanent / permanent | 30 | 0.00 | 3.01 | 178/180 | 0/30 | {'RETRY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.011497025245216272; tool use on request 1 (min) 1.0; unclassifiable 0.00034722222222222224
- run statuses: {'complete': 480}
- cost: {'runs_recorded': 480, 'from_cache': 0, 'agent_calls': 12438, 'equiv_usd': 1.3078}
