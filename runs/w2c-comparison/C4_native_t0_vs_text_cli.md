# W2-C format: Haiku 5.5 C4, native API thinking off vs text through the CLI: DIFFERENT

- A: `runs/w2c-c4-claude-haiku-5-5-t0`
- B: `runs/live-claude-haiku-5-5`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| S | yes | +0.694 | +0.344 | +0.350 [+0.306, +0.394] | DIFFERENT |
| give_up_trap_success | yes | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| retry_trap_success | yes | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| L_star |  | +0.111 | -0.004 | +0.115 [+0.042, +0.190] | SAME |
| success / format / fixable |  | +0.406 | +0.972 | -0.567 [-0.644, -0.489] | DIFFERENT |
| success / format / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / format / transient |  | +0.033 | +1.000 | -0.967 [-1.000, -0.900] | DIFFERENT |
| success / neutral / fixable |  | +0.000 | +0.100 | -0.100 [-0.156, -0.044] | SAME |
| success / neutral / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / neutral / transient |  | +0.000 | +0.967 | -0.967 [-1.000, -0.900] | DIFFERENT |
| success / permanent / fixable |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / permanent / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / permanent / transient |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / transient / fixable |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / transient / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / transient / transient |  | +0.367 | +1.000 | -0.633 [-0.800, -0.467] | DIFFERENT |
