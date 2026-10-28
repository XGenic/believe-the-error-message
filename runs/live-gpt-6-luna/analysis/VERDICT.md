# C4 kill test verdict: CONTINUE_CREDULOUS

**LIVE MODEL RUN**: transport `openai_responses`, model `gpt-6-luna`; 30 runs per cell.

- S +0.956 (CI +0.922, +0.983); L* +0.000 (CI -0.019, +0.020)

## Steering (request 1): follow rate of the claim's strategy minus the neutral baseline

| Misleading cell (claim, true fault) | Δ |
|---|---|
| format|transient | 1.000 |
| format|permanent | 0.967 |
| transient|fixable | 1.000 |
| transient|permanent | 0.933 |
| permanent|fixable | 0.900 |
| permanent|transient | 0.933 |

- **S** = 0.956 [0.922, 0.983]

## Learning: follow rate on requests 1–2 minus requests 5–6

| Cell | Kind | L |
|---|---|---|
| format|transient | misleading | 0.000 |
| format|permanent | misleading | -0.017 |
| transient|fixable | misleading | -0.017 |
| transient|permanent | misleading | 0.017 |
| permanent|fixable | misleading | 0.017 |
| permanent|transient | misleading | 0.000 |
| format|fixable | accurate | -0.017 |
| transient|transient | accurate | 0.000 |
| permanent|permanent | accurate | 0.017 |

- format|transient is excluded from L\*: obeying the format claim succeeds there (any third call does), so outcomes never contradict it.

- **L\*** = mean misleading L (five cells) − mean accurate L = 0.000 [-0.019, 0.020]

## Per cell (secondary)

| Cell | Runs | First response, request 1 | First response, requests 5–6 | Success by request | Calls, requests 5–6 | UNKNOWN | Unsupported |
|---|---|---|---|---|---|---|---|
| format|fixable | 30 | {'REFORMAT': 29, 'STOP': 1} | {'REFORMAT': 58} | 0.87 / 0.97 / 0.97 / 1.00 / 0.93 / 1.00 | 3.150 | 0.044 | 0 |
| format|transient | 30 | {'REFORMAT': 30} | {'REFORMAT': 60} | 0.97 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3.017 | 0.006 | 0 |
| format|permanent | 30 | {'REFORMAT': 29, 'STOP': 1} | {'REFORMAT': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.883 | 1.000 | 0 |
| transient|fixable | 30 | {'RETRY': 30} | {'RETRY': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.700 | 1.000 | 0 |
| transient|transient | 30 | {'RETRY': 30} | {'RETRY': 60} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3 | 0.000 | 0 |
| transient|permanent | 30 | {'RETRY': 30} | {'RETRY': 59, 'STOP': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.600 | 1.000 | 0 |
| permanent|fixable | 30 | {'STOP': 30} | {'STOP': 59, 'SITE_ONLY': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.017 | 1.000 | 0 |
| permanent|transient | 30 | {'STOP': 30} | {'STOP': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1 | 1.000 | 0 |
| permanent|permanent | 30 | {'STOP': 30} | {'STOP': 59, 'RETRY': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.017 | 1.000 | 0 |
| neutral|fixable | 30 | {'SITE_ONLY': 27, 'STOP': 3} | {'SITE_ONLY': 29, 'STOP': 8, 'REFORMAT': 11, 'RETRY': 1} | 0.27 / 0.20 / 0.13 / 0.23 / 0.23 / 0.17 | 3.383 | 0.794 | 0 |
| neutral|transient | 30 | {'SITE_ONLY': 28, 'STOP': 2} | {'REFORMAT': 36, 'SITE_ONLY': 17, 'STOP': 7} | 0.43 / 0.63 / 0.70 / 0.73 / 0.73 / 0.80 | 2.683 | 0.328 | 0 |
| neutral|permanent | 30 | {'SITE_ONLY': 27, 'STOP': 1, 'RETRY': 2} | {'SITE_ONLY': 47, 'RETRY': 2, 'REFORMAT': 3, 'STOP': 7} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 4.383 | 1.000 | 0 |

## H3 (stability → expectancy): calls on requests 5–6, 'unavailable' minus 'temporary' claim

- true fault fixable: -4.683 (1.017 vs 5.700)
- true fault transient: -2 (1 vs 3)
- true fault permanent: -4.583 (1.017 vs 5.600)

## Superstition probe (format claim over a transient fault)

- requests 2–6 whose first call already changes the SKU spelling: format claim 0.040, neutral message 0.300; index -0.260

## H4 (talked out of a fixable fault): success by request in permanent|fixable: 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00

## Validity

- completion (min over cells) 1.000; protocol failures 0.013; tool use on request 1 (min over cells) 1.000; unclassifiable responses 0.000
- run statuses: {'complete': 360}
- cost: {'runs_recorded': 360, 'from_cache': 0, 'agent_calls': 9337, 'equiv_usd': 1.0421}
