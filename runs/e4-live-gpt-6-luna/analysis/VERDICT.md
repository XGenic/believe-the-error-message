# C4 extension E4 verdict: VALID

**LIVE MODEL RUN (extension E4)**: transport `openai_responses`, model `gpt-6-luna`; 12 mixed requests per run, 40 runs per cell.

## Primary: the bounded caution against control, per mix

| Mix | Verdict | Give-up rescue | Extra calls, true 'unavailable' | Harm flags |
|---|---|---|---|---|
| rare | **HOLDS** | +0.525 [+0.350, +0.675] | +0.617 [-0.158, +1.350] | none |
| common | **FADES** | +0.350 [+0.188, +0.512] | +0.288 [-0.438, +1.000] | none |

## Net effect over all requests, and the accurate request types

| Mix | Δ success, all | Δ calls, all | Extra calls per extra success | Δ success, true 'temporary' | Δ success, true 'format' | Δ success, retry trap |
|---|---|---|---|---|---|---|
| rare | +0.035 [+0.002, +0.067] | +0.131 [-0.115, +0.358] | +3.706 [-3.864, +12.692] | +0.000 [+0.000, +0.000] | -0.075 [-0.144, -0.012] | +0.200 [+0.000, +0.400] |
| common | +0.040 [-0.008, +0.094] | -0.056 [-0.263, +0.158] | -1.421 [-12.375, +3.237] | -0.012 [-0.037, +0.000] | -0.106 [-0.188, -0.013] | +0.112 [-0.050, +0.275] |

## Secondary: does the share of false messages change how often the agent follows them?

Follow rate of each message's implied strategy at the first failure (stop after 'unavailable', identical retry after 'temporary'). The first failure looks the same whether the message is true or false.

| Arm | Message | Common minus rare | Late minus early, rare | Late minus early, common |
|---|---|---|---|---|
| control | unavailable | -0.106 [-0.313, +0.113] | -0.119 [-0.206, -0.049] | -0.082 [-0.161, -0.017] |
| control | temporary | -0.050 [-0.181, +0.081] | -0.076 [-0.155, -0.000] | -0.203 [-0.320, -0.095] |
| caution_bounded | unavailable | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| caution_bounded | temporary | +0.019 [-0.019, +0.069] | -0.023 [-0.061, +0.000] | -0.032 [-0.073, +0.000] |

## By request kind (success / calls per request)

| Arm, mix | Runs | true_unavailable | give_up_trap | true_temporary | retry_trap | true_format | all |
|---|---|---|---|---|---|---|---|
| control, rare | 40 | 0.00 / 3.10 | 0.45 / 1.93 | 1.00 / 3 | 0.25 / 5.38 | 0.93 / 3.05 | 0.62 / 3.15 |
| control, common | 40 | 0.00 / 3.52 | 0.55 / 2.14 | 1.00 / 3 | 0.46 / 5.21 | 0.94 / 3.09 | 0.65 / 3.34 |
| caution_bounded, rare | 40 | 0.00 / 3.72 | 0.97 / 2.98 | 1.00 / 3 | 0.45 / 3.62 | 0.86 / 3.16 | 0.65 / 3.28 |
| caution_bounded, common | 40 | 0.00 / 3.81 | 0.90 / 2.94 | 0.99 / 3 | 0.57 / 3.36 | 0.83 / 3.31 | 0.69 / 3.29 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.00847457627118644; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 160}
- cost: {'runs_recorded': 160, 'from_cache': 0, 'agent_calls': 8260, 'equiv_usd': 1.3212}
