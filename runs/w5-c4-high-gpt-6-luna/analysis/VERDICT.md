# C4 kill test verdict: CONTINUE_CREDULOUS

**LIVE MODEL RUN (study W5: the C4 grid through native tool calls, reasoning high)**: transport `openai_responses_native`, model `gpt-6-luna`; 30 runs per cell.

- S +0.939 (CI +0.900, +0.972); L* +0.030 (CI -0.031, +0.090)

## Steering (request 1): follow rate of the claim's strategy minus the neutral baseline

| Misleading cell (claim, true fault) | Δ |
|---|---|
| format|transient | 1.000 |
| format|permanent | 0.967 |
| transient|fixable | 0.933 |
| transient|permanent | 0.933 |
| permanent|fixable | 0.867 |
| permanent|transient | 0.933 |

- **S** = 0.939 [0.900, 0.972]

## Learning: follow rate on requests 1–2 minus requests 5–6

| Cell | Kind | L |
|---|---|---|
| format|transient | misleading | 0.033 |
| format|permanent | misleading | 0.017 |
| transient|fixable | misleading | 0.000 |
| transient|permanent | misleading | 0.017 |
| permanent|fixable | misleading | 0.133 |
| permanent|transient | misleading | 0.233 |
| format|fixable | accurate | -0.033 |
| transient|transient | accurate | 0.033 |
| permanent|permanent | accurate | 0.150 |

- format|transient is excluded from L\*: obeying the format claim succeeds there (any third call does), so outcomes never contradict it.

- **L\*** = mean misleading L (five cells) − mean accurate L = 0.030 [-0.031, 0.090]

## Per cell (secondary)

| Cell | Runs | First response, request 1 | First response, requests 5–6 | Success by request | Calls, requests 5–6 | UNKNOWN | Unsupported |
|---|---|---|---|---|---|---|---|
| format|fixable | 30 | {'REFORMAT': 28, 'STOP': 2} | {'REFORMAT': 60} | 0.83 / 0.93 / 0.93 / 0.93 / 0.93 / 0.90 | 3.350 | 0.089 | 0 |
| format|transient | 30 | {'REFORMAT': 30} | {'REFORMAT': 56, 'SITE_ONLY': 4} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3 | 0.000 | 0 |
| format|permanent | 30 | {'REFORMAT': 29, 'STOP': 1} | {'REFORMAT': 56, 'SITE_ONLY': 4} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 6 | 1.000 | 0 |
| transient|fixable | 30 | {'RETRY': 28, 'SITE_ONLY': 2} | {'RETRY': 56, 'OTHER': 2, 'SITE_ONLY': 2} | 0.03 / 0.00 / 0.00 / 0.03 / 0.00 / 0.00 | 5.983 | 0.989 | 0 |
| transient|transient | 30 | {'RETRY': 29, 'SITE_ONLY': 1} | {'RETRY': 56, 'SITE_ONLY': 2, 'REFORMAT': 2} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3.083 | 0.000 | 0 |
| transient|permanent | 30 | {'RETRY': 28, 'OTHER': 1, 'SITE_ONLY': 1} | {'RETRY': 53, 'SITE_ONLY': 7} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.950 | 1.000 | 0 |
| permanent|fixable | 30 | {'STOP': 29, 'SITE_ONLY': 1} | {'STOP': 47, 'RETRY': 6, 'SITE_ONLY': 7} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.367 | 1.000 | 0 |
| permanent|transient | 30 | {'STOP': 29, 'SITE_ONLY': 1} | {'STOP': 44, 'SITE_ONLY': 10, 'REFORMAT': 4, 'RETRY': 2} | 0.03 / 0.03 / 0.07 / 0.10 / 0.17 / 0.23 | 1.533 | 0.894 | 0 |
| permanent|permanent | 30 | {'STOP': 29, 'SITE_ONLY': 1} | {'STOP': 47, 'RETRY': 5, 'SITE_ONLY': 8} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.433 | 1.000 | 0 |
| neutral|fixable | 30 | {'SITE_ONLY': 27, 'STOP': 3} | {'REFORMAT': 24, 'SITE_ONLY': 28, 'STOP': 2} | 0.30 / 0.23 / 0.33 / 0.40 / 0.27 / 0.37 | 4.467 | 0.683 | 0 |
| neutral|transient | 30 | {'SITE_ONLY': 28, 'RETRY': 1, 'STOP': 1} | {'SITE_ONLY': 24, 'REFORMAT': 33, 'RETRY': 1, 'STOP': 2} | 0.83 / 0.83 / 0.87 / 0.93 / 0.93 / 0.93 | 2.917 | 0.111 | 0 |
| neutral|permanent | 30 | {'SITE_ONLY': 30} | {'SITE_ONLY': 46, 'REFORMAT': 10, 'OTHER': 1, 'STOP': 3} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.283 | 1.000 | 0 |

## H3 (stability → expectancy): calls on requests 5–6, 'unavailable' minus 'temporary' claim

- true fault fixable: -4.617 (1.367 vs 5.983)
- true fault transient: -1.550 (1.533 vs 3.083)
- true fault permanent: -4.517 (1.433 vs 5.950)

## Superstition probe (format claim over a transient fault)

- requests 2–6 whose first call already changes the SKU spelling: format claim 0.027, neutral message 0.433; index -0.407

## H4 (talked out of a fixable fault): success by request in permanent|fixable: 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00

## Validity

- completion (min over cells) 1.000; protocol failures 0.000; tool use on request 1 (min over cells) 1.000; unclassifiable responses 0.000
- run statuses: {'complete': 360}
- cost: {'runs_recorded': 360, 'from_cache': 0, 'agent_calls': 9999, 'equiv_usd': 1.2366}
