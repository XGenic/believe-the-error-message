# C4 extension E5 verdict: CONFIRMED

**LIVE MODEL RUN (study W2-A) (W2 open-weight panel: E5 through OpenRouter, Alibaba (Qwen), reasoning r0 = {"effort": "none"})**: transport `openrouter_chat_native`, model `qwen/qwen3.8-27b`; 3 requests per run, 60 runs per condition.

- secondary: INCONCLUSIVE

## Per condition (request 1 = prime; request 2 = target, 'unavailable' over a transient fault)

| Prime | Runs | Manipulation check | Stops at once on the target | Target solved | Target calls | Calls on the true outage (request 3) |
|---|---|---|---|---|---|---|
| none | 60 | 1.00 | 0.90 | 0.02 | 1.12 | 1.17 |
| cleared | 60 | 1.00 | 0.03 | 0.62 | 2.58 | 3.70 |
| not_cleared | 60 | 0.98 | 0.13 | 0.60 | 2.48 | 4.17 |

## Contrasts

| Contrast | Stops at once | Target solved | Target calls | Calls on the true outage |
|---|---|---|---|---|
| **primary:** no error minus cleared error | +0.867 [+0.767, +0.950] | -0.600 [-0.717, -0.467] | -1.467 [-1.633, -1.283] | -2.533 [-2.933, -2.133] |
| **secondary:** uncleared errors minus cleared error | +0.100 [+0.000, +0.200] | -0.017 [-0.183, +0.150] | -0.100 [-0.317, +0.133] | +0.467 [-0.150, +1.067] |
| no error minus uncleared errors | +0.767 [+0.650, +0.883] | -0.583 [-0.717, -0.450] | -1.367 [-1.583, -1.150] | -3.000 [-3.533, -2.467] |

- primary verdict: **CONFIRMED**; secondary: **INCONCLUSIVE**

## Validity

- completion (min) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0; manipulation check (min) 0.9833333333333333
- run statuses: {'complete': 180}
- cost: {'runs_recorded': 180, 'from_cache': 0, 'agent_calls': 2005, 'equiv_usd': 0.3307}
