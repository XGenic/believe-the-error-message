# C4 extension E4 verdict: INVALID

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-e4-non-engager`; 12 mixed requests per run, 40 runs per cell.

- tool use on request 1 0.0 below 0.9 in some cell: agents did not engage
- unclassifiable responses None above 0.1

## Primary: the bounded caution against control, per mix

| Mix | Verdict | Give-up rescue | Extra calls, true 'unavailable' | Harm flags |
|---|---|---|---|---|
| rare | **FADES** | +0.000 [+0.000, +0.000] | 0 [0, 0] | none |
| common | **FADES** | +0.000 [+0.000, +0.000] | 0 [0, 0] | none |

## Net effect over all requests, and the accurate request types

| Mix | Δ success, all | Δ calls, all | Extra calls per extra success | Δ success, true 'temporary' | Δ success, true 'format' | Δ success, retry trap |
|---|---|---|---|---|---|---|
| rare | +0.000 [+0.000, +0.000] | 0 [0, 0] | n/a | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| common | +0.000 [+0.000, +0.000] | 0 [0, 0] | n/a | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |

## Secondary: does the share of false messages change how often the agent follows them?

Follow rate of each message's implied strategy at the first failure (stop after 'unavailable', identical retry after 'temporary'). The first failure looks the same whether the message is true or false.

| Arm | Message | Common minus rare | Late minus early, rare | Late minus early, common |
|---|---|---|---|---|
| control | unavailable | n/a | n/a | n/a |
| control | temporary | n/a | n/a | n/a |
| caution_bounded | unavailable | n/a | n/a | n/a |
| caution_bounded | temporary | n/a | n/a | n/a |

## By request kind (success / calls per request)

| Arm, mix | Runs | true_unavailable | give_up_trap | true_temporary | retry_trap | true_format | all |
|---|---|---|---|---|---|---|---|
| control, rare | 40 | 0.00 / 0 | 0.00 / 0 | 0.00 / 0 | 0.00 / 0 | 0.00 / 0 | 0.00 / 0 |
| control, common | 40 | 0.00 / 0 | 0.00 / 0 | 0.00 / 0 | 0.00 / 0 | 0.00 / 0 | 0.00 / 0 |
| caution_bounded, rare | 40 | 0.00 / 0 | 0.00 / 0 | 0.00 / 0 | 0.00 / 0 | 0.00 / 0 | 0.00 / 0 |
| caution_bounded, common | 40 | 0.00 / 0 | 0.00 / 0 | 0.00 / 0 | 0.00 / 0 | 0.00 / 0 | 0.00 / 0 |

## Validity

- completion (min over cells) 1.000; protocol failures 0.0; tool use on request 1 (min) 0.0; unclassifiable None
- run statuses: {'complete': 160}
- cost: {'runs_recorded': 160, 'from_cache': 0, 'agent_calls': 1920, 'equiv_usd': 0.0}
