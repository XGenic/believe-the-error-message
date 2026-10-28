# C4 kill test verdict: CONTINUE_CREDULOUS

**LIVE MODEL RUN (study W5: the C4 grid through native tool calls, reasoning medium)**: transport `openai_responses_native`, model `gpt-6-luna`; 30 runs per cell.

- S +0.922 (CI +0.878, +0.961); L* +0.067 (CI +0.013, +0.118)

## Steering (request 1): follow rate of the claim's strategy minus the neutral baseline

| Misleading cell (claim, true fault) | Δ |
|---|---|
| format|transient | 0.933 |
| format|permanent | 0.967 |
| transient|fixable | 1.000 |
| transient|permanent | 0.967 |
| permanent|fixable | 0.800 |
| permanent|transient | 0.867 |

- **S** = 0.922 [0.878, 0.961]

## Learning: follow rate on requests 1–2 minus requests 5–6

| Cell | Kind | L |
|---|---|---|
| format|transient | misleading | -0.033 |
| format|permanent | misleading | 0.017 |
| transient|fixable | misleading | 0.033 |
| transient|permanent | misleading | 0.000 |
| permanent|fixable | misleading | 0.083 |
| permanent|transient | misleading | 0.367 |
| format|fixable | accurate | -0.017 |
| transient|transient | accurate | 0.017 |
| permanent|permanent | accurate | 0.100 |

- format|transient is excluded from L\*: obeying the format claim succeeds there (any third call does), so outcomes never contradict it.

- **L\*** = mean misleading L (five cells) − mean accurate L = 0.067 [0.013, 0.118]

## Per cell (secondary)

| Cell | Runs | First response, request 1 | First response, requests 5–6 | Success by request | Calls, requests 5–6 | UNKNOWN | Unsupported |
|---|---|---|---|---|---|---|---|
| format|fixable | 30 | {'REFORMAT': 29, 'STOP': 1} | {'REFORMAT': 59} | 0.90 / 0.83 / 0.90 / 0.87 / 0.90 / 0.93 | 3.433 | 0.111 | 0 |
| format|transient | 30 | {'REFORMAT': 28, 'STOP': 2} | {'REFORMAT': 60} | 0.93 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3 | 0.011 | 0 |
| format|permanent | 30 | {'REFORMAT': 29, 'STOP': 1} | {'REFORMAT': 55, 'SITE_ONLY': 5} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.967 | 1.000 | 0 |
| transient|fixable | 30 | {'RETRY': 30} | {'RETRY': 58, 'SITE_ONLY': 2} | 0.03 / 0.00 / 0.00 / 0.03 / 0.00 / 0.00 | 5.850 | 0.989 | 0 |
| transient|transient | 30 | {'RETRY': 30} | {'RETRY': 58, 'SITE_ONLY': 2} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3 | 0.000 | 0 |
| transient|permanent | 30 | {'RETRY': 29, 'OTHER': 1} | {'RETRY': 58, 'SITE_ONLY': 1, 'OTHER': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 6 | 1.000 | 0 |
| permanent|fixable | 30 | {'STOP': 30} | {'STOP': 55, 'RETRY': 3, 'SITE_ONLY': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.217 | 1.000 | 0 |
| permanent|transient | 30 | {'STOP': 29, 'SITE_ONLY': 1} | {'STOP': 35, 'RETRY': 8, 'SITE_ONLY': 15, 'REFORMAT': 2} | 0.03 / 0.07 / 0.10 / 0.13 / 0.27 / 0.27 | 1.683 | 0.856 | 0 |
| permanent|permanent | 30 | {'STOP': 30} | {'SITE_ONLY': 5, 'STOP': 53, 'RETRY': 2} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.200 | 1.000 | 0 |
| neutral|fixable | 30 | {'STOP': 6, 'SITE_ONLY': 24} | {'SITE_ONLY': 26, 'REFORMAT': 24, 'STOP': 5, 'RETRY': 1} | 0.23 / 0.23 / 0.23 / 0.30 / 0.30 / 0.27 | 4.333 | 0.739 | 0 |
| neutral|transient | 30 | {'SITE_ONLY': 27, 'STOP': 3} | {'REFORMAT': 27, 'SITE_ONLY': 31, 'STOP': 2} | 0.60 / 0.77 / 0.80 / 0.87 / 0.90 / 0.90 | 2.950 | 0.194 | 0 |
| neutral|permanent | 30 | {'SITE_ONLY': 28, 'STOP': 2} | {'SITE_ONLY': 47, 'REFORMAT': 7, 'STOP': 5, 'OTHER': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 4.983 | 1.000 | 0 |

## H3 (stability → expectancy): calls on requests 5–6, 'unavailable' minus 'temporary' claim

- true fault fixable: -4.633 (1.217 vs 5.850)
- true fault transient: -1.317 (1.683 vs 3)
- true fault permanent: -4.800 (1.200 vs 6)

## Superstition probe (format claim over a transient fault)

- requests 2–6 whose first call already changes the SKU spelling: format claim 0.020, neutral message 0.320; index -0.300

## H4 (talked out of a fixable fault): success by request in permanent|fixable: 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00

## Validity

- completion (min over cells) 1.000; protocol failures 0.000; tool use on request 1 (min over cells) 1.000; unclassifiable responses 0.000
- run statuses: {'complete': 360}
- cost: {'runs_recorded': 360, 'from_cache': 0, 'agent_calls': 9794, 'equiv_usd': 1.1802}
