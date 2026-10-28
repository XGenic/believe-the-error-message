# C4 extension E5 verdict: CONFIRMED

**LIVE MODEL RUN (study W5: E5 through native tool calls, reasoning medium)**: transport `openai_responses_native`, model `gpt-6-luna`; 3 requests per run, 60 runs per condition.

- secondary: CLEARING_SPECIFIC

## Per condition (request 1 = prime; request 2 = target, 'unavailable' over a transient fault)

| Prime | Runs | Manipulation check | Stops at once on the target | Target solved | Target calls | Calls on the true outage (request 3) |
|---|---|---|---|---|---|---|
| none | 60 | 0.95 | 0.90 | 0.03 | 1.15 | 2.38 |
| cleared | 60 | 1.00 | 0.02 | 0.98 | 2.97 | 5.95 |
| not_cleared | 60 | 1.00 | 0.53 | 0.47 | 1.93 | 4.90 |

## Contrasts

| Contrast | Stops at once | Target solved | Target calls | Calls on the true outage |
|---|---|---|---|---|
| **primary:** no error minus cleared error | +0.883 [+0.800, +0.950] | -0.950 [-1.000, -0.883] | -1.817 [-1.950, -1.650] | -3.567 [-4.050, -3.050] |
| **secondary:** uncleared errors minus cleared error | +0.517 [+0.383, +0.633] | -0.517 [-0.633, -0.383] | -1.033 [-1.267, -0.767] | -1.050 [-1.567, -0.550] |
| no error minus uncleared errors | +0.367 [+0.217, +0.517] | -0.433 [-0.567, -0.300] | -0.783 [-1.067, -0.500] | -2.517 [-3.233, -1.783] |

- primary verdict: **CONFIRMED**; secondary: **CLEARING_SPECIFIC**

## Validity

- completion (min) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0; manipulation check (min) 0.95
- run statuses: {'complete': 180}
- cost: {'runs_recorded': 180, 'from_cache': 0, 'agent_calls': 2285, 'equiv_usd': 0.1814}
