# C4 extension E4 verdict: VALID

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-e4-deaf`; 12 mixed requests per run, 40 runs per cell.

## Primary: the bounded caution against control, per mix

| Mix | Verdict | Give-up rescue | Extra calls, true 'unavailable' | Harm flags |
|---|---|---|---|---|
| rare | **FADES** | -0.050 [-0.125, +0.000] | -0.133 [-0.300, +0.033] | none |
| common | **FADES** | +0.025 [-0.025, +0.075] | -0.137 [-0.288, -0.025] | none |

## Net effect over all requests, and the accurate request types

| Mix | Δ success, all | Δ calls, all | Extra calls per extra success | Δ success, true 'temporary' | Δ success, true 'format' | Δ success, retry trap |
|---|---|---|---|---|---|---|
| rare | -0.004 [-0.023, +0.015] | -0.046 [-0.123, +0.029] | n/a | +0.008 [-0.033, +0.050] | -0.006 [-0.044, +0.031] | +0.000 [+0.000, +0.000] |
| common | +0.006 [-0.013, +0.025] | +0.029 [-0.054, +0.119] | n/a | -0.013 [-0.075, +0.050] | +0.019 [-0.019, +0.062] | -0.012 [-0.062, +0.038] |

## Secondary: does the share of false messages change how often the agent follows them?

Follow rate of each message's implied strategy at the first failure (stop after 'unavailable', identical retry after 'temporary'). The first failure looks the same whether the message is true or false.

| Arm | Message | Common minus rare | Late minus early, rare | Late minus early, common |
|---|---|---|---|---|
| control | unavailable | +0.069 [+0.013, +0.125] | +0.027 [-0.051, +0.106] | -0.026 [-0.101, +0.046] |
| control | temporary | +0.025 [-0.031, +0.081] | +0.032 [-0.054, +0.131] | +0.058 [+0.002, +0.125] |
| caution_bounded | unavailable | +0.025 [-0.019, +0.075] | +0.009 [-0.054, +0.070] | -0.036 [-0.096, +0.014] |
| caution_bounded | temporary | -0.031 [-0.088, +0.025] | -0.012 [-0.071, +0.047] | -0.017 [-0.121, +0.098] |

## By request kind (success / calls per request)

| Arm, mix | Runs | true_unavailable | give_up_trap | true_temporary | retry_trap | true_format | all |
|---|---|---|---|---|---|---|---|
| control, rare | 40 | 0.00 / 1.26 | 0.05 / 1.12 | 0.97 / 2.93 | 0.00 / 5.88 | 0.98 / 3.00 | 0.57 / 2.63 |
| control, common | 40 | 0.00 / 1.15 | 0.01 / 1.02 | 0.96 / 2.92 | 0.04 / 5.75 | 0.96 / 2.98 | 0.49 / 2.80 |
| caution_bounded, rare | 40 | 0.00 / 1.12 | 0.00 / 1.05 | 0.97 / 2.95 | 0.00 / 5.75 | 0.97 / 3.00 | 0.57 / 2.59 |
| caution_bounded, common | 40 | 0.00 / 1.01 | 0.04 / 1.09 | 0.95 / 2.90 | 0.03 / 5.92 | 0.98 / 3.03 | 0.50 / 2.83 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 160}
- cost: {'runs_recorded': 160, 'from_cache': 0, 'agent_calls': 7128, 'equiv_usd': 0.0}
