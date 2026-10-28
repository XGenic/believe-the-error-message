# C4 extension E4 verdict: VALID

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-e4-unbounded`; 12 mixed requests per run, 40 runs per cell.

## Primary: the bounded caution against control, per mix

| Mix | Verdict | Give-up rescue | Extra calls, true 'unavailable' | Harm flags |
|---|---|---|---|---|
| rare | **RESCUE_ONLY** | +0.900 [+0.800, +0.975] | +3.525 [+3.317, +3.733] | none |
| common | **RESCUE_ONLY** | +0.963 [+0.912, +1.000] | +3.863 [+3.675, +4.025] | none |

## Net effect over all requests, and the accurate request types

| Mix | Δ success, all | Δ calls, all | Extra calls per extra success | Δ success, true 'temporary' | Δ success, true 'format' | Δ success, retry trap |
|---|---|---|---|---|---|---|
| rare | +0.154 [+0.135, +0.173] | +0.783 [+0.710, +0.867] | +5.081 [+4.538, +5.758] | +0.008 [-0.033, +0.050] | +0.000 [-0.031, +0.025] | +0.925 [+0.825, +1.000] |
| common | +0.313 [+0.292, +0.331] | +0.512 [+0.419, +0.608] | +1.640 [+1.376, +1.904] | -0.025 [-0.088, +0.037] | +0.000 [-0.044, +0.044] | +0.938 [+0.875, +0.988] |

## Secondary: does the share of false messages change how often the agent follows them?

Follow rate of each message's implied strategy at the first failure (stop after 'unavailable', identical retry after 'temporary'). The first failure looks the same whether the message is true or false.

| Arm | Message | Common minus rare | Late minus early, rare | Late minus early, common |
|---|---|---|---|---|
| control | unavailable | +0.069 [+0.013, +0.125] | +0.027 [-0.051, +0.106] | -0.026 [-0.101, +0.046] |
| control | temporary | +0.025 [-0.031, +0.081] | +0.032 [-0.054, +0.131] | +0.058 [+0.002, +0.125] |
| caution_bounded | unavailable | -0.038 [-0.081, +0.006] | -0.041 [-0.127, +0.034] | -0.013 [-0.055, +0.030] |
| caution_bounded | temporary | +0.019 [-0.006, +0.044] | +0.025 [+0.000, +0.075] | -0.012 [-0.057, +0.026] |

## By request kind (success / calls per request)

| Arm, mix | Runs | true_unavailable | give_up_trap | true_temporary | retry_trap | true_format | all |
|---|---|---|---|---|---|---|---|
| control, rare | 40 | 0.00 / 1.26 | 0.05 / 1.12 | 0.97 / 2.93 | 0.00 / 5.88 | 0.98 / 3.00 | 0.57 / 2.63 |
| control, common | 40 | 0.00 / 1.15 | 0.01 / 1.02 | 0.96 / 2.92 | 0.04 / 5.75 | 0.96 / 2.98 | 0.49 / 2.80 |
| caution_bounded, rare | 40 | 0.00 / 4.78 | 0.95 / 2.90 | 0.97 / 2.95 | 0.93 / 2.73 | 0.98 / 3.04 | 0.73 / 3.41 |
| caution_bounded, common | 40 | 0.00 / 5.01 | 0.97 / 2.95 | 0.94 / 2.88 | 0.97 / 3.06 | 0.96 / 2.99 | 0.80 / 3.31 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 160}
- cost: {'runs_recorded': 160, 'from_cache': 0, 'agent_calls': 7758, 'equiv_usd': 0.0}
