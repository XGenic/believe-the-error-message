# C4 kill test verdict: KILL_WORDING_IRRELEVANT

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-message_blind`; 30 runs per cell.

- S +0.028 (CI -0.006, +0.061); L* +0.031 (CI -0.021, +0.087)

## Steering (request 1): follow rate of the claim's strategy minus the neutral baseline

| Misleading cell (claim, true fault) | Δ |
|---|---|
| format|transient | 0.067 |
| format|permanent | 0.033 |
| transient|fixable | 0.067 |
| transient|permanent | 0.000 |
| permanent|fixable | 0.000 |
| permanent|transient | 0.000 |

- **S** = 0.028 [-0.006, 0.061]

## Learning: follow rate on requests 1–2 minus requests 5–6

| Cell | Kind | L |
|---|---|---|
| format|transient | misleading | 0.133 |
| format|permanent | misleading | 0.033 |
| transient|fixable | misleading | 0.017 |
| transient|permanent | misleading | -0.017 |
| permanent|fixable | misleading | -0.050 |
| permanent|transient | misleading | -0.050 |
| format|fixable | accurate | 0.000 |
| transient|transient | accurate | -0.083 |
| permanent|permanent | accurate | -0.050 |

- format|transient is excluded from L\*: obeying the format claim succeeds there (any third call does), so outcomes never contradict it.

- **L\*** = mean misleading L (five cells) − mean accurate L = 0.031 [-0.021, 0.087]

## Per cell (secondary)

| Cell | Runs | First response, request 1 | First response, requests 5–6 | Success by request | Calls, requests 5–6 | UNKNOWN | Unsupported |
|---|---|---|---|---|---|---|---|
| format|fixable | 30 | {'REFORMAT': 27, 'RETRY': 2, 'STOP': 1} | {'REFORMAT': 55, 'RETRY': 3, 'STOP': 2} | 0.97 / 1.00 / 0.90 / 0.97 / 0.97 / 0.97 | 3.033 | 0.039 | 0 |
| format|transient | 30 | {'REFORMAT': 30} | {'STOP': 5, 'REFORMAT': 52, 'RETRY': 3} | 1.00 / 1.00 / 1.00 / 0.97 / 0.93 / 0.90 | 2.833 | 0.033 | 0 |
| format|permanent | 30 | {'REFORMAT': 29, 'RETRY': 1} | {'REFORMAT': 56, 'STOP': 1, 'RETRY': 3} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 4.983 | 1.000 | 0 |
| transient|fixable | 30 | {'REFORMAT': 27, 'RETRY': 3} | {'REFORMAT': 54, 'STOP': 4, 'RETRY': 2} | 1.00 / 1.00 / 0.93 / 0.97 / 0.90 / 0.97 | 2.833 | 0.039 | 0 |
| transient|transient | 30 | {'REFORMAT': 30} | {'STOP': 6, 'RETRY': 6, 'REFORMAT': 48} | 1.00 / 0.93 / 1.00 / 0.97 / 0.90 / 0.90 | 2.800 | 0.050 | 0 |
| transient|permanent | 30 | {'REFORMAT': 30} | {'REFORMAT': 55, 'STOP': 3, 'RETRY': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 4.833 | 1.000 | 0 |
| permanent|fixable | 30 | {'REFORMAT': 30} | {'RETRY': 4, 'REFORMAT': 53, 'STOP': 3} | 1.00 / 1.00 / 0.97 / 0.97 / 0.93 / 0.97 | 2.883 | 0.028 | 0 |
| permanent|transient | 30 | {'REFORMAT': 29, 'RETRY': 1} | {'REFORMAT': 54, 'STOP': 3, 'RETRY': 3} | 1.00 / 1.00 / 0.93 / 0.97 / 0.97 / 0.93 | 2.900 | 0.033 | 0 |
| permanent|permanent | 30 | {'REFORMAT': 28, 'RETRY': 2} | {'REFORMAT': 55, 'RETRY': 2, 'STOP': 3} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 4.833 | 1.000 | 0 |
| neutral|fixable | 30 | {'REFORMAT': 29, 'RETRY': 1} | {'REFORMAT': 56, 'RETRY': 3, 'STOP': 1} | 1.00 / 0.97 / 1.00 / 1.00 / 0.97 / 1.00 | 2.950 | 0.011 | 0 |
| neutral|transient | 30 | {'REFORMAT': 28, 'RETRY': 2} | {'REFORMAT': 59, 'STOP': 1} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 0.97 | 2.967 | 0.006 | 0 |
| neutral|permanent | 30 | {'REFORMAT': 28, 'STOP': 2} | {'REFORMAT': 58, 'STOP': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 4.867 | 1.000 | 0 |

## H3 (stability → expectancy): calls on requests 5–6, 'unavailable' minus 'temporary' claim

- true fault fixable: 0.050 (2.883 vs 2.833)
- true fault transient: 0.100 (2.900 vs 2.800)
- true fault permanent: 0.000 (4.833 vs 4.833)

## Superstition probe (format claim over a transient fault)

- requests 2–6 whose first call already changes the SKU spelling: format claim 0.000, neutral message 0.000; index 0.000

## H4 (talked out of a fixable fault): success by request in permanent|fixable: 1.00 / 1.00 / 0.97 / 0.97 / 0.93 / 0.97

## Validity

- completion (min over cells) 1.000; protocol failures 0.000; tool use on request 1 (min over cells) 1.000; unclassifiable responses 0.000
- run statuses: {'complete': 360}
- cost: {'runs_recorded': 360, 'from_cache': 0, 'agent_calls': 9964, 'equiv_usd': 0.0}
