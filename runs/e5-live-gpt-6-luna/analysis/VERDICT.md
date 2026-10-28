# C4 extension E5 verdict: CONFIRMED

**LIVE MODEL RUN (extension E5)**: transport `openai_responses`, model `gpt-6-luna`; 3 requests per run, 60 runs per condition.

- secondary: INCONCLUSIVE

## Per condition (request 1 = prime; request 2 = target, 'unavailable' over a transient fault)

| Prime | Runs | Manipulation check | Stops at once on the target | Target solved | Target calls | Calls on the true outage (request 3) |
|---|---|---|---|---|---|---|
| none | 60 | 1.00 | 1.00 | 0.00 | 1 | 1 |
| cleared | 60 | 1.00 | 0.03 | 0.97 | 2.93 | 5.93 |
| not_cleared | 60 | 1.00 | 0.22 | 0.78 | 2.57 | 5.22 |

## Contrasts

| Contrast | Stops at once | Target solved | Target calls | Calls on the true outage |
|---|---|---|---|---|
| **primary:** no error minus cleared error | +0.967 [+0.917, +1.000] | -0.967 [-1.000, -0.917] | -1.933 [-2, -1.833] | -4.933 [-5, -4.817] |
| **secondary:** uncleared errors minus cleared error | +0.183 [+0.067, +0.300] | -0.183 [-0.300, -0.067] | -0.367 [-0.600, -0.133] | -0.717 [-1.200, -0.283] |
| no error minus uncleared errors | +0.783 [+0.683, +0.883] | -0.783 [-0.883, -0.683] | -1.567 [-1.767, -1.367] | -4.217 [-4.633, -3.750] |

- primary verdict: **CONFIRMED**; secondary: **INCONCLUSIVE**

## Validity

- completion (min) 1.000; protocol failures 0.013608428446005268; tool use on request 1 (min) 1.0; unclassifiable 0.0; manipulation check (min) 1.0
- run statuses: {'complete': 180}
- cost: {'runs_recorded': 180, 'from_cache': 0, 'agent_calls': 2278, 'equiv_usd': 0.1693}
