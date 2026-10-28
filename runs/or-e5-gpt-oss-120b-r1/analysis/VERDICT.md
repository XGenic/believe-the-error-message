# C4 extension E5 verdict: INCONCLUSIVE

**PROPOSED, NOT APPROVED (W2 open-weight panel: E5 through OpenRouter, OpenAI, reasoning r1 = {"effort": "low"})**: transport `openrouter_chat_native`, model `openai/gpt-oss-120b`; 3 requests per run, 60 runs per condition.

- secondary: NOT_APPLICABLE

## Per condition (request 1 = prime; request 2 = target, 'unavailable' over a transient fault)

| Prime | Runs | Manipulation check | Stops at once on the target | Target solved | Target calls | Calls on the true outage (request 3) |
|---|---|---|---|---|---|---|
| none | 60 | 1.00 | 0.93 | 0.00 | 1.07 | 1.15 |
| cleared | 60 | 0.80 | 0.68 | 0.13 | 1.45 | 1.63 |
| not_cleared | 60 | 0.98 | 0.98 | 0.00 | 1.02 | 1.25 |

## Contrasts

| Contrast | Stops at once | Target solved | Target calls | Calls on the true outage |
|---|---|---|---|---|
| **primary:** no error minus cleared error | +0.250 [+0.117, +0.400] | -0.133 [-0.217, -0.050] | -0.383 [-0.583, -0.183] | -0.483 [-0.700, -0.267] |
| **secondary:** uncleared errors minus cleared error | +0.300 [+0.183, +0.433] | -0.133 [-0.217, -0.050] | -0.433 [-0.633, -0.250] | -0.383 [-0.633, -0.150] |
| no error minus uncleared errors | -0.050 [-0.117, +0.017] | +0.000 [+0.000, +0.000] | +0.050 [-0.017, +0.117] | -0.100 [-0.283, +0.083] |

- primary verdict: **INCONCLUSIVE**; secondary: **NOT_APPLICABLE**

## Validity

- completion (min) 1.000; protocol failures 0.02642559109874826; tool use on request 1 (min) 1.0; unclassifiable 0.0; manipulation check (min) 0.8
- run statuses: {'complete': 180}
- cost: {'runs_recorded': 180, 'from_cache': 0, 'agent_calls': 1438, 'equiv_usd': 0.0388}
