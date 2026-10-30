# C4 extension E5 verdict: CONFIRMED

**LIVE MODEL RUN (study W2-D: E5, the first-encounter test, gpt-6.1-sol, native tool calls, reasoning low)**: transport `openai_responses_native`, model `gpt-6.1-sol`; 3 requests per run, 60 runs per condition.

- secondary: CLEARING_SPECIFIC

## Per condition (request 1 = prime; request 2 = target, 'unavailable' over a transient fault)

| Prime | Runs | Manipulation check | Stops at once on the target | Target solved | Target calls | Calls on the true outage (request 3) |
|---|---|---|---|---|---|---|
| none | 60 | 1.00 | 1.00 | 0.00 | 1 | 1 |
| cleared | 60 | 1.00 | 0.00 | 0.12 | 2.12 | 1.60 |
| not_cleared | 60 | 1.00 | 0.92 | 0.00 | 1.08 | 1 |

## Contrasts

| Contrast | Stops at once | Target solved | Target calls | Calls on the true outage |
|---|---|---|---|---|
| **primary:** no error minus cleared error | +1.000 [+1.000, +1.000] | -0.117 [-0.200, -0.050] | -1.117 [-1.200, -1.050] | -0.600 [-1.017, -0.250] |
| **secondary:** uncleared errors minus cleared error | +0.917 [+0.833, +0.983] | -0.117 [-0.200, -0.050] | -1.033 [-1.133, -0.933] | -0.600 [-1.017, -0.250] |
| no error minus uncleared errors | +0.083 [+0.017, +0.167] | +0.000 [+0.000, +0.000] | -0.083 [-0.167, -0.017] | 0 [0, 0] |

- primary verdict: **CONFIRMED**; secondary: **CLEARING_SPECIFIC**

## Validity

- completion (min) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0; manipulation check (min) 1.0
- run statuses: {'complete': 180}
- cost: {'runs_recorded': 180, 'from_cache': 0, 'agent_calls': 1608, 'equiv_usd': 2.1159}
