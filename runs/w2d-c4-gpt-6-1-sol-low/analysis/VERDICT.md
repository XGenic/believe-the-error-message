# C4 kill test verdict: CONTINUE_CREDULOUS

**LIVE MODEL RUN (study W2-D: the C4 grid, gpt-6.1-sol, native tool calls, reasoning low)**: transport `openai_responses_native`, model `gpt-6.1-sol`; 30 runs per cell.

- S +0.667 (CI +0.667, +0.667); L* +0.020 (CI +0.003, +0.043)

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
| format|permanent | misleading | 0.100 |
| transient|fixable | misleading | 0.000 |
| transient|permanent | misleading | 0.000 |
| permanent|fixable | misleading | 0.000 |
| permanent|transient | misleading | 0.000 |
| format|fixable | accurate | 0.000 |
| transient|transient | accurate | 0.000 |
| permanent|permanent | accurate | 0.000 |

- format|transient is excluded from L\*: obeying the format claim succeeds there (any third call does), so outcomes never contradict it.

- **L\*** = mean misleading L (five cells) − mean accurate L = 0.020 [0.003, 0.043]

## Per cell (secondary)

| Cell | Runs | First response, request 1 | First response, requests 5–6 | Success by request | Calls, requests 5–6 | UNKNOWN | Unsupported |
|---|---|---|---|---|---|---|---|
| format|fixable | 30 | {'REFORMAT': 30} | {'REFORMAT': 5} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 1.200 | 0.000 | 0 |
| format|transient | 30 | {'REFORMAT': 30} | {'REFORMAT': 60} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3 | 0.000 | 0 |
| format|permanent | 30 | {'REFORMAT': 30} | {'REFORMAT': 54, 'STOP': 6} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.117 | 1.000 | 0 |
| transient|fixable | 30 | {'RETRY': 30} | {'RETRY': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 6 | 1.000 | 0 |
| transient|transient | 30 | {'RETRY': 30} | {'RETRY': 60} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3 | 0.000 | 0 |
| transient|permanent | 30 | {'RETRY': 30} | {'RETRY': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 6 | 1.000 | 0 |
| permanent|fixable | 30 | {'STOP': 30} | {'STOP': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1 | 1.000 | 0 |
| permanent|transient | 30 | {'STOP': 30} | {'STOP': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1 | 1.000 | 0 |
| permanent|permanent | 30 | {'STOP': 30} | {'STOP': 60} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1 | 1.000 | 0 |
| neutral|fixable | 30 | {'RETRY': 30} | {'STOP': 33, 'SITE_ONLY': 25, 'REFORMAT': 2} | 0.03 / 0.00 / 0.00 / 0.00 / 0.00 / 0.03 | 1.517 | 0.989 | 0 |
| neutral|transient | 30 | {'RETRY': 30} | {'SITE_ONLY': 24, 'REFORMAT': 26, 'RETRY': 10} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3 | 0.000 | 0 |
| neutral|permanent | 30 | {'RETRY': 30} | {'STOP': 39, 'SITE_ONLY': 21} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.350 | 1.000 | 0 |

## H3 (stability → expectancy): calls on requests 5–6, 'unavailable' minus 'temporary' claim

- true fault fixable: -5 (1 vs 6)
- true fault transient: -2 (1 vs 3)
- true fault permanent: -5 (1 vs 6)

## Superstition probe (format claim over a transient fault)

- requests 2–6 whose first call already changes the SKU spelling: format claim 0.713, neutral message 0.293; index 0.420

## H4 (talked out of a fixable fault): success by request in permanent|fixable: 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00

## Validity

- completion (min over cells) 1.000; protocol failures 0.000; tool use on request 1 (min over cells) 1.000; unclassifiable responses 0.000
- run statuses: {'complete': 360}
- cost: {'runs_recorded': 360, 'from_cache': 10, 'agent_calls': 8619, 'equiv_usd': 10.0718}
