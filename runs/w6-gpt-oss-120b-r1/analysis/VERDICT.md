# C4 study W6 verdict: VALID

**LIVE MODEL RUN (study W6: wordings of the bounded caution, openai/gpt-oss-120b, Crusoe, reasoning {"effort": "low"})**: transport `openrouter_chat_native`, model `openai/gpt-oss-120b`; 6 requests per run, 30 runs per cell.

## Primary: each wording of the stopping rule

The floor that keeps the give-up rescue is 3 calls on a true outage: the transient fault clears on the third.

| Wording | Verdict | Give-up rescue (vs control) | Outage calls | True-'temporary' success (vs control) | E3's verdict |
|---|---|---|---|---|---|
| caution_bounded | **WEAK_RESCUE** | +0.200 [+0.011, +0.394] | 1.32 [1.23, 1.40] | +0.322 [+0.111, +0.528] | NO_GAIN |
| caution_few | **WEAK_RESCUE** | +0.189 [+0.006, +0.378] | 1.26 [1.17, 1.34] | +0.328 [+0.133, +0.522] | NO_GAIN |
| caution_three | **RECOMMENDABLE** | +0.689 [+0.561, +0.806] | 1.74 [1.59, 1.88] | +0.378 [+0.200, +0.567] | RESCUE_ONLY |

## Secondary: each new wording minus `caution_bounded`

| Wording | Give-up trap | True 'temporary' | Retry trap |
|---|---|---|---|
| caution_few | SAME -0.011 [-0.244, +0.222] | SAME +0.006 [-0.139, +0.156] | SAME -0.033 [-0.078, +0.000] |
| caution_three | DIFFERENT +0.489 [+0.300, +0.667] | SAME +0.056 [-0.061, +0.189] | SAME -0.033 [-0.078, +0.000] |

## Reference and secondary (vs control)

| Arm | Give-up rescue | Outage calls | Outage calls vs plain caution | True-'temporary' success | Retry trap |
|---|---|---|---|---|---|
| caution | -0.028 [-0.150, +0.094] | 1.21 [1.13, 1.29] |  | +0.322 [+0.122, +0.522] | +0.006 [+0.000, +0.017] |
| caution_bounded | +0.200 [+0.011, +0.394] | 1.32 [1.23, 1.40] | +0.111 [-0.006, +0.222] | +0.322 [+0.111, +0.528] | +0.033 [+0.000, +0.078] |
| caution_few | +0.189 [+0.006, +0.378] | 1.26 [1.17, 1.34] | +0.050 [-0.067, +0.172] | +0.328 [+0.133, +0.522] | +0.000 [+0.000, +0.000] |
| caution_three | +0.689 [+0.561, +0.806] | 1.74 [1.59, 1.88] | +0.533 [+0.378, +0.694] | +0.378 [+0.200, +0.567] | +0.000 [+0.000, +0.000] |

## Descriptive: true 'temporary' requests in which every call differed from the earlier ones

- control: 20/180 requests, 3 of them failed
- caution: 47/180 requests, 7 of them failed
- caution_bounded: 76/180 requests, 2 of them failed
- caution_few: 10/180 requests, 2 of them failed
- caution_three: 0/180 requests, 0 of them failed

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| control / transient / fixable | 30 | 0.00 | 1.11 | 16/180 | 2/30 | {'RETRY': 27, 'STOP': 3} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / transient / transient | 30 | 0.54 | 2.14 | 98/180 | 9/30 | {'RETRY': 29, 'STOP': 1} | 0.57 / 0.50 / 0.57 / 0.53 / 0.53 / 0.53 |
| control / permanent / transient | 30 | 0.12 | 1.26 | 21/180 | 5/30 | {'STOP': 25, 'SITE_ONLY': 4, 'REFORMAT': 1} | 0.03 / 0.07 / 0.10 / 0.13 / 0.17 / 0.20 |
| control / permanent / permanent | 30 | 0.00 | 0.98 | 4/180 | 3/30 | {'STOP': 26, 'SITE_ONLY': 3, 'RETRY': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / fixable | 30 | 0.01 | 1.64 | 44/180 | 3/30 | {'RETRY': 28, 'SITE_ONLY': 1, 'STOP': 1} | 0.03 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / transient | 30 | 0.86 | 2.81 | 155/180 | 20/30 | {'STOP': 3, 'SITE_ONLY': 5, 'RETRY': 22} | 0.80 / 0.87 / 0.87 / 0.87 / 0.90 / 0.87 |
| caution / permanent / transient | 30 | 0.09 | 1.31 | 16/180 | 4/30 | {'STOP': 16, 'RETRY': 9, 'SITE_ONLY': 5} | 0.03 / 0.07 / 0.10 / 0.13 / 0.07 / 0.13 |
| caution / permanent / permanent | 30 | 0.00 | 1.21 | 9/180 | 7/30 | {'RETRY': 9, 'SITE_ONLY': 9, 'STOP': 12} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_bounded / transient / fixable | 30 | 0.03 | 1.69 | 45/180 | 10/30 | {'RETRY': 24, 'SITE_ONLY': 4, 'OTHER': 2} | 0.07 / 0.03 / 0.03 / 0.03 / 0.03 / 0.00 |
| caution_bounded / transient / transient | 30 | 0.86 | 2.84 | 158/180 | 26/30 | {'OTHER': 1, 'RETRY': 28, 'SITE_ONLY': 1} | 0.87 / 0.87 / 0.87 / 0.83 / 0.87 / 0.87 |
| caution_bounded / permanent / transient | 30 | 0.32 | 1.80 | 57/180 | 12/30 | {'RETRY': 10, 'SITE_ONLY': 19, 'REFORMAT': 1} | 0.30 / 0.30 / 0.30 / 0.33 / 0.33 / 0.33 |
| caution_bounded / permanent / permanent | 30 | 0.00 | 1.32 | 14/180 | 9/30 | {'SITE_ONLY': 11, 'RETRY': 18, 'REFORMAT': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_few / transient / fixable | 30 | 0.00 | 1.55 | 41/180 | 6/30 | {'RETRY': 26, 'OTHER': 4} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_few / transient / transient | 30 | 0.87 | 2.87 | 161/180 | 18/30 | {'RETRY': 29, 'OTHER': 1} | 0.83 / 0.87 / 0.80 / 0.90 / 0.87 / 0.93 |
| caution_few / permanent / transient | 30 | 0.31 | 1.74 | 55/180 | 8/30 | {'SITE_ONLY': 8, 'RETRY': 22} | 0.30 / 0.30 / 0.30 / 0.30 / 0.30 / 0.33 |
| caution_few / permanent / permanent | 30 | 0.00 | 1.26 | 12/180 | 2/30 | {'RETRY': 24, 'SITE_ONLY': 6} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / fixable | 30 | 0.00 | 1.97 | 74/180 | 1/30 | {'RETRY': 29, 'OTHER': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / transient | 30 | 0.92 | 2.94 | 169/180 | 4/30 | {'OTHER': 2, 'RETRY': 28} | 0.90 / 0.87 / 0.97 / 0.93 / 0.90 / 0.93 |
| caution_three / permanent / transient | 30 | 0.81 | 2.80 | 146/180 | 6/30 | {'RETRY': 29, 'SITE_ONLY': 1} | 0.97 / 0.80 / 0.77 / 0.67 / 0.77 / 0.87 |
| caution_three / permanent / permanent | 30 | 0.00 | 1.74 | 53/180 | 3/30 | {'RETRY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.07261054344877475; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 600}
- cost: {'runs_recorded': 600, 'from_cache': 598, 'agent_calls': 11059, 'equiv_usd': 0.6099}
