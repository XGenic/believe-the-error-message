# C4 kill test verdict: INCONCLUSIVE

**LIVE MODEL RUN (study W2-A) (W2 open-weight panel: C4 through OpenRouter, Alibaba (Qwen), reasoning r1 = {"effort": "low"})**: transport `openrouter_chat_native`, model `qwen/qwen3.8-27b`; 30 runs per cell.

- S +0.783 (CI +0.722, +0.839); L* +0.126 (CI +0.062, +0.193)

## Steering (request 1): follow rate of the claim's strategy minus the neutral baseline

| Misleading cell (claim, true fault) | Δ |
|---|---|
| format|transient | 0.900 |
| format|permanent | 0.933 |
| transient|fixable | 0.833 |
| transient|permanent | 0.700 |
| permanent|fixable | 0.667 |
| permanent|transient | 0.667 |

- **S** = 0.783 [0.722, 0.839]

## Learning: follow rate on requests 1–2 minus requests 5–6

| Cell | Kind | L |
|---|---|---|
| format|transient | misleading | 0.033 |
| format|permanent | misleading | 0.233 |
| transient|fixable | misleading | 0.283 |
| transient|permanent | misleading | 0.167 |
| permanent|fixable | misleading | 0.000 |
| permanent|transient | misleading | 0.000 |
| format|fixable | accurate | -0.053 |
| transient|transient | accurate | 0.117 |
| permanent|permanent | accurate | -0.033 |

- format|transient is excluded from L\*: obeying the format claim succeeds there (any third call does), so outcomes never contradict it.

- **L\*** = mean misleading L (five cells) − mean accurate L = 0.126 [0.062, 0.193]

## Per cell (secondary)

| Cell | Runs | First response, request 1 | First response, requests 5–6 | Success by request | Calls, requests 5–6 | UNKNOWN | Unsupported |
|---|---|---|---|---|---|---|---|
| format|fixable | 30 | {'REFORMAT': 28, 'OTHER': 1, 'RETRY': 1} | {'REFORMAT': 33} | 0.90 / 0.93 / 0.87 / 0.87 / 1.00 / 0.97 | 2.117 | 0.078 | 0 |
| format|transient | 30 | {'REFORMAT': 27, 'OTHER': 2, 'SITE_ONLY': 1} | {'REFORMAT': 53, 'RETRY': 2, 'SITE_ONLY': 3, 'OTHER': 2} | 1.00 / 0.97 / 0.97 / 0.97 / 0.97 / 0.97 | 3.083 | 0.028 | 0 |
| format|permanent | 30 | {'REFORMAT': 28, 'OTHER': 1, 'SITE_ONLY': 1} | {'OTHER': 5, 'REFORMAT': 42, 'SITE_ONLY': 13} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 4.250 | 1.000 | 0 |
| transient|fixable | 30 | {'RETRY': 29, 'SITE_ONLY': 1} | {'RETRY': 36, 'SITE_ONLY': 19, 'STOP': 3, 'REFORMAT': 2} | 0.03 / 0.03 / 0.00 / 0.00 / 0.00 / 0.00 | 4.717 | 0.989 | 0 |
| transient|transient | 30 | {'RETRY': 29, 'SITE_ONLY': 1} | {'RETRY': 44, 'REFORMAT': 8, 'SITE_ONLY': 8} | 0.97 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3 | 0.006 | 0 |
| transient|permanent | 30 | {'RETRY': 28, 'SITE_ONLY': 2} | {'RETRY': 41, 'STOP': 4, 'SITE_ONLY': 15} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 4.550 | 1.000 | 0 |
| permanent|fixable | 30 | {'STOP': 24, 'SITE_ONLY': 5, 'RETRY': 1} | {'STOP': 49, 'REFORMAT': 2, 'SITE_ONLY': 9} | 0.00 / 0.00 / 0.03 / 0.03 / 0.00 / 0.00 | 1.217 | 0.989 | 0 |
| permanent|transient | 30 | {'SITE_ONLY': 7, 'STOP': 22, 'RETRY': 1} | {'SITE_ONLY': 12, 'REFORMAT': 2, 'STOP': 46} | 0.03 / 0.07 / 0.07 / 0.07 / 0.07 / 0.07 | 1.300 | 0.939 | 0 |
| permanent|permanent | 30 | {'SITE_ONLY': 5, 'STOP': 24, 'RETRY': 1} | {'SITE_ONLY': 9, 'STOP': 51} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.217 | 1.000 | 0 |
| neutral|fixable | 30 | {'STOP': 4, 'SITE_ONLY': 22, 'RETRY': 4} | {'STOP': 17, 'REFORMAT': 13, 'SITE_ONLY': 25, 'RETRY': 1} | 0.20 / 0.20 / 0.17 / 0.13 / 0.23 / 0.20 | 2.700 | 0.811 | 0 |
| neutral|transient | 30 | {'RETRY': 5, 'SITE_ONLY': 23, 'STOP': 2} | {'REFORMAT': 18, 'SITE_ONLY': 32, 'STOP': 9, 'RETRY': 1} | 0.63 / 0.77 / 0.77 / 0.77 / 0.77 / 0.77 | 2.633 | 0.256 | 0 |
| neutral|permanent | 30 | {'SITE_ONLY': 19, 'RETRY': 7, 'STOP': 4} | {'SITE_ONLY': 35, 'RETRY': 2, 'STOP': 23} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 2.017 | 1.000 | 0 |

## H3 (stability → expectancy): calls on requests 5–6, 'unavailable' minus 'temporary' claim

- true fault fixable: -3.500 (1.217 vs 4.717)
- true fault transient: -1.700 (1.300 vs 3)
- true fault permanent: -3.333 (1.217 vs 4.550)

## Superstition probe (format claim over a transient fault)

- requests 2–6 whose first call already changes the SKU spelling: format claim 0.633, neutral message 0.220; index 0.413

## H4 (talked out of a fixable fault): success by request in permanent|fixable: 0.00 / 0.00 / 0.03 / 0.03 / 0.00 / 0.00

## Validity

- completion (min over cells) 1.000; protocol failures 0.013; tool use on request 1 (min over cells) 1.000; unclassifiable responses 0.000
- run statuses: {'complete': 360}
- cost: {'runs_recorded': 360, 'from_cache': 0, 'agent_calls': 8729, 'equiv_usd': 2.3212}
