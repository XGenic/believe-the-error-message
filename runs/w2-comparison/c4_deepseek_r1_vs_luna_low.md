# W2-A: DeepSeek V4.1 Flash r1 vs Luna reasoning low (C4): DIFFERENT

- A: `runs/or-c4-deepseek-v4-1-flash-r1`
- B: `runs/n1-c4-native-low-gpt-6-luna`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| S | yes | +0.661 | +0.789 | -0.128 [-0.183, -0.067] | SAME |
| give_up_trap_success | yes | +0.017 | +0.028 | -0.011 [-0.083, +0.050] | SAME |
| retry_trap_success | yes | +0.161 | +0.000 | +0.161 [+0.100, +0.228] | DIFFERENT |
| L_star |  | -0.010 | +0.029 | -0.039 [-0.140, +0.063] | SAME |
| success / format / fixable |  | +0.944 | +0.867 | +0.078 [+0.000, +0.161] | SAME |
| success / format / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / format / transient |  | +1.000 | +1.000 | +0.000 [+0.000, +0.000] | SAME |
| success / neutral / fixable |  | +0.456 | +0.156 | +0.300 [+0.178, +0.417] | DIFFERENT |
| success / neutral / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / neutral / transient |  | +1.000 | +0.494 | +0.506 [+0.344, +0.667] | DIFFERENT |
| success / permanent / fixable |  | +0.011 | +0.000 | +0.011 [+0.000, +0.033] | SAME |
| success / permanent / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / permanent / transient |  | +0.017 | +0.028 | -0.011 [-0.083, +0.050] | SAME |
| success / transient / fixable |  | +0.161 | +0.000 | +0.161 [+0.100, +0.228] | DIFFERENT |
| success / transient / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / transient / transient |  | +1.000 | +0.961 | +0.039 [+0.000, +0.117] | SAME |
