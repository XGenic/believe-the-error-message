# W2-C: Haiku 5.5 E5, thinking on vs off (t0 INVALID: descriptive): SAME

- A: `runs/w2c-e5-claude-haiku-5-5-t1`
- B: `runs/w2c-e5-claude-haiku-5-5-t0`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| D1 | yes | +0.033 | +0.050 | -0.017 [-0.150, +0.100] | SAME |
| stop / cleared |  | +0.083 | +0.950 | -0.867 [-0.950, -0.767] | DIFFERENT |
| stop / none |  | +0.117 | +1.000 | -0.883 [-0.950, -0.800] | DIFFERENT |
| stop / not_cleared |  | +0.917 | +1.000 | -0.083 [-0.167, -0.017] | SAME |
