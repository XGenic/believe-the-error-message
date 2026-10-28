# W5: Luna E5, reasoning high vs low: DIFFERENT

- A: `runs/w5-e5-high-gpt-6-luna`
- B: `runs/w5-e5-low-gpt-6-luna`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| D1 | yes | +0.783 | +0.933 | -0.150 [-0.267, -0.033] | DIFFERENT |
| stop / cleared |  | +0.000 | +0.033 | -0.033 [-0.083, +0.000] | SAME |
| stop / none |  | +0.783 | +0.967 | -0.183 [-0.300, -0.067] | DIFFERENT |
| stop / not_cleared |  | +0.317 | +0.617 | -0.300 [-0.467, -0.117] | DIFFERENT |
