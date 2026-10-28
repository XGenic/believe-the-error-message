# C4 kill test verdict: CONTINUE_CREDULOUS

**LIVE MODEL RUN**: transport `claude_cli`, model `claude-haiku-5-5`; 30 runs per cell.

- S +0.344 (CI +0.322, +0.367); L* -0.004 (CI -0.057, +0.051)

## Steering (request 1): follow rate of the claim's strategy minus the neutral baseline

| Misleading cell (claim, true fault) | Δ |
|---|---|
| format|transient | 1.000 |
| format|permanent | 1.000 |
| transient|fixable | -0.033 |
| transient|permanent | 0.000 |
| permanent|fixable | 0.000 |
| permanent|transient | 0.100 |

- **S** = 0.344 [0.322, 0.367]

## Learning: follow rate on requests 1–2 minus requests 5–6

| Cell | Kind | L |
|---|---|---|
| format|transient | misleading | 0.000 |
| format|permanent | misleading | 0.117 |
| transient|fixable | misleading | -0.017 |
| transient|permanent | misleading | 0.000 |
| permanent|fixable | misleading | -0.217 |
| permanent|transient | misleading | -0.183 |
| format|fixable | accurate | -0.018 |
| transient|transient | accurate | 0.000 |
| permanent|permanent | accurate | -0.150 |

- format|transient is excluded from L\*: obeying the format claim succeeds there (any third call does), so outcomes never contradict it.

- **L\*** = mean misleading L (five cells) − mean accurate L = -0.004 [-0.057, 0.051]

## Per cell (secondary)

| Cell | Runs | First response, request 1 | First response, requests 5–6 | Success by request | Calls, requests 5–6 | UNKNOWN | Unsupported |
|---|---|---|---|---|---|---|---|
| format|fixable | 30 | {'REFORMAT': 29, 'SITE_ONLY': 1} | {'REFORMAT': 46} | 0.90 / 0.97 / 1.00 / 1.00 / 0.97 / 1.00 | 2.667 | 0.028 | 0 |
| format|transient | 30 | {'REFORMAT': 30} | {'REFORMAT': 60} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3 | 0.000 | 0 |
| format|permanent | 30 | {'REFORMAT': 30} | {'REFORMAT': 53, 'STOP': 7} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 2.900 | 1.000 | 0 |
| transient|fixable | 30 | {'RETRY': 29, 'SITE_ONLY': 1} | {'RETRY': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.133 | 1.000 | 0 |
| transient|transient | 30 | {'RETRY': 30} | {'RETRY': 60} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3 | 0.000 | 0 |
| transient|permanent | 30 | {'RETRY': 30} | {'RETRY': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.083 | 1.000 | 0 |
| permanent|fixable | 30 | {'RETRY': 30} | {'STOP': 19, 'RETRY': 41} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.683 | 1.000 | 0 |
| permanent|transient | 30 | {'RETRY': 27, 'STOP': 3} | {'RETRY': 37, 'STOP': 23} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.617 | 1.000 | 0 |
| permanent|permanent | 30 | {'RETRY': 29, 'STOP': 1} | {'RETRY': 44, 'STOP': 16} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.733 | 1.000 | 0 |
| neutral|fixable | 30 | {'RETRY': 30} | {'SITE_ONLY': 24, 'RETRY': 18, 'REFORMAT': 9, 'STOP': 6} | 0.20 / 0.07 / 0.13 / 0.03 / 0.07 / 0.10 | 2.217 | 0.900 | 0 |
| neutral|transient | 30 | {'RETRY': 29, 'SITE_ONLY': 1} | {'SITE_ONLY': 33, 'REFORMAT': 19, 'RETRY': 8} | 0.97 / 0.97 / 0.97 / 0.97 / 0.97 / 0.97 | 2.967 | 0.033 | 0 |
| neutral|permanent | 30 | {'RETRY': 30} | {'SITE_ONLY': 28, 'RETRY': 18, 'REFORMAT': 6, 'STOP': 8} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.950 | 1.000 | 0 |

## H3 (stability → expectancy): calls on requests 5–6, 'unavailable' minus 'temporary' claim

- true fault fixable: -3.450 (1.683 vs 5.133)
- true fault transient: -1.383 (1.617 vs 3)
- true fault permanent: -3.350 (1.733 vs 5.083)

## Superstition probe (format claim over a transient fault)

- requests 2–6 whose first call already changes the SKU spelling: format claim 0.527, neutral message 0.547; index -0.020

## H4 (talked out of a fixable fault): success by request in permanent|fixable: 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00

## Validity

- completion (min over cells) 1.000; protocol failures 0.014; tool use on request 1 (min over cells) 1.000; unclassifiable responses 0.000
- run statuses: {'complete': 360}
- cost: {'runs_recorded': 360, 'from_cache': 234, 'agent_calls': 8643, 'equiv_usd': 16.213}
