# C4 extension E1 verdict: NO_LEARNING

**LIVE MODEL RUN (extension E1)**: transport `claude_cli`, model `claude-haiku-5-5`; 18 requests per run, 12 runs per cell.

- L_E1 +0.056 (CI -0.042, +0.167)

## Primary: change in following the claim, requests 1–3 minus the last three

| Cell | L |
|---|---|
| transient|fixable | 0.000 |
| transient|transient | 0.000 |
| permanent|transient | -0.056 |
| permanent|permanent | -0.167 |

| Claim: misleading vs accurate fault | L(misleading) − L(accurate) |
|---|---|
| permanent: transient vs permanent | 0.111 |
| transient: fixable vs transient | 0.000 |

- **L_E1** (mean over claims) = 0.056 [-0.042, 0.167]

## Curves by request (bins 1–3 / 4–6 / 7–9 / 10–12 / 13–15 / 16–18)

| Cell | Kind | Follows the claim | Success | Calls per request | Runs ever deviating | Runs ever reformatting |
|---|---|---|---|---|---|---|
| transient|fixable | misleading | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 5.56 / 5.00 / 4.92 / 4.92 / 4.92 / 4.75 | 0/12 | 0/12 |
| transient|transient | accurate | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 3.00 / 3.00 / 3.00 / 3.00 / 3.00 / 3.00 | 0/12 | 0/12 |
| permanent|transient | misleading | 0.19 / 0.25 / 0.28 / 0.25 / 0.25 / 0.25 | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.81 / 1.75 / 1.72 / 1.75 / 1.75 / 1.75 | 12/12 | 0/12 |
| permanent|permanent | accurate | 0.08 / 0.25 / 0.22 / 0.25 / 0.25 / 0.25 | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | 1.92 / 1.75 / 1.78 / 1.75 / 1.75 / 1.75 | 12/12 | 0/12 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.004; tool use on request 1 (min) 1.000; unclassifiable 0.000
- run statuses: {'complete': 48}
- cost: {'runs_recorded': 48, 'from_cache': 0, 'agent_calls': 3373, 'equiv_usd': 11.5719}
