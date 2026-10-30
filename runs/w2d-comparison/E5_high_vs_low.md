# W2-D: Sol, E5, high minus low: SAME

- A: `runs/w2d-e5-gpt-6-1-sol-high`
- B: `runs/w2d-e5-gpt-6-1-sol-low`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| D1 | yes | +0.867 | +1.000 | -0.133 [-0.217, -0.050] | SAME |
| stop / cleared |  | +0.133 | +0.000 | +0.133 [+0.050, +0.217] | SAME |
| stop / none |  | +1.000 | +1.000 | +0.000 [+0.000, +0.000] | SAME |
| stop / not_cleared |  | +0.950 | +0.917 | +0.033 [-0.050, +0.133] | SAME |
