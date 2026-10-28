# C4 extension E5 verdict: CONFIRMED

**LIVE MODEL RUN (study W5: E5 through native tool calls, reasoning high)**: transport `openai_responses_native`, model `gpt-6-luna`; 3 requests per run, 60 runs per condition.

- secondary: CLEARING_SPECIFIC

## Per condition (request 1 = prime; request 2 = target, 'unavailable' over a transient fault)

| Prime | Runs | Manipulation check | Stops at once on the target | Target solved | Target calls | Calls on the true outage (request 3) |
|---|---|---|---|---|---|---|
| none | 60 | 0.95 | 0.78 | 0.12 | 1.35 | 2.67 |
| cleared | 60 | 1.00 | 0.00 | 1.00 | 3.03 | 6 |
| not_cleared | 60 | 1.00 | 0.32 | 0.68 | 2.37 | 5.25 |

## Contrasts

| Contrast | Stops at once | Target solved | Target calls | Calls on the true outage |
|---|---|---|---|---|
| **primary:** no error minus cleared error | +0.783 [+0.683, +0.883] | -0.883 [-0.950, -0.800] | -1.683 [-1.850, -1.483] | -3.333 [-3.900, -2.767] |
| **secondary:** uncleared errors minus cleared error | +0.317 [+0.200, +0.433] | -0.317 [-0.433, -0.200] | -0.667 [-0.917, -0.433] | -0.750 [-1.250, -0.333] |
| no error minus uncleared errors | +0.467 [+0.300, +0.617] | -0.567 [-0.700, -0.417] | -1.017 [-1.300, -0.700] | -2.583 [-3.267, -1.833] |

- primary verdict: **CONFIRMED**; secondary: **CLEARING_SPECIFIC**

## Validity

- completion (min) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0; manipulation check (min) 0.95
- run statuses: {'complete': 180}
- cost: {'runs_recorded': 180, 'from_cache': 0, 'agent_calls': 2381, 'equiv_usd': 0.1947}
