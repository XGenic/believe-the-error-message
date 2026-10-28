# C4 extension E5 verdict: NOT_CONFIRMED

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-e5-credulous`; 3 requests per run, 60 runs per condition.

- secondary: NOT_APPLICABLE

## Per condition (request 1 = prime; request 2 = target, 'unavailable' over a transient fault)

| Prime | Runs | Manipulation check | Stops at once on the target | Target solved | Target calls | Calls on the true outage (request 3) |
|---|---|---|---|---|---|---|
| none | 60 | 1.00 | 0.92 | 0.05 | 1.13 | 1.03 |
| cleared | 60 | 0.98 | 0.93 | 0.05 | 1.12 | 1.10 |
| not_cleared | 60 | 0.98 | 0.95 | 0.03 | 1.08 | 1.08 |

## Contrasts

| Contrast | Stops at once | Target solved | Target calls | Calls on the true outage |
|---|---|---|---|---|
| **primary:** no error minus cleared error | -0.017 [-0.117, +0.083] | +0.000 [-0.067, +0.083] | +0.017 [-0.150, +0.183] | -0.067 [-0.217, +0.050] |
| **secondary:** uncleared errors minus cleared error | +0.017 [-0.067, +0.100] | -0.017 [-0.083, +0.050] | -0.033 [-0.183, +0.117] | -0.017 [-0.200, +0.150] |
| no error minus uncleared errors | -0.033 [-0.133, +0.050] | +0.017 [-0.050, +0.083] | +0.050 [-0.100, +0.200] | -0.050 [-0.167, +0.050] |

- primary verdict: **NOT_CONFIRMED**; secondary: **NOT_APPLICABLE**

## Validity

- completion (min) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0; manipulation check (min) 0.9833333333333333
- run statuses: {'complete': 180}
- cost: {'runs_recorded': 180, 'from_cache': 0, 'agent_calls': 1526, 'equiv_usd': 0.0}
