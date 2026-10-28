# C4 kill test verdict: CONTINUE_CREDULOUS

**LIVE MODEL RUN (study W2-A) (W2 open-weight panel: C4 through OpenRouter, Alibaba (Qwen), reasoning r0 = {"effort": "none"})**: transport `openrouter_chat_native`, model `qwen/qwen3.8-27b`; 30 runs per cell.

- S +0.500 (CI +0.428, +0.572); L* +0.078 (CI -0.005, +0.152)

## Steering (request 1): follow rate of the claim's strategy minus the neutral baseline

| Misleading cell (claim, true fault) | Δ |
|---|---|
| format|transient | 0.767 |
| format|permanent | 0.733 |
| transient|fixable | 0.467 |
| transient|permanent | 0.533 |
| permanent|fixable | 0.133 |
| permanent|transient | 0.367 |

- **S** = 0.500 [0.428, 0.572]

## Learning: follow rate on requests 1–2 minus requests 5–6

| Cell | Kind | L |
|---|---|---|
| format|transient | misleading | -0.083 |
| format|permanent | misleading | -0.067 |
| transient|fixable | misleading | 0.133 |
| transient|permanent | misleading | 0.150 |
| permanent|fixable | misleading | -0.150 |
| permanent|transient | misleading | -0.033 |
| format|fixable | accurate | -0.080 |
| transient|transient | accurate | -0.017 |
| permanent|permanent | accurate | -0.117 |

- format|transient is excluded from L\*: obeying the format claim succeeds there (any third call does), so outcomes never contradict it.

- **L\*** = mean misleading L (five cells) − mean accurate L = 0.078 [-0.005, 0.152]

## Per cell (secondary)

| Cell | Runs | First response, request 1 | First response, requests 5–6 | Success by request | Calls, requests 5–6 | UNKNOWN | Unsupported |
|---|---|---|---|---|---|---|---|
| format|fixable | 30 | {'REFORMAT': 22, 'SITE_ONLY': 8} | {'REFORMAT': 49, 'SITE_ONLY': 4, 'OTHER': 1} | 0.73 / 0.70 / 0.70 / 0.83 / 0.67 / 0.83 | 3.250 | 0.256 | 0 |
| format|transient | 30 | {'SITE_ONLY': 6, 'REFORMAT': 23, 'STOP': 1} | {'REFORMAT': 53, 'SITE_ONLY': 7} | 0.93 / 0.97 / 0.97 / 1.00 / 1.00 / 1.00 | 3.067 | 0.056 | 0 |
| format|permanent | 30 | {'REFORMAT': 22, 'SITE_ONLY': 8} | {'REFORMAT': 47, 'SITE_ONLY': 13} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.050 | 1.000 | 0 |
| transient|fixable | 30 | {'SITE_ONLY': 10, 'RETRY': 20} | {'RETRY': 26, 'SITE_ONLY': 33, 'REFORMAT': 1} | 0.03 / 0.07 / 0.00 / 0.03 / 0.00 / 0.03 | 4.750 | 0.972 | 0 |
| transient|transient | 30 | {'RETRY': 20, 'SITE_ONLY': 10} | {'RETRY': 39, 'SITE_ONLY': 19, 'REFORMAT': 2} | 0.97 / 0.97 / 0.97 / 0.97 / 0.97 / 0.97 | 2.967 | 0.033 | 0 |
| transient|permanent | 30 | {'RETRY': 22, 'SITE_ONLY': 8} | {'SITE_ONLY': 32, 'RETRY': 28} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.083 | 1.000 | 0 |
| permanent|fixable | 30 | {'SITE_ONLY': 26, 'STOP': 4} | {'SITE_ONLY': 37, 'STOP': 23} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.617 | 1.000 | 0 |
| permanent|transient | 30 | {'SITE_ONLY': 18, 'STOP': 12} | {'SITE_ONLY': 31, 'STOP': 29} | 0.03 / 0.03 / 0.03 / 0.03 / 0.03 / 0.03 | 1.550 | 0.967 | 0 |
| permanent|permanent | 30 | {'STOP': 11, 'SITE_ONLY': 18, 'OTHER': 1} | {'STOP': 31, 'SITE_ONLY': 29} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.817 | 1.000 | 0 |
| neutral|fixable | 30 | {'SITE_ONLY': 24, 'RETRY': 6} | {'SITE_ONLY': 40, 'REFORMAT': 11, 'STOP': 2, 'RETRY': 4} | 0.17 / 0.20 / 0.10 / 0.13 / 0.17 / 0.17 | 3.450 | 0.850 | 0 |
| neutral|transient | 30 | {'SITE_ONLY': 26, 'STOP': 1, 'RETRY': 3} | {'SITE_ONLY': 35, 'REFORMAT': 15, 'STOP': 8, 'RETRY': 2} | 0.50 / 0.53 / 0.53 / 0.53 / 0.53 / 0.53 | 2.400 | 0.472 | 0 |
| neutral|permanent | 30 | {'SITE_ONLY': 23, 'RETRY': 6, 'STOP': 1} | {'SITE_ONLY': 48, 'RETRY': 6, 'STOP': 6} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 3.017 | 1.000 | 0 |

## H3 (stability → expectancy): calls on requests 5–6, 'unavailable' minus 'temporary' claim

- true fault fixable: -3.133 (1.617 vs 4.750)
- true fault transient: -1.417 (1.550 vs 2.967)
- true fault permanent: -3.267 (1.817 vs 5.083)

## Superstition probe (format claim over a transient fault)

- requests 2–6 whose first call already changes the SKU spelling: format claim 0.133, neutral message 0.113; index 0.020

## H4 (talked out of a fixable fault): success by request in permanent|fixable: 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00

## Validity

- completion (min over cells) 1.000; protocol failures 0.000; tool use on request 1 (min over cells) 1.000; unclassifiable responses 0.000
- run statuses: {'complete': 360}
- cost: {'runs_recorded': 360, 'from_cache': 0, 'agent_calls': 9087, 'equiv_usd': 1.7789}
