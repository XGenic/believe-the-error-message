# C4 extension E5 verdict: CONFIRMED

**LIVE MODEL RUN (study W2-A) (W2 open-weight panel: E5 through OpenRouter, Alibaba (Qwen), reasoning r1 = {"effort": "low"})**: transport `openrouter_chat_native`, model `qwen/qwen3.8-27b`; 3 requests per run, 60 runs per condition.

- secondary: INCONCLUSIVE

## Per condition (request 1 = prime; request 2 = target, 'unavailable' over a transient fault)

| Prime | Runs | Manipulation check | Stops at once on the target | Target solved | Target calls | Calls on the true outage (request 3) |
|---|---|---|---|---|---|---|
| none | 60 | 1.00 | 0.80 | 0.03 | 1.23 | 1.22 |
| cleared | 60 | 0.98 | 0.10 | 0.60 | 2.50 | 3.90 |
| not_cleared | 60 | 1.00 | 0.25 | 0.48 | 2.23 | 3.42 |

## Contrasts

| Contrast | Stops at once | Target solved | Target calls | Calls on the true outage |
|---|---|---|---|---|
| **primary:** no error minus cleared error | +0.700 [+0.567, +0.817] | -0.567 [-0.683, -0.433] | -1.267 [-1.467, -1.050] | -2.683 [-3.100, -2.233] |
| **secondary:** uncleared errors minus cleared error | +0.150 [+0.017, +0.283] | -0.117 [-0.283, +0.067] | -0.267 [-0.517, +0.000] | -0.483 [-1.133, +0.183] |
| no error minus uncleared errors | +0.550 [+0.400, +0.683] | -0.450 [-0.583, -0.317] | -1.000 [-1.233, -0.750] | -2.200 [-2.717, -1.683] |

- primary verdict: **CONFIRMED**; secondary: **INCONCLUSIVE**

## Validity

- completion (min) 1.000; protocol failures 0.0020060180541624875; tool use on request 1 (min) 1.0; unclassifiable 0.0; manipulation check (min) 0.9833333333333333
- run statuses: {'complete': 180}
- cost: {'runs_recorded': 180, 'from_cache': 0, 'agent_calls': 1994, 'equiv_usd': 0.468}
