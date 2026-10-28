# C4 extension E5 verdict: CONFIRMED

**LIVE MODEL RUN (study W5: E5 through native tool calls, reasoning none)**: transport `openai_responses_native`, model `gpt-6-luna`; 3 requests per run, 60 runs per condition.

- secondary: INCONCLUSIVE

## Per condition (request 1 = prime; request 2 = target, 'unavailable' over a transient fault)

| Prime | Runs | Manipulation check | Stops at once on the target | Target solved | Target calls | Calls on the true outage (request 3) |
|---|---|---|---|---|---|---|
| none | 60 | 1.00 | 0.98 | 0.00 | 1.02 | 2.02 |
| cleared | 60 | 0.93 | 0.10 | 0.88 | 2.78 | 5.92 |
| not_cleared | 60 | 0.93 | 0.37 | 0.60 | 2.23 | 5.13 |

## Contrasts

| Contrast | Stops at once | Target solved | Target calls | Calls on the true outage |
|---|---|---|---|---|
| **primary:** no error minus cleared error | +0.883 [+0.783, +0.950] | -0.883 [-0.950, -0.800] | -1.767 [-1.900, -1.583] | -3.900 [-4.367, -3.417] |
| **secondary:** uncleared errors minus cleared error | +0.267 [+0.117, +0.417] | -0.283 [-0.433, -0.133] | -0.550 [-0.850, -0.267] | -0.783 [-1.300, -0.333] |
| no error minus uncleared errors | +0.617 [+0.483, +0.733] | -0.600 [-0.717, -0.467] | -1.217 [-1.450, -0.950] | -3.117 [-3.750, -2.450] |

- primary verdict: **CONFIRMED**; secondary: **INCONCLUSIVE**

## Validity

- completion (min) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0; manipulation check (min) 0.9333333333333333
- run statuses: {'complete': 180}
- cost: {'runs_recorded': 180, 'from_cache': 0, 'agent_calls': 2236, 'equiv_usd': 0.1732}
