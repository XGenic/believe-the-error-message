# W2-D: E5 at low, Sol minus Luna (W5): SAME

- A: `runs/w2d-e5-gpt-6-1-sol-low`
- B: `runs/w5-e5-low-gpt-6-luna`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| D1 | yes | +1.000 | +0.933 | +0.067 [+0.017, +0.133] | SAME |
| stop / cleared |  | +0.000 | +0.033 | -0.033 [-0.083, +0.000] | SAME |
| stop / none |  | +1.000 | +0.967 | +0.033 [+0.000, +0.083] | SAME |
| stop / not_cleared |  | +0.917 | +0.617 | +0.300 [+0.150, +0.450] | DIFFERENT |
