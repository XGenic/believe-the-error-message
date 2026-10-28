# C4 extension E5 verdict: CONFIRMED

**LIVE MODEL RUN (study N1-B: E5 through native tool calls, reasoning low)**: transport `openai_responses_native`, model `gpt-6-luna`; 3 requests per run, 60 runs per condition.

- secondary: CLEARING_SPECIFIC

## Per condition (request 1 = prime; request 2 = target, 'unavailable' over a transient fault)

| Prime | Runs | Manipulation check | Stops at once on the target | Target solved | Target calls | Calls on the true outage (request 3) |
|---|---|---|---|---|---|---|
| none | 60 | 0.97 | 1.00 | 0.00 | 1 | 1.60 |
| cleared | 60 | 0.95 | 0.07 | 0.92 | 2.85 | 5.75 |
| not_cleared | 60 | 1.00 | 0.63 | 0.35 | 1.72 | 3.43 |

## Contrasts

| Contrast | Stops at once | Target solved | Target calls | Calls on the true outage |
|---|---|---|---|---|
| **primary:** no error minus cleared error | +0.933 [+0.867, +0.983] | -0.917 [-0.967, -0.833] | -1.850 [-1.967, -1.700] | -4.150 [-4.567, -3.667] |
| **secondary:** uncleared errors minus cleared error | +0.567 [+0.433, +0.700] | -0.567 [-0.700, -0.417] | -1.133 [-1.383, -0.850] | -2.317 [-2.950, -1.667] |
| no error minus uncleared errors | +0.367 [+0.250, +0.483] | -0.350 [-0.467, -0.233] | -0.717 [-0.950, -0.483] | -1.833 [-2.500, -1.167] |

- primary verdict: **CONFIRMED**; secondary: **CLEARING_SPECIFIC**

## Validity

- completion (min) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0; manipulation check (min) 0.95
- run statuses: {'complete': 180}
- cost: {'runs_recorded': 180, 'from_cache': 0, 'agent_calls': 2082, 'equiv_usd': 0.157}
