# W5: Luna E5, reasoning medium vs low: SAME

- A: `runs/w5-e5-medium-gpt-6-luna`
- B: `runs/w5-e5-low-gpt-6-luna`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| D1 | yes | +0.883 | +0.933 | -0.050 [-0.150, +0.050] | SAME |
| stop / cleared |  | +0.017 | +0.033 | -0.017 [-0.083, +0.033] | SAME |
| stop / none |  | +0.900 | +0.967 | -0.067 [-0.167, +0.017] | SAME |
| stop / not_cleared |  | +0.533 | +0.617 | -0.083 [-0.267, +0.100] | UNCLEAR |
