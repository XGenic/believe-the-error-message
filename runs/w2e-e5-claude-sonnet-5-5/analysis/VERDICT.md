# C4 extension E5 verdict: NOT_CONFIRMED

**LIVE MODEL RUN (study W2-E: E5, claude-sonnet-5-5, native tool use, adaptive thinking, effort high)**: transport `anthropic_messages_native`, model `claude-sonnet-5-5`; 3 requests per run, 60 runs per condition.

- secondary: NOT_APPLICABLE

## Per condition (request 1 = prime; request 2 = target, 'unavailable' over a transient fault)

| Prime | Runs | Manipulation check | Stops at once on the target | Target solved | Target calls | Calls on the true outage (request 3) |
|---|---|---|---|---|---|---|
| none | 60 | 1.00 | 0.00 | 0.12 | 2.12 | 2.23 |
| cleared | 60 | 1.00 | 0.00 | 0.43 | 2.43 | 3.67 |
| not_cleared | 60 | 1.00 | 0.17 | 0.00 | 1.83 | 1.13 |

## Contrasts

| Contrast | Stops at once | Target solved | Target calls | Calls on the true outage |
|---|---|---|---|---|
| **primary:** no error minus cleared error | +0.000 [+0.000, +0.000] | -0.317 [-0.467, -0.167] | -0.317 [-0.467, -0.167] | -1.433 [-1.950, -0.933] |
| **secondary:** uncleared errors minus cleared error | +0.167 [+0.083, +0.267] | -0.433 [-0.567, -0.317] | -0.600 [-0.767, -0.450] | -2.533 [-3.050, -2.033] |
| no error minus uncleared errors | -0.167 [-0.267, -0.083] | +0.117 [+0.050, +0.200] | +0.283 [+0.167, +0.417] | +1.100 [+0.917, +1.300] |

- primary verdict: **NOT_CONFIRMED**; secondary: **NOT_APPLICABLE**

## Validity

- completion (min) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0; manipulation check (min) 1.0
- run statuses: {'complete': 180}
- cost: {'runs_recorded': 180, 'from_cache': 0, 'agent_calls': 1923, 'equiv_usd': 2.0352}
