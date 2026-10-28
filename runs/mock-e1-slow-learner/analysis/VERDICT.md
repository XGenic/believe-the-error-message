# C4 extension E1 verdict: LEARNS

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-e1-slow_learner`; 18 requests per run, 12 runs per cell.

- L_E1 +0.847 (CI +0.736, +0.944)

## Primary: change in following the claim, requests 1–3 minus the last three

| Cell | L |
|---|---|
| transient|fixable | 0.861 |
| transient|transient | 0.111 |
| permanent|transient | 0.972 |
| permanent|permanent | 0.028 |

| Claim: misleading vs accurate fault | L(misleading) − L(accurate) |
|---|---|
| permanent: transient vs permanent | 0.944 |
| transient: fixable vs transient | 0.750 |

- **L_E1** (mean over claims) = 0.847 [0.736, 0.944]

## Curves by request (bins 1–3 / 4–6 / 7–9 / 10–12 / 13–15 / 16–18)

| Cell | Kind | Follows the claim | Success | Calls per request | Runs ever deviating | Runs ever reformatting |
|---|---|---|---|---|---|---|
| transient|fixable | misleading | 0.97 / 0.89 / 0.17 / 0.03 / 0.06 / 0.11 | 0.03 / 0.08 / 0.89 / 0.92 / 0.92 / 0.89 | 5.89 / 5.61 / 3.39 / 2.86 / 3.00 / 2.81 | 12/12 | 12/12 |
| transient|transient | accurate | 0.97 / 0.94 / 0.97 / 0.94 / 0.94 / 0.86 | 0.97 / 0.97 / 0.97 / 0.97 / 0.94 / 0.92 | 2.94 / 2.94 / 2.94 / 2.94 / 2.89 / 2.83 | 7/12 | 4/12 |
| permanent|transient | misleading | 1.00 / 0.89 / 0.06 / 0.00 / 0.00 / 0.03 | 0.00 / 0.03 / 0.94 / 1.00 / 1.00 / 0.97 | 1.00 / 1.14 / 2.89 / 3.00 / 3.00 / 2.94 | 12/12 | 12/12 |
| permanent|permanent | accurate | 0.97 / 0.94 / 0.64 / 0.92 / 0.97 / 0.94 | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.08 / 1.17 / 2.47 / 1.19 / 1.08 / 1.11 | 12/12 | 12/12 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.000; tool use on request 1 (min) 1.000; unclassifiable 0.000
- run statuses: {'complete': 48}
- cost: {'runs_recorded': 48, 'from_cache': 0, 'agent_calls': 3137, 'equiv_usd': 0.0}
