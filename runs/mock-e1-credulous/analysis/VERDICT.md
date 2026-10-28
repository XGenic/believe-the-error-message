# C4 extension E1 verdict: NO_LEARNING

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-e1-credulous`; 18 requests per run, 12 runs per cell.

- L_E1 -0.028 (CI -0.139, +0.069)

## Primary: change in following the claim, requests 1–3 minus the last three

| Cell | L |
|---|---|
| transient|fixable | 0.056 |
| transient|transient | 0.111 |
| permanent|transient | 0.028 |
| permanent|permanent | 0.028 |

| Claim: misleading vs accurate fault | L(misleading) − L(accurate) |
|---|---|
| permanent: transient vs permanent | 0.000 |
| transient: fixable vs transient | -0.056 |

- **L_E1** (mean over claims) = -0.028 [-0.139, 0.069]

## Curves by request (bins 1–3 / 4–6 / 7–9 / 10–12 / 13–15 / 16–18)

| Cell | Kind | Follows the claim | Success | Calls per request | Runs ever deviating | Runs ever reformatting |
|---|---|---|---|---|---|---|
| transient|fixable | misleading | 0.97 / 0.89 / 0.97 / 0.92 / 0.94 / 0.92 | 0.03 / 0.08 / 0.03 / 0.06 / 0.03 / 0.06 | 5.89 / 5.61 / 5.92 / 5.67 / 5.75 / 5.67 | 9/12 | 8/12 |
| transient|transient | accurate | 0.97 / 0.94 / 0.97 / 0.94 / 0.94 / 0.86 | 0.97 / 0.97 / 0.97 / 0.97 / 0.94 / 0.92 | 2.94 / 2.94 / 2.94 / 2.94 / 2.89 / 2.83 | 7/12 | 4/12 |
| permanent|transient | misleading | 1.00 / 0.89 / 0.94 / 0.94 / 0.94 / 0.97 | 0.00 / 0.03 / 0.03 / 0.00 / 0.03 / 0.03 | 1.00 / 1.14 / 1.08 / 1.06 / 1.08 / 1.06 | 7/12 | 4/12 |
| permanent|permanent | accurate | 0.97 / 0.94 / 0.89 / 0.92 / 0.97 / 0.94 | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.08 / 1.17 / 1.22 / 1.19 / 1.08 / 1.11 | 9/12 | 6/12 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.000; tool use on request 1 (min) 1.000; unclassifiable 0.000
- run statuses: {'complete': 48}
- cost: {'runs_recorded': 48, 'from_cache': 0, 'agent_calls': 3214, 'equiv_usd': 0.0}
