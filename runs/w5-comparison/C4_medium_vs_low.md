# W5: Luna C4, reasoning medium vs low: SAME

- A: `runs/w5-c4-medium-gpt-6-luna`
- B: `runs/w5-c4-low-gpt-6-luna`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| S | yes | +0.922 | +0.794 | +0.128 [+0.061, +0.194] | SAME |
| give_up_trap_success | yes | +0.144 | +0.022 | +0.122 [+0.022, +0.233] | SAME |
| retry_trap_success | yes | +0.011 | +0.011 | +0.000 [-0.033, +0.033] | SAME |
| L_star |  | +0.067 | +0.008 | +0.059 [-0.014, +0.131] | SAME |
| success / format / fixable |  | +0.889 | +0.894 | -0.006 [-0.089, +0.089] | SAME |
| success / format / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / format / transient |  | +0.989 | +0.994 | -0.006 [-0.028, +0.011] | SAME |
| success / neutral / fixable |  | +0.261 | +0.194 | +0.067 [-0.033, +0.161] | SAME |
| success / neutral / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / neutral / transient |  | +0.806 | +0.461 | +0.344 [+0.139, +0.539] | DIFFERENT |
| success / permanent / fixable |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / permanent / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / permanent / transient |  | +0.144 | +0.022 | +0.122 [+0.022, +0.233] | SAME |
| success / transient / fixable |  | +0.011 | +0.011 | +0.000 [-0.033, +0.033] | SAME |
| success / transient / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / transient / transient |  | +1.000 | +1.000 | +0.000 [+0.000, +0.000] | SAME |
