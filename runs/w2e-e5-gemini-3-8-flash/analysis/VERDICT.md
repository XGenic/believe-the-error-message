# C4 extension E5 verdict: NOT_CONFIRMED

**LIVE MODEL RUN (study W2-E: E5, gemini-3.8-flash through OpenRouter, reasoning medium, flex tier)**: transport `openrouter_chat_native`, model `google/gemini-3.8-flash`; 3 requests per run, 60 runs per condition.

- secondary: NOT_APPLICABLE

## Per condition (request 1 = prime; request 2 = target, 'unavailable' over a transient fault)

| Prime | Runs | Manipulation check | Stops at once on the target | Target solved | Target calls | Calls on the true outage (request 3) |
|---|---|---|---|---|---|---|
| none | 60 | 1.00 | 0.02 | 0.08 | 2.07 | 1.78 |
| cleared | 60 | 1.00 | 0.00 | 0.43 | 2.43 | 3.43 |
| not_cleared | 60 | 1.00 | 0.00 | 0.10 | 2.10 | 2.25 |

## Contrasts

| Contrast | Stops at once | Target solved | Target calls | Calls on the true outage |
|---|---|---|---|---|
| **primary:** no error minus cleared error | +0.017 [+0.000, +0.067] | -0.350 [-0.500, -0.200] | -0.367 [-0.517, -0.217] | -1.650 [-2.200, -1.133] |
| **secondary:** uncleared errors minus cleared error | +0.000 [+0.000, +0.000] | -0.333 [-0.483, -0.200] | -0.333 [-0.483, -0.200] | -1.183 [-1.733, -0.667] |
| no error minus uncleared errors | +0.017 [+0.000, +0.067] | -0.017 [-0.117, +0.083] | -0.033 [-0.150, +0.067] | -0.467 [-0.817, -0.133] |

- primary verdict: **NOT_CONFIRMED**; secondary: **NOT_APPLICABLE**

## Validity

- completion (min) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0; manipulation check (min) 1.0
- run statuses: {'complete': 180}
- cost: {'runs_recorded': 180, 'from_cache': 0, 'agent_calls': 1984, 'equiv_usd': 1.3633}
