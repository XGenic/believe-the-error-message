# C4 extension E5 verdict: NOT_CONFIRMED

**LIVE MODEL RUN (study W2-C: E5, the first-encounter test, claude-haiku-5-5, native tool use, thinking on)**: transport `anthropic_messages_native`, model `claude-haiku-5-5`; 3 requests per run, 60 runs per condition.

- secondary: NOT_APPLICABLE

## Per condition (request 1 = prime; request 2 = target, 'unavailable' over a transient fault)

| Prime | Runs | Manipulation check | Stops at once on the target | Target solved | Target calls | Calls on the true outage (request 3) |
|---|---|---|---|---|---|---|
| none | 60 | 1.00 | 0.12 | 0.00 | 1.88 | 1.60 |
| cleared | 60 | 1.00 | 0.08 | 0.02 | 1.93 | 1.62 |
| not_cleared | 60 | 1.00 | 0.92 | 0.00 | 1.08 | 1.08 |

## Contrasts

| Contrast | Stops at once | Target solved | Target calls | Calls on the true outage |
|---|---|---|---|---|
| **primary:** no error minus cleared error | +0.033 [-0.083, +0.133] | -0.017 [-0.050, +0.000] | -0.050 [-0.167, +0.067] | -0.017 [-0.233, +0.183] |
| **secondary:** uncleared errors minus cleared error | +0.833 [+0.733, +0.933] | -0.017 [-0.050, +0.000] | -0.850 [-0.950, -0.750] | -0.533 [-0.717, -0.367] |
| no error minus uncleared errors | -0.800 [-0.900, -0.683] | +0.000 [+0.000, +0.000] | +0.800 [+0.683, +0.900] | +0.517 [+0.367, +0.650] |

- primary verdict: **NOT_CONFIRMED**; secondary: **NOT_APPLICABLE**

## Validity

- completion (min) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0; manipulation check (min) 1.0
- run statuses: {'complete': 180}
- cost: {'runs_recorded': 180, 'from_cache': 0, 'agent_calls': 1525, 'equiv_usd': 0.1043}
