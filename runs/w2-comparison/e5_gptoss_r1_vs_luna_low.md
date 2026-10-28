# W2-A: gpt-oss-120b r1 minus Luna (E5, native calls): DIFFERENT

- A: `runs/or-e5-gpt-oss-120b-r1`
- B: `runs/n1-e5-native-low-gpt-6-luna`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| D1 | yes | +0.250 | +0.933 | -0.683 [-0.833, -0.533] | DIFFERENT |
| stop / cleared |  | +0.683 | +0.067 | +0.617 [+0.483, +0.750] | DIFFERENT |
| stop / none |  | +0.933 | +1.000 | -0.067 [-0.133, -0.017] | SAME |
| stop / not_cleared |  | +0.983 | +0.633 | +0.350 [+0.217, +0.483] | DIFFERENT |
