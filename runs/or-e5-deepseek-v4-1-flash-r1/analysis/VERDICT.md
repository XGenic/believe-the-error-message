# C4 extension E5 verdict: CONFIRMED

**LIVE MODEL RUN (study W2-A) (W2 open-weight panel: E5 through OpenRouter, DeepSeek, reasoning r1 = {"effort": "low"})**: transport `openrouter_chat_native`, model `deepseek/deepseek-v4.1-flash`; 3 requests per run, 60 runs per condition.

- secondary: EXPOSURE_GENERAL

## Per condition (request 1 = prime; request 2 = target, 'unavailable' over a transient fault)

| Prime | Runs | Manipulation check | Stops at once on the target | Target solved | Target calls | Calls on the true outage (request 3) |
|---|---|---|---|---|---|---|
| none | 60 | 1.00 | 0.43 | 0.00 | 1.57 | 1.70 |
| cleared | 60 | 1.00 | 0.02 | 0.62 | 2.62 | 4.82 |
| not_cleared | 60 | 1.00 | 0.02 | 0.55 | 2.68 | 4.25 |

## Contrasts

| Contrast | Stops at once | Target solved | Target calls | Calls on the true outage |
|---|---|---|---|---|
| **primary:** no error minus cleared error | +0.417 [+0.300, +0.550] | -0.617 [-0.733, -0.500] | -1.050 [-1.233, -0.883] | -3.117 [-3.533, -2.717] |
| **secondary:** uncleared errors minus cleared error | +0.000 [-0.050, +0.050] | -0.067 [-0.233, +0.100] | +0.067 [-0.133, +0.267] | -0.567 [-1.133, +0.017] |
| no error minus uncleared errors | +0.417 [+0.283, +0.550] | -0.550 [-0.683, -0.417] | -1.117 [-1.317, -0.917] | -2.550 [-3.033, -2.083] |

- primary verdict: **CONFIRMED**; secondary: **EXPOSURE_GENERAL**

## Validity

- completion (min) 1.000; protocol failures 0.0009099181073703367; tool use on request 1 (min) 1.0; unclassifiable 0.0; manipulation check (min) 1.0
- run statuses: {'complete': 180}
- cost: {'runs_recorded': 180, 'from_cache': 102, 'agent_calls': 2198, 'equiv_usd': 0.1064}
