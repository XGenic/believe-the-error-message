# W2-D: C4 at low, Sol minus Luna (W5): SAME

- A: `runs/w2d-c4-gpt-6-1-sol-low`
- B: `runs/w5-c4-low-gpt-6-luna`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| S | yes | +0.667 | +0.794 | -0.128 [-0.183, -0.072] | SAME |
| give_up_trap_success | yes | +0.000 | +0.022 | -0.022 [-0.067, +0.000] | SAME |
| retry_trap_success | yes | +0.000 | +0.011 | -0.011 [-0.033, +0.000] | SAME |
| L_star |  | +0.020 | +0.008 | +0.012 [-0.048, +0.069] | SAME |
| success / format / fixable |  | +1.000 | +0.894 | +0.106 [+0.044, +0.172] | SAME |
| success / format / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / format / transient |  | +1.000 | +0.994 | +0.006 [+0.000, +0.017] | SAME |
| success / neutral / fixable |  | +0.011 | +0.194 | -0.183 [-0.272, -0.106] | DIFFERENT |
| success / neutral / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / neutral / transient |  | +1.000 | +0.461 | +0.539 [+0.372, +0.711] | DIFFERENT |
| success / permanent / fixable |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / permanent / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / permanent / transient |  | +0.000 | +0.022 | -0.022 [-0.067, +0.000] | SAME |
| success / transient / fixable |  | +0.000 | +0.011 | -0.011 [-0.033, +0.000] | SAME |
| success / transient / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / transient / transient |  | +1.000 | +1.000 | +0.000 [+0.000, +0.000] | SAME |
