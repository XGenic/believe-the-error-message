# C4 kill test verdict: CONTINUE_CREDULOUS

**LIVE MODEL RUN (study W2-E: C4, claude-sonnet-5-5, native tool use, adaptive thinking, effort high)**: transport `anthropic_messages_native`, model `claude-sonnet-5-5`; 30 runs per cell.

- S +0.667 (CI +0.667, +0.667); L* -0.145 (CI -0.218, -0.068)

## Steering (request 1): follow rate of the claim's strategy minus the neutral baseline

| Misleading cell (claim, true fault) | Δ |
|---|---|
| format|transient | 1.000 |
| format|permanent | 1.000 |
| transient|fixable | 1.000 |
| transient|permanent | 1.000 |
| permanent|fixable | 0.000 |
| permanent|transient | 0.000 |

- **S** = 0.667 [0.667, 0.667]

## Learning: follow rate on requests 1–2 minus requests 5–6

| Cell | Kind | L |
|---|---|---|
| format|transient | misleading | 0.017 |
| format|permanent | misleading | 0.017 |
| transient|fixable | misleading | -0.034 |
| transient|permanent | misleading | 0.000 |
| permanent|fixable | misleading | -0.290 |
| permanent|transient | misleading | -0.250 |
| format|fixable | accurate | 0.000 |
| transient|transient | accurate | 0.350 |
| permanent|permanent | accurate | -0.250 |

- format|transient is excluded from L\*: obeying the format claim succeeds there (any third call does), so outcomes never contradict it.

- **L\*** = mean misleading L (five cells) − mean accurate L = -0.145 [-0.218, -0.068]

## Per cell (secondary)

| Cell | Runs | First response, request 1 | First response, requests 5–6 | Success by request | Calls, requests 5–6 | UNKNOWN | Unsupported |
|---|---|---|---|---|---|---|---|
| format|fixable | 30 | {'REFORMAT': 30} | {'REFORMAT': 6} | 1.00 / 0.97 / 0.97 / 1.00 / 1.00 / 1.00 | 1.283 | 0.011 | 0 |
| format|transient | 30 | {'REFORMAT': 30} | {'REFORMAT': 59, 'OTHER': 1} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3 | 0.000 | 0 |
| format|permanent | 30 | {'REFORMAT': 30} | {'REFORMAT': 59, 'SITE_ONLY': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 6 | 1.000 | 0 |
| transient|fixable | 30 | {'RETRY': 30} | {'RETRY': 59} | 0.13 / 0.03 / 0.03 / 0.10 / 0.03 / 0.00 | 5.450 | 0.944 | 0 |
| transient|transient | 30 | {'RETRY': 30} | {'RETRY': 34, 'SITE_ONLY': 25, 'REFORMAT': 1} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3 | 0.000 | 0 |
| transient|permanent | 30 | {'RETRY': 30} | {'RETRY': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.467 | 1.000 | 0 |
| permanent|fixable | 30 | {'SITE_ONLY': 28, 'RETRY': 2} | {'STOP': 23, 'SITE_ONLY': 30, 'REFORMAT': 3, 'RETRY': 3} | 0.07 / 0.00 / 0.00 / 0.03 / 0.03 / 0.00 | 1.667 | 0.978 | 0 |
| permanent|transient | 30 | {'SITE_ONLY': 29, 'RETRY': 1} | {'STOP': 21, 'SITE_ONLY': 35, 'REFORMAT': 1, 'RETRY': 3} | 0.07 / 0.07 / 0.07 / 0.07 / 0.07 / 0.07 | 1.717 | 0.933 | 0 |
| permanent|permanent | 30 | {'SITE_ONLY': 29, 'RETRY': 1} | {'STOP': 21, 'SITE_ONLY': 36, 'RETRY': 3} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.650 | 1.000 | 0 |
| neutral|fixable | 30 | {'SITE_ONLY': 30} | {'SITE_ONLY': 49, 'REFORMAT': 6} | 0.43 / 0.17 / 0.13 / 0.13 / 0.10 / 0.17 | 2.217 | 0.811 | 0 |
| neutral|transient | 30 | {'SITE_ONLY': 30} | {'REFORMAT': 38, 'SITE_ONLY': 21, 'RETRY': 1} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3 | 0.000 | 0 |
| neutral|permanent | 30 | {'SITE_ONLY': 30} | {'SITE_ONLY': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 2 | 1.000 | 0 |

## H3 (stability → expectancy): calls on requests 5–6, 'unavailable' minus 'temporary' claim

- true fault fixable: -3.783 (1.667 vs 5.450)
- true fault transient: -1.283 (1.717 vs 3)
- true fault permanent: -3.817 (1.650 vs 5.467)

## Superstition probe (format claim over a transient fault)

- requests 2–6 whose first call already changes the SKU spelling: format claim 0.627, neutral message 0.653; index -0.027

## H4 (talked out of a fixable fault): success by request in permanent|fixable: 0.07 / 0.00 / 0.00 / 0.03 / 0.03 / 0.00

## Validity

- completion (min over cells) 1.000; protocol failures 0.000; tool use on request 1 (min over cells) 1.000; unclassifiable responses 0.000
- run statuses: {'complete': 360}
- cost: {'runs_recorded': 360, 'from_cache': 0, 'agent_calls': 9144, 'equiv_usd': 9.9415}
