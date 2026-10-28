# C4 study H1 verdict: CARRYOVER

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-h1-helpless`; 8 training + 4 test requests per run, 30 runs per condition.

- secondary: CONTROLLABILITY_MATTERS

## Per condition (test block: every call works)

| Training condition | Runs | Training success | Failed calls in training | No-call, last 3 training | **No-call, test block** | Test success |
|---|---|---|---|---|---|---|
| no_failure | 30 | 1.00 | 0 | 0.00 | **0.00** | 1.00 |
| controllable | 30 | 0.94 | 16.03 | 0.00 | **0.00** | 1.00 |
| uncontrollable | 30 | 0.00 | 14.97 | 0.79 | **0.77** | 0.23 |
| uncontrollable_temporary | 30 | 0.00 | 23.70 | 0.78 | **0.84** | 0.16 |

## No-call share by request (1–8 training, 9–12 test)

- no_failure: 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00
- controllable: 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00
- uncontrollable: 0.00 0.00 0.00 0.83 0.97 0.87 0.77 0.73 0.73 0.77 0.73 0.83
- uncontrollable_temporary: 0.00 0.00 0.00 0.83 0.80 0.80 0.77 0.77 0.87 0.90 0.80 0.80

## Contrasts

| Contrast | No-call, test | Test success | No-call, last 3 training |
|---|---|---|---|
| **primary:** uncontrollable minus no failure | +0.767 [+0.692, +0.842] | -0.767 [-0.842, -0.692] | +0.789 [+0.689, +0.878] |
| **secondary:** uncontrollable minus controllable | +0.767 [+0.692, +0.842] | -0.767 [-0.842, -0.692] | +0.789 [+0.689, +0.878] |
| message: 'temporary' minus format, both uncontrollable | +0.075 [-0.025, +0.175] | -0.075 [-0.175, +0.025] | -0.011 [-0.133, +0.111] |

- primary verdict: **CARRYOVER**; secondary: **CONTROLLABILITY_MATTERS**

## Validity

- completion (min) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 120}
- cost: {'runs_recorded': 120, 'from_cache': 120, 'agent_calls': 3833, 'equiv_usd': 0.0}
