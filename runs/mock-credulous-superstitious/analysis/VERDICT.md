# C4 kill test verdict: CONTINUE_CREDULOUS

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-credulous-superstitious`; 30 runs per cell.

- S +0.633 (CI +0.600, +0.661); L* +0.016 (CI -0.058, +0.090)

## Steering (request 1): follow rate of the claim's strategy minus the neutral baseline

| Misleading cell (claim, true fault) | Δ |
|---|---|
| format|transient | 1.000 |
| format|permanent | 0.900 |
| transient|fixable | -0.033 |
| transient|permanent | 0.100 |
| permanent|fixable | 0.933 |
| permanent|transient | 0.900 |

- **S** = 0.633 [0.600, 0.661]

## Learning: follow rate on requests 1–2 minus requests 5–6

| Cell | Kind | L |
|---|---|---|
| format|transient | misleading | 0.133 |
| format|permanent | misleading | 0.033 |
| transient|fixable | misleading | 0.102 |
| transient|permanent | misleading | -0.017 |
| permanent|fixable | misleading | -0.011 |
| permanent|transient | misleading | 0.000 |
| format|fixable | accurate | -0.033 |
| transient|transient | accurate | 0.033 |
| permanent|permanent | accurate | 0.017 |

- format|transient is excluded from L\*: obeying the format claim succeeds there (any third call does), so outcomes never contradict it.

- **L\*** = mean misleading L (five cells) − mean accurate L = 0.016 [-0.058, 0.090]

## Per cell (secondary)

| Cell | Runs | First response, request 1 | First response, requests 5–6 | Success by request | Calls, requests 5–6 | UNKNOWN | Unsupported |
|---|---|---|---|---|---|---|---|
| format|fixable | 30 | {'REFORMAT': 27, 'RETRY': 2, 'STOP': 1} | {'REFORMAT': 47, 'STOP': 2, 'RETRY': 1} | 0.97 / 1.00 / 0.97 / 0.93 / 0.93 / 1.00 | 2.250 | 0.033 | 0 |
| format|transient | 30 | {'REFORMAT': 30} | {'STOP': 5, 'REFORMAT': 52, 'RETRY': 3} | 1.00 / 1.00 / 1.00 / 0.97 / 0.93 / 0.90 | 2.833 | 0.033 | 0 |
| format|permanent | 30 | {'REFORMAT': 29, 'RETRY': 1} | {'REFORMAT': 56, 'STOP': 1, 'RETRY': 3} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 4 | 1.000 | 0 |
| transient|fixable | 30 | {'RETRY': 29, 'REFORMAT': 1} | {'RETRY': 51, 'STOP': 4, 'REFORMAT': 4} | 0.03 / 0.03 / 0.03 / 0.07 / 0.03 / 0.13 | 5.383 | 0.944 | 0 |
| transient|transient | 30 | {'RETRY': 28, 'REFORMAT': 2} | {'STOP': 6, 'RETRY': 52, 'REFORMAT': 2} | 1.00 / 0.93 / 1.00 / 0.97 / 0.90 / 0.90 | 2.800 | 0.050 | 0 |
| transient|permanent | 30 | {'RETRY': 29, 'REFORMAT': 1} | {'RETRY': 56, 'STOP': 3, 'REFORMAT': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.750 | 1.000 | 0 |
| permanent|fixable | 30 | {'STOP': 28, 'REFORMAT': 2} | {'RETRY': 4, 'STOP': 51} | 0.07 / 0.10 / 0.13 / 0.07 / 0.07 / 0.10 | 1.067 | 0.911 | 0 |
| permanent|transient | 30 | {'STOP': 27, 'REFORMAT': 2, 'RETRY': 1} | {'STOP': 55, 'REFORMAT': 2, 'RETRY': 3} | 0.07 / 0.03 / 0.00 / 0.07 / 0.03 / 0.03 | 1.117 | 0.961 | 0 |
| permanent|permanent | 30 | {'STOP': 27, 'RETRY': 2, 'REFORMAT': 1} | {'STOP': 55, 'REFORMAT': 3, 'RETRY': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.183 | 1.000 | 0 |
| neutral|fixable | 30 | {'RETRY': 30} | {'RETRY': 55, 'REFORMAT': 3, 'STOP': 1} | 0.00 / 0.00 / 0.03 / 0.03 / 0.03 / 0.10 | 5.667 | 0.967 | 0 |
| neutral|transient | 30 | {'RETRY': 30} | {'REFORMAT': 1, 'RETRY': 58, 'STOP': 1} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 0.97 | 2.967 | 0.006 | 0 |
| neutral|permanent | 30 | {'RETRY': 26, 'STOP': 2, 'REFORMAT': 2} | {'RETRY': 56, 'REFORMAT': 2, 'STOP': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.833 | 1.000 | 0 |

## H3 (stability → expectancy): calls on requests 5–6, 'unavailable' minus 'temporary' claim

- true fault fixable: -4.317 (1.067 vs 5.383)
- true fault transient: -1.683 (1.117 vs 2.800)
- true fault permanent: -4.567 (1.183 vs 5.750)

## Superstition probe (format claim over a transient fault)

- requests 2–6 whose first call already changes the SKU spelling: format claim 1.000, neutral message 0.047; index 0.953

## H4 (talked out of a fixable fault): success by request in permanent|fixable: 0.07 / 0.10 / 0.13 / 0.07 / 0.07 / 0.10

## Validity

- completion (min over cells) 1.000; protocol failures 0.000; tool use on request 1 (min over cells) 1.000; unclassifiable responses 0.000
- run statuses: {'complete': 360}
- cost: {'runs_recorded': 360, 'from_cache': 0, 'agent_calls': 9663, 'equiv_usd': 0.0}
