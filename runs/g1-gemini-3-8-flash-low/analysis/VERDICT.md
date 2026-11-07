# C4 study G1, one run: VALID

**LIVE MODEL RUN (study G1: the give-up trap and its comparison, gemini-3.8-flash through OpenRouter, reasoning low, flex tier)**: transport `openrouter_chat_native`, model `google/gemini-3.8-flash`; 6 requests per run, 30 runs per cell.

- the study's verdict comes from `python -m causetest g1`

| Cell | Runs | Solved | Third call on request 1 | Reasoning on request 1: mean, median, p90 | Reasoning per call |
|---|---|---|---|---|---|
| permanent|transient | 30 | 0.172 | 6 | 290, 325, 500 | 25 |
| neutral|transient | 30 | 1.000 | 30 | 257, 264, 518 | 60 |
