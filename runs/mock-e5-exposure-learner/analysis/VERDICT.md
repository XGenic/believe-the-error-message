# C4 extension E5 verdict: CONFIRMED

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-e5-exposure-learner`; 3 requests per run, 60 runs per condition.

- secondary: EXPOSURE_GENERAL

## Per condition (request 1 = prime; request 2 = target, 'unavailable' over a transient fault)

| Prime | Runs | Manipulation check | Stops at once on the target | Target solved | Target calls | Calls on the true outage (request 3) |
|---|---|---|---|---|---|---|
| none | 60 | 1.00 | 0.92 | 0.05 | 1.13 | 1.37 |
| cleared | 60 | 0.98 | 0.07 | 0.93 | 2.87 | 4.80 |
| not_cleared | 60 | 0.98 | 0.08 | 0.92 | 2.83 | 4.83 |

## Contrasts

| Contrast | Stops at once | Target solved | Target calls | Calls on the true outage |
|---|---|---|---|---|
| **primary:** no error minus cleared error | +0.850 [+0.750, +0.933] | -0.883 [-0.967, -0.800] | -1.733 [-1.883, -1.550] | -3.433 [-3.767, -3.050] |
| **secondary:** uncleared errors minus cleared error | +0.017 [-0.083, +0.100] | -0.017 [-0.100, +0.083] | -0.033 [-0.200, +0.167] | +0.033 [-0.267, +0.333] |
| no error minus uncleared errors | +0.833 [+0.733, +0.917] | -0.867 [-0.950, -0.783] | -1.700 [-1.867, -1.517] | -3.467 [-3.800, -3.083] |

- primary verdict: **CONFIRMED**; secondary: **EXPOSURE_GENERAL**

## Validity

- completion (min) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0; manipulation check (min) 0.9833333333333333
- run statuses: {'complete': 180}
- cost: {'runs_recorded': 180, 'from_cache': 0, 'agent_calls': 2203, 'equiv_usd': 0.0}
