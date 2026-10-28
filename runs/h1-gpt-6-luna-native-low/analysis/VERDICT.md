# C4 study H1 verdict: NO_CARRYOVER

**LIVE MODEL RUN (study H1: GPT-6-luna, native calls, reasoning low)**: transport `openai_responses_native`, model `gpt-6-luna`; 8 training + 4 test requests per run, 30 runs per condition.

- secondary: NOT_APPLICABLE

## Per condition (test block: every call works)

| Training condition | Runs | Training success | Failed calls in training | No-call, last 3 training | **No-call, test block** | Test success |
|---|---|---|---|---|---|---|
| no_failure | 30 | 1.00 | 0.03 | 0.00 | **0.00** | 1.00 |
| controllable | 30 | 0.94 | 19.47 | 0.00 | **0.00** | 1.00 |
| uncontrollable | 30 | 0.00 | 46.27 | 0.00 | **0.00** | 1.00 |
| uncontrollable_temporary | 30 | 0.00 | 44.43 | 0.00 | **0.00** | 1.00 |

## No-call share by request (1–8 training, 9–12 test)

- no_failure: 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00
- controllable: 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00
- uncontrollable: 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00
- uncontrollable_temporary: 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00

## Contrasts

| Contrast | No-call, test | Test success | No-call, last 3 training |
|---|---|---|---|
| **primary:** uncontrollable minus no failure | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| **secondary:** uncontrollable minus controllable | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| message: 'temporary' minus format, both uncontrollable | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |

- primary verdict: **NO_CARRYOVER**; secondary: **NOT_APPLICABLE**

## Validity

- completion (min) 1.000; protocol failures 0.0; tool use on request 1 (min) 1.0; unclassifiable 0.0
- run statuses: {'complete': 120}
- cost: {'runs_recorded': 120, 'from_cache': 0, 'agent_calls': 5692, 'equiv_usd': 0.9678}
