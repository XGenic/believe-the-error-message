# Cost probes

Accurate cells only, on development seeds: not evidence, and in no verdict or panel. Token use, cost and transport health only. Misleading cells may use more tokens per call than these, so the projections are planning figures, and the study's own pilot and cap still apply. Spend is every billed call; the other columns and the projections use complete runs only, so a probe stopped by its cap is understated.

| Probe | Runs | Calls | Spend | Input/call | Cached | Written | Output/call | Reasoning/call: mean, median, p90, max | Calls with reasoning | Refused | Cut off | Latency: median, p95 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| probe-claude-sonnet-5-5-t0 | 9 of 9 | 182 | $0.20 | 1725 | 93% | 7% | 66 | 0, 0, 0, 0 | 0% | 0 | 0 | 1.7 s, 2.8 s |
| probe-claude-sonnet-5-5-t1 | 9 of 9 | 177 | $0.19 | 1681 | 93% | 7% | 61 | 5, 0, 29, 61 | 13% | 0 | 0 | 1.6 s, 2.8 s |
| probe-claude-sonnet-5-5-t2 | 9 of 9 | 180 | $0.40 | 2833 | 94% | 6% | 150 | 94, 0, 300, 2691 | 47% | 0 | 0 | 1.7 s, 5.1 s |
| probe-gemini-3-8-flash-low | 9 of 9 | 175 | $0.21 | 1461 | 17% | 0% | 68 | 48, 11, 93, 1350 | 68% | 0 | 0 | 2.0 s, 4.6 s |
| probe-gemini-3-8-flash-low-flex | 9 of 9 | 178 | $0.10 | 1226 | 0% | 0% | 54 | 34, 9, 95, 554 | 64% | 0 | 0 | 1.9 s, 3.4 s |
| probe-gemini-3-8-flash-medium-flex | 9 of 9 | 182 | $0.19 | 3430 | 53% | 0% | 192 | 171, 21, 439, 4222 | 85% | 0 | 0 | 2.0 s, 6.5 s |
| probe-gemini-3-8-flash-high | 7 of 9 | 152 | $0.72 | 7493 | 69% | 0% | 408 | 387, 55, 499, 7678 | 89% | 0 | 0 | 2.2 s, 22.4 s |

## Projected cost of the full design, per setting

| Probe | Volume like | C4 | E5 | W6 | Total |
|---|---|---|---|---|---|
| probe-claude-sonnet-5-5-t0 | Haiku | $5.44 | $1.18 | $12.64 | $19.26 |
| probe-claude-sonnet-5-5-t0 | Sol | $10.50 | $1.57 | $17.57 | $29.64 |
| probe-claude-sonnet-5-5-t1 | Haiku | $5.17 | $1.11 | $12.03 | $18.31 |
| probe-claude-sonnet-5-5-t1 | Sol | $10.00 | $1.49 | $16.74 | $28.23 |
| probe-claude-sonnet-5-5-t2 | Haiku | $11.02 | $2.44 | $25.20 | $38.65 |
| probe-claude-sonnet-5-5-t2 | Sol | $20.61 | $3.22 | $34.63 | $58.46 |
| probe-gemini-3-8-flash-low | Haiku | $5.51 | $1.06 | $13.69 | $20.25 |
| probe-gemini-3-8-flash-low | Sol | $12.11 | $1.46 | $19.98 | $33.55 |
| probe-gemini-3-8-flash-low-flex | Haiku | $2.61 | $0.49 | $6.53 | $9.63 |
| probe-gemini-3-8-flash-low-flex | Sol | $5.81 | $0.68 | $9.57 | $16.06 |
| probe-gemini-3-8-flash-medium-flex | Haiku | $4.93 | $0.99 | $11.96 | $17.88 |
| probe-gemini-3-8-flash-medium-flex | Sol | $10.36 | $1.34 | $17.18 | $28.88 |
| probe-gemini-3-8-flash-high | Haiku | $17.46 | $3.58 | $41.80 | $62.85 |
| probe-gemini-3-8-flash-high | Sol | $35.76 | $4.84 | $59.45 | $100.06 |
