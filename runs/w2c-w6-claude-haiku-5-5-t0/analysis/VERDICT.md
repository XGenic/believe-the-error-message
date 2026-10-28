# C4 study W6 verdict: VALID

**LIVE MODEL RUN (study W2-C: W6, the stopping-rule wordings, claude-haiku-5-5, native tool use, thinking off)**: transport `anthropic_messages_native`, model `claude-haiku-5-5`; 6 requests per run, 30 runs per cell.

## Primary: each wording of the stopping rule

The floor that keeps the give-up rescue is 3 calls on a true outage: the transient fault clears on the third.

| Wording | Verdict | Give-up rescue (vs control) | Outage calls | True-'temporary' success (vs control) | E3's verdict |
|---|---|---|---|---|---|
| caution_bounded | **WEAK_RESCUE** | +0.433 [+0.267, +0.600] | 1.48 [1.41, 1.57] | +0.700 [+0.533, +0.867] | NO_GAIN |
| caution_few | **WEAK_RESCUE** | +0.300 [+0.133, +0.467] | 1.41 [1.29, 1.57] | +0.700 [+0.533, +0.867] | NO_GAIN |
| caution_three | **RECOMMENDABLE** | +0.967 [+0.900, +1.000] | 2.53 [2.31, 2.74] | +0.700 [+0.533, +0.867] | RESCUE_ONLY |

## Secondary: each new wording minus `caution_bounded`

| Wording | Give-up trap | True 'temporary' | Retry trap |
|---|---|---|---|
| caution_few | UNCLEAR -0.133 [-0.361, +0.100] | SAME +0.000 [+0.000, +0.000] | SAME -0.011 [-0.033, +0.000] |
| caution_three | DIFFERENT +0.533 [+0.339, +0.700] | SAME +0.000 [+0.000, +0.000] | SAME -0.011 [-0.033, +0.000] |

## Reference and secondary (vs control)

| Arm | Give-up rescue | Outage calls | Outage calls vs plain caution | True-'temporary' success | Retry trap |
|---|---|---|---|---|---|
| caution | +0.000 [+0.000, +0.000] | 1.48 [1.36, 1.62] |  | +0.600 [+0.400, +0.800] | +0.000 [+0.000, +0.000] |
| caution_bounded | +0.433 [+0.267, +0.600] | 1.48 [1.41, 1.57] | +0.000 [-0.167, +0.161] | +0.700 [+0.533, +0.867] | +0.011 [+0.000, +0.033] |
| caution_few | +0.300 [+0.133, +0.467] | 1.41 [1.29, 1.57] | -0.072 [-0.256, +0.133] | +0.700 [+0.533, +0.867] | +0.000 [+0.000, +0.000] |
| caution_three | +0.967 [+0.900, +1.000] | 2.53 [2.31, 2.74] | +1.050 [+0.778, +1.306] | +0.700 [+0.533, +0.867] | +0.000 [+0.000, +0.000] |

## Descriptive: true 'temporary' requests in which every call differed from the earlier ones

- control: 1/180 requests, 1 of them failed
- caution: 5/180 requests, 0 of them failed
- caution_bounded: 6/180 requests, 0 of them failed
- caution_few: 0/180 requests, 0 of them failed
- caution_three: 0/180 requests, 0 of them failed

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| control / transient / fixable | 30 | 0.00 | 1.64 | 36/180 | 0/30 | {'RETRY': 29, 'SITE_ONLY': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / transient / transient | 30 | 0.30 | 1.86 | 54/180 | 0/30 | {'RETRY': 29, 'SITE_ONLY': 1} | 0.30 / 0.30 / 0.30 / 0.30 / 0.30 / 0.30 |
| control / permanent / transient | 30 | 0.00 | 1.01 | 0/180 | 0/30 | {'STOP': 29, 'RETRY': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / permanent / permanent | 30 | 0.00 | 1.00 | 0/180 | 0/30 | {'STOP': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / fixable | 30 | 0.00 | 2.44 | 112/180 | 0/30 | {'RETRY': 26, 'SITE_ONLY': 4} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / transient | 30 | 0.90 | 2.87 | 162/180 | 1/30 | {'RETRY': 28, 'SITE_ONLY': 2} | 0.90 / 0.90 / 0.90 / 0.90 / 0.90 / 0.90 |
| caution / permanent / transient | 30 | 0.00 | 1.42 | 0/180 | 0/30 | {'RETRY': 24, 'SITE_ONLY': 6} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / permanent / permanent | 30 | 0.00 | 1.48 | 0/180 | 0/30 | {'RETRY': 27, 'SITE_ONLY': 2, 'STOP': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_bounded / transient / fixable | 30 | 0.01 | 2.09 | 67/180 | 1/30 | {'SITE_ONLY': 10, 'RETRY': 20} | 0.03 / 0.03 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_bounded / transient / transient | 30 | 1.00 | 3.00 | 180/180 | 1/30 | {'RETRY': 19, 'SITE_ONLY': 11} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_bounded / permanent / transient | 30 | 0.43 | 2.06 | 78/180 | 4/30 | {'SITE_ONLY': 21, 'RETRY': 9} | 0.47 / 0.40 / 0.43 / 0.43 / 0.43 / 0.43 |
| caution_bounded / permanent / permanent | 30 | 0.00 | 1.48 | 16/180 | 3/30 | {'SITE_ONLY': 20, 'RETRY': 10} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_few / transient / fixable | 30 | 0.00 | 2.47 | 115/180 | 0/30 | {'RETRY': 29, 'SITE_ONLY': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_few / transient / transient | 30 | 1.00 | 3.00 | 180/180 | 0/30 | {'RETRY': 30} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_few / permanent / transient | 30 | 0.30 | 1.77 | 54/180 | 0/30 | {'RETRY': 28, 'SITE_ONLY': 2} | 0.30 / 0.30 / 0.30 / 0.30 / 0.30 / 0.30 |
| caution_few / permanent / permanent | 30 | 0.00 | 1.41 | 17/180 | 0/30 | {'SITE_ONLY': 5, 'RETRY': 25} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / fixable | 30 | 0.00 | 2.73 | 156/180 | 0/30 | {'RETRY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / transient | 30 | 1.00 | 3.00 | 180/180 | 0/30 | {'RETRY': 30} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_three / permanent / transient | 30 | 0.97 | 2.93 | 174/180 | 0/30 | {'RETRY': 29, 'STOP': 1} | 0.97 / 0.97 / 0.97 / 0.97 / 0.97 / 0.97 |
| caution_three / permanent / permanent | 30 | 0.00 | 2.53 | 138/180 | 0/30 | {'RETRY': 28, 'SITE_ONLY': 1, 'STOP': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 600}
- cost: {'runs_recorded': 600, 'from_cache': 0, 'agent_calls': 11199, 'equiv_usd': 0.6476}
