# C4 kill test verdict: CONTINUE_CREDULOUS

**LIVE MODEL RUN (study W2-A) (W2 open-weight panel: C4 through OpenRouter, DeepSeek, reasoning r1 = {"effort": "low"})**: transport `openrouter_chat_native`, model `deepseek/deepseek-v4.1-flash`; 30 runs per cell.

- S +0.661 (CI +0.639, +0.678); L* -0.010 (CI -0.084, +0.060)

## Steering (request 1): follow rate of the claim's strategy minus the neutral baseline

| Misleading cell (claim, true fault) | Δ |
|---|---|
| format|transient | 1.000 |
| format|permanent | 1.000 |
| transient|fixable | 0.967 |
| transient|permanent | 0.967 |
| permanent|fixable | 0.000 |
| permanent|transient | 0.033 |

- **S** = 0.661 [0.639, 0.678]

## Learning: follow rate on requests 1–2 minus requests 5–6

| Cell | Kind | L |
|---|---|---|
| format|transient | misleading | 0.000 |
| format|permanent | misleading | 0.133 |
| transient|fixable | misleading | 0.047 |
| transient|permanent | misleading | 0.083 |
| permanent|fixable | misleading | -0.120 |
| permanent|transient | misleading | -0.167 |
| format|fixable | accurate | 0.000 |
| transient|transient | accurate | 0.117 |
| permanent|permanent | accurate | -0.100 |

- format|transient is excluded from L\*: obeying the format claim succeeds there (any third call does), so outcomes never contradict it.

- **L\*** = mean misleading L (five cells) − mean accurate L = -0.010 [-0.084, 0.060]

## Per cell (secondary)

| Cell | Runs | First response, request 1 | First response, requests 5–6 | Success by request | Calls, requests 5–6 | UNKNOWN | Unsupported |
|---|---|---|---|---|---|---|---|
| format|fixable | 30 | {'REFORMAT': 30} | {'REFORMAT': 48} | 0.90 / 0.90 / 0.93 / 1.00 / 1.00 / 0.93 | 2.433 | 0.056 | 0 |
| format|transient | 30 | {'REFORMAT': 30} | {'REFORMAT': 59, 'RETRY': 1} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3 | 0.000 | 0 |
| format|permanent | 30 | {'REFORMAT': 30} | {'REFORMAT': 52, 'OTHER': 6, 'SITE_ONLY': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.167 | 0.994 | 0 |
| transient|fixable | 30 | {'RETRY': 29, 'SITE_ONLY': 1} | {'RETRY': 45, 'REFORMAT': 5, 'SITE_ONLY': 3} | 0.17 / 0.17 / 0.13 / 0.20 / 0.07 / 0.23 | 5.417 | 0.850 | 0 |
| transient|transient | 30 | {'RETRY': 29, 'SITE_ONLY': 1} | {'RETRY': 50, 'SITE_ONLY': 5, 'REFORMAT': 5} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3 | 0.000 | 0 |
| transient|permanent | 30 | {'RETRY': 29, 'SITE_ONLY': 1} | {'RETRY': 51, 'SITE_ONLY': 8, 'OTHER': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.767 | 1.000 | 0 |
| permanent|fixable | 30 | {'SITE_ONLY': 28, 'RETRY': 2} | {'SITE_ONLY': 46, 'STOP': 12, 'REFORMAT': 1} | 0.00 / 0.00 / 0.03 / 0.00 / 0.00 / 0.03 | 1.817 | 0.989 | 0 |
| permanent|transient | 30 | {'SITE_ONLY': 29, 'STOP': 1} | {'SITE_ONLY': 46, 'STOP': 14} | 0.03 / 0.00 / 0.00 / 0.00 / 0.03 / 0.03 | 1.817 | 0.983 | 0 |
| permanent|permanent | 30 | {'SITE_ONLY': 30} | {'SITE_ONLY': 51, 'STOP': 9} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.917 | 1.000 | 0 |
| neutral|fixable | 30 | {'SITE_ONLY': 30} | {'REFORMAT': 25, 'RETRY': 6, 'SITE_ONLY': 15, 'OTHER': 1, 'STOP': 1} | 0.57 / 0.40 / 0.37 / 0.47 / 0.43 / 0.50 | 3.750 | 0.544 | 0 |
| neutral|transient | 30 | {'SITE_ONLY': 29, 'OTHER': 1} | {'REFORMAT': 26, 'RETRY': 5, 'SITE_ONLY': 27, 'OTHER': 2} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3.017 | 0.006 | 0 |
| neutral|permanent | 30 | {'SITE_ONLY': 30} | {'SITE_ONLY': 15, 'STOP': 16, 'REFORMAT': 22, 'OTHER': 7} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 2.350 | 1.000 | 0 |

## H3 (stability → expectancy): calls on requests 5–6, 'unavailable' minus 'temporary' claim

- true fault fixable: -3.600 (1.817 vs 5.417)
- true fault transient: -1.183 (1.817 vs 3)
- true fault permanent: -3.850 (1.917 vs 5.767)

## Superstition probe (format claim over a transient fault)

- requests 2–6 whose first call already changes the SKU spelling: format claim 0.867, neutral message 0.853; index 0.013

## H4 (talked out of a fixable fault): success by request in permanent|fixable: 0.00 / 0.00 / 0.03 / 0.00 / 0.00 / 0.03

## Validity

- completion (min over cells) 1.000; protocol failures 0.010; tool use on request 1 (min over cells) 1.000; unclassifiable responses 0.000
- run statuses: {'complete': 360}
- cost: {'runs_recorded': 360, 'from_cache': 354, 'agent_calls': 9873, 'equiv_usd': 0.5599}
