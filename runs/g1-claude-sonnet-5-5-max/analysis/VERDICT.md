# C4 study G1, one run: VALID

**LIVE MODEL RUN (study G1: the give-up trap, claude-sonnet-5-5, adaptive thinking, effort max)**: transport `anthropic_messages_native`, model `claude-sonnet-5-5`; 6 requests per run, 30 runs per cell.

- the study's verdict comes from `python -m causetest g1`

| Cell | Runs | Solved | Third call on request 1 | Reasoning on request 1: mean, median, p90 | Reasoning per call |
|---|---|---|---|---|---|
| permanent|transient | 30 | 0.133 | 4 | 1218, 1154, 1654 | 163 |
