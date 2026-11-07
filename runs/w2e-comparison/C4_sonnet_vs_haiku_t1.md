# W2-E: Sonnet 5.5 minus Haiku 5.5, thinking on (C4): SAME

- A: `runs/w2e-c4-claude-sonnet-5-5`
- B: `runs/w2c-c4-claude-haiku-5-5-t1`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| S | yes | +0.667 | +0.606 | +0.061 [+0.028, +0.100] | SAME |
| give_up_trap_success | yes | +0.067 | +0.000 | +0.067 [+0.000, +0.167] | SAME |
| retry_trap_success | yes | +0.056 | +0.000 | +0.056 [+0.011, +0.100] | SAME |
| L_star |  | -0.145 | +0.041 | -0.186 [-0.287, -0.079] | DIFFERENT |
| success / format / fixable |  | +0.989 | +0.778 | +0.211 [+0.133, +0.283] | DIFFERENT |
| success / format / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / format / transient |  | +1.000 | +1.000 | +0.000 [+0.000, +0.000] | SAME |
| success / neutral / fixable |  | +0.189 | +0.044 | +0.144 [+0.056, +0.244] | SAME |
| success / neutral / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / neutral / transient |  | +1.000 | +0.467 | +0.533 [+0.367, +0.700] | DIFFERENT |
| success / permanent / fixable |  | +0.022 | +0.000 | +0.022 [+0.000, +0.056] | SAME |
| success / permanent / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / permanent / transient |  | +0.067 | +0.000 | +0.067 [+0.000, +0.167] | SAME |
| success / transient / fixable |  | +0.056 | +0.000 | +0.056 [+0.011, +0.100] | SAME |
| success / transient / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / transient / transient |  | +1.000 | +1.000 | +0.000 [+0.000, +0.000] | SAME |
