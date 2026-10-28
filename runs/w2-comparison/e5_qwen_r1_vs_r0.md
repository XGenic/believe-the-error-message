# W2-A: Qwen3.8-27B r1 minus r0 (E5, reasoning effect): DIFFERENT

- A: `runs/or-e5-qwen3-8-27b-r1`
- B: `runs/or-e5-qwen3-8-27b-r0`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| D1 | yes | +0.700 | +0.867 | -0.167 [-0.317, -0.017] | DIFFERENT |
| stop / cleared |  | +0.100 | +0.033 | +0.067 [-0.017, +0.150] | SAME |
| stop / none |  | +0.800 | +0.900 | -0.100 [-0.233, +0.033] | SAME |
| stop / not_cleared |  | +0.250 | +0.133 | +0.117 [-0.017, +0.250] | UNCLEAR |
