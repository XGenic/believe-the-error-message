# W5: Luna C4, reasoning high vs low: SAME

- A: `runs/w5-c4-high-gpt-6-luna`
- B: `runs/w5-c4-low-gpt-6-luna`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| S | yes | +0.939 | +0.794 | +0.144 [+0.078, +0.211] | SAME |
| give_up_trap_success | yes | +0.106 | +0.022 | +0.083 [+0.000, +0.178] | SAME |
| retry_trap_success | yes | +0.011 | +0.011 | +0.000 [-0.033, +0.033] | SAME |
| L_star |  | +0.030 | +0.008 | +0.022 [-0.057, +0.102] | SAME |
| success / format / fixable |  | +0.911 | +0.894 | +0.017 [-0.061, +0.106] | SAME |
| success / format / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / format / transient |  | +1.000 | +0.994 | +0.006 [+0.000, +0.017] | SAME |
| success / neutral / fixable |  | +0.317 | +0.194 | +0.122 [+0.017, +0.222] | SAME |
| success / neutral / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / neutral / transient |  | +0.889 | +0.461 | +0.428 [+0.228, +0.617] | DIFFERENT |
| success / permanent / fixable |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / permanent / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / permanent / transient |  | +0.106 | +0.022 | +0.083 [+0.000, +0.178] | SAME |
| success / transient / fixable |  | +0.011 | +0.011 | +0.000 [-0.033, +0.033] | SAME |
| success / transient / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / transient / transient |  | +1.000 | +1.000 | +0.000 [+0.000, +0.000] | SAME |
