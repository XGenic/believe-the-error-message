# C4 kill test verdict: INVALID

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-non_engager`; 30 runs per cell.

- tool use on request 1 0.0 below 0.9 in some cell: agents did not engage
- unclassifiable responses None above 0.1
- S or L* could not be computed (a cell had no classified responses)

## Steering (request 1): follow rate of the claim's strategy minus the neutral baseline

| Misleading cell (claim, true fault) | Δ |
|---|---|
| format|transient | n/a |
| format|permanent | n/a |
| transient|fixable | n/a |
| transient|permanent | n/a |
| permanent|fixable | n/a |
| permanent|transient | n/a |

- **S** = n/a [n/a, n/a]

## Learning: follow rate on requests 1–2 minus requests 5–6

| Cell | Kind | L |
|---|---|---|
| format|transient | misleading | n/a |
| format|permanent | misleading | n/a |
| transient|fixable | misleading | n/a |
| transient|permanent | misleading | n/a |
| permanent|fixable | misleading | n/a |
| permanent|transient | misleading | n/a |
| format|fixable | accurate | n/a |
| transient|transient | accurate | n/a |
| permanent|permanent | accurate | n/a |

- format|transient is excluded from L\*: obeying the format claim succeeds there (any third call does), so outcomes never contradict it.

- **L\*** = mean misleading L (five cells) − mean accurate L = n/a [n/a, n/a]

## Per cell (secondary)

| Cell | Runs | First response, request 1 | First response, requests 5–6 | Success by request | Calls, requests 5–6 | UNKNOWN | Unsupported |
|---|---|---|---|---|---|---|---|
| format|fixable | 30 | {} | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 0 | 1.000 | 0 |
| format|transient | 30 | {} | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 0 | 1.000 | 0 |
| format|permanent | 30 | {} | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 0 | 1.000 | 0 |
| transient|fixable | 30 | {} | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 0 | 1.000 | 0 |
| transient|transient | 30 | {} | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 0 | 1.000 | 0 |
| transient|permanent | 30 | {} | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 0 | 1.000 | 0 |
| permanent|fixable | 30 | {} | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 0 | 1.000 | 0 |
| permanent|transient | 30 | {} | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 0 | 1.000 | 0 |
| permanent|permanent | 30 | {} | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 0 | 1.000 | 0 |
| neutral|fixable | 30 | {} | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 0 | 1.000 | 0 |
| neutral|transient | 30 | {} | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 0 | 1.000 | 0 |
| neutral|permanent | 30 | {} | {} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 0 | 1.000 | 0 |

## H3 (stability → expectancy): calls on requests 5–6, 'unavailable' minus 'temporary' claim

- true fault fixable: 0 (0 vs 0)
- true fault transient: 0 (0 vs 0)
- true fault permanent: 0 (0 vs 0)

## Superstition probe (format claim over a transient fault)

- requests 2–6 whose first call already changes the SKU spelling: format claim 0.000, neutral message 0.000; index 0.000

## H4 (talked out of a fixable fault): success by request in permanent|fixable: 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00

## Validity

- completion (min over cells) 1.000; protocol failures 0.000; tool use on request 1 (min over cells) 0.000; unclassifiable responses n/a
- run statuses: {'complete': 360}
- cost: {'runs_recorded': 360, 'from_cache': 0, 'agent_calls': 2160, 'equiv_usd': 0.0}
