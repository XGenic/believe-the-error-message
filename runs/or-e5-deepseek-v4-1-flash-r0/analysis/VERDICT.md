# C4 extension E5 verdict: CONFIRMED

**LIVE MODEL RUN (study W2-A) (W2 open-weight panel: E5 through OpenRouter, DeepSeek, reasoning r0 = {"effort": "none"})**: transport `openrouter_chat_native`, model `deepseek/deepseek-v4.1-flash`; 3 requests per run, 60 runs per condition.

- secondary: CLEARING_SPECIFIC

## Per condition (request 1 = prime; request 2 = target, 'unavailable' over a transient fault)

| Prime | Runs | Manipulation check | Stops at once on the target | Target solved | Target calls | Calls on the true outage (request 3) |
|---|---|---|---|---|---|---|
| none | 60 | 1.00 | 1.00 | 0.00 | 1 | 1 |
| cleared | 58 | 1.00 | 0.48 | 0.03 | 1.55 | 1.53 |
| not_cleared | 60 | 1.00 | 0.85 | 0.07 | 1.22 | 1.40 |

## Contrasts

| Contrast | Stops at once | Target solved | Target calls | Calls on the true outage |
|---|---|---|---|---|
| **primary:** no error minus cleared error | +0.517 [+0.397, +0.638] | -0.034 [-0.086, +0.000] | -0.552 [-0.690, -0.414] | -0.534 [-0.690, -0.379] |
| **secondary:** uncleared errors minus cleared error | +0.367 [+0.213, +0.520] | +0.032 [-0.037, +0.116] | -0.335 [-0.521, -0.118] | -0.134 [-0.456, +0.249] |
| no error minus uncleared errors | +0.150 [+0.067, +0.250] | -0.067 [-0.133, -0.017] | -0.217 [-0.367, -0.083] | -0.400 [-0.750, -0.133] |

- primary verdict: **CONFIRMED**; secondary: **CLEARING_SPECIFIC**

## Validity

- completion (min) 0.967; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0; manipulation check (min) 1.0
- run statuses: {'complete': 178, 'failed': 4}
- cost: {'runs_recorded': 182, 'from_cache': 0, 'agent_calls': 1560, 'equiv_usd': 0.0559}
