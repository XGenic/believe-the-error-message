# W2-A: gpt-oss-120b r1 (Crusoe) minus Luna reasoning low (C4 grid, native calls): SAME

- A: `runs/or-c4-gpt-oss-120b-r1-crusoe`
- B: `runs/n1-c4-native-low-gpt-6-luna`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| S | yes | +0.922 | +0.789 | +0.133 [+0.067, +0.200] | SAME |
| give_up_trap_success | yes | +0.033 | +0.028 | +0.006 [-0.061, +0.072] | SAME |
| retry_trap_success | yes | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| L_star |  | +0.140 | +0.029 | +0.111 [-0.010, +0.233] | SAME |
| success / format / fixable |  | +0.833 | +0.867 | -0.033 [-0.128, +0.061] | SAME |
| success / format / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / format / transient |  | +1.000 | +1.000 | +0.000 [+0.000, +0.000] | SAME |
| success / neutral / fixable |  | +0.028 | +0.156 | -0.128 [-0.200, -0.050] | SAME |
| success / neutral / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / neutral / transient |  | +1.000 | +0.494 | +0.506 [+0.344, +0.667] | DIFFERENT |
| success / permanent / fixable |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / permanent / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / permanent / transient |  | +0.033 | +0.028 | +0.006 [-0.061, +0.072] | SAME |
| success / transient / fixable |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / transient / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / transient / transient |  | +0.461 | +0.961 | -0.500 [-0.689, -0.317] | DIFFERENT |
