# C4 kill test verdict: INCONCLUSIVE

**LIVE MODEL RUN (study W2-C: the C4 grid, claude-haiku-5-5, native tool use, thinking off)**: transport `anthropic_messages_native`, model `claude-haiku-5-5`; 30 runs per cell.

- S +0.694 (CI +0.661, +0.733); L* +0.111 (CI +0.057, +0.162)

## Steering (request 1): follow rate of the claim's strategy minus the neutral baseline

| Misleading cell (claim, true fault) | Δ |
|---|---|
| format|transient | 1.000 |
| format|permanent | 1.000 |
| transient|fixable | 0.867 |
| transient|permanent | 0.900 |
| permanent|fixable | 0.233 |
| permanent|transient | 0.167 |

- **S** = 0.694 [0.661, 0.733]

## Learning: follow rate on requests 1–2 minus requests 5–6

| Cell | Kind | L |
|---|---|---|
| format|transient | misleading | 0.217 |
| format|permanent | misleading | 0.150 |
| transient|fixable | misleading | 0.317 |
| transient|permanent | misleading | 0.400 |
| permanent|fixable | misleading | -0.017 |
| permanent|transient | misleading | 0.000 |
| format|fixable | accurate | -0.039 |
| transient|transient | accurate | 0.233 |
| permanent|permanent | accurate | -0.017 |

- format|transient is excluded from L\*: obeying the format claim succeeds there (any third call does), so outcomes never contradict it.

- **L\*** = mean misleading L (five cells) − mean accurate L = 0.111 [0.057, 0.162]

## Per cell (secondary)

| Cell | Runs | First response, request 1 | First response, requests 5–6 | Success by request | Calls, requests 5–6 | UNKNOWN | Unsupported |
|---|---|---|---|---|---|---|---|
| format|fixable | 30 | {'REFORMAT': 30} | {'REFORMAT': 44, 'STOP': 4} | 0.50 / 0.30 / 0.40 / 0.47 / 0.43 / 0.33 | 1.933 | 0.594 | 0 |
| format|transient | 30 | {'REFORMAT': 30} | {'STOP': 26, 'REFORMAT': 34} | 0.03 / 0.03 / 0.03 / 0.03 / 0.03 / 0.03 | 1.600 | 0.967 | 0 |
| format|permanent | 30 | {'REFORMAT': 30} | {'STOP': 18, 'REFORMAT': 42} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.733 | 1.000 | 0 |
| transient|fixable | 30 | {'RETRY': 30} | {'RETRY': 22, 'STOP': 38} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.567 | 1.000 | 0 |
| transient|transient | 30 | {'RETRY': 30} | {'RETRY': 32, 'STOP': 28} | 0.37 / 0.37 / 0.37 / 0.37 / 0.37 / 0.37 | 1.900 | 0.633 | 0 |
| transient|permanent | 30 | {'RETRY': 30} | {'RETRY': 12, 'STOP': 48} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.300 | 1.000 | 0 |
| permanent|fixable | 30 | {'STOP': 29, 'RETRY': 1} | {'STOP': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1 | 1.000 | 0 |
| permanent|transient | 30 | {'STOP': 30} | {'STOP': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1 | 1.000 | 0 |
| permanent|permanent | 30 | {'STOP': 29, 'RETRY': 1} | {'STOP': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1 | 1.000 | 0 |
| neutral|fixable | 30 | {'SITE_ONLY': 4, 'STOP': 22, 'RETRY': 4} | {'STOP': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1 | 1.000 | 0 |
| neutral|transient | 30 | {'STOP': 25, 'SITE_ONLY': 2, 'RETRY': 3} | {'STOP': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1 | 1.000 | 0 |
| neutral|permanent | 30 | {'STOP': 23, 'SITE_ONLY': 4, 'RETRY': 3} | {'STOP': 58, 'SITE_ONLY': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.033 | 1.000 | 0 |

## H3 (stability → expectancy): calls on requests 5–6, 'unavailable' minus 'temporary' claim

- true fault fixable: -0.567 (1 vs 1.567)
- true fault transient: -0.900 (1 vs 1.900)
- true fault permanent: -0.300 (1 vs 1.300)

## Superstition probe (format claim over a transient fault)

- requests 2–6 whose first call already changes the SKU spelling: format claim 0.007, neutral message 0.000; index 0.007

## H4 (talked out of a fixable fault): success by request in permanent|fixable: 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00

## Validity

- completion (min over cells) 1.000; protocol failures 0.000; tool use on request 1 (min over cells) 1.000; unclassifiable responses 0.000
- run statuses: {'complete': 360}
- cost: {'runs_recorded': 360, 'from_cache': 0, 'agent_calls': 5181, 'equiv_usd': 0.2563}
