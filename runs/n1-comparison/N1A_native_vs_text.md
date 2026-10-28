# N1-A: C4 grid, native tool calls minus text format (Luna, reasoning low): DIFFERENT

- A: `runs/n1-c4-native-low-gpt-6-luna`
- B: `runs/live-gpt-6-luna`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| S | yes | +0.789 | +0.956 | -0.167 [-0.228, -0.100] | DIFFERENT |
| give_up_trap_success | yes | +0.028 | +0.000 | +0.028 [+0.000, +0.083] | SAME |
| retry_trap_success | yes | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| L_star |  | +0.029 | +0.000 | +0.029 [-0.040, +0.096] | SAME |
| success / format / fixable |  | +0.867 | +0.956 | -0.089 [-0.172, -0.006] | SAME |
| success / format / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / format / transient |  | +1.000 | +0.994 | +0.006 [+0.000, +0.017] | SAME |
| success / neutral / fixable |  | +0.156 | +0.206 | -0.050 [-0.139, +0.044] | SAME |
| success / neutral / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / neutral / transient |  | +0.494 | +0.672 | -0.178 [-0.389, +0.050] | UNCLEAR |
| success / permanent / fixable |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / permanent / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / permanent / transient |  | +0.028 | +0.000 | +0.028 [+0.000, +0.083] | SAME |
| success / transient / fixable |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / transient / permanent |  | +0.000 | +0.000 | +0.000 [+0.000, +0.000] | SAME |
| success / transient / transient |  | +0.961 | +1.000 | -0.039 [-0.117, +0.000] | SAME |
