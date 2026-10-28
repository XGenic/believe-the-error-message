# C4 extension E1 verdict: ENTRENCHMENT

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-e1-entrencher`; 18 requests per run, 12 runs per cell.

- L_E1 -0.319 (CI -0.500, -0.153)

## Primary: change in following the claim, requests 1–3 minus the last three

| Cell | L |
|---|---|
| transient|fixable | -0.417 |
| transient|transient | 0.056 |
| permanent|transient | -0.583 |
| permanent|permanent | -0.417 |

| Claim: misleading vs accurate fault | L(misleading) − L(accurate) |
|---|---|
| permanent: transient vs permanent | -0.167 |
| transient: fixable vs transient | -0.472 |

- **L_E1** (mean over claims) = -0.319 [-0.500, -0.153]

## Curves by request (bins 1–3 / 4–6 / 7–9 / 10–12 / 13–15 / 16–18)

| Cell | Kind | Follows the claim | Success | Calls per request | Runs ever deviating | Runs ever reformatting |
|---|---|---|---|---|---|---|
| transient|fixable | misleading | 0.50 / 0.44 / 0.58 / 0.69 / 0.94 / 0.92 | 0.56 / 0.53 / 0.47 / 0.28 / 0.03 / 0.06 | 4.47 / 4.25 / 4.67 / 5.00 / 5.75 / 5.67 | 12/12 | 12/12 |
| transient|transient | accurate | 0.42 / 0.42 / 0.36 / 0.31 / 0.31 / 0.36 | 0.97 / 0.97 / 0.97 / 0.97 / 0.94 / 0.92 | 2.94 / 2.94 / 2.94 / 2.94 / 2.89 / 2.83 | 12/12 | 12/12 |
| permanent|transient | misleading | 0.36 / 0.28 / 0.56 / 0.72 / 0.86 / 0.94 | 0.64 / 0.67 / 0.42 / 0.22 / 0.11 / 0.06 | 2.28 / 2.39 / 1.86 / 1.50 / 1.25 / 1.11 | 12/12 | 12/12 |
| permanent|permanent | accurate | 0.53 / 0.67 / 0.86 / 0.92 / 0.97 / 0.94 | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 2.86 / 2.28 / 1.44 / 1.19 / 1.08 / 1.11 | 12/12 | 12/12 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.000; tool use on request 1 (min) 1.000; unclassifiable 0.000
- run statuses: {'complete': 48}
- cost: {'runs_recorded': 48, 'from_cache': 0, 'agent_calls': 3300, 'equiv_usd': 0.0}
