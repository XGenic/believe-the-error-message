# W2-C: Haiku 5.5 C4, thinking on vs off: SAME

- A: `runs/w2c-c4-claude-haiku-5-5-t1`
- B: `runs/w2c-c4-claude-haiku-5-5-t0`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| S | yes | +0.606 | +0.694 | -0.089 [-0.139, -0.039] | SAME |
| give_up_trap_success | yes | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| retry_trap_success | yes | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| L_star |  | +0.041 | +0.111 | -0.070 [-0.158, +0.018] | SAME |
| success / format / fixable |  | +0.778 | +0.406 | +0.372 [+0.267, +0.478] | DIFFERENT |
| success / format / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / format / transient |  | +1.000 | +0.033 | +0.967 [+0.900, +1.000] | DIFFERENT |
| success / neutral / fixable |  | +0.044 | +0.000 | +0.044 [+0.011, +0.089] | SAME |
| success / neutral / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / neutral / transient |  | +0.467 | +0.000 | +0.467 [+0.267, +0.633] | DIFFERENT |
| success / permanent / fixable |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / permanent / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / permanent / transient |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / transient / fixable |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / transient / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / transient / transient |  | +1.000 | +0.367 | +0.633 [+0.467, +0.800] | DIFFERENT |
