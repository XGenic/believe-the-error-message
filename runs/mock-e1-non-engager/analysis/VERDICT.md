# C4 extension E1 verdict: INVALID

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-e1-non_engager`; 18 requests per run, 12 runs per cell.

- tool use on request 1 0.0 below 0.9 in some cell: agents did not engage
- unclassifiable responses None above 0.1
- L_E1 could not be computed

## Primary: change in following the claim, requests 1–3 minus the last three

| Cell | L |
|---|---|
| transient|fixable | n/a |
| transient|transient | n/a |
| permanent|transient | n/a |
| permanent|permanent | n/a |

| Claim: misleading vs accurate fault | L(misleading) − L(accurate) |
|---|---|
| permanent: transient vs permanent | n/a |
| transient: fixable vs transient | n/a |

- **L_E1** (mean over claims) = n/a [n/a, n/a]

## Curves by request (bins 1–3 / 4–6 / 7–9 / 10–12 / 13–15 / 16–18)

| Cell | Kind | Follows the claim | Success | Calls per request | Runs ever deviating | Runs ever reformatting |
|---|---|---|---|---|---|---|
| transient|fixable | misleading | n/a / n/a / n/a / n/a / n/a / n/a | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 0/12 | 0/12 |
| transient|transient | accurate | n/a / n/a / n/a / n/a / n/a / n/a | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 0/12 | 0/12 |
| permanent|transient | misleading | n/a / n/a / n/a / n/a / n/a / n/a | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 0/12 | 0/12 |
| permanent|permanent | accurate | n/a / n/a / n/a / n/a / n/a / n/a | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 0/12 | 0/12 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.000; tool use on request 1 (min) 0.000; unclassifiable n/a
- run statuses: {'complete': 48}
- cost: {'runs_recorded': 48, 'from_cache': 0, 'agent_calls': 864, 'equiv_usd': 0.0}
