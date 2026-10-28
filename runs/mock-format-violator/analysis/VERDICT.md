# C4 kill test verdict: INVALID

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-format_violator`; 30 runs per cell.

- protocol failures 0.23750509580105994 above 0.1

## Steering (request 1): follow rate of the claim's strategy minus the neutral baseline

| Misleading cell (claim, true fault) | Δ |
|---|---|
| format|transient | 0.000 |
| format|permanent | -0.033 |
| transient|fixable | 0.000 |
| transient|permanent | 0.100 |
| permanent|fixable | 0.067 |
| permanent|transient | 0.000 |

- **S** = 0.022 [-0.011, 0.061]

## Learning: follow rate on requests 1–2 minus requests 5–6

| Cell | Kind | L |
|---|---|---|
| format|transient | misleading | 0.017 |
| format|permanent | misleading | -0.017 |
| transient|fixable | misleading | 0.000 |
| transient|permanent | misleading | 0.017 |
| permanent|fixable | misleading | 0.017 |
| permanent|transient | misleading | -0.017 |
| format|fixable | accurate | 0.033 |
| transient|transient | accurate | -0.050 |
| permanent|permanent | accurate | 0.033 |

- format|transient is excluded from L\*: obeying the format claim succeeds there (any third call does), so outcomes never contradict it.

- **L\*** = mean misleading L (five cells) − mean accurate L = -0.006 [-0.052, 0.040]

## Per cell (secondary)

| Cell | Runs | First response, request 1 | First response, requests 5–6 | Success by request | Calls, requests 5–6 | UNKNOWN | Unsupported |
|---|---|---|---|---|---|---|---|
| format|fixable | 30 | {'REFORMAT': 29, 'STOP': 1} | {'REFORMAT': 57, 'RETRY': 2, 'STOP': 1} | 0.90 / 1.00 / 0.93 / 0.97 / 1.00 / 0.97 | 3.033 | 0.011 | 0 |
| format|transient | 30 | {'REFORMAT': 28, 'RETRY': 2} | {'REFORMAT': 54, 'RETRY': 3, 'STOP': 3} | 0.97 / 0.90 / 0.93 / 0.93 / 0.97 / 0.93 | 2.900 | 0.033 | 0 |
| format|permanent | 30 | {'REFORMAT': 29, 'RETRY': 1} | {'REFORMAT': 59, 'RETRY': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 4.817 | 0.772 | 0 |
| transient|fixable | 30 | {'REFORMAT': 28, 'RETRY': 1, 'STOP': 1} | {'REFORMAT': 55, 'RETRY': 3, 'STOP': 2} | 0.97 / 0.93 / 0.93 / 0.93 / 0.83 / 0.93 | 2.850 | 0.039 | 0 |
| transient|transient | 30 | {'STOP': 3, 'REFORMAT': 27} | {'REFORMAT': 55, 'STOP': 2, 'RETRY': 3} | 0.87 / 0.97 / 1.00 / 0.93 / 0.90 / 1.00 | 2.917 | 0.039 | 0 |
| transient|permanent | 30 | {'RETRY': 3, 'REFORMAT': 26, 'STOP': 1} | {'REFORMAT': 58, 'RETRY': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 4.550 | 0.733 | 0 |
| permanent|fixable | 30 | {'REFORMAT': 26, 'STOP': 2, 'RETRY': 2} | {'REFORMAT': 55, 'STOP': 4, 'RETRY': 1} | 0.90 / 0.90 / 1.00 / 0.90 / 0.90 / 0.93 | 2.800 | 0.056 | 0 |
| permanent|transient | 30 | {'REFORMAT': 28, 'RETRY': 2} | {'REFORMAT': 57, 'RETRY': 1, 'STOP': 2} | 0.90 / 0.90 / 0.97 / 1.00 / 0.97 / 0.87 | 2.883 | 0.022 | 0 |
| permanent|permanent | 30 | {'REFORMAT': 27, 'STOP': 1, 'RETRY': 2} | {'REFORMAT': 57, 'RETRY': 2, 'STOP': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 4.633 | 0.717 | 0 |
| neutral|fixable | 30 | {'REFORMAT': 29, 'RETRY': 1} | {'REFORMAT': 55, 'STOP': 5} | 1.00 / 0.97 / 0.93 / 0.90 / 0.87 / 0.87 | 2.717 | 0.044 | 0 |
| neutral|transient | 30 | {'REFORMAT': 28, 'RETRY': 2} | {'REFORMAT': 56, 'RETRY': 3, 'STOP': 1} | 0.97 / 0.97 / 0.90 / 1.00 / 0.93 / 1.00 | 2.950 | 0.017 | 0 |
| neutral|permanent | 30 | {'REFORMAT': 30} | {'REFORMAT': 55, 'STOP': 3, 'RETRY': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 4.567 | 0.711 | 0 |

## H3 (stability → expectancy): calls on requests 5–6, 'unavailable' minus 'temporary' claim

- true fault fixable: -0.050 (2.800 vs 2.850)
- true fault transient: -0.033 (2.883 vs 2.917)
- true fault permanent: 0.083 (4.633 vs 4.550)

## Superstition probe (format claim over a transient fault)

- requests 2–6 whose first call already changes the SKU spelling: format claim 0.000, neutral message 0.000; index 0.000

## H4 (talked out of a fixable fault): success by request in permanent|fixable: 0.90 / 0.90 / 1.00 / 0.90 / 0.90 / 0.93

## Validity

- completion (min over cells) 1.000; protocol failures 0.238; tool use on request 1 (min over cells) 1.000; unclassifiable responses 0.000
- run statuses: {'complete': 360}
- cost: {'runs_recorded': 360, 'from_cache': 0, 'agent_calls': 12265, 'equiv_usd': 0.0}
