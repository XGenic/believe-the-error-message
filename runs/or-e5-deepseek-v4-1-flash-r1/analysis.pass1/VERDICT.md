# C4 extension E5 verdict: INVALID

**LIVE MODEL RUN (study W2-A) (W2 open-weight panel: E5 through OpenRouter, DeepSeek, reasoning r1 = {"effort": "low"})**: transport `openrouter_chat_native`, model `deepseek/deepseek-v4.1-flash`; 3 requests per run, 60 runs per condition.

- completion 0.550 below 0.95 in some cell

## Per condition (request 1 = prime; request 2 = target, 'unavailable' over a transient fault)

| Prime | Runs | Manipulation check | Stops at once on the target | Target solved | Target calls | Calls on the true outage (request 3) |
|---|---|---|---|---|---|---|
| none | 34 | 1.00 | 0.44 | 0.00 | 1.56 | 1.85 |
| cleared | 33 | 1.00 | 0.00 | 0.58 | 2.58 | 4.67 |
| not_cleared | 35 | 1.00 | 0.03 | 0.40 | 2.54 | 3.74 |

## Contrasts

| Contrast | Stops at once | Target solved | Target calls | Calls on the true outage |
|---|---|---|---|---|
| **primary:** no error minus cleared error | +0.441 [+0.294, +0.618] | -0.576 [-0.727, -0.394] | -1.017 [-1.256, -0.781] | -2.814 [-3.411, -2.209] |
| **secondary:** uncleared errors minus cleared error | +0.029 [+0.000, +0.086] | -0.176 [-0.413, +0.061] | -0.033 [-0.294, +0.231] | -0.924 [-1.728, -0.097] |
| no error minus uncleared errors | +0.413 [+0.238, +0.589] | -0.400 [-0.571, -0.229] | -0.984 [-1.245, -0.728] | -1.890 [-2.524, -1.292] |

- primary verdict: **CONFIRMED**; secondary: **EXPOSURE_GENERAL**

## Validity

- completion (min) 0.550; protocol failures 0.0008169934640522876; tool use on request 1 (min) 1.0; unclassifiable 0.0; manipulation check (min) 1.0
- run statuses: {'complete': 102, 'failed': 176}
- cost: {'runs_recorded': 278, 'from_cache': 0, 'agent_calls': 1289, 'equiv_usd': 0.0622}
