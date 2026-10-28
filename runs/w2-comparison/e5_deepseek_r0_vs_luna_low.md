# W2-A: DeepSeek V4.1 Flash r0 vs Luna (E5): DIFFERENT

- A: `runs/or-e5-deepseek-v4-1-flash-r0`
- B: `runs/n1-e5-native-low-gpt-6-luna`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| D1 | yes | +0.517 | +0.933 | -0.416 [-0.553, -0.263] | DIFFERENT |
| stop / cleared |  | +0.483 | +0.067 | +0.416 [+0.263, +0.553] | DIFFERENT |
| stop / none |  | +1.000 | +1.000 | +0.000 [+0.000, +0.000] | SAME |
| stop / not_cleared |  | +0.850 | +0.633 | +0.217 [+0.067, +0.367] | DIFFERENT |
