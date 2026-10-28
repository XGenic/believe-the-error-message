# C4 extension E3 verdict: VALID

**LIVE MODEL RUN (study W2-B: E3's bounded caution, qwen/qwen3.8-27b, DeepInfra, reasoning {"effort": "none"})**: transport `openrouter_chat_native`, model `qwen/qwen3.8-27b`; 6 requests per run, 30 runs per cell.

## Primary: does the stopping rule keep the rescue and cut the cost?

| Arm | Verdict | Give-up rescue (vs control) | Outage calls vs plain caution | True-'temporary' success (vs control) |
|---|---|---|---|---|
| caution_bounded | **RESCUE_ONLY** | +0.722 [+0.556, +0.867] | +0.172 [-0.433, +0.717] | +0.000 [+0.000, +0.000] |

## Calls per request on a true outage ('unavailable' over a permanent fault)

The lowest cost that keeps the give-up rescue is 3 calls: the transient fault clears on the third.

- control: 1.89
- caution: 2.64
- caution_bounded: 2.82
- caution_three: n/a

## Reference and secondary (vs control)

| Arm | Give-up rescue | Outage calls | True-'temporary' success | Retry trap |
|---|---|---|---|---|
| caution | +0.572 [+0.406, +0.739] | +0.750 [+0.228, +1.328] | +0.000 [+0.000, +0.000] | +0.144 [+0.067, +0.211] |
| caution_bounded | +0.722 [+0.556, +0.867] | +0.922 [+0.517, +1.339] | +0.000 [+0.000, +0.000] | +0.094 [+0.017, +0.172] |

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| control / transient / fixable | 30 | 0.04 | 5.08 | 175/180 | 5/30 | {'RETRY': 17, 'SITE_ONLY': 13} | 0.00 / 0.07 / 0.07 / 0.00 / 0.07 / 0.07 |
| control / transient / transient | 30 | 1.00 | 3.01 | 180/180 | 3/30 | {'RETRY': 17, 'SITE_ONLY': 13} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| control / permanent / transient | 30 | 0.00 | 1.67 | 0/180 | 0/30 | {'SITE_ONLY': 23, 'STOP': 7} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / permanent / permanent | 30 | 0.00 | 1.89 | 24/180 | 3/30 | {'SITE_ONLY': 22, 'STOP': 6, 'RETRY': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / fixable | 30 | 0.19 | 4.64 | 167/180 | 17/30 | {'SITE_ONLY': 18, 'RETRY': 12} | 0.20 / 0.13 / 0.20 / 0.13 / 0.27 / 0.20 |
| caution / transient / transient | 30 | 1.00 | 3.02 | 180/180 | 16/30 | {'SITE_ONLY': 17, 'RETRY': 13} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution / permanent / transient | 30 | 0.57 | 2.52 | 103/180 | 5/30 | {'SITE_ONLY': 28, 'STOP': 2} | 0.60 / 0.57 / 0.57 / 0.57 / 0.57 / 0.57 |
| caution / permanent / permanent | 30 | 0.00 | 2.64 | 71/180 | 9/30 | {'SITE_ONLY': 27, 'STOP': 3} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_bounded / transient / fixable | 30 | 0.14 | 3.80 | 162/180 | 17/30 | {'SITE_ONLY': 14, 'RETRY': 16} | 0.17 / 0.13 / 0.17 / 0.17 / 0.17 / 0.03 |
| caution_bounded / transient / transient | 30 | 1.00 | 3.00 | 180/180 | 13/30 | {'SITE_ONLY': 14, 'RETRY': 16} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_bounded / permanent / transient | 30 | 0.72 | 2.72 | 131/180 | 15/30 | {'SITE_ONLY': 30} | 0.70 / 0.70 / 0.73 / 0.73 / 0.73 / 0.73 |
| caution_bounded / permanent / permanent | 30 | 0.00 | 2.82 | 105/180 | 13/30 | {'SITE_ONLY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.00011383039271485487; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 360}
- cost: {'runs_recorded': 360, 'from_cache': 0, 'agent_calls': 8785, 'equiv_usd': 1.7627}
