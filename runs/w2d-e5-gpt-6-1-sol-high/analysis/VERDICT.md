# C4 extension E5 verdict: CONFIRMED

**LIVE MODEL RUN (study W2-D: E5, the first-encounter test, gpt-6.1-sol, native tool calls, reasoning high)**: transport `openai_responses_native`, model `gpt-6.1-sol`; 3 requests per run, 60 runs per condition.

- secondary: CLEARING_SPECIFIC

## Per condition (request 1 = prime; request 2 = target, 'unavailable' over a transient fault)

| Prime | Runs | Manipulation check | Stops at once on the target | Target solved | Target calls | Calls on the true outage (request 3) |
|---|---|---|---|---|---|---|
| none | 60 | 1.00 | 1.00 | 0.00 | 1 | 1 |
| cleared | 60 | 1.00 | 0.13 | 0.08 | 1.95 | 1.63 |
| not_cleared | 60 | 1.00 | 0.95 | 0.00 | 1.05 | 1 |

## Contrasts

| Contrast | Stops at once | Target solved | Target calls | Calls on the true outage |
|---|---|---|---|---|
| **primary:** no error minus cleared error | +0.867 [+0.767, +0.950] | -0.083 [-0.167, -0.017] | -0.950 [-1.067, -0.833] | -0.633 [-1.017, -0.300] |
| **secondary:** uncleared errors minus cleared error | +0.817 [+0.700, +0.917] | -0.083 [-0.167, -0.017] | -0.900 [-1.017, -0.767] | -0.633 [-1.017, -0.300] |
| no error minus uncleared errors | +0.050 [+0.000, +0.117] | +0.000 [+0.000, +0.000] | -0.050 [-0.117, 0] | 0 [0, 0] |

- primary verdict: **CONFIRMED**; secondary: **CLEARING_SPECIFIC**

## Validity

- completion (min) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0; manipulation check (min) 1.0
- run statuses: {'complete': 180}
- cost: {'runs_recorded': 180, 'from_cache': 0, 'agent_calls': 1598, 'equiv_usd': 2.1684}
