# C4 extension E5 verdict: CONFIRMED

**LIVE MODEL RUN (study W5: E5 through native tool calls, reasoning low)**: transport `openai_responses_native`, model `gpt-6-luna`; 3 requests per run, 60 runs per condition.

- secondary: CLEARING_SPECIFIC

## Per condition (request 1 = prime; request 2 = target, 'unavailable' over a transient fault)

| Prime | Runs | Manipulation check | Stops at once on the target | Target solved | Target calls | Calls on the true outage (request 3) |
|---|---|---|---|---|---|---|
| none | 60 | 0.97 | 0.97 | 0.02 | 1.05 | 1.50 |
| cleared | 60 | 1.00 | 0.03 | 0.90 | 2.92 | 6 |
| not_cleared | 60 | 1.00 | 0.62 | 0.35 | 1.82 | 3.87 |

## Contrasts

| Contrast | Stops at once | Target solved | Target calls | Calls on the true outage |
|---|---|---|---|---|
| **primary:** no error minus cleared error | +0.933 [+0.867, +0.983] | -0.883 [-0.967, -0.800] | -1.867 [-2.000, -1.717] | -4.500 [-4.800, -4.133] |
| **secondary:** uncleared errors minus cleared error | +0.583 [+0.450, +0.717] | -0.550 [-0.683, -0.417] | -1.100 [-1.383, -0.767] | -2.133 [-2.700, -1.567] |
| no error minus uncleared errors | +0.350 [+0.217, +0.483] | -0.333 [-0.467, -0.200] | -0.767 [-1.067, -0.483] | -2.367 [-3.033, -1.717] |

- primary verdict: **CONFIRMED**; secondary: **CLEARING_SPECIFIC**

## Validity

- completion (min) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0; manipulation check (min) 0.9666666666666667
- run statuses: {'complete': 180}
- cost: {'runs_recorded': 180, 'from_cache': 0, 'agent_calls': 2129, 'equiv_usd': 0.1623}
