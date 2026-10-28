# W2-A: Qwen3.8-27B r0 minus Luna reasoning none (C4 grid, native calls): SAME

- A: `runs/or-c4-qwen3-8-27b-r0`
- B: `runs/n1-c4-native-none-gpt-6-luna`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| S | yes | +0.500 | +0.544 | -0.044 [-0.139, +0.056] | SAME |
| give_up_trap_success | yes | +0.033 | +0.050 | -0.017 [-0.106, +0.078] | SAME |
| retry_trap_success | yes | +0.028 | +0.011 | +0.017 [-0.022, +0.056] | SAME |
| L_star |  | +0.078 | +0.124 | -0.047 [-0.150, +0.054] | SAME |
| success / format / fixable |  | +0.744 | +0.828 | -0.083 [-0.200, +0.044] | SAME |
| success / format / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / format / transient |  | +0.978 | +0.978 | +0.000 [-0.050, +0.050] | SAME |
| success / neutral / fixable |  | +0.156 | +0.044 | +0.111 [+0.033, +0.194] | SAME |
| success / neutral / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / neutral / transient |  | +0.528 | +0.250 | +0.278 [+0.044, +0.511] | DIFFERENT |
| success / permanent / fixable |  | +0.000 | +0.039 | -0.039 [-0.100, +0.000] | SAME |
| success / permanent / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / permanent / transient |  | +0.033 | +0.050 | -0.017 [-0.106, +0.078] | SAME |
| success / transient / fixable |  | +0.028 | +0.011 | +0.017 [-0.022, +0.056] | SAME |
| success / transient / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / transient / transient |  | +0.967 | +0.956 | +0.011 [-0.089, +0.106] | SAME |
