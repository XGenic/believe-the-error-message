# W2-A: DeepSeek V4.1 Flash r1 vs Luna (E5): DIFFERENT

- A: `runs/or-e5-deepseek-v4-1-flash-r1`
- B: `runs/n1-e5-native-low-gpt-6-luna`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| D1 | yes | +0.417 | +0.933 | -0.517 [-0.650, -0.367] | DIFFERENT |
| stop / cleared |  | +0.017 | +0.067 | -0.050 [-0.117, +0.017] | SAME |
| stop / none |  | +0.433 | +1.000 | -0.567 [-0.683, -0.433] | DIFFERENT |
| stop / not_cleared |  | +0.017 | +0.633 | -0.617 [-0.750, -0.483] | DIFFERENT |
