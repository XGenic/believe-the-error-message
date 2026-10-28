# C4 study H1 verdict: INVALID

**MOCK INSTRUMENT VALIDATION, NOT EVIDENCE**: transport `mock`, model `MOCK-h1-non-engager`; 8 training + 4 test requests per run, 30 runs per condition.

- tool use on request 1 0.0 below 0.9 in some cell: agents did not engage
- unclassifiable responses None above 0.1

## Per condition (test block: every call works)

| Training condition | Runs | Training success | Failed calls in training | No-call, last 3 training | **No-call, test block** | Test success |
|---|---|---|---|---|---|---|
| no_failure | 30 | 0.00 | 0 | 1.00 | **1.00** | 0.00 |
| controllable | 30 | 0.00 | 0 | 1.00 | **1.00** | 0.00 |
| uncontrollable | 30 | 0.00 | 0 | 1.00 | **1.00** | 0.00 |
| uncontrollable_temporary | 30 | 0.00 | 0 | 1.00 | **1.00** | 0.00 |

## No-call share by request (1–8 training, 9–12 test)

- no_failure: 1.00 1.00 1.00 1.00 1.00 1.00 1.00 1.00 1.00 1.00 1.00 1.00
- controllable: 1.00 1.00 1.00 1.00 1.00 1.00 1.00 1.00 1.00 1.00 1.00 1.00
- uncontrollable: 1.00 1.00 1.00 1.00 1.00 1.00 1.00 1.00 1.00 1.00 1.00 1.00
- uncontrollable_temporary: 1.00 1.00 1.00 1.00 1.00 1.00 1.00 1.00 1.00 1.00 1.00 1.00

## Contrasts

| Contrast | No-call, test | Test success | No-call, last 3 training |
|---|---|---|---|
| **primary:** uncontrollable minus no failure | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| **secondary:** uncontrollable minus controllable | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| message: 'temporary' minus format, both uncontrollable | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |

- primary verdict: **NO_CARRYOVER**; secondary: **NOT_APPLICABLE**

## Validity

- completion (min) 1.000; protocol failures 0.0; tool use on request 1 (min) 0.0; unclassifiable None
- run statuses: {'complete': 120}
- cost: {'runs_recorded': 120, 'from_cache': 120, 'agent_calls': 1440, 'equiv_usd': 0.0}
