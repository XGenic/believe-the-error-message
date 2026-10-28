# C4 extension E3 verdict: VALID

**LIVE MODEL RUN (study W2-B: E3's bounded caution, qwen/qwen3.8-27b, DeepInfra, reasoning {"effort": "low"})**: transport `openrouter_chat_native`, model `qwen/qwen3.8-27b`; 6 requests per run, 30 runs per cell.

## Primary: does the stopping rule keep the rescue and cut the cost?

| Arm | Verdict | Give-up rescue (vs control) | Outage calls vs plain caution | True-'temporary' success (vs control) |
|---|---|---|---|---|
| caution_bounded | **RESCUE_ONLY** | +0.561 [+0.383, +0.739] | -0.406 [-0.783, -0.039] | -0.006 [-0.017, +0.000] |

## Calls per request on a true outage ('unavailable' over a permanent fault)

The lowest cost that keeps the give-up rescue is 3 calls: the transient fault clears on the third.

- control: 1.21
- caution: 2.54
- caution_bounded: 2.13
- caution_three: n/a

## Reference and secondary (vs control)

| Arm | Give-up rescue | Outage calls | True-'temporary' success | Retry trap |
|---|---|---|---|---|
| caution | +0.567 [+0.406, +0.722] | +1.328 [+0.967, +1.711] | -0.006 [-0.017, +0.000] | +0.094 [+0.039, +0.156] |
| caution_bounded | +0.561 [+0.383, +0.739] | +0.922 [+0.744, +1.117] | -0.006 [-0.017, +0.000] | +0.067 [+0.011, +0.122] |

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| control / transient / fixable | 30 | 0.01 | 5.01 | 166/180 | 2/30 | {'RETRY': 29, 'SITE_ONLY': 1} | 0.00 / 0.00 / 0.00 / 0.03 / 0.03 / 0.00 |
| control / transient / transient | 30 | 1.00 | 3.02 | 180/180 | 3/30 | {'RETRY': 27, 'SITE_ONLY': 3} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| control / permanent / transient | 30 | 0.02 | 1.31 | 4/180 | 0/30 | {'STOP': 20, 'SITE_ONLY': 7, 'RETRY': 3} | 0.00 / 0.00 / 0.00 / 0.03 / 0.03 / 0.07 |
| control / permanent / permanent | 30 | 0.00 | 1.21 | 3/180 | 0/30 | {'STOP': 21, 'SITE_ONLY': 4, 'RETRY': 5} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / fixable | 30 | 0.11 | 4.74 | 158/180 | 12/30 | {'RETRY': 21, 'SITE_ONLY': 9} | 0.10 / 0.07 / 0.13 / 0.10 / 0.10 / 0.13 |
| caution / transient / transient | 30 | 0.99 | 2.99 | 179/180 | 15/30 | {'SITE_ONLY': 12, 'RETRY': 18} | 1.00 / 1.00 / 1.00 / 0.97 / 1.00 / 1.00 |
| caution / permanent / transient | 30 | 0.59 | 2.53 | 106/180 | 11/30 | {'RETRY': 3, 'SITE_ONLY': 23, 'STOP': 4} | 0.40 / 0.53 / 0.60 / 0.60 / 0.70 / 0.70 |
| caution / permanent / permanent | 30 | 0.00 | 2.54 | 65/180 | 8/30 | {'STOP': 6, 'SITE_ONLY': 21, 'RETRY': 3} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_bounded / transient / fixable | 30 | 0.08 | 2.58 | 104/180 | 13/30 | {'RETRY': 10, 'SITE_ONLY': 20} | 0.00 / 0.07 / 0.17 / 0.07 / 0.13 / 0.03 |
| caution_bounded / transient / transient | 30 | 0.99 | 2.99 | 179/180 | 21/30 | {'SITE_ONLY': 21, 'RETRY': 9} | 1.00 / 1.00 / 1.00 / 1.00 / 0.97 / 1.00 |
| caution_bounded / permanent / transient | 30 | 0.58 | 2.53 | 106/180 | 12/30 | {'SITE_ONLY': 30} | 0.50 / 0.60 / 0.60 / 0.57 / 0.60 / 0.63 |
| caution_bounded / permanent / permanent | 30 | 0.00 | 2.13 | 46/180 | 6/30 | {'SITE_ONLY': 28, 'RETRY': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.016063294174058978; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 360}
- cost: {'runs_recorded': 360, 'from_cache': 0, 'agent_calls': 8342, 'equiv_usd': 2.0904}
