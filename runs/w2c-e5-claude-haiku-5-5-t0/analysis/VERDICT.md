# C4 extension E5 verdict: INVALID

**LIVE MODEL RUN (study W2-C: E5, the first-encounter test, claude-haiku-5-5, native tool use, thinking off)**: transport `anthropic_messages_native`, model `claude-haiku-5-5`; 3 requests per run, 60 runs per condition.

- manipulation check 0.3333333333333333 below 0.8 in some condition: the prime did not give the intended experience

## Per condition (request 1 = prime; request 2 = target, 'unavailable' over a transient fault)

| Prime | Runs | Manipulation check | Stops at once on the target | Target solved | Target calls | Calls on the true outage (request 3) |
|---|---|---|---|---|---|---|
| none | 60 | 1.00 | 1.00 | 0.00 | 1 | 1 |
| cleared | 60 | 0.33 | 0.95 | 0.00 | 1.05 | 1 |
| not_cleared | 60 | 1.00 | 1.00 | 0.00 | 1 | 1 |

## Contrasts

| Contrast | Stops at once | Target solved | Target calls | Calls on the true outage |
|---|---|---|---|---|
| **primary:** no error minus cleared error | +0.050 [+0.000, +0.117] | +0.000 [+0.000, +0.000] | -0.050 [-0.117, 0] | 0 [0, 0] |
| **secondary:** uncleared errors minus cleared error | +0.050 [+0.000, +0.117] | +0.000 [+0.000, +0.000] | -0.050 [-0.117, 0] | 0 [0, 0] |
| no error minus uncleared errors | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | 0 [0, 0] | 0 [0, 0] |

- primary verdict: **NOT_CONFIRMED**; secondary: **NOT_APPLICABLE**

## Validity

- completion (min) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0; manipulation check (min) 0.3333333333333333
- run statuses: {'complete': 180}
- cost: {'runs_recorded': 180, 'from_cache': 0, 'agent_calls': 1243, 'equiv_usd': 0.064}
