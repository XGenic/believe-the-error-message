# W2-A: DeepSeek V4.1 Flash reasoning low vs none (E5): UNCLEAR

- A: `runs/or-e5-deepseek-v4-1-flash-r1`
- B: `runs/or-e5-deepseek-v4-1-flash-r0`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| D1 | yes | +0.417 | +0.517 | -0.101 [-0.273, +0.083] | UNCLEAR |
| stop / cleared |  | +0.017 | +0.483 | -0.466 [-0.588, -0.329] | DIFFERENT |
| stop / none |  | +0.433 | +1.000 | -0.567 [-0.683, -0.433] | DIFFERENT |
| stop / not_cleared |  | +0.017 | +0.850 | -0.833 [-0.917, -0.733] | DIFFERENT |
