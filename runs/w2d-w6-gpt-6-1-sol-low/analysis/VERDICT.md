# C4 study W6 verdict: VALID

**LIVE MODEL RUN (study W2-D: W6, the stopping-rule wordings, gpt-6.1-sol, native tool calls, reasoning low)**: transport `openai_responses_native`, model `gpt-6.1-sol`; 6 requests per run, 30 runs per cell.

## Primary: each wording of the stopping rule

The floor that keeps the give-up rescue is 3 calls on a true outage: the transient fault clears on the third.

| Wording | Verdict | Give-up rescue (vs control) | Outage calls | True-'temporary' success (vs control) | E3's verdict |
|---|---|---|---|---|---|
| caution_bounded | **RECOMMENDABLE** | +1.000 [+1.000, +1.000] | 3.00 [3.00, 3.00] | +0.000 [+0.000, +0.000] | RESCUE_ONLY |
| caution_few | **RECOMMENDABLE** | +1.000 [+1.000, +1.000] | 3.00 [3.00, 3.00] | +0.000 [+0.000, +0.000] | RESCUE_ONLY |
| caution_three | **RECOMMENDABLE** | +1.000 [+1.000, +1.000] | 3.00 [3.00, 3.00] | +0.000 [+0.000, +0.000] | RESCUE_ONLY |

## Secondary: each new wording minus `caution_bounded`

| Wording | Give-up trap | True 'temporary' | Retry trap |
|---|---|---|---|
| caution_few | SAME +0.000 [+0.000, +0.000] | SAME +0.000 [+0.000, +0.000] | DIFFERENT -0.328 [-0.333, -0.317] |
| caution_three | SAME +0.000 [+0.000, +0.000] | SAME +0.000 [+0.000, +0.000] | DIFFERENT -0.328 [-0.333, -0.317] |

## Reference and secondary (vs control)

| Arm | Give-up rescue | Outage calls | Outage calls vs plain caution | True-'temporary' success | Retry trap |
|---|---|---|---|---|---|
| caution | +1.000 [+1.000, +1.000] | 3.74 [3.46, 4.09] |  | +0.000 [+0.000, +0.000] | +0.333 [+0.333, +0.333] |
| caution_bounded | +1.000 [+1.000, +1.000] | 3.00 [3.00, 3.00] | -0.744 [-1.094, -0.450] | +0.000 [+0.000, +0.000] | +0.328 [+0.317, +0.333] |
| caution_few | +1.000 [+1.000, +1.000] | 3.00 [3.00, 3.00] | -0.744 [-1.094, -0.450] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| caution_three | +1.000 [+1.000, +1.000] | 3.00 [3.00, 3.00] | -0.744 [-1.094, -0.450] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |

## Descriptive: true 'temporary' requests in which every call differed from the earlier ones

- control: 0/180 requests, 0 of them failed
- caution: 140/180 requests, 0 of them failed
- caution_bounded: 178/180 requests, 0 of them failed
- caution_few: 0/180 requests, 0 of them failed
- caution_three: 0/180 requests, 0 of them failed

## Per cell

| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | Runs ever reformatting | First response, request 1 | Success by request |
|---|---|---|---|---|---|---|---|
| control / transient / fixable | 30 | 0.00 | 6.00 | 180/180 | 0/30 | {'RETRY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / transient / transient | 30 | 1.00 | 3.00 | 180/180 | 0/30 | {'RETRY': 30} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| control / permanent / transient | 30 | 0.00 | 1.00 | 0/180 | 0/30 | {'STOP': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| control / permanent / permanent | 30 | 0.00 | 1.00 | 0/180 | 0/30 | {'STOP': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution / transient / fixable | 30 | 0.33 | 4.89 | 150/180 | 30/30 | {'RETRY': 30} | 0.57 / 0.47 / 0.20 / 0.33 / 0.20 / 0.23 |
| caution / transient / transient | 30 | 1.00 | 3.00 | 180/180 | 28/30 | {'RETRY': 30} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution / permanent / transient | 30 | 1.00 | 3.00 | 180/180 | 26/30 | {'SITE_ONLY': 29, 'RETRY': 1} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution / permanent / permanent | 30 | 0.00 | 3.74 | 172/180 | 30/30 | {'RETRY': 2, 'SITE_ONLY': 28} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_bounded / transient / fixable | 30 | 0.33 | 2.99 | 178/180 | 30/30 | {'SITE_ONLY': 28, 'RETRY': 2} | 0.53 / 0.47 / 0.20 / 0.33 / 0.20 / 0.23 |
| caution_bounded / transient / transient | 30 | 1.00 | 3.00 | 180/180 | 30/30 | {'SITE_ONLY': 28, 'RETRY': 2} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_bounded / permanent / transient | 30 | 1.00 | 3.00 | 180/180 | 30/30 | {'SITE_ONLY': 30} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_bounded / permanent / permanent | 30 | 0.00 | 3.00 | 180/180 | 30/30 | {'SITE_ONLY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_few / transient / fixable | 30 | 0.00 | 3.00 | 180/180 | 0/30 | {'RETRY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_few / transient / transient | 30 | 1.00 | 3.00 | 180/180 | 0/30 | {'RETRY': 30} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_few / permanent / transient | 30 | 1.00 | 3.00 | 180/180 | 0/30 | {'RETRY': 30} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_few / permanent / permanent | 30 | 0.00 | 3.00 | 180/180 | 0/30 | {'RETRY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / fixable | 30 | 0.00 | 3.00 | 180/180 | 0/30 | {'RETRY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |
| caution_three / transient / transient | 30 | 1.00 | 3.00 | 180/180 | 0/30 | {'RETRY': 30} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_three / permanent / transient | 30 | 1.00 | 3.00 | 180/180 | 0/30 | {'RETRY': 30} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| caution_three / permanent / permanent | 30 | 0.00 | 3.00 | 180/180 | 0/30 | {'RETRY': 30} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 600}
- cost: {'runs_recorded': 600, 'from_cache': 0, 'agent_calls': 14694, 'equiv_usd': 17.7325}
