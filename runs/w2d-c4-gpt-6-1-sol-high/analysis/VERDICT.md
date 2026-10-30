# C4 kill test verdict: CONTINUE_CREDULOUS

**LIVE MODEL RUN (study W2-D: the C4 grid, gpt-6.1-sol, native tool calls, reasoning high)**: transport `openai_responses_native`, model `gpt-6.1-sol`; 30 runs per cell.

- S +0.667 (CI +0.667, +0.667); L* +0.013 (CI +0.000, +0.030)

## Steering (request 1): follow rate of the claim's strategy minus the neutral baseline

| Misleading cell (claim, true fault) | Δ |
|---|---|
| format|transient | 1.000 |
| format|permanent | 1.000 |
| transient|fixable | 0.000 |
| transient|permanent | 0.000 |
| permanent|fixable | 1.000 |
| permanent|transient | 1.000 |

- **S** = 0.667 [0.667, 0.667]

## Learning: follow rate on requests 1–2 minus requests 5–6

| Cell | Kind | L |
|---|---|---|
| format|transient | misleading | 0.000 |
| format|permanent | misleading | 0.067 |
| transient|fixable | misleading | 0.000 |
| transient|permanent | misleading | 0.000 |
| permanent|fixable | misleading | 0.000 |
| permanent|transient | misleading | 0.000 |
| format|fixable | accurate | 0.000 |
| transient|transient | accurate | 0.000 |
| permanent|permanent | accurate | 0.000 |

- format|transient is excluded from L\*: obeying the format claim succeeds there (any third call does), so outcomes never contradict it.

- **L\*** = mean misleading L (five cells) − mean accurate L = 0.013 [0.000, 0.030]

## Per cell (secondary)

| Cell | Runs | First response, request 1 | First response, requests 5–6 | Success by request | Calls, requests 5–6 | UNKNOWN | Unsupported |
|---|---|---|---|---|---|---|---|
| format|fixable | 30 | {'REFORMAT': 30} | {'REFORMAT': 5} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 1.167 | 0.000 | 0 |
| format|transient | 30 | {'REFORMAT': 30} | {'REFORMAT': 60} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3 | 0.000 | 0 |
| format|permanent | 30 | {'REFORMAT': 30} | {'REFORMAT': 56, 'STOP': 4} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.367 | 1.000 | 0 |
| transient|fixable | 30 | {'RETRY': 30} | {'RETRY': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 6 | 1.000 | 0 |
| transient|transient | 30 | {'RETRY': 30} | {'RETRY': 60} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3 | 0.000 | 0 |
| transient|permanent | 30 | {'RETRY': 30} | {'RETRY': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 6 | 1.000 | 0 |
| permanent|fixable | 30 | {'STOP': 30} | {'STOP': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1 | 1.000 | 0 |
| permanent|transient | 30 | {'STOP': 30} | {'STOP': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1 | 1.000 | 0 |
| permanent|permanent | 30 | {'STOP': 30} | {'STOP': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1 | 1.000 | 0 |
| neutral|fixable | 30 | {'RETRY': 30} | {'REFORMAT': 9, 'STOP': 44, 'SITE_ONLY': 6} | 0.17 / 0.00 / 0.07 / 0.00 / 0.03 / 0.07 | 1.717 | 0.944 | 0 |
| neutral|transient | 30 | {'RETRY': 30} | {'REFORMAT': 35, 'SITE_ONLY': 25} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3 | 0.000 | 0 |
| neutral|permanent | 30 | {'RETRY': 30} | {'STOP': 52, 'SITE_ONLY': 8} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.133 | 1.000 | 0 |

## H3 (stability → expectancy): calls on requests 5–6, 'unavailable' minus 'temporary' claim

- true fault fixable: -5 (1 vs 6)
- true fault transient: -2 (1 vs 3)
- true fault permanent: -5 (1 vs 6)

## Superstition probe (format claim over a transient fault)

- requests 2–6 whose first call already changes the SKU spelling: format claim 0.627, neutral message 0.367; index 0.260

## H4 (talked out of a fixable fault): success by request in permanent|fixable: 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00

## Validity

- completion (min over cells) 1.000; protocol failures 0.000; tool use on request 1 (min over cells) 1.000; unclassifiable responses 0.000
- run statuses: {'complete': 360}
- cost: {'runs_recorded': 360, 'from_cache': 0, 'agent_calls': 8640, 'equiv_usd': 10.4995}
