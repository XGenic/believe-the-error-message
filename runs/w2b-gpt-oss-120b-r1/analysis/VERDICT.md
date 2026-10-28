# C4 extension E3 verdict: VALID

**LIVE MODEL RUN (study W2-B: E3's bounded caution, openai/gpt-oss-120b, Crusoe, reasoning {"effort": "low"})**: transport `openrouter_chat_native`, model `openai/gpt-oss-120b`; 6 requests per run, 30 runs per cell.

## Primary: does the stopping rule keep the rescue and cut the cost?

| Arm | Verdict | Give-up rescue (vs control) | Outage calls vs plain caution | True-'temporary' success (vs control) |
|---|---|---|---|---|
| caution_bounded | **NO_GAIN** | +0.339 [+0.183, +0.494] | +0.061 [-0.067, +0.183] | +0.278 [+0.078, +0.478] |

## Calls per request on a true outage ('unavailable' over a permanent fault)

The lowest cost that keeps the give-up rescue is 3 calls: the transient fault clears on the third.

- control: 1.01
- caution: 1.21
- caution_bounded: 1.27
- caution_three: n/a

## Reference and secondary (vs control)

| Arm | Give-up rescue | Outage calls | True-'temporary' success | Retry trap |
|---|---|---|---|---|
| caution | +0.072 [-0.022, +0.178] | +0.200 [+0.083, +0.322] | +0.372 [+0.194, +0.550] | +0.028 [+0.000, +0.061] |
| caution_bounded | +0.339 [+0.183, +0.494] | +0.261 [+0.144, +0.372] | +0.278 [+0.078, +0.478] | +0.011 [+0.000, +0.033] |

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| control / transient / fixable | 30 | 0.00 | 1.18 | 19/180 | 0/30 | {'RETRY': 28, 'STOP': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / transient / transient | 30 | 0.57 | 2.21 | 102/180 | 9/30 | {'RETRY': 27, 'STOP': 2, 'OTHER': 1} | 0.53 / 0.60 / 0.53 / 0.60 / 0.57 / 0.57 |
| control / permanent / transient | 30 | 0.04 | 1.11 | 7/180 | 4/30 | {'STOP': 27, 'SITE_ONLY': 3} | 0.00 / 0.00 / 0.07 / 0.07 / 0.03 / 0.07 |
| control / permanent / permanent | 30 | 0.00 | 1.01 | 1/180 | 1/30 | {'STOP': 28, 'SITE_ONLY': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / fixable | 30 | 0.03 | 1.68 | 42/180 | 7/30 | {'RETRY': 27, 'SITE_ONLY': 3} | 0.07 / 0.03 / 0.03 / 0.03 / 0.00 / 0.00 |
| caution / transient / transient | 30 | 0.94 | 2.94 | 169/180 | 22/30 | {'RETRY': 28, 'SITE_ONLY': 2} | 0.97 / 0.90 / 0.90 / 0.93 / 0.97 / 0.97 |
| caution / permanent / transient | 30 | 0.11 | 1.40 | 20/180 | 6/30 | {'STOP': 14, 'RETRY': 9, 'SITE_ONLY': 7} | 0.10 / 0.07 / 0.10 / 0.17 / 0.13 / 0.10 |
| caution / permanent / permanent | 30 | 0.00 | 1.21 | 10/180 | 3/30 | {'SITE_ONLY': 4, 'RETRY': 14, 'STOP': 12} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_bounded / transient / fixable | 30 | 0.01 | 1.66 | 47/180 | 14/30 | {'RETRY': 23, 'OTHER': 4, 'SITE_ONLY': 3} | 0.03 / 0.00 / 0.00 / 0.03 / 0.00 / 0.00 |
| caution_bounded / transient / transient | 30 | 0.84 | 2.82 | 155/180 | 23/30 | {'RETRY': 23, 'OTHER': 4, 'SITE_ONLY': 3} | 0.80 / 0.83 / 0.87 / 0.87 / 0.83 / 0.87 |
| caution_bounded / permanent / transient | 30 | 0.38 | 1.94 | 69/180 | 14/30 | {'RETRY': 10, 'SITE_ONLY': 20} | 0.43 / 0.33 / 0.40 / 0.33 / 0.40 / 0.37 |
| caution_bounded / permanent / permanent | 30 | 0.00 | 1.27 | 16/180 | 5/30 | {'SITE_ONLY': 17, 'RETRY': 12, 'STOP': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.07654516640253566; tool use on request 1 (min) 1.0; unclassifiable 0.0020876826722338203
- run statuses: {'complete': 360, 'failed': 12}
- cost: {'runs_recorded': 372, 'from_cache': 0, 'agent_calls': 6428, 'equiv_usd': 0.3434}
