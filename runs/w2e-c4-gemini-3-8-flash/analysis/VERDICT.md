# C4 kill test verdict: CONTINUE_CREDULOUS

**LIVE MODEL RUN (study W2-E: C4, gemini-3.8-flash through OpenRouter, reasoning medium, flex tier)**: transport `openrouter_chat_native`, model `google/gemini-3.8-flash`; 30 runs per cell.

- S +0.628 (CI +0.600, +0.656); L* -0.059 (CI -0.169, +0.059)

## Steering (request 1): follow rate of the claim's strategy minus the neutral baseline

| Misleading cell (claim, true fault) | Δ |
|---|---|
| format|transient | 1.000 |
| format|permanent | 0.967 |
| transient|fixable | 0.933 |
| transient|permanent | 0.867 |
| permanent|fixable | 0.000 |
| permanent|transient | 0.000 |

- **S** = 0.628 [0.600, 0.656]

## Learning: follow rate on requests 1–2 minus requests 5–6

| Cell | Kind | L |
|---|---|---|
| format|transient | misleading | 0.083 |
| format|permanent | misleading | 0.167 |
| transient|fixable | misleading | -0.017 |
| transient|permanent | misleading | 0.000 |
| permanent|fixable | misleading | -0.467 |
| permanent|transient | misleading | -0.300 |
| format|fixable | accurate | 0.124 |
| transient|transient | accurate | 0.167 |
| permanent|permanent | accurate | -0.483 |

- format|transient is excluded from L\*: obeying the format claim succeeds there (any third call does), so outcomes never contradict it.

- **L\*** = mean misleading L (five cells) − mean accurate L = -0.059 [-0.169, 0.059]

## Per cell (secondary)

| Cell | Runs | First response, request 1 | First response, requests 5–6 | Success by request | Calls, requests 5–6 | UNKNOWN | Unsupported |
|---|---|---|---|---|---|---|---|
| format|fixable | 30 | {'REFORMAT': 30} | {'REFORMAT': 6, 'OTHER': 1} | 0.90 / 0.97 / 1.00 / 1.00 / 0.97 / 0.93 | 1.350 | 0.039 | 0 |
| format|transient | 30 | {'REFORMAT': 30} | {'REFORMAT': 53, 'OTHER': 2, 'SITE_ONLY': 2, 'RETRY': 3} | 1.00 / 0.97 / 1.00 / 1.00 / 1.00 / 1.00 | 3.083 | 0.022 | 0 |
| format|permanent | 30 | {'REFORMAT': 29, 'OTHER': 1} | {'REFORMAT': 39, 'OTHER': 16, 'STOP': 5} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.500 | 1.000 | 0 |
| transient|fixable | 30 | {'RETRY': 28, 'SITE_ONLY': 2} | {'RETRY': 58, 'REFORMAT': 1, 'SITE_ONLY': 1} | 0.03 / 0.00 / 0.03 / 0.00 / 0.00 / 0.00 | 5.933 | 0.978 | 2 |
| transient|transient | 30 | {'RETRY': 28, 'SITE_ONLY': 2} | {'SITE_ONLY': 13, 'RETRY': 47} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3 | 0.000 | 0 |
| transient|permanent | 30 | {'RETRY': 26, 'SITE_ONLY': 4} | {'RETRY': 55, 'SITE_ONLY': 5} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 6 | 1.000 | 0 |
| permanent|fixable | 30 | {'SITE_ONLY': 30} | {'STOP': 33, 'SITE_ONLY': 27} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.450 | 1.000 | 0 |
| permanent|transient | 30 | {'SITE_ONLY': 29, 'OTHER': 1} | {'RETRY': 14, 'SITE_ONLY': 25, 'STOP': 21} | 0.60 / 0.63 / 0.60 / 0.60 / 0.60 / 0.60 | 2.250 | 0.406 | 0 |
| permanent|permanent | 30 | {'SITE_ONLY': 30} | {'SITE_ONLY': 25, 'STOP': 35} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.450 | 1.000 | 0 |
| neutral|fixable | 30 | {'SITE_ONLY': 30} | {'SITE_ONLY': 18, 'STOP': 26, 'OTHER': 2, 'REFORMAT': 5} | 0.47 / 0.43 / 0.40 / 0.30 / 0.30 / 0.27 | 1.633 | 0.750 | 0 |
| neutral|transient | 30 | {'SITE_ONLY': 30} | {'RETRY': 43, 'REFORMAT': 9, 'SITE_ONLY': 8} | 1.00 / 0.97 / 1.00 / 0.97 / 1.00 / 1.00 | 3 | 0.017 | 0 |
| neutral|permanent | 30 | {'SITE_ONLY': 30} | {'STOP': 38, 'SITE_ONLY': 22} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.367 | 1.000 | 0 |

## H3 (stability → expectancy): calls on requests 5–6, 'unavailable' minus 'temporary' claim

- true fault fixable: -4.483 (1.450 vs 5.933)
- true fault transient: -0.750 (2.250 vs 3)
- true fault permanent: -4.550 (1.450 vs 6)

## Superstition probe (format claim over a transient fault)

- requests 2–6 whose first call already changes the SKU spelling: format claim 0.600, neutral message 0.293; index 0.307

## H4 (talked out of a fixable fault): success by request in permanent|fixable: 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00

## Validity

- completion (min over cells) 1.000; protocol failures 0.000; tool use on request 1 (min over cells) 1.000; unclassifiable responses 0.000
- run statuses: {'complete': 360}
- cost: {'runs_recorded': 360, 'from_cache': 0, 'agent_calls': 9421, 'equiv_usd': 11.0251}
