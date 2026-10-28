# C4 extension E3 verdict: VALID

**LIVE MODEL RUN (study W2-B: E3's bounded caution, deepseek/deepseek-v4.1-flash, DeepInfra, reasoning {"effort": "none"})**: transport `openrouter_chat_native`, model `deepseek/deepseek-v4.1-flash`; 6 requests per run, 30 runs per cell.

## Primary: does the stopping rule keep the rescue and cut the cost?

| Arm | Verdict | Give-up rescue (vs control) | Outage calls vs plain caution | True-'temporary' success (vs control) |
|---|---|---|---|---|
| caution_bounded | **NO_GAIN** | +0.450 [+0.300, +0.589] | +0.878 [+0.700, +1.067] | -0.033 [-0.133, +0.061] |

## Calls per request on a true outage ('unavailable' over a permanent fault)

The lowest cost that keeps the give-up rescue is 3 calls: the transient fault clears on the third.

- control: 1.04
- caution: 1.69
- caution_bounded: 2.57
- caution_three: n/a

## Reference and secondary (vs control)

| Arm | Give-up rescue | Outage calls | True-'temporary' success | Retry trap |
|---|---|---|---|---|
| caution | +0.239 [+0.100, +0.400] | +0.644 [+0.494, +0.789] | +0.028 [-0.017, +0.100] | +0.194 [+0.128, +0.261] |
| caution_bounded | +0.450 [+0.300, +0.589] | +1.522 [+1.400, +1.656] | -0.033 [-0.133, +0.061] | +0.122 [+0.061, +0.189] |

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| control / transient / fixable | 30 | 0.00 | 5.53 | 177/180 | 0/30 | {'RETRY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / transient / transient | 30 | 0.97 | 2.93 | 174/180 | 0/30 | {'RETRY': 29, 'STOP': 1} | 0.97 / 0.97 / 0.97 / 0.97 / 0.97 / 0.97 |
| control / permanent / transient | 30 | 0.00 | 1.06 | 0/180 | 0/30 | {'STOP': 25, 'SITE_ONLY': 2, 'RETRY': 3} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / permanent / permanent | 30 | 0.00 | 1.04 | 0/180 | 0/30 | {'STOP': 24, 'SITE_ONLY': 4, 'RETRY': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / fixable | 30 | 0.19 | 4.57 | 159/180 | 18/30 | {'RETRY': 27, 'SITE_ONLY': 3} | 0.17 / 0.13 / 0.23 / 0.10 / 0.30 / 0.23 |
| caution / transient / transient | 30 | 0.99 | 3.02 | 180/180 | 14/30 | {'RETRY': 29, 'SITE_ONLY': 1} | 1.00 / 0.97 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution / permanent / transient | 30 | 0.24 | 1.89 | 43/180 | 8/30 | {'RETRY': 10, 'REFORMAT': 2, 'SITE_ONLY': 15, 'STOP': 3} | 0.27 / 0.23 / 0.23 / 0.23 / 0.23 / 0.23 |
| caution / permanent / permanent | 30 | 0.00 | 1.69 | 6/180 | 2/30 | {'SITE_ONLY': 19, 'RETRY': 7, 'STOP': 3, 'REFORMAT': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_bounded / transient / fixable | 30 | 0.12 | 3.17 | 160/180 | 16/30 | {'RETRY': 17, 'REFORMAT': 2, 'SITE_ONLY': 10, 'OTHER': 1} | 0.10 / 0.10 / 0.13 / 0.13 / 0.17 / 0.10 |
| caution_bounded / transient / transient | 30 | 0.93 | 2.98 | 172/180 | 22/30 | {'SITE_ONLY': 8, 'REFORMAT': 2, 'RETRY': 20} | 0.97 / 0.97 / 0.97 / 0.83 / 0.93 / 0.93 |
| caution_bounded / permanent / transient | 30 | 0.45 | 2.86 | 155/180 | 17/30 | {'SITE_ONLY': 24, 'RETRY': 4, 'OTHER': 2} | 0.50 / 0.47 / 0.43 / 0.43 / 0.50 / 0.37 |
| caution_bounded / permanent / permanent | 30 | 0.00 | 2.57 | 102/180 | 9/30 | {'OTHER': 2, 'SITE_ONLY': 23, 'REFORMAT': 3, 'RETRY': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.00851063829787234; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 360}
- cost: {'runs_recorded': 360, 'from_cache': 0, 'agent_calls': 8225, 'equiv_usd': 0.3112}
