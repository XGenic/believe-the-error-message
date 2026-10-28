# C4 study W6 verdict: VALID

**LIVE MODEL RUN (study W6: wordings of the bounded caution, gpt-6-luna, reasoning {"effort": "low"})**: transport `openai_responses_native`, model `gpt-6-luna`; 6 requests per run, 30 runs per cell.

## Primary: each wording of the stopping rule

The floor that keeps the give-up rescue is 3 calls on a true outage: the transient fault clears on the third.

| Wording | Verdict | Give-up rescue (vs control) | Outage calls | True-'temporary' success (vs control) | E3's verdict |
|---|---|---|---|---|---|
| caution_bounded | **RESCUE_COSTLY** | +0.933 [+0.872, +0.983] | 4.94 [4.69, 5.18] | -0.028 [-0.100, +0.011] | RESCUE_ONLY |
| caution_few | **RESCUE_COSTLY** | +1.000 [+1.000, +1.000] | 5.18 [4.91, 5.44] | +0.006 [+0.000, +0.017] | RESCUE_ONLY |
| caution_three | **RECOMMENDABLE** | +1.000 [+1.000, +1.000] | 3.01 [3.00, 3.02] | +0.000 [-0.017, +0.017] | COST_AWARE |

## Secondary: each new wording minus `caution_bounded`

| Wording | Give-up trap | True 'temporary' | Retry trap |
|---|---|---|---|
| caution_few | SAME +0.067 [+0.017, +0.128] | SAME +0.033 [+0.000, +0.100] | DIFFERENT -0.233 [-0.300, -0.161] |
| caution_three | SAME +0.067 [+0.017, +0.128] | SAME +0.028 [-0.017, +0.100] | DIFFERENT -0.256 [-0.317, -0.194] |

## Reference and secondary (vs control)

| Arm | Give-up rescue | Outage calls | Outage calls vs plain caution | True-'temporary' success | Retry trap |
|---|---|---|---|---|---|
| caution | +0.983 [+0.956, +1.000] | 5.71 [5.44, 5.88] |  | +0.006 [+0.000, +0.017] | +0.067 [+0.011, +0.144] |
| caution_bounded | +0.933 [+0.872, +0.983] | 4.94 [4.69, 5.18] | -0.767 [-1.083, -0.417] | -0.028 [-0.100, +0.011] | +0.256 [+0.194, +0.317] |
| caution_few | +1.000 [+1.000, +1.000] | 5.18 [4.91, 5.44] | -0.528 [-0.850, -0.167] | +0.006 [+0.000, +0.017] | +0.022 [+0.000, +0.056] |
| caution_three | +1.000 [+1.000, +1.000] | 3.01 [3.00, 3.02] | -2.700 [-2.878, -2.439] | +0.000 [-0.017, +0.017] | +0.000 [+0.000, +0.000] |

## Descriptive: true 'temporary' requests in which every call differed from the earlier ones

- control: 0/180 requests, 0 of them failed
- caution: 45/180 requests, 0 of them failed
- caution_bounded: 154/180 requests, 6 of them failed
- caution_few: 6/180 requests, 0 of them failed
- caution_three: 0/180 requests, 0 of them failed

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| control / transient / fixable | 30 | 0.00 | 5.48 | 179/180 | 0/30 | {'RETRY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / transient / transient | 30 | 0.99 | 2.99 | 179/180 | 0/30 | {'RETRY': 30} | 0.97 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| control / permanent / transient | 30 | 0.00 | 1.01 | 0/180 | 0/30 | {'STOP': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / permanent / permanent | 30 | 0.00 | 1.07 | 3/180 | 1/30 | {'STOP': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / fixable | 30 | 0.07 | 5.61 | 174/180 | 4/30 | {'RETRY': 26, 'SITE_ONLY': 4} | 0.10 / 0.07 / 0.07 / 0.07 / 0.07 / 0.03 |
| caution / transient / transient | 30 | 1.00 | 3.07 | 180/180 | 8/30 | {'RETRY': 25, 'SITE_ONLY': 5} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution / permanent / transient | 30 | 0.98 | 3.14 | 177/180 | 24/30 | {'RETRY': 10, 'SITE_ONLY': 18, 'OTHER': 1, 'STOP': 1} | 0.93 / 0.97 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution / permanent / permanent | 30 | 0.00 | 5.71 | 172/180 | 21/30 | {'SITE_ONLY': 16, 'RETRY': 12, 'STOP': 1, 'OTHER': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_bounded / transient / fixable | 30 | 0.26 | 4.83 | 180/180 | 23/30 | {'SITE_ONLY': 19, 'RETRY': 8, 'OTHER': 3} | 0.37 / 0.40 / 0.17 / 0.23 / 0.17 / 0.20 |
| caution_bounded / transient / transient | 30 | 0.97 | 3.20 | 180/180 | 24/30 | {'SITE_ONLY': 20, 'OTHER': 3, 'RETRY': 7} | 0.97 / 0.97 / 0.97 / 0.97 / 0.97 / 0.97 |
| caution_bounded / permanent / transient | 30 | 0.93 | 3.26 | 179/180 | 26/30 | {'SITE_ONLY': 26, 'OTHER': 1, 'RETRY': 3} | 0.83 / 0.90 / 0.93 / 0.93 / 1.00 / 1.00 |
| caution_bounded / permanent / permanent | 30 | 0.00 | 4.94 | 178/180 | 28/30 | {'SITE_ONLY': 26, 'RETRY': 3, 'OTHER': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_few / transient / fixable | 30 | 0.02 | 5.12 | 180/180 | 2/30 | {'RETRY': 27, 'SITE_ONLY': 3} | 0.07 / 0.03 / 0.00 / 0.03 / 0.00 / 0.00 |
| caution_few / transient / transient | 30 | 1.00 | 3.03 | 180/180 | 1/30 | {'RETRY': 28, 'SITE_ONLY': 2} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_few / permanent / transient | 30 | 1.00 | 3.03 | 180/180 | 7/30 | {'RETRY': 26, 'SITE_ONLY': 4} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_few / permanent / permanent | 30 | 0.00 | 5.18 | 179/180 | 7/30 | {'RETRY': 24, 'SITE_ONLY': 6} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / fixable | 30 | 0.00 | 3.08 | 180/180 | 0/30 | {'RETRY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / transient | 30 | 0.99 | 3.00 | 180/180 | 0/30 | {'RETRY': 29, 'OTHER': 1} | 0.97 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_three / permanent / transient | 30 | 1.00 | 3.00 | 180/180 | 0/30 | {'RETRY': 30} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_three / permanent / permanent | 30 | 0.00 | 3.01 | 180/180 | 0/30 | {'RETRY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 600}
- cost: {'runs_recorded': 600, 'from_cache': 0, 'agent_calls': 16696, 'equiv_usd': 1.955}
