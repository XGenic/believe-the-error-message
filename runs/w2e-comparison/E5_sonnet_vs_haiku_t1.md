# W2-E: Sonnet 5.5 minus Haiku 5.5, thinking on (E5): SAME

- A: `runs/w2e-e5-claude-sonnet-5-5`
- B: `runs/w2c-e5-claude-haiku-5-5-t1`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| D1 | yes | +0.000 | +0.033 | -0.033 [-0.133, +0.067] | SAME |
| stop / cleared |  | +0.000 | +0.083 | -0.083 [-0.150, -0.017] | SAME |
| stop / none |  | +0.000 | +0.117 | -0.117 [-0.200, -0.033] | SAME |
| stop / not_cleared |  | +0.167 | +0.917 | -0.750 [-0.850, -0.617] | DIFFERENT |
