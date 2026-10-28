# W2-A: DeepSeek V4.1 Flash reasoning low vs none (C4): DIFFERENT

- A: `runs/or-c4-deepseek-v4-1-flash-r1`
- B: `runs/or-c4-deepseek-v4-1-flash-r0`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| S | yes | +0.661 | +0.783 | -0.122 [-0.183, -0.061] | SAME |
| give_up_trap_success | yes | +0.017 | +0.000 | +0.017 [+0.000, +0.050] | SAME |
| retry_trap_success | yes | +0.161 | +0.000 | +0.161 [+0.094, +0.228] | DIFFERENT |
| L_star |  | -0.010 | +0.027 | -0.037 [-0.126, +0.048] | SAME |
| success / format / fixable |  | +0.944 | +0.778 | +0.167 [+0.072, +0.267] | DIFFERENT |
| success / format / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / format / transient |  | +1.000 | +0.633 | +0.367 [+0.211, +0.533] | DIFFERENT |
| success / neutral / fixable |  | +0.456 | +0.028 | +0.428 [+0.328, +0.522] | DIFFERENT |
| success / neutral / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / neutral / transient |  | +1.000 | +0.283 | +0.717 [+0.550, +0.867] | DIFFERENT |
| success / permanent / fixable |  | +0.011 | +0.000 | +0.011 [+0.000, +0.033] | SAME |
| success / permanent / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / permanent / transient |  | +0.017 | +0.000 | +0.017 [+0.000, +0.050] | SAME |
| success / transient / fixable |  | +0.161 | +0.000 | +0.161 [+0.094, +0.228] | DIFFERENT |
| success / transient / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / transient / transient |  | +1.000 | +0.994 | +0.006 [+0.000, +0.023] | SAME |
