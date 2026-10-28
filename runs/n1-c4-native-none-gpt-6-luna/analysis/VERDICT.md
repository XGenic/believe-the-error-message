# C4 kill test verdict: INCONCLUSIVE

**LIVE MODEL RUN (study N1-C: native tool calls, reasoning none)**: transport `openai_responses_native`, model `gpt-6-luna`; 30 runs per cell.

- S +0.544 (CI +0.489, +0.606); L* +0.124 (CI +0.061, +0.190)

## Steering (request 1): follow rate of the claim's strategy minus the neutral baseline

| Misleading cell (claim, true fault) | Δ |
|---|---|
| format|transient | 0.533 |
| format|permanent | 0.600 |
| transient|fixable | 0.867 |
| transient|permanent | 0.900 |
| permanent|fixable | 0.167 |
| permanent|transient | 0.200 |

- **S** = 0.544 [0.489, 0.606]

## Learning: follow rate on requests 1–2 minus requests 5–6

| Cell | Kind | L |
|---|---|---|
| format|transient | misleading | -0.217 |
| format|permanent | misleading | -0.017 |
| transient|fixable | misleading | -0.017 |
| transient|permanent | misleading | -0.017 |
| permanent|fixable | misleading | 0.067 |
| permanent|transient | misleading | 0.050 |
| format|fixable | accurate | -0.350 |
| transient|transient | accurate | 0.033 |
| permanent|permanent | accurate | -0.017 |

- format|transient is excluded from L\*: obeying the format claim succeeds there (any third call does), so outcomes never contradict it.

- **L\*** = mean misleading L (five cells) − mean accurate L = 0.124 [0.061, 0.190]

## Per cell (secondary)

| Cell | Runs | First response, request 1 | First response, requests 5–6 | Success by request | Calls, requests 5–6 | UNKNOWN | Unsupported |
|---|---|---|---|---|---|---|---|
| format|fixable | 30 | {'REFORMAT': 15, 'SITE_ONLY': 14, 'STOP': 1} | {'REFORMAT': 57, 'SITE_ONLY': 3} | 0.80 / 0.77 / 0.83 / 0.87 / 0.87 / 0.83 | 3.783 | 0.172 | 0 |
| format|transient | 30 | {'SITE_ONLY': 10, 'STOP': 2, 'REFORMAT': 16, 'OTHER': 2} | {'REFORMAT': 53, 'SITE_ONLY': 7} | 0.93 / 0.97 / 0.97 / 1.00 / 1.00 / 1.00 | 3 | 0.022 | 0 |
| format|permanent | 30 | {'REFORMAT': 18, 'SITE_ONLY': 12} | {'SITE_ONLY': 21, 'REFORMAT': 39} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 6 | 1.000 | 0 |
| transient|fixable | 30 | {'RETRY': 26, 'STOP': 1, 'SITE_ONLY': 1, 'OTHER': 2} | {'RETRY': 54, 'SITE_ONLY': 4, 'OTHER': 2} | 0.00 / 0.00 / 0.03 / 0.00 / 0.00 / 0.03 | 5.917 | 0.989 | 0 |
| transient|transient | 30 | {'RETRY': 29, 'OTHER': 1} | {'RETRY': 56, 'REFORMAT': 2, 'OTHER': 2} | 0.90 / 0.97 / 0.97 / 0.97 / 0.97 / 0.97 | 3.117 | 0.044 | 0 |
| transient|permanent | 30 | {'RETRY': 27, 'SITE_ONLY': 2, 'STOP': 1} | {'RETRY': 56, 'SITE_ONLY': 4} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.933 | 1.000 | 0 |
| permanent|fixable | 30 | {'STOP': 30} | {'STOP': 54, 'RETRY': 2, 'SITE_ONLY': 2, 'REFORMAT': 2} | 0.00 / 0.03 / 0.07 / 0.03 / 0.03 / 0.07 | 1.300 | 0.961 | 0 |
| permanent|transient | 30 | {'STOP': 30} | {'STOP': 56, 'REFORMAT': 4} | 0.00 / 0.03 / 0.07 / 0.07 / 0.07 / 0.07 | 1.133 | 0.950 | 0 |
| permanent|permanent | 30 | {'STOP': 30} | {'STOP': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1 | 1.000 | 0 |
| neutral|fixable | 30 | {'STOP': 25, 'SITE_ONLY': 4, 'OTHER': 1} | {'STOP': 37, 'REFORMAT': 4, 'SITE_ONLY': 18} | 0.00 / 0.03 / 0.03 / 0.13 / 0.07 / 0.00 | 2.033 | 0.956 | 0 |
| neutral|transient | 30 | {'STOP': 24, 'SITE_ONLY': 6} | {'STOP': 37, 'SITE_ONLY': 12, 'REFORMAT': 11} | 0.20 / 0.23 / 0.27 / 0.27 / 0.27 / 0.27 | 1.650 | 0.750 | 0 |
| neutral|permanent | 30 | {'STOP': 27, 'SITE_ONLY': 2, 'OTHER': 1} | {'STOP': 34, 'SITE_ONLY': 26} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 2.050 | 1.000 | 0 |

## H3 (stability → expectancy): calls on requests 5–6, 'unavailable' minus 'temporary' claim

- true fault fixable: -4.617 (1.300 vs 5.917)
- true fault transient: -1.983 (1.133 vs 3.117)
- true fault permanent: -4.933 (1 vs 5.933)

## Superstition probe (format claim over a transient fault)

- requests 2–6 whose first call already changes the SKU spelling: format claim 0.020, neutral message 0.107; index -0.087

## H4 (talked out of a fixable fault): success by request in permanent|fixable: 0.00 / 0.03 / 0.07 / 0.03 / 0.03 / 0.07

## Validity

- completion (min over cells) 1.000; protocol failures 0.000; tool use on request 1 (min over cells) 1.000; unclassifiable responses 0.000
- run statuses: {'complete': 360}
- cost: {'runs_recorded': 360, 'from_cache': 0, 'agent_calls': 8630, 'equiv_usd': 0.974}
