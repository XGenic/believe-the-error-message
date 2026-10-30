# W2-D: Sol, C4, high minus low: SAME

- A: `runs/w2d-c4-gpt-6-1-sol-high`
- B: `runs/w2d-c4-gpt-6-1-sol-low`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| S | yes | +0.667 | +0.667 | +0.000 [+0.000, +0.000] | SAME |
| give_up_trap_success | yes | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| retry_trap_success | yes | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| L_star |  | +0.013 | +0.020 | -0.007 [-0.033, +0.017] | SAME |
| success / format / fixable |  | +1.000 | +1.000 | +0.000 [+0.000, +0.000] | SAME |
| success / format / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / format / transient |  | +1.000 | +1.000 | +0.000 [+0.000, +0.000] | SAME |
| success / neutral / fixable |  | +0.056 | +0.011 | +0.044 [+0.000, +0.089] | SAME |
| success / neutral / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / neutral / transient |  | +1.000 | +1.000 | +0.000 [+0.000, +0.000] | SAME |
| success / permanent / fixable |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / permanent / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / permanent / transient |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / transient / fixable |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / transient / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / transient / transient |  | +1.000 | +1.000 | +0.000 [+0.000, +0.000] | SAME |
