# W2-A: Qwen3.8-27B r1 minus Luna (E5, native calls): DIFFERENT

- A: `runs/or-e5-qwen3-8-27b-r1`
- B: `runs/n1-e5-native-low-gpt-6-luna`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| D1 | yes | +0.700 | +0.933 | -0.233 [-0.383, -0.100] | DIFFERENT |
| stop / cleared |  | +0.100 | +0.067 | +0.033 [-0.067, +0.133] | SAME |
| stop / none |  | +0.800 | +1.000 | -0.200 [-0.300, -0.100] | DIFFERENT |
| stop / not_cleared |  | +0.250 | +0.633 | -0.383 [-0.550, -0.217] | DIFFERENT |
