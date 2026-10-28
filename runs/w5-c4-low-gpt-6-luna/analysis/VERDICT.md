# C4 kill test verdict: CONTINUE_CREDULOUS

**LIVE MODEL RUN (study W5: the C4 grid through native tool calls, reasoning low)**: transport `openai_responses_native`, model `gpt-6-luna`; 30 runs per cell.

- S +0.794 (CI +0.739, +0.850); L* +0.008 (CI -0.043, +0.064)

## Steering (request 1): follow rate of the claim's strategy minus the neutral baseline

| Misleading cell (claim, true fault) | Δ |
|---|---|
| format|transient | 0.667 |
| format|permanent | 0.867 |
| transient|fixable | 0.867 |
| transient|permanent | 0.967 |
| permanent|fixable | 0.833 |
| permanent|transient | 0.567 |

- **S** = 0.794 [0.739, 0.850]

## Learning: follow rate on requests 1–2 minus requests 5–6

| Cell | Kind | L |
|---|---|---|
| format|transient | misleading | -0.183 |
| format|permanent | misleading | -0.050 |
| transient|fixable | misleading | -0.050 |
| transient|permanent | misleading | -0.017 |
| permanent|fixable | misleading | -0.017 |
| permanent|transient | misleading | 0.033 |
| format|fixable | accurate | -0.167 |
| transient|transient | accurate | 0.050 |
| permanent|permanent | accurate | 0.033 |

- format|transient is excluded from L\*: obeying the format claim succeeds there (any third call does), so outcomes never contradict it.

- **L\*** = mean misleading L (five cells) − mean accurate L = 0.008 [-0.043, 0.064]

## Per cell (secondary)

| Cell | Runs | First response, request 1 | First response, requests 5–6 | Success by request | Calls, requests 5–6 | UNKNOWN | Unsupported |
|---|---|---|---|---|---|---|---|
| format|fixable | 30 | {'REFORMAT': 22, 'OTHER': 1, 'SITE_ONLY': 6, 'STOP': 1} | {'REFORMAT': 58, 'SITE_ONLY': 2} | 0.87 / 0.80 / 0.93 / 0.93 / 0.93 / 0.90 | 3.517 | 0.106 | 0 |
| format|transient | 30 | {'REFORMAT': 20, 'STOP': 1, 'SITE_ONLY': 9} | {'REFORMAT': 58, 'SITE_ONLY': 2} | 0.97 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3 | 0.006 | 0 |
| format|permanent | 30 | {'REFORMAT': 26, 'SITE_ONLY': 4} | {'REFORMAT': 54, 'SITE_ONLY': 6} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.933 | 1.000 | 0 |
| transient|fixable | 30 | {'RETRY': 26, 'SITE_ONLY': 3, 'OTHER': 1} | {'RETRY': 52, 'SITE_ONLY': 6, 'OTHER': 2} | 0.03 / 0.00 / 0.00 / 0.00 / 0.03 / 0.00 | 5.767 | 0.989 | 0 |
| transient|transient | 30 | {'RETRY': 29, 'SITE_ONLY': 1} | {'RETRY': 52, 'SITE_ONLY': 5, 'REFORMAT': 3} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3 | 0.000 | 0 |
| transient|permanent | 30 | {'RETRY': 29, 'STOP': 1} | {'RETRY': 54, 'SITE_ONLY': 6} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.650 | 1.000 | 0 |
| permanent|fixable | 30 | {'STOP': 30} | {'STOP': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1 | 1.000 | 0 |
| permanent|transient | 30 | {'STOP': 30} | {'STOP': 58, 'RETRY': 2} | 0.00 / 0.00 / 0.03 / 0.03 / 0.03 / 0.03 | 1.067 | 0.978 | 0 |
| permanent|permanent | 30 | {'STOP': 30} | {'STOP': 57, 'RETRY': 1, 'SITE_ONLY': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.117 | 1.000 | 0 |
| neutral|fixable | 30 | {'SITE_ONLY': 25, 'STOP': 5} | {'REFORMAT': 12, 'SITE_ONLY': 27, 'STOP': 16} | 0.30 / 0.10 / 0.17 / 0.20 / 0.20 / 0.20 | 3.150 | 0.806 | 0 |
| neutral|transient | 30 | {'SITE_ONLY': 17, 'STOP': 13} | {'SITE_ONLY': 18, 'REFORMAT': 22, 'STOP': 20} | 0.40 / 0.43 / 0.47 / 0.47 / 0.50 / 0.50 | 2.183 | 0.539 | 0 |
| neutral|permanent | 30 | {'SITE_ONLY': 22, 'STOP': 8} | {'STOP': 33, 'SITE_ONLY': 25, 'REFORMAT': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 2.317 | 1.000 | 0 |

## H3 (stability → expectancy): calls on requests 5–6, 'unavailable' minus 'temporary' claim

- true fault fixable: -4.767 (1 vs 5.767)
- true fault transient: -1.933 (1.067 vs 3)
- true fault permanent: -4.533 (1.117 vs 5.650)

## Superstition probe (format claim over a transient fault)

- requests 2–6 whose first call already changes the SKU spelling: format claim 0.047, neutral message 0.167; index -0.120

## H4 (talked out of a fixable fault): success by request in permanent|fixable: 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00

## Validity

- completion (min over cells) 1.000; protocol failures 0.000; tool use on request 1 (min over cells) 1.000; unclassifiable responses 0.000
- run statuses: {'complete': 360}
- cost: {'runs_recorded': 360, 'from_cache': 0, 'agent_calls': 8851, 'equiv_usd': 0.9994}
