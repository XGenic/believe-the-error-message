# C4 kill test verdict: INCONCLUSIVE

**LIVE MODEL RUN (study W2-A, deviation W2-7: C4 through OpenRouter, OpenAI gpt-oss-120b on Crusoe bf16, reasoning r1 = {"effort": "low"})**: transport `openrouter_chat_native`, model `openai/gpt-oss-120b`; 30 runs per cell.

- S +0.922 (CI +0.883, +0.961); L* +0.140 (CI +0.029, +0.247)

## Steering (request 1): follow rate of the claim's strategy minus the neutral baseline

| Misleading cell (claim, true fault) | Δ |
|---|---|
| format|transient | 0.967 |
| format|permanent | 0.900 |
| transient|fixable | 0.900 |
| transient|permanent | 0.833 |
| permanent|fixable | 0.967 |
| permanent|transient | 0.967 |

- **S** = 0.922 [0.883, 0.961]

## Learning: follow rate on requests 1–2 minus requests 5–6

| Cell | Kind | L |
|---|---|---|
| format|transient | misleading | -0.017 |
| format|permanent | misleading | 0.496 |
| transient|fixable | misleading | 0.512 |
| transient|permanent | misleading | 0.442 |
| permanent|fixable | misleading | 0.252 |
| permanent|transient | misleading | 0.269 |
| format|fixable | accurate | -0.029 |
| transient|transient | accurate | 0.438 |
| permanent|permanent | accurate | 0.355 |

- format|transient is excluded from L\*: obeying the format claim succeeds there (any third call does), so outcomes never contradict it.

- **L\*** = mean misleading L (five cells) − mean accurate L = 0.140 [0.029, 0.247]

## Per cell (secondary)

| Cell | Runs | First response, request 1 | First response, requests 5–6 | Success by request | Calls, requests 5–6 | UNKNOWN | Unsupported |
|---|---|---|---|---|---|---|---|
| format|fixable | 30 | {'REFORMAT': 27, 'SITE_ONLY': 3} | {'REFORMAT': 42, 'SITE_ONLY': 1} | 0.90 / 0.87 / 0.80 / 0.83 / 0.83 / 0.77 | 2.750 | 0.183 | 0 |
| format|transient | 30 | {'REFORMAT': 29, 'SITE_ONLY': 1} | {'REFORMAT': 60} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3 | 0.017 | 0 |
| format|permanent | 30 | {'REFORMAT': 27, 'RETRY': 1, 'SITE_ONLY': 2} | {'REFORMAT': 21, 'STOP': 24, 'OTHER': 2, 'SITE_ONLY': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.433 | 0.878 | 22 |
| transient|fixable | 30 | {'RETRY': 29, 'OTHER': 1} | {'STOP': 24, 'RETRY': 1, 'SITE_ONLY': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 0.467 | 0.894 | 19 |
| transient|transient | 30 | {'OTHER': 1, 'RETRY': 29} | {'REFORMAT': 4, 'RETRY': 15, 'STOP': 18, 'SITE_ONLY': 10, 'OTHER': 1} | 0.43 / 0.47 / 0.47 / 0.47 / 0.47 / 0.47 | 1.783 | 0.489 | 10 |
| transient|permanent | 30 | {'RETRY': 25, 'STOP': 5} | {'STOP': 20, 'OTHER': 1, 'RETRY': 3} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 0.467 | 0.928 | 13 |
| permanent|fixable | 30 | {'STOP': 29, 'SITE_ONLY': 1} | {'SITE_ONLY': 4, 'STOP': 25, 'OTHER': 5, 'REFORMAT': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 0.767 | 0.922 | 14 |
| permanent|transient | 30 | {'STOP': 29, 'SITE_ONLY': 1} | {'SITE_ONLY': 10, 'REFORMAT': 2, 'STOP': 30} | 0.00 / 0.00 / 0.07 / 0.03 / 0.07 / 0.03 | 0.950 | 0.906 | 11 |
| permanent|permanent | 30 | {'STOP': 29, 'SITE_ONLY': 1} | {'OTHER': 6, 'SITE_ONLY': 6, 'STOP': 22, 'REFORMAT': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 0.817 | 0.900 | 18 |
| neutral|fixable | 30 | {'SITE_ONLY': 28, 'RETRY': 2} | {'SITE_ONLY': 8, 'STOP': 17, 'OTHER': 1, 'RETRY': 3, 'REFORMAT': 2} | 0.10 / 0.00 / 0.03 / 0.00 / 0.00 / 0.03 | 0.983 | 0.894 | 12 |
| neutral|transient | 30 | {'SITE_ONLY': 30} | {'REFORMAT': 25, 'RETRY': 7, 'SITE_ONLY': 26, 'OTHER': 2} | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3.017 | 0.022 | 0 |
| neutral|permanent | 30 | {'SITE_ONLY': 30} | {'STOP': 22, 'RETRY': 2, 'SITE_ONLY': 6, 'UNCLASSIFIABLE': 1, 'OTHER': 1} | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 0.950 | 0.883 | 15 |

## H3 (stability → expectancy): calls on requests 5–6, 'unavailable' minus 'temporary' claim

- true fault fixable: 0.300 (0.767 vs 0.467)
- true fault transient: -0.833 (0.950 vs 1.783)
- true fault permanent: 0.350 (0.817 vs 0.467)

## Superstition probe (format claim over a transient fault)

- requests 2–6 whose first call already changes the SKU spelling: format claim 0.447, neutral message 0.153; index 0.293

## H4 (talked out of a fixable fault): success by request in permanent|fixable: 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00

## Validity

- completion (min over cells) 1.000; protocol failures 0.067; tool use on request 1 (min over cells) 1.000; unclassifiable responses 0.001
- run statuses: {'complete': 360, 'failed': 4}
- cost: {'runs_recorded': 364, 'from_cache': 0, 'agent_calls': 7003, 'equiv_usd': 0.4151}
