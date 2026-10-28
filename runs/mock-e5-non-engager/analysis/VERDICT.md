# C4 extension E5 verdict: INVALID

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-e5-non-engager`; 3 requests per run, 60 runs per condition.

- tool use on request 1 0.0 below 0.9 in some cell: agents did not engage
- unclassifiable responses None above 0.1
- manipulation check 0.0 below 0.8 in some condition: the prime did not give the intended experience
- the primary contrast could not be estimated

## Per condition (request 1 = prime; request 2 = target, 'unavailable' over a transient fault)

| Prime | Runs | Manipulation check | Stops at once on the target | Target solved | Target calls | Calls on the true outage (request 3) |
|---|---|---|---|---|---|---|
| none | 60 | 0.00 | n/a | 0.00 | 0 | 0 |
| cleared | 60 | 0.00 | n/a | 0.00 | 0 | 0 |
| not_cleared | 60 | 0.00 | n/a | 0.00 | 0 | 0 |

## Contrasts

| Contrast | Stops at once | Target solved | Target calls | Calls on the true outage |
|---|---|---|---|---|
| **primary:** no error minus cleared error | n/a | +0.000 [+0.000, +0.000] | 0 [0, 0] | 0 [0, 0] |
| **secondary:** uncleared errors minus cleared error | n/a | +0.000 [+0.000, +0.000] | 0 [0, 0] | 0 [0, 0] |
| no error minus uncleared errors | n/a | +0.000 [+0.000, +0.000] | 0 [0, 0] | 0 [0, 0] |

- primary verdict: **NOT_ESTIMABLE**; secondary: **NOT_APPLICABLE**

## Validity

- completion (min) 1.000; protocol failures 0.0; tool use on request 1 (min) 0.0; unclassifiable None; manipulation check (min) 0.0
- run statuses: {'complete': 180}
- cost: {'runs_recorded': 180, 'from_cache': 0, 'agent_calls': 540, 'equiv_usd': 0.0}
