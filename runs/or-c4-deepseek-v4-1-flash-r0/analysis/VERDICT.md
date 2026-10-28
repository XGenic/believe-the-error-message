# C4 kill test verdict: CONTINUE_CREDULOUS

**LIVE MODEL RUN (study W2-A) (W2 open-weight panel: C4 through OpenRouter, DeepSeek, reasoning r0 = {"effort": "none"})**: transport `openrouter_chat_native`, model `deepseek/deepseek-v4.1-flash`; 30 runs per cell.

- S +0.783 (CI +0.722, +0.839); L* +0.027 (CI -0.018, +0.071)

## Steering (request 1): follow rate of the claim's strategy minus the neutral baseline

| Misleading cell (claim, true fault) | Δ |
|---|---|
| format|transient | 0.533 |
| format|permanent | 0.700 |
| transient|fixable | 0.933 |
| transient|permanent | 0.967 |
| permanent|fixable | 0.800 |
| permanent|transient | 0.767 |

- **S** = 0.783 [0.722, 0.839]

## Learning: follow rate on requests 1–2 minus requests 5–6

| Cell | Kind | L |
|---|---|---|
| format|transient | misleading | 0.033 |
| format|permanent | misleading | 0.050 |
| transient|fixable | misleading | 0.000 |
| transient|permanent | misleading | 0.017 |
| permanent|fixable | misleading | -0.033 |
| permanent|transient | misleading | -0.083 |
| format|fixable | accurate | -0.027 |
| transient|transient | accurate | 0.000 |
| permanent|permanent | accurate | -0.083 |

- format|transient is excluded from L\*: obeying the format claim succeeds there (any third call does), so outcomes never contradict it.

- **L\*** = mean misleading L (five cells) − mean accurate L = 0.027 [-0.018, 0.071]

## Per cell (secondary)

| Cell | Runs | First response, request 1 | First response, requests 5–6 | Success by request | Calls, requests 5–6 | UNKNOWN | Unsupported |
|---|---|---|---|---|---|---|---|
| format|fixable | 30 | {'REFORMAT': 25, 'SITE_ONLY': 4, 'STOP': 1} | {'REFORMAT': 40, 'STOP': 2, 'SITE_ONLY': 2} | 0.93 / 0.67 / 0.63 / 0.73 / 0.87 / 0.83 | 2.400 | 0.222 | 0 |
| format|transient | 30 | {'STOP': 10, 'SITE_ONLY': 3, 'REFORMAT': 17} | {'STOP': 20, 'SITE_ONLY': 6, 'REFORMAT': 34} | 0.63 / 0.63 / 0.67 / 0.63 / 0.63 / 0.60 | 2.283 | 0.367 | 0 |
| format|permanent | 30 | {'STOP': 6, 'REFORMAT': 23, 'SITE_ONLY': 1} | {'STOP': 17, 'REFORMAT': 43} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 3.483 | 1.000 | 0 |
| transient|fixable | 30 | {'RETRY': 30} | {'RETRY': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.317 | 1.000 | 0 |
| transient|transient | 29 | {'RETRY': 29} | {'RETRY': 58} | 1.00 / 1.00 / 1.00 / 1.00 / 0.97 / 1.00 | 2.983 | 0.006 | 0 |
| transient|permanent | 29 | {'RETRY': 29} | {'RETRY': 57, 'STOP': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.224 | 1.000 | 0 |
| permanent|fixable | 30 | {'STOP': 28, 'SITE_ONLY': 1, 'RETRY': 1} | {'STOP': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1 | 1.000 | 0 |
| permanent|transient | 30 | {'STOP': 24, 'SITE_ONLY': 4, 'RETRY': 2} | {'STOP': 58, 'SITE_ONLY': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.033 | 1.000 | 0 |
| permanent|permanent | 30 | {'STOP': 25, 'SITE_ONLY': 2, 'RETRY': 3} | {'STOP': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1 | 1.000 | 0 |
| neutral|fixable | 30 | {'SITE_ONLY': 21, 'STOP': 4, 'RETRY': 2, 'OTHER': 2, 'REFORMAT': 1} | {'SITE_ONLY': 21, 'STOP': 27, 'RETRY': 4, 'OTHER': 4, 'REFORMAT': 3} | 0.00 / 0.07 / 0.00 / 0.03 / 0.07 / 0.00 | 1.650 | 0.972 | 0 |
| neutral|transient | 30 | {'SITE_ONLY': 19, 'STOP': 1, 'OTHER': 4, 'RETRY': 5, 'REFORMAT': 1} | {'STOP': 22, 'SITE_ONLY': 18, 'REFORMAT': 13, 'OTHER': 3, 'RETRY': 2} | 0.30 / 0.30 / 0.27 / 0.27 / 0.27 / 0.30 | 1.867 | 0.717 | 0 |
| neutral|permanent | 30 | {'SITE_ONLY': 22, 'STOP': 3, 'OTHER': 2, 'RETRY': 1, 'REFORMAT': 2} | {'SITE_ONLY': 19, 'REFORMAT': 5, 'RETRY': 1, 'STOP': 33, 'OTHER': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.550 | 1.000 | 0 |

## H3 (stability → expectancy): calls on requests 5–6, 'unavailable' minus 'temporary' claim

- true fault fixable: -4.317 (1 vs 5.317)
- true fault transient: -1.949 (1.033 vs 2.983)
- true fault permanent: -4.224 (1 vs 5.224)

## Superstition probe (format claim over a transient fault)

- requests 2–6 whose first call already changes the SKU spelling: format claim 0.533, neutral message 0.187; index 0.347

## H4 (talked out of a fixable fault): success by request in permanent|fixable: 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00

## Validity

- completion (min over cells) 0.967; protocol failures 0.014; tool use on request 1 (min over cells) 1.000; unclassifiable responses 0.000
- run statuses: {'failed': 11, 'complete': 358}
- cost: {'runs_recorded': 369, 'from_cache': 0, 'agent_calls': 7906, 'equiv_usd': 0.2919}
