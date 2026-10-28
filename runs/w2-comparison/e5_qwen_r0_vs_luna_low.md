# W2-A: Qwen3.8-27B r0 minus Luna (E5, native calls): SAME

- A: `runs/or-e5-qwen3-8-27b-r0`
- B: `runs/n1-e5-native-low-gpt-6-luna`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| D1 | yes | +0.867 | +0.933 | -0.067 [-0.167, +0.033] | SAME |
| stop / cleared |  | +0.033 | +0.067 | -0.033 [-0.117, +0.033] | SAME |
| stop / none |  | +0.900 | +1.000 | -0.100 [-0.183, -0.033] | SAME |
| stop / not_cleared |  | +0.133 | +0.633 | -0.500 [-0.650, -0.350] | DIFFERENT |
