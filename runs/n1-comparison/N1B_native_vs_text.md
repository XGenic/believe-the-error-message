# N1-B: E5, native tool calls minus text format (Luna, reasoning low): SAME

- A: `runs/n1-e5-native-low-gpt-6-luna`
- B: `runs/e5-live-gpt-6-luna`
- Δ = A − B; 95% percentile bootstrap, 2000 resamples, seed 20261801. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and interval excludes 0.

| Measure | Primary | A | B | Δ [95% interval] | Verdict |
|---|---|---|---|---|---|
| D1 | yes | +0.933 | +0.967 | -0.033 [-0.117, +0.050] | SAME |
| stop / cleared |  | +0.067 | +0.033 | +0.033 [-0.050, +0.117] | SAME |
| stop / none |  | +1.000 | +1.000 | +0.000 [+0.000, +0.000] | SAME |
| stop / not_cleared |  | +0.633 | +0.217 | +0.417 [+0.267, +0.567] | DIFFERENT |
