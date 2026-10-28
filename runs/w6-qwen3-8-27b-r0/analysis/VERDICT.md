# C4 study W6 verdict: VALID

**LIVE MODEL RUN (study W6: wordings of the bounded caution, qwen/qwen3.8-27b, DeepInfra, reasoning {"effort": "none"})**: transport `openrouter_chat_native`, model `qwen/qwen3.8-27b`; 6 requests per run, 30 runs per cell.

## Primary: each wording of the stopping rule

The floor that keeps the give-up rescue is 3 calls on a true outage: the transient fault clears on the third.

| Wording | Verdict | Give-up rescue (vs control) | Outage calls | True-'temporary' success (vs control) | E3's verdict |
|---|---|---|---|---|---|
| caution_bounded | **WEAK_RESCUE** | +0.444 [+0.222, +0.667] | 2.73 [2.41, 3.12] | +0.033 [+0.000, +0.100] | NO_GAIN |
| caution_few | **RECOMMENDABLE** | +0.556 [+0.333, +0.756] | 2.79 [2.47, 3.15] | +0.033 [+0.000, +0.100] | RESCUE_ONLY |
| caution_three | **RECOMMENDABLE** | +0.761 [+0.600, +0.900] | 3.00 [3.00, 3.00] | +0.033 [+0.000, +0.100] | RESCUE_ONLY |

## Secondary: each new wording minus `caution_bounded`

| Wording | Give-up trap | True 'temporary' | Retry trap |
|---|---|---|---|
| caution_few | UNCLEAR +0.111 [-0.100, +0.322] | SAME +0.000 [+0.000, +0.000] | SAME -0.122 [-0.194, -0.039] |
| caution_three | DIFFERENT +0.317 [+0.161, +0.489] | SAME +0.000 [+0.000, +0.000] | DIFFERENT -0.239 [-0.289, -0.178] |

## Reference and secondary (vs control)

| Arm | Give-up rescue | Outage calls | Outage calls vs plain caution | True-'temporary' success | Retry trap |
|---|---|---|---|---|---|
| caution | +0.333 [+0.100, +0.567] | 3.07 [2.58, 3.59] |  | +0.033 [+0.000, +0.100] | +0.061 [-0.033, +0.150] |
| caution_bounded | +0.444 [+0.222, +0.667] | 2.73 [2.41, 3.12] | -0.339 [-0.967, +0.289] | +0.033 [+0.000, +0.100] | +0.150 [+0.072, +0.228] |
| caution_few | +0.556 [+0.333, +0.756] | 2.79 [2.47, 3.15] | -0.278 [-0.894, +0.344] | +0.033 [+0.000, +0.100] | +0.028 [-0.061, +0.111] |
| caution_three | +0.761 [+0.600, +0.900] | 3.00 [3.00, 3.00] | -0.072 [-0.594, +0.422] | +0.033 [+0.000, +0.100] | -0.089 [-0.156, -0.022] |

## Descriptive: true 'temporary' requests in which every call differed from the earlier ones

- control: 21/180 requests, 0 of them failed
- caution: 63/180 requests, 0 of them failed
- caution_bounded: 94/180 requests, 0 of them failed
- caution_few: 47/180 requests, 0 of them failed
- caution_three: 19/180 requests, 0 of them failed

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| control / transient / fixable | 30 | 0.11 | 4.92 | 167/180 | 9/30 | {'RETRY': 20, 'SITE_ONLY': 10} | 0.17 / 0.17 / 0.03 / 0.10 / 0.13 / 0.07 |
| control / transient / transient | 30 | 0.97 | 2.97 | 174/180 | 4/30 | {'SITE_ONLY': 11, 'RETRY': 19} | 0.97 / 0.97 / 0.97 / 0.97 / 0.97 / 0.97 |
| control / permanent / transient | 30 | 0.23 | 1.94 | 42/180 | 2/30 | {'SITE_ONLY': 22, 'RETRY': 3, 'STOP': 5} | 0.23 / 0.23 / 0.23 / 0.23 / 0.23 / 0.23 |
| control / permanent / permanent | 30 | 0.00 | 1.49 | 8/180 | 2/30 | {'STOP': 9, 'SITE_ONLY': 21} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / fixable | 30 | 0.17 | 4.99 | 172/180 | 17/30 | {'RETRY': 15, 'SITE_ONLY': 15} | 0.37 / 0.20 / 0.10 / 0.17 / 0.10 / 0.10 |
| caution / transient / transient | 30 | 1.00 | 3.00 | 180/180 | 11/30 | {'RETRY': 8, 'SITE_ONLY': 22} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution / permanent / transient | 30 | 0.57 | 2.55 | 102/180 | 12/30 | {'SITE_ONLY': 28, 'STOP': 1, 'RETRY': 1} | 0.57 / 0.57 / 0.57 / 0.57 / 0.57 / 0.57 |
| caution / permanent / permanent | 30 | 0.00 | 3.07 | 84/180 | 15/30 | {'SITE_ONLY': 27, 'STOP': 2, 'RETRY': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_bounded / transient / fixable | 30 | 0.26 | 4.26 | 172/180 | 25/30 | {'SITE_ONLY': 21, 'RETRY': 9} | 0.53 / 0.40 / 0.10 / 0.27 / 0.13 / 0.13 |
| caution_bounded / transient / transient | 30 | 1.00 | 3.02 | 180/180 | 18/30 | {'SITE_ONLY': 20, 'RETRY': 10} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_bounded / permanent / transient | 30 | 0.68 | 2.65 | 122/180 | 16/30 | {'SITE_ONLY': 30} | 0.67 / 0.70 / 0.67 / 0.67 / 0.67 / 0.70 |
| caution_bounded / permanent / permanent | 30 | 0.00 | 2.73 | 101/180 | 16/30 | {'SITE_ONLY': 29, 'STOP': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_few / transient / fixable | 30 | 0.14 | 4.62 | 172/180 | 13/30 | {'RETRY': 24, 'SITE_ONLY': 6} | 0.27 / 0.20 / 0.10 / 0.10 / 0.07 / 0.10 |
| caution_few / transient / transient | 30 | 1.00 | 3.01 | 180/180 | 10/30 | {'RETRY': 21, 'SITE_ONLY': 9} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_few / permanent / transient | 30 | 0.79 | 2.79 | 142/180 | 13/30 | {'SITE_ONLY': 29, 'RETRY': 1} | 0.77 / 0.77 / 0.80 / 0.80 / 0.80 / 0.80 |
| caution_few / permanent / permanent | 30 | 0.00 | 2.79 | 105/180 | 8/30 | {'SITE_ONLY': 29, 'RETRY': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / fixable | 30 | 0.02 | 3.27 | 180/180 | 4/30 | {'SITE_ONLY': 9, 'RETRY': 21} | 0.03 / 0.07 / 0.00 / 0.00 / 0.00 / 0.03 |
| caution_three / transient / transient | 30 | 1.00 | 3.01 | 180/180 | 4/30 | {'RETRY': 21, 'SITE_ONLY': 9} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_three / permanent / transient | 30 | 0.99 | 3.02 | 179/180 | 8/30 | {'SITE_ONLY': 26, 'RETRY': 4} | 0.97 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_three / permanent / permanent | 30 | 0.00 | 3.00 | 180/180 | 4/30 | {'SITE_ONLY': 22, 'RETRY': 8} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.00020054816498429038; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 600}
- cost: {'runs_recorded': 600, 'from_cache': 30, 'agent_calls': 14959, 'equiv_usd': 2.808}
