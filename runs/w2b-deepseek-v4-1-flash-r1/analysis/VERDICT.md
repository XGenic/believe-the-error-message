# C4 extension E3 verdict: VALID

**LIVE MODEL RUN (study W2-B: E3's bounded caution, deepseek/deepseek-v4.1-flash, DeepInfra, reasoning {"effort": "low"})**: transport `openrouter_chat_native`, model `deepseek/deepseek-v4.1-flash`; 6 requests per run, 30 runs per cell.

## Primary: does the stopping rule keep the rescue and cut the cost?

| Arm | Verdict | Give-up rescue (vs control) | Outage calls vs plain caution | True-'temporary' success (vs control) |
|---|---|---|---|---|
| caution_bounded | **HARMS_TRUE_TEMPORARY** | +0.594 [+0.417, +0.772] | -1.433 [-1.689, -1.178] | -0.167 [-0.289, -0.061] |

## Calls per request on a true outage ('unavailable' over a permanent fault)

The lowest cost that keeps the give-up rescue is 3 calls: the transient fault clears on the third.

- control: 1.93
- caution: 3.99
- caution_bounded: 2.56
- caution_three: n/a

## Reference and secondary (vs control)

| Arm | Give-up rescue | Outage calls | True-'temporary' success | Retry trap |
|---|---|---|---|---|
| caution | +0.911 [+0.822, +0.989] | +2.067 [+1.811, +2.328] | +0.000 [+0.000, +0.000] | +0.300 [+0.233, +0.367] |
| caution_bounded | +0.594 [+0.417, +0.772] | +0.633 [+0.528, +0.733] | -0.167 [-0.289, -0.061] | +0.106 [+0.022, +0.189] |

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| control / transient / fixable | 30 | 0.06 | 5.82 | 175/180 | 5/30 | {'RETRY': 28, 'SITE_ONLY': 2} | 0.07 / 0.00 / 0.03 / 0.13 / 0.03 / 0.07 |
| control / transient / transient | 30 | 1.00 | 3.00 | 180/180 | 4/30 | {'RETRY': 29, 'SITE_ONLY': 1} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| control / permanent / transient | 30 | 0.08 | 1.94 | 14/180 | 3/30 | {'SITE_ONLY': 28, 'STOP': 2} | 0.03 / 0.07 / 0.07 / 0.10 / 0.10 / 0.10 |
| control / permanent / permanent | 30 | 0.00 | 1.93 | 6/180 | 1/30 | {'SITE_ONLY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / fixable | 30 | 0.36 | 4.57 | 147/180 | 30/30 | {'RETRY': 14, 'SITE_ONLY': 16} | 0.33 / 0.30 / 0.40 / 0.43 / 0.47 / 0.20 |
| caution / transient / transient | 30 | 1.00 | 3.07 | 180/180 | 30/30 | {'RETRY': 17, 'SITE_ONLY': 12, 'OTHER': 1} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution / permanent / transient | 30 | 0.99 | 3.11 | 178/180 | 30/30 | {'SITE_ONLY': 30} | 0.97 / 0.97 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution / permanent / permanent | 30 | 0.00 | 3.99 | 159/180 | 29/30 | {'SITE_ONLY': 29, 'OTHER': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_bounded / transient / fixable | 30 | 0.16 | 3.24 | 150/180 | 21/30 | {'SITE_ONLY': 17, 'RETRY': 13} | 0.13 / 0.13 / 0.07 / 0.13 / 0.20 / 0.30 |
| caution_bounded / transient / transient | 30 | 0.83 | 3.06 | 173/180 | 26/30 | {'SITE_ONLY': 25, 'RETRY': 5} | 0.73 / 0.77 / 0.83 / 0.87 / 0.90 / 0.90 |
| caution_bounded / permanent / transient | 30 | 0.67 | 2.86 | 153/180 | 22/30 | {'SITE_ONLY': 30} | 0.60 / 0.60 / 0.63 / 0.70 / 0.73 / 0.77 |
| caution_bounded / permanent / permanent | 30 | 0.00 | 2.56 | 98/180 | 21/30 | {'SITE_ONLY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0062614703659721474; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 360}
- cost: {'runs_recorded': 360, 'from_cache': 0, 'agent_calls': 9263, 'equiv_usd': 0.4628}
