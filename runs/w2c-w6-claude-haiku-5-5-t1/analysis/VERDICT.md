# C4 study W6 verdict: VALID

**LIVE MODEL RUN (study W2-C: W6, the stopping-rule wordings, claude-haiku-5-5, native tool use, thinking on)**: transport `anthropic_messages_native`, model `claude-haiku-5-5`; 6 requests per run, 30 runs per cell.

## Primary: each wording of the stopping rule

The floor that keeps the give-up rescue is 3 calls on a true outage: the transient fault clears on the third.

| Wording | Verdict | Give-up rescue (vs control) | Outage calls | True-'temporary' success (vs control) | E3's verdict |
|---|---|---|---|---|---|
| caution_bounded | **RECOMMENDABLE** | +1.000 [+1.000, +1.000] | 1.93 [1.79, 2.08] | +0.000 [+0.000, +0.000] | RESCUE_ONLY |
| caution_few | **RECOMMENDABLE** | +1.000 [+1.000, +1.000] | 2.38 [2.22, 2.54] | +0.000 [+0.000, +0.000] | RESCUE_ONLY |
| caution_three | **RECOMMENDABLE** | +1.000 [+1.000, +1.000] | 2.82 [2.67, 2.94] | +0.000 [+0.000, +0.000] | RESCUE_ONLY |

## Secondary: each new wording minus `caution_bounded`

| Wording | Give-up trap | True 'temporary' | Retry trap |
|---|---|---|---|
| caution_few | SAME +0.000 [+0.000, +0.000] | SAME +0.000 [+0.000, +0.000] | DIFFERENT -0.167 [-0.222, -0.111] |
| caution_three | SAME +0.000 [+0.000, +0.000] | SAME +0.000 [+0.000, +0.000] | DIFFERENT -0.167 [-0.222, -0.111] |

## Reference and secondary (vs control)

| Arm | Give-up rescue | Outage calls | Outage calls vs plain caution | True-'temporary' success | Retry trap |
|---|---|---|---|---|---|
| caution | +0.906 [+0.800, +1.000] | 1.87 [1.75, 2.00] |  | +0.000 [+0.000, +0.000] | +0.044 [+0.011, +0.089] |
| caution_bounded | +1.000 [+1.000, +1.000] | 1.93 [1.79, 2.08] | +0.056 [-0.139, +0.250] | +0.000 [+0.000, +0.000] | +0.167 [+0.111, +0.222] |
| caution_few | +1.000 [+1.000, +1.000] | 2.38 [2.22, 2.54] | +0.506 [+0.300, +0.717] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| caution_three | +1.000 [+1.000, +1.000] | 2.82 [2.67, 2.94] | +0.944 [+0.750, +1.122] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |

## Descriptive: true 'temporary' requests in which every call differed from the earlier ones

- control: 0/180 requests, 0 of them failed
- caution: 0/180 requests, 0 of them failed
- caution_bounded: 35/180 requests, 0 of them failed
- caution_few: 0/180 requests, 0 of them failed
- caution_three: 0/180 requests, 0 of them failed

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| control / transient / fixable | 30 | 0.00 | 3.20 | 180/180 | 1/30 | {'RETRY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / transient / transient | 30 | 1.00 | 3.00 | 180/180 | 0/30 | {'RETRY': 30} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| control / permanent / transient | 30 | 0.00 | 1.49 | 0/180 | 0/30 | {'SITE_ONLY': 10, 'RETRY': 20} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / permanent / permanent | 30 | 0.00 | 1.58 | 0/180 | 0/30 | {'RETRY': 17, 'SITE_ONLY': 13} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / fixable | 30 | 0.04 | 3.81 | 164/180 | 5/30 | {'RETRY': 30} | 0.07 / 0.03 / 0.03 / 0.07 / 0.00 / 0.07 |
| caution / transient / transient | 30 | 1.00 | 3.00 | 180/180 | 0/30 | {'RETRY': 30} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution / permanent / transient | 30 | 0.91 | 2.89 | 163/180 | 11/30 | {'RETRY': 19, 'SITE_ONLY': 11} | 0.93 / 0.90 / 0.90 / 0.90 / 0.90 / 0.90 |
| caution / permanent / permanent | 30 | 0.00 | 1.87 | 29/180 | 7/30 | {'RETRY': 20, 'SITE_ONLY': 10} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_bounded / transient / fixable | 30 | 0.17 | 2.74 | 127/180 | 15/30 | {'RETRY': 25, 'SITE_ONLY': 5} | 0.30 / 0.23 / 0.03 / 0.20 / 0.10 / 0.13 |
| caution_bounded / transient / transient | 30 | 1.00 | 3.00 | 180/180 | 8/30 | {'RETRY': 24, 'SITE_ONLY': 6} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_bounded / permanent / transient | 30 | 1.00 | 3.00 | 180/180 | 18/30 | {'SITE_ONLY': 25, 'RETRY': 4, 'REFORMAT': 1} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_bounded / permanent / permanent | 30 | 0.00 | 1.93 | 61/180 | 19/30 | {'SITE_ONLY': 22, 'RETRY': 5, 'REFORMAT': 3} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_few / transient / fixable | 30 | 0.00 | 2.99 | 176/180 | 0/30 | {'RETRY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_few / transient / transient | 30 | 1.00 | 3.00 | 180/180 | 0/30 | {'RETRY': 29, 'SITE_ONLY': 1} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_few / permanent / transient | 30 | 1.00 | 3.00 | 180/180 | 0/30 | {'SITE_ONLY': 1, 'RETRY': 29} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_few / permanent / permanent | 30 | 0.00 | 2.38 | 104/180 | 1/30 | {'RETRY': 25, 'SITE_ONLY': 5} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / fixable | 30 | 0.00 | 3.01 | 180/180 | 0/30 | {'RETRY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / transient | 30 | 1.00 | 3.00 | 180/180 | 0/30 | {'RETRY': 30} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_three / permanent / transient | 30 | 1.00 | 3.00 | 180/180 | 0/30 | {'RETRY': 30} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_three / permanent / permanent | 30 | 0.00 | 2.82 | 165/180 | 0/30 | {'RETRY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 600, 'failed': 5}
- cost: {'runs_recorded': 605, 'from_cache': 0, 'agent_calls': 13513, 'equiv_usd': 0.9449}
