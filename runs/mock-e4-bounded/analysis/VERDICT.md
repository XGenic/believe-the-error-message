# C4 extension E4 verdict: VALID

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-e4-bounded`; 12 mixed requests per run, 40 runs per cell.

## Primary: the bounded caution against control, per mix

| Mix | Verdict | Give-up rescue | Extra calls, true 'unavailable' | Harm flags |
|---|---|---|---|---|
| rare | **HOLDS** | +0.900 [+0.800, +0.975] | +1.642 [+1.467, +1.800] | success on true format requests fell by 0.39 |
| common | **HOLDS** | +0.975 [+0.938, +1.000] | +1.800 [+1.650, +1.925] | success on true format requests fell by 0.35 |

## Net effect over all requests, and the accurate request types

| Mix | Δ success, all | Δ calls, all | Extra calls per extra success | Δ success, true 'temporary' | Δ success, true 'format' | Δ success, retry trap |
|---|---|---|---|---|---|---|
| rare | -0.000 [-0.029, +0.027] | +0.156 [+0.087, +0.223] | n/a | +0.017 [-0.025, +0.058] | -0.387 [-0.444, -0.331] | +0.600 [+0.450, +0.750] |
| common | +0.138 [+0.108, +0.167] | -0.006 [-0.081, +0.079] | -0.045 [-0.596, +0.581] | -0.025 [-0.088, +0.038] | -0.350 [-0.425, -0.269] | +0.575 [+0.450, +0.688] |

## Secondary: does the share of false messages change how often the agent follows them?

Follow rate of each message's implied strategy at the first failure (stop after 'unavailable', identical retry after 'temporary'). The first failure looks the same whether the message is true or false.

| Arm | Message | Common minus rare | Late minus early, rare | Late minus early, common |
|---|---|---|---|---|
| control | unavailable | +0.069 [+0.013, +0.125] | +0.027 [-0.051, +0.106] | -0.026 [-0.101, +0.046] |
| control | temporary | +0.025 [-0.031, +0.081] | +0.032 [-0.054, +0.131] | +0.058 [+0.002, +0.125] |
| caution_bounded | unavailable | -0.031 [-0.081, +0.012] | -0.012 [-0.088, +0.061] | -0.012 [-0.090, +0.062] |
| caution_bounded | temporary | +0.025 [-0.013, +0.069] | +0.009 [-0.030, +0.046] | +0.010 [-0.090, +0.113] |

## By request kind (success / calls per request)

| Arm, mix | Runs | true_unavailable | give_up_trap | true_temporary | retry_trap | true_format | all |
|---|---|---|---|---|---|---|---|
| control, rare | 40 | 0.00 / 1.26 | 0.05 / 1.12 | 0.97 / 2.93 | 0.00 / 5.88 | 0.98 / 3.00 | 0.57 / 2.63 |
| control, common | 40 | 0.00 / 1.15 | 0.01 / 1.02 | 0.96 / 2.92 | 0.04 / 5.75 | 0.96 / 2.98 | 0.49 / 2.80 |
| caution_bounded, rare | 40 | 0.00 / 2.90 | 0.95 / 2.90 | 0.98 / 2.97 | 0.60 / 2.45 | 0.59 / 2.62 | 0.57 / 2.79 |
| caution_bounded, common | 40 | 0.00 / 2.95 | 0.99 / 2.98 | 0.94 / 2.88 | 0.61 / 2.71 | 0.61 / 2.63 | 0.63 / 2.80 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 160}
- cost: {'runs_recorded': 160, 'from_cache': 0, 'agent_calls': 7208, 'equiv_usd': 0.0}
