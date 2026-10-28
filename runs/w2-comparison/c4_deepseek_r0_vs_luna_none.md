# W2-A: DeepSeek V4.1 Flash r0 vs Luna reasoning none (C4): DIFFERENT

- A: `runs/or-c4-deepseek-v4-1-flash-r0`
- B: `runs/n1-c4-native-none-gpt-6-luna`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| S | yes | +0.783 | +0.544 | +0.239 [+0.156, +0.322] | DIFFERENT |
| give_up_trap_success | yes | +0.000 | +0.050 | -0.050 [-0.122, +0.000] | SAME |
| retry_trap_success | yes | +0.000 | +0.011 | -0.011 [-0.033, +0.000] | SAME |
| L_star |  | +0.027 | +0.124 | -0.098 [-0.176, -0.018] | SAME |
| success / format / fixable |  | +0.778 | +0.828 | -0.050 [-0.178, +0.083] | SAME |
| success / format / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / format / transient |  | +0.633 | +0.978 | -0.344 [-0.522, -0.178] | DIFFERENT |
| success / neutral / fixable |  | +0.028 | +0.044 | -0.017 [-0.067, +0.028] | SAME |
| success / neutral / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / neutral / transient |  | +0.283 | +0.250 | +0.033 [-0.200, +0.250] | UNCLEAR |
| success / permanent / fixable |  | +0.000 | +0.039 | -0.039 [-0.100, +0.000] | SAME |
| success / permanent / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / permanent / transient |  | +0.000 | +0.050 | -0.050 [-0.122, +0.000] | SAME |
| success / transient / fixable |  | +0.000 | +0.011 | -0.011 [-0.033, +0.000] | SAME |
| success / transient / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / transient / transient |  | +0.994 | +0.956 | +0.039 [-0.006, +0.117] | SAME |
