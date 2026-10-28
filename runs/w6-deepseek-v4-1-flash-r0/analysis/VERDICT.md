# C4 study W6 verdict: VALID

**LIVE MODEL RUN (study W6: wordings of the bounded caution, deepseek/deepseek-v4.1-flash, DeepInfra, reasoning {"effort": "none"})**: transport `openrouter_chat_native`, model `deepseek/deepseek-v4.1-flash`; 6 requests per run, 30 runs per cell.

## Primary: each wording of the stopping rule

The floor that keeps the give-up rescue is 3 calls on a true outage: the transient fault clears on the third.

| Wording | Verdict | Give-up rescue (vs control) | Outage calls | True-'temporary' success (vs control) | E3's verdict |
|---|---|---|---|---|---|
| caution_bounded | **RECOMMENDABLE** | +0.533 [+0.367, +0.700] | 2.49 [2.34, 2.63] | -0.028 [-0.078, +0.000] | RESCUE_ONLY |
| caution_few | **RECOMMENDABLE** | +0.850 [+0.717, +0.961] | 2.69 [2.56, 2.82] | +0.000 [+0.000, +0.000] | RESCUE_ONLY |
| caution_three | **RECOMMENDABLE** | +0.983 [+0.961, +1.000] | 2.98 [2.96, 3.00] | -0.033 [-0.100, +0.000] | RESCUE_ONLY |

## Secondary: each new wording minus `caution_bounded`

| Wording | Give-up trap | True 'temporary' | Retry trap |
|---|---|---|---|
| caution_few | DIFFERENT +0.317 [+0.117, +0.517] | SAME +0.028 [+0.000, +0.078] | SAME -0.106 [-0.161, -0.056] |
| caution_three | DIFFERENT +0.450 [+0.283, +0.611] | SAME -0.006 [-0.094, +0.067] | SAME -0.106 [-0.161, -0.056] |

## Reference and secondary (vs control)

| Arm | Give-up rescue | Outage calls | Outage calls vs plain caution | True-'temporary' success | Retry trap |
|---|---|---|---|---|---|
| caution | +0.178 [+0.067, +0.311] | 1.71 [1.53, 1.91] |  | +0.000 [+0.000, +0.000] | +0.194 [+0.122, +0.272] |
| caution_bounded | +0.533 [+0.367, +0.700] | 2.49 [2.34, 2.63] | +0.783 [+0.539, +1.017] | -0.028 [-0.078, +0.000] | +0.106 [+0.056, +0.161] |
| caution_few | +0.850 [+0.717, +0.961] | 2.69 [2.56, 2.82] | +0.983 [+0.750, +1.200] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| caution_three | +0.983 [+0.961, +1.000] | 2.98 [2.96, 3.00] | +1.278 [+1.078, +1.456] | -0.033 [-0.100, +0.000] | +0.000 [+0.000, +0.000] |

## Descriptive: true 'temporary' requests in which every call differed from the earlier ones

- control: 0/180 requests, 0 of them failed
- caution: 29/180 requests, 0 of them failed
- caution_bounded: 116/180 requests, 5 of them failed
- caution_few: 5/180 requests, 0 of them failed
- caution_three: 0/180 requests, 0 of them failed

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| control / transient / fixable | 30 | 0.00 | 5.34 | 180/180 | 1/30 | {'RETRY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / transient / transient | 30 | 1.00 | 3.00 | 180/180 | 2/30 | {'RETRY': 29, 'REFORMAT': 1} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| control / permanent / transient | 30 | 0.00 | 1.04 | 0/180 | 0/30 | {'STOP': 28, 'SITE_ONLY': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / permanent / permanent | 30 | 0.00 | 1.03 | 0/180 | 0/30 | {'STOP': 24, 'RETRY': 3, 'SITE_ONLY': 2, 'OTHER': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / fixable | 30 | 0.19 | 4.37 | 153/180 | 18/30 | {'RETRY': 24, 'STOP': 1, 'SITE_ONLY': 3, 'OTHER': 1, 'REFORMAT': 1} | 0.23 / 0.27 / 0.10 / 0.20 / 0.13 / 0.23 |
| caution / transient / transient | 30 | 1.00 | 3.00 | 180/180 | 9/30 | {'RETRY': 29, 'SITE_ONLY': 1} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution / permanent / transient | 30 | 0.18 | 1.88 | 35/180 | 5/30 | {'SITE_ONLY': 19, 'STOP': 2, 'RETRY': 8, 'OTHER': 1} | 0.20 / 0.20 / 0.17 / 0.17 / 0.17 / 0.17 |
| caution / permanent / permanent | 30 | 0.00 | 1.71 | 18/180 | 3/30 | {'SITE_ONLY': 13, 'STOP': 3, 'RETRY': 10, 'REFORMAT': 2, 'OTHER': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_bounded / transient / fixable | 30 | 0.11 | 3.26 | 169/180 | 15/30 | {'RETRY': 21, 'SITE_ONLY': 8, 'OTHER': 1} | 0.20 / 0.20 / 0.00 / 0.10 / 0.10 / 0.03 |
| caution_bounded / transient / transient | 30 | 0.97 | 3.01 | 178/180 | 25/30 | {'RETRY': 18, 'SITE_ONLY': 9, 'REFORMAT': 3} | 1.00 / 1.00 / 0.97 / 0.93 / 0.97 / 0.97 |
| caution_bounded / permanent / transient | 30 | 0.53 | 2.82 | 146/180 | 17/30 | {'SITE_ONLY': 21, 'RETRY': 7, 'REFORMAT': 2} | 0.60 / 0.53 / 0.40 / 0.53 / 0.57 / 0.57 |
| caution_bounded / permanent / permanent | 30 | 0.00 | 2.49 | 97/180 | 13/30 | {'SITE_ONLY': 24, 'REFORMAT': 2, 'RETRY': 3, 'OTHER': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_few / transient / fixable | 30 | 0.00 | 3.20 | 173/180 | 1/30 | {'RETRY': 28, 'SITE_ONLY': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_few / transient / transient | 30 | 1.00 | 3.00 | 180/180 | 1/30 | {'RETRY': 29, 'SITE_ONLY': 1} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_few / permanent / transient | 30 | 0.85 | 2.93 | 168/180 | 8/30 | {'SITE_ONLY': 10, 'RETRY': 20} | 0.87 / 0.87 / 0.80 / 0.87 / 0.87 / 0.83 |
| caution_few / permanent / permanent | 30 | 0.00 | 2.69 | 122/180 | 3/30 | {'RETRY': 20, 'SITE_ONLY': 10} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / fixable | 30 | 0.00 | 3.01 | 180/180 | 0/30 | {'RETRY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / transient | 30 | 0.97 | 3.01 | 180/180 | 0/30 | {'RETRY': 28, 'OTHER': 1, 'SITE_ONLY': 1} | 0.97 / 0.97 / 0.97 / 0.97 / 0.97 / 0.97 |
| caution_three / permanent / transient | 30 | 0.98 | 3.00 | 180/180 | 3/30 | {'RETRY': 26, 'SITE_ONLY': 4} | 0.90 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_three / permanent / permanent | 30 | 0.00 | 2.98 | 177/180 | 1/30 | {'RETRY': 26, 'SITE_ONLY': 4} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.003462204270051933; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 600}
- cost: {'runs_recorded': 600, 'from_cache': 0, 'agent_calls': 13864, 'equiv_usd': 0.5205}
