# C4 extension E1 verdict: NO_LEARNING

**LIVE MODEL RUN (extension E1)**: transport `openai_responses`, model `gpt-6-luna`; 18 requests per run, 12 runs per cell.

- L_E1 +0.000 (CI +0.000, +0.000)

## Primary: change in following the claim, requests 1–3 minus the last three

| Cell | L |
|---|---|
| transient|fixable | 0.000 |
| transient|transient | 0.000 |
| permanent|transient | 0.000 |
| permanent|permanent | 0.000 |

| Claim: misleading vs accurate fault | L(misleading) − L(accurate) |
|---|---|
| permanent: transient vs permanent | 0.000 |
| transient: fixable vs transient | 0.000 |

- **L_E1** (mean over claims) = 0.000 [0.000, 0.000]

## Curves by request (bins 1–3 / 4–6 / 7–9 / 10–12 / 13–15 / 16–18)

| Cell | Kind | Follows the claim | Success | Calls per request | Runs ever deviating | Runs ever reformatting |
|---|---|---|---|---|---|---|
| transient|fixable | misleading | 1.00 / 1.00 / 0.97 / 1.00 / 1.00 / 1.00 | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.83 / 5.83 / 5.56 / 5.69 / 5.42 / 5.39 | 1/12 | 0/12 |
| transient|transient | accurate | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3.00 / 3.00 / 3.00 / 3.00 / 3.03 / 3.00 | 0/12 | 0/12 |
| permanent|transient | misleading | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 0/12 | 0/12 |
| permanent|permanent | accurate | 1.00 / 1.00 / 0.97 / 0.92 / 1.00 / 1.00 | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.00 / 1.00 / 1.03 / 1.08 / 1.00 / 1.00 | 4/12 | 0/12 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.011; tool use on request 1 (min) 1.000; unclassifiable 0.000
- run statuses: {'complete': 48}
- cost: {'runs_recorded': 48, 'from_cache': 0, 'agent_calls': 3199, 'equiv_usd': 0.6626}
