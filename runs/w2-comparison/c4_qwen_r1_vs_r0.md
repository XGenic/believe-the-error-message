# W2-A: Qwen3.8-27B r1 minus r0 (C4 grid, reasoning effect): DIFFERENT

- A: `runs/or-c4-qwen3-8-27b-r1`
- B: `runs/or-c4-qwen3-8-27b-r0`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| S | yes | +0.783 | +0.500 | +0.283 [+0.194, +0.378] | DIFFERENT |
| give_up_trap_success | yes | +0.061 | +0.033 | +0.028 [-0.067, +0.133] | SAME |
| retry_trap_success | yes | +0.011 | +0.028 | -0.017 [-0.056, +0.022] | SAME |
| L_star |  | +0.126 | +0.078 | +0.049 [-0.059, +0.148] | SAME |
| success / format / fixable |  | +0.922 | +0.744 | +0.178 [+0.078, +0.278] | DIFFERENT |
| success / format / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / format / transient |  | +0.972 | +0.978 | -0.006 [-0.078, +0.050] | SAME |
| success / neutral / fixable |  | +0.189 | +0.156 | +0.033 [-0.061, +0.133] | SAME |
| success / neutral / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / neutral / transient |  | +0.744 | +0.528 | +0.217 [-0.022, +0.444] | UNCLEAR |
| success / permanent / fixable |  | +0.011 | +0.000 | +0.011 [+0.000, +0.033] | SAME |
| success / permanent / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / permanent / transient |  | +0.061 | +0.033 | +0.028 [-0.067, +0.133] | SAME |
| success / transient / fixable |  | +0.011 | +0.028 | -0.017 [-0.056, +0.022] | SAME |
| success / transient / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / transient / transient |  | +0.994 | +0.967 | +0.028 [-0.011, +0.100] | SAME |
