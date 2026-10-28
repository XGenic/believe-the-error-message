# C4 kill test verdict: CONTINUE_CREDULOUS

**LIVE MODEL RUN (study N1-A: native tool calls, reasoning low)**: transport `openai_responses_native`, model `gpt-6-luna`; 30 runs per cell.

- S +0.789 (CI +0.733, +0.844); L* +0.029 (CI -0.036, +0.093)

## Steering (request 1): follow rate of the claim's strategy minus the neutral baseline

| Misleading cell (claim, true fault) | Δ |
|---|---|
| format|transient | 0.733 |
| format|permanent | 0.533 |
| transient|fixable | 1.000 |
| transient|permanent | 0.900 |
| permanent|fixable | 0.800 |
| permanent|transient | 0.767 |

- **S** = 0.789 [0.733, 0.844]

## Learning: follow rate on requests 1–2 minus requests 5–6

| Cell | Kind | L |
|---|---|---|
| format|transient | misleading | -0.150 |
| format|permanent | misleading | -0.083 |
| transient|fixable | misleading | -0.017 |
| transient|permanent | misleading | -0.017 |
| permanent|fixable | misleading | 0.017 |
| permanent|transient | misleading | 0.050 |
| format|fixable | accurate | -0.149 |
| transient|transient | accurate | 0.033 |
| permanent|permanent | accurate | 0.000 |

- format|transient is excluded from L\*: obeying the format claim succeeds there (any third call does), so outcomes never contradict it.

- **L\*** = mean misleading L (five cells) − mean accurate L = 0.029 [-0.036, 0.093]

## Per cell (secondary)

| Cell | Runs | First response, request 1 | First response, requests 5–6 | Success by request | Calls, requests 5–6 | UNKNOWN | Unsupported |
|---|---|---|---|---|---|---|---|
| format|fixable | 30 | {'REFORMAT': 22, 'SITE_ONLY': 8} | {'REFORMAT': 57, 'SITE_ONLY': 2} | 0.93 / 0.77 / 0.87 / 0.90 / 0.87 / 0.87 | 3.767 | 0.133 | 0 |
| format|transient | 30 | {'REFORMAT': 22, 'SITE_ONLY': 7, 'OTHER': 1} | {'REFORMAT': 57, 'SITE_ONLY': 3} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3 | 0.000 | 0 |
| format|permanent | 30 | {'REFORMAT': 16, 'SITE_ONLY': 12, 'STOP': 2} | {'REFORMAT': 39, 'SITE_ONLY': 21} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.967 | 1.000 | 0 |
| transient|fixable | 30 | {'RETRY': 30} | {'RETRY': 59, 'STOP': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.467 | 1.000 | 0 |
| transient|transient | 30 | {'RETRY': 28, 'OTHER': 1, 'SITE_ONLY': 1} | {'RETRY': 54, 'OTHER': 2, 'SITE_ONLY': 2, 'REFORMAT': 2} | 0.93 / 0.97 / 0.97 / 0.97 / 0.97 / 0.97 | 3.117 | 0.039 | 0 |
| transient|permanent | 30 | {'RETRY': 27, 'SITE_ONLY': 2, 'OTHER': 1} | {'RETRY': 54, 'SITE_ONLY': 4, 'OTHER': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.350 | 1.000 | 0 |
| permanent|fixable | 30 | {'STOP': 30} | {'STOP': 58, 'SITE_ONLY': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.033 | 1.000 | 0 |
| permanent|transient | 30 | {'STOP': 30} | {'STOP': 55, 'SITE_ONLY': 3, 'RETRY': 2} | 0.00 / 0.03 / 0.03 / 0.03 / 0.03 / 0.03 | 1.150 | 0.972 | 0 |
| permanent|permanent | 30 | {'STOP': 30} | {'STOP': 56, 'SITE_ONLY': 3, 'RETRY': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.133 | 1.000 | 0 |
| neutral|fixable | 30 | {'SITE_ONLY': 24, 'STOP': 6} | {'REFORMAT': 11, 'STOP': 24, 'SITE_ONLY': 23, 'OTHER': 1} | 0.23 / 0.07 / 0.13 / 0.20 / 0.17 / 0.13 | 2.950 | 0.844 | 0 |
| neutral|transient | 30 | {'SITE_ONLY': 23, 'STOP': 7} | {'STOP': 13, 'SITE_ONLY': 34, 'REFORMAT': 13} | 0.40 / 0.43 / 0.47 / 0.47 / 0.57 / 0.63 | 2.467 | 0.506 | 0 |
| neutral|permanent | 30 | {'SITE_ONLY': 23, 'STOP': 7} | {'SITE_ONLY': 21, 'STOP': 39} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.950 | 1.000 | 0 |

## H3 (stability → expectancy): calls on requests 5–6, 'unavailable' minus 'temporary' claim

- true fault fixable: -4.433 (1.033 vs 5.467)
- true fault transient: -1.967 (1.150 vs 3.117)
- true fault permanent: -4.217 (1.133 vs 5.350)

## Superstition probe (format claim over a transient fault)

- requests 2–6 whose first call already changes the SKU spelling: format claim 0.033, neutral message 0.233; index -0.200

## H4 (talked out of a fixable fault): success by request in permanent|fixable: 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00

## Validity

- completion (min over cells) 1.000; protocol failures 0.000; tool use on request 1 (min over cells) 1.000; unclassifiable responses 0.000
- run statuses: {'complete': 360}
- cost: {'runs_recorded': 360, 'from_cache': 0, 'agent_calls': 8862, 'equiv_usd': 1.0003}
