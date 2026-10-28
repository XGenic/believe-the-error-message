# C4 kill test verdict: CONTINUE_CREDULOUS

**LIVE MODEL RUN (study W2-C: the C4 grid, claude-haiku-5-5, native tool use, thinking on)**: transport `anthropic_messages_native`, model `claude-haiku-5-5`; 30 runs per cell.

- S +0.606 (CI +0.572, +0.633); L* +0.041 (CI -0.027, +0.111)

## Steering (request 1): follow rate of the claim's strategy minus the neutral baseline

| Misleading cell (claim, true fault) | Δ |
|---|---|
| format|transient | 1.000 |
| format|permanent | 1.000 |
| transient|fixable | 0.767 |
| transient|permanent | 0.867 |
| permanent|fixable | 0.000 |
| permanent|transient | 0.000 |

- **S** = 0.606 [0.572, 0.633]

## Learning: follow rate on requests 1–2 minus requests 5–6

| Cell | Kind | L |
|---|---|---|
| format|transient | misleading | 0.050 |
| format|permanent | misleading | 0.233 |
| transient|fixable | misleading | 0.017 |
| transient|permanent | misleading | 0.017 |
| permanent|fixable | misleading | -0.350 |
| permanent|transient | misleading | -0.367 |
| format|fixable | accurate | 0.023 |
| transient|transient | accurate | 0.017 |
| permanent|permanent | accurate | -0.433 |

- format|transient is excluded from L\*: obeying the format claim succeeds there (any third call does), so outcomes never contradict it.

- **L\*** = mean misleading L (five cells) − mean accurate L = 0.041 [-0.027, 0.111]

## Per cell (secondary)

| Cell | Runs | First response, request 1 | First response, requests 5–6 | Success by request | Calls, requests 5–6 | UNKNOWN | Unsupported |
|---|---|---|---|---|---|---|---|
| format|fixable | 30 | {'REFORMAT': 30} | {'REFORMAT': 43, 'SITE_ONLY': 1} | 0.63 / 0.67 / 0.80 / 0.80 / 0.87 / 0.90 | 2.167 | 0.222 | 0 |
| format|transient | 30 | {'REFORMAT': 30} | {'REFORMAT': 57, 'SITE_ONLY': 3} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3 | 0.000 | 0 |
| format|permanent | 30 | {'REFORMAT': 30} | {'REFORMAT': 46, 'SITE_ONLY': 3, 'OTHER': 2, 'STOP': 9} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 2.550 | 1.000 | 0 |
| transient|fixable | 30 | {'RETRY': 30} | {'RETRY': 58, 'SITE_ONLY': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 3.100 | 1.000 | 0 |
| transient|transient | 30 | {'RETRY': 28, 'SITE_ONLY': 2} | {'RETRY': 57, 'OTHER': 1, 'SITE_ONLY': 2} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3 | 0.000 | 0 |
| transient|permanent | 30 | {'RETRY': 30} | {'RETRY': 59, 'OTHER': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 3.267 | 1.000 | 0 |
| permanent|fixable | 30 | {'RETRY': 21, 'SITE_ONLY': 9} | {'RETRY': 12, 'SITE_ONLY': 5, 'STOP': 43} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.283 | 1.000 | 0 |
| permanent|transient | 30 | {'RETRY': 23, 'SITE_ONLY': 7} | {'RETRY': 12, 'STOP': 42, 'SITE_ONLY': 6} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.300 | 1.000 | 0 |
| permanent|permanent | 30 | {'RETRY': 19, 'SITE_ONLY': 11} | {'STOP': 44, 'SITE_ONLY': 8, 'RETRY': 8} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.267 | 1.000 | 0 |
| neutral|fixable | 30 | {'SITE_ONLY': 23, 'RETRY': 7} | {'SITE_ONLY': 34, 'RETRY': 8, 'REFORMAT': 2, 'STOP': 13} | 0.13 / 0.00 / 0.00 / 0.03 / 0.07 / 0.03 | 1.883 | 0.956 | 0 |
| neutral|transient | 30 | {'RETRY': 4, 'SITE_ONLY': 26} | {'RETRY': 2, 'REFORMAT': 14, 'SITE_ONLY': 38, 'STOP': 6} | 0.47 / 0.47 / 0.47 / 0.47 / 0.47 / 0.47 | 2.367 | 0.533 | 0 |
| neutral|permanent | 30 | {'SITE_ONLY': 26, 'RETRY': 4} | {'SITE_ONLY': 39, 'STOP': 18, 'OTHER': 1, 'REFORMAT': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.700 | 1.000 | 0 |

## H3 (stability → expectancy): calls on requests 5–6, 'unavailable' minus 'temporary' claim

- true fault fixable: -1.817 (1.283 vs 3.100)
- true fault transient: -1.700 (1.300 vs 3)
- true fault permanent: -2.000 (1.267 vs 3.267)

## Superstition probe (format claim over a transient fault)

- requests 2–6 whose first call already changes the SKU spelling: format claim 0.480, neutral message 0.227; index 0.253

## H4 (talked out of a fixable fault): success by request in permanent|fixable: 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00

## Validity

- completion (min over cells) 1.000; protocol failures 0.000; tool use on request 1 (min over cells) 1.000; unclassifiable responses 0.000
- run statuses: {'complete': 360}
- cost: {'runs_recorded': 360, 'from_cache': 0, 'agent_calls': 7261, 'equiv_usd': 0.5519}
