# W5 drift check: Luna C4 low, W5 vs N1-A: SAME

- A: `runs/w5-c4-low-gpt-6-luna`
- B: `runs/n1-c4-native-low-gpt-6-luna`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| S | yes | +0.794 | +0.789 | +0.006 [-0.072, +0.089] | SAME |
| give_up_trap_success | yes | +0.022 | +0.028 | -0.006 [-0.083, +0.067] | SAME |
| retry_trap_success | yes | +0.011 | +0.000 | +0.011 [+0.000, +0.033] | SAME |
| L_star |  | +0.008 | +0.029 | -0.021 [-0.099, +0.064] | SAME |
| success / format / fixable |  | +0.894 | +0.867 | +0.028 [-0.067, +0.128] | SAME |
| success / format / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / format / transient |  | +0.994 | +1.000 | -0.006 [-0.017, +0.000] | SAME |
| success / neutral / fixable |  | +0.194 | +0.156 | +0.039 [-0.067, +0.150] | SAME |
| success / neutral / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / neutral / transient |  | +0.461 | +0.494 | -0.033 [-0.267, +0.211] | UNCLEAR |
| success / permanent / fixable |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / permanent / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / permanent / transient |  | +0.022 | +0.028 | -0.006 [-0.083, +0.067] | SAME |
| success / transient / fixable |  | +0.011 | +0.000 | +0.011 [+0.000, +0.033] | SAME |
| success / transient / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / transient / transient |  | +1.000 | +0.961 | +0.039 [+0.000, +0.117] | SAME |
