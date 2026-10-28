# C4 extension E5 verdict: CONFIRMED

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-e5-clear-learner`; 3 requests per run, 60 runs per condition.

- secondary: CLEARING_SPECIFIC

## Per condition (request 1 = prime; request 2 = target, 'unavailable' over a transient fault)

| Prime | Runs | Manipulation check | Stops at once on the target | Target solved | Target calls | Calls on the true outage (request 3) |
|---|---|---|---|---|---|---|
| none | 60 | 1.00 | 0.92 | 0.05 | 1.13 | 1.23 |
| cleared | 60 | 0.98 | 0.07 | 0.93 | 2.87 | 4.80 |
| not_cleared | 60 | 0.98 | 0.95 | 0.03 | 1.08 | 1.22 |

## Contrasts

| Contrast | Stops at once | Target solved | Target calls | Calls on the true outage |
|---|---|---|---|---|
| **primary:** no error minus cleared error | +0.850 [+0.750, +0.933] | -0.883 [-0.967, -0.800] | -1.733 [-1.883, -1.550] | -3.567 [-3.850, -3.233] |
| **secondary:** uncleared errors minus cleared error | +0.883 [+0.800, +0.967] | -0.900 [-0.967, -0.817] | -1.783 [-1.933, -1.617] | -3.583 [-3.850, -3.267] |
| no error minus uncleared errors | -0.033 [-0.133, +0.050] | +0.017 [-0.050, +0.083] | +0.050 [-0.100, +0.200] | +0.017 [-0.300, +0.333] |

- primary verdict: **CONFIRMED**; secondary: **CLEARING_SPECIFIC**

## Validity

- completion (min) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0; manipulation check (min) 0.9833333333333333
- run statuses: {'complete': 180}
- cost: {'runs_recorded': 180, 'from_cache': 0, 'agent_calls': 1873, 'equiv_usd': 0.0}
