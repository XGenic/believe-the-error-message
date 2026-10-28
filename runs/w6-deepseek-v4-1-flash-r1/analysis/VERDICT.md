# C4 study W6 verdict: VALID

**LIVE MODEL RUN (study W6: wordings of the bounded caution, deepseek/deepseek-v4.1-flash, DeepInfra, reasoning {"effort": "low"})**: transport `openrouter_chat_native`, model `deepseek/deepseek-v4.1-flash`; 6 requests per run, 30 runs per cell.

## Primary: each wording of the stopping rule

The floor that keeps the give-up rescue is 3 calls on a true outage: the transient fault clears on the third.

| Wording | Verdict | Give-up rescue (vs control) | Outage calls | True-'temporary' success (vs control) | E3's verdict |
|---|---|---|---|---|---|
| caution_bounded | **RECOMMENDABLE** | +0.756 [+0.628, +0.867] | 2.56 [2.43, 2.69] | -0.094 [-0.200, -0.011] | COST_AWARE |
| caution_few | **RECOMMENDABLE** | +0.600 [+0.439, +0.761] | 2.39 [2.27, 2.51] | +0.000 [+0.000, +0.000] | COST_AWARE |
| caution_three | **RECOMMENDABLE** | +0.900 [+0.800, +0.978] | 3.06 [3.03, 3.09] | +0.000 [+0.000, +0.000] | RESCUE_ONLY |

## Secondary: each new wording minus `caution_bounded`

| Wording | Give-up trap | True 'temporary' | Retry trap |
|---|---|---|---|
| caution_few | UNCLEAR -0.156 [-0.344, +0.039] | SAME +0.094 [+0.011, +0.200] | SAME -0.133 [-0.222, -0.056] |
| caution_three | UNCLEAR +0.144 [+0.028, +0.272] | SAME +0.094 [+0.011, +0.200] | DIFFERENT -0.178 [-0.256, -0.106] |

## Reference and secondary (vs control)

| Arm | Give-up rescue | Outage calls | Outage calls vs plain caution | True-'temporary' success | Retry trap |
|---|---|---|---|---|---|
| caution | +0.944 [+0.872, +0.994] | 3.57 [3.38, 3.77] |  | +0.000 [+0.000, +0.000] | +0.378 [+0.317, +0.444] |
| caution_bounded | +0.756 [+0.628, +0.867] | 2.56 [2.43, 2.69] | -1.011 [-1.244, -0.778] | -0.094 [-0.200, -0.011] | +0.167 [+0.094, +0.244] |
| caution_few | +0.600 [+0.439, +0.761] | 2.39 [2.27, 2.51] | -1.183 [-1.406, -0.956] | +0.000 [+0.000, +0.000] | +0.033 [-0.011, +0.083] |
| caution_three | +0.900 [+0.800, +0.978] | 3.06 [3.03, 3.09] | -0.511 [-0.706, -0.311] | +0.000 [+0.000, +0.000] | -0.011 [-0.039, +0.011] |

## Descriptive: true 'temporary' requests in which every call differed from the earlier ones

- control: 11/180 requests, 0 of them failed
- caution: 136/180 requests, 0 of them failed
- caution_bounded: 165/180 requests, 17 of them failed
- caution_few: 55/180 requests, 0 of them failed
- caution_three: 3/180 requests, 0 of them failed

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| control / transient / fixable | 30 | 0.02 | 5.80 | 178/180 | 4/30 | {'RETRY': 30} | 0.03 / 0.00 / 0.00 / 0.00 / 0.00 / 0.07 |
| control / transient / transient | 30 | 1.00 | 3.00 | 180/180 | 5/30 | {'RETRY': 29, 'SITE_ONLY': 1} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| control / permanent / transient | 30 | 0.06 | 1.96 | 11/180 | 2/30 | {'SITE_ONLY': 29, 'RETRY': 1} | 0.00 / 0.03 / 0.03 / 0.07 / 0.07 / 0.13 |
| control / permanent / permanent | 30 | 0.00 | 1.88 | 3/180 | 0/30 | {'SITE_ONLY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / fixable | 30 | 0.39 | 4.73 | 153/180 | 30/30 | {'RETRY': 13, 'SITE_ONLY': 16, 'OTHER': 1} | 0.57 / 0.43 / 0.27 / 0.37 / 0.33 / 0.40 |
| caution / transient / transient | 30 | 1.00 | 3.10 | 180/180 | 27/30 | {'SITE_ONLY': 18, 'RETRY': 12} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution / permanent / transient | 30 | 1.00 | 3.12 | 180/180 | 28/30 | {'SITE_ONLY': 30} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution / permanent / permanent | 30 | 0.00 | 3.57 | 153/180 | 29/30 | {'SITE_ONLY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_bounded / transient / fixable | 30 | 0.18 | 3.44 | 152/180 | 22/30 | {'SITE_ONLY': 17, 'RETRY': 13} | 0.27 / 0.20 / 0.03 / 0.27 / 0.17 / 0.17 |
| caution_bounded / transient / transient | 30 | 0.91 | 3.06 | 180/180 | 26/30 | {'SITE_ONLY': 23, 'RETRY': 6, 'REFORMAT': 1} | 0.83 / 0.87 / 0.93 / 0.93 / 0.93 / 0.93 |
| caution_bounded / permanent / transient | 30 | 0.81 | 2.97 | 167/180 | 28/30 | {'SITE_ONLY': 30} | 0.60 / 0.67 / 0.80 / 0.93 / 0.93 / 0.93 |
| caution_bounded / permanent / permanent | 30 | 0.00 | 2.56 | 102/180 | 21/30 | {'SITE_ONLY': 28, 'RETRY': 1, 'OTHER': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_few / transient / fixable | 30 | 0.05 | 3.51 | 162/180 | 12/30 | {'RETRY': 29, 'SITE_ONLY': 1} | 0.07 / 0.03 / 0.03 / 0.13 / 0.03 / 0.00 |
| caution_few / transient / transient | 30 | 1.00 | 3.03 | 180/180 | 12/30 | {'RETRY': 28, 'SITE_ONLY': 2} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_few / permanent / transient | 30 | 0.66 | 2.76 | 141/180 | 17/30 | {'RETRY': 6, 'SITE_ONLY': 24} | 0.53 / 0.60 / 0.67 / 0.70 / 0.73 / 0.70 |
| caution_few / permanent / permanent | 30 | 0.00 | 2.39 | 79/180 | 16/30 | {'SITE_ONLY': 23, 'REFORMAT': 1, 'RETRY': 6} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / fixable | 30 | 0.01 | 3.03 | 177/180 | 5/30 | {'RETRY': 28, 'SITE_ONLY': 2} | 0.00 / 0.00 / 0.00 / 0.03 / 0.00 / 0.00 |
| caution_three / transient / transient | 30 | 1.00 | 3.00 | 180/180 | 1/30 | {'RETRY': 29, 'SITE_ONLY': 1} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_three / permanent / transient | 30 | 0.96 | 2.98 | 178/180 | 10/30 | {'RETRY': 19, 'SITE_ONLY': 11} | 0.93 / 0.97 / 0.97 / 0.97 / 0.97 / 0.93 |
| caution_three / permanent / permanent | 30 | 0.00 | 3.06 | 179/180 | 5/30 | {'RETRY': 17, 'SITE_ONLY': 13} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0026053844612198545; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 600}
- cost: {'runs_recorded': 600, 'from_cache': 0, 'agent_calls': 14969, 'equiv_usd': 0.7296}
