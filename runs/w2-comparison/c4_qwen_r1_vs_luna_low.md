# W2-A: Qwen3.8-27B r1 minus Luna reasoning low (C4 grid, native calls): SAME

- A: `runs/or-c4-qwen3-8-27b-r1`
- B: `runs/n1-c4-native-low-gpt-6-luna`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| S | yes | +0.783 | +0.789 | -0.006 [-0.089, +0.083] | SAME |
| give_up_trap_success | yes | +0.061 | +0.028 | +0.033 [-0.056, +0.133] | SAME |
| retry_trap_success | yes | +0.011 | +0.000 | +0.011 [+0.000, +0.033] | SAME |
| L_star |  | +0.126 | +0.029 | +0.098 [+0.002, +0.190] | SAME |
| success / format / fixable |  | +0.922 | +0.867 | +0.056 [-0.028, +0.144] | SAME |
| success / format / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / format / transient |  | +0.972 | +1.000 | -0.028 [-0.083, +0.000] | SAME |
| success / neutral / fixable |  | +0.189 | +0.156 | +0.033 [-0.067, +0.133] | SAME |
| success / neutral / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / neutral / transient |  | +0.744 | +0.494 | +0.250 [+0.017, +0.478] | DIFFERENT |
| success / permanent / fixable |  | +0.011 | +0.000 | +0.011 [+0.000, +0.033] | SAME |
| success / permanent / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / permanent / transient |  | +0.061 | +0.028 | +0.033 [-0.056, +0.133] | SAME |
| success / transient / fixable |  | +0.011 | +0.000 | +0.011 [+0.000, +0.033] | SAME |
| success / transient / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / transient / transient |  | +0.994 | +0.961 | +0.033 [-0.011, +0.111] | SAME |
