# C4 study H1 verdict: CARRYOVER

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-h1-failure-counter`; 8 training + 4 test requests per run, 30 runs per condition.

- secondary: FAILURE_GENERAL

## Per condition (test block: every call works)

| Training condition | Runs | Training success | Failed calls in training | No-call, last 3 training | **No-call, test block** | Test success |
|---|---|---|---|---|---|---|
| no_failure | 30 | 1.00 | 0 | 0.00 | **0.00** | 1.00 |
| controllable | 30 | 0.76 | 13.30 | 0.51 | **0.82** | 0.18 |
| uncontrollable | 30 | 0.00 | 15.53 | 0.77 | **0.78** | 0.22 |
| uncontrollable_temporary | 30 | 0.00 | 18.67 | 0.79 | **0.81** | 0.19 |

## No-call share by request (1–8 training, 9–12 test)

- no_failure: 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00
- controllable: 0.00 0.00 0.00 0.00 0.03 0.17 0.53 0.83 0.77 0.87 0.77 0.87
- uncontrollable: 0.00 0.00 0.00 0.77 0.93 0.83 0.77 0.70 0.80 0.77 0.73 0.83
- uncontrollable_temporary: 0.00 0.00 0.70 0.83 0.93 0.73 0.80 0.83 0.80 0.80 0.83 0.80

## Contrasts

| Contrast | No-call, test | Test success | No-call, last 3 training |
|---|---|---|---|
| **primary:** uncontrollable minus no failure | +0.783 [+0.708, +0.858] | -0.783 [-0.858, -0.708] | +0.767 [+0.667, +0.867] |
| **secondary:** uncontrollable minus controllable | -0.033 [-0.142, +0.067] | +0.033 [-0.067, +0.142] | +0.256 [+0.122, +0.389] |
| message: 'temporary' minus format, both uncontrollable | +0.025 [-0.083, +0.142] | -0.025 [-0.133, +0.083] | +0.022 [-0.100, +0.156] |

- primary verdict: **CARRYOVER**; secondary: **FAILURE_GENERAL**

## Validity

- completion (min) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 120}
- cost: {'runs_recorded': 120, 'from_cache': 120, 'agent_calls': 3478, 'equiv_usd': 0.0}
