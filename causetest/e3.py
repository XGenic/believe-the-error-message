"""Extension E3: a caution with a stopping rule. See PROTOCOL_E3.md.

In E2 the caution sentence ("error messages do not always state the true cause") rescued the give-up
trap, but it also made GPT-6-luna doubt a true outage: about 5 calls per request instead of 1. E3 adds
a stopping rule to the caution and asks whether it keeps the rescue while cutting that cost:

  control          C4 as run
  caution          the E2 caution, for reference
  caution_bounded  the caution, plus: accept the error if it keeps coming back after a few different attempts
  caution_three    the caution, plus: accept the error if it comes back on three attempts in a row

Per bounded arm, against control and the plain caution:
  give-up rescue           success in the give-up trap, arm minus control
  outage calls vs caution  calls per request on a true outage, arm minus caution (the saving)
  true-temporary success   success in the accurate "temporary" cell, arm minus control (harm check)
"""

from __future__ import annotations

from statistics import mean
from typing import Any, Dict, List, Optional, Tuple

from causetest.e2 import TRAPS, _boot, cell_lines, cell_table, validity_reasons

BOUNDED = ("caution_bounded", "caution_three")
REFERENCE = ("caution",) + BOUNDED
GU_TRAP, GU_TRUE = TRAPS["give_up_trap"]   # "unavailable" over a transient fault; over a permanent one
RT_TRAP, RT_TRUE = TRAPS["retry_trap"]     # "temporary" over a fixable fault; over a transient one


def contrasts_e3(stats: Dict[Tuple[str, str, str], List[Tuple[float, float]]]) -> Dict[str, Optional[float]]:
    def succ(arm, cf):
        v = stats.get((arm,) + cf)
        return mean(x[0] for x in v) if v else None

    def calls(arm, cf):
        v = stats.get((arm,) + cf)
        return mean(x[1] for x in v) if v else None

    def diff(a, b):
        return None if a is None or b is None else a - b

    out: Dict[str, Optional[float]] = {}
    for arm in REFERENCE:
        if (arm,) + GU_TRAP not in stats:
            continue
        out[f"{arm}|give_up_rescue"] = diff(succ(arm, GU_TRAP), succ("control", GU_TRAP))
        out[f"{arm}|outage_calls_vs_control"] = diff(calls(arm, GU_TRUE), calls("control", GU_TRUE))
        out[f"{arm}|true_temporary_success"] = diff(succ(arm, RT_TRUE), succ("control", RT_TRUE))
        out[f"{arm}|retry_trap"] = diff(succ(arm, RT_TRAP), succ("control", RT_TRAP))
        if arm in BOUNDED:
            out[f"{arm}|outage_calls_vs_caution"] = diff(calls(arm, GU_TRUE), calls("caution", GU_TRUE))
    return out


def arm_verdict(arm: str, est: Dict[str, Optional[float]], ci, th: Dict[str, float]) -> str:
    """Decision rule for one bounded arm, applied in order (PROTOCOL_E3.md)."""
    keys = [f"{arm}|give_up_rescue", f"{arm}|outage_calls_vs_caution", f"{arm}|true_temporary_success"]
    if any(est.get(k) is None or ci.get(k, (None, None))[0] is None for k in keys):
        return "NOT_ESTIMABLE"
    (r, c, h), (r_ci, c_ci, h_ci) = [est[k] for k in keys], [ci[k] for k in keys]
    if h <= th["e3_harm_drop"] and h_ci[1] < th["e3_harm_ci_hi"]:
        return "HARMS_TRUE_TEMPORARY"
    rescue = r >= th["e3_rescue_min"] and r_ci[0] > th["e3_rescue_ci_lo"]
    cut = c <= th["e3_cut_calls"] and c_ci[1] < th["e3_cut_ci_hi"]
    if rescue and cut:
        return "COST_AWARE"
    if rescue:
        return "RESCUE_ONLY"
    if cut:
        return "LOSES_RESCUE"
    return "NO_GAIN"


def summarize_e3(rows: List[Dict[str, Any]], cfg: Dict[str, Any]) -> Dict[str, Any]:
    th, n_runs = cfg["thresholds"], cfg["runs_per_cell"]
    stats, details, validity = cell_table(rows, cfg)
    est = contrasts_e3(stats)
    ci = _boot(stats, cfg["bootstrap_reps"], cfg["bootstrap_seed"], contrasts_e3)
    verdicts = {arm: arm_verdict(arm, est, ci, th) for arm in BOUNDED if f"{arm}|give_up_rescue" in est}
    outage_calls = {arm: details.get("|".join((arm,) + GU_TRUE), {}).get("calls_per_request") for arm in
                    ("control",) + REFERENCE}
    s = {"label": cfg.get("label", ""), "model": cfg["model"], "transport": cfg["transport"], "design": "E3",
         "n_tasks": int(cfg.get("n_tasks", 6)), "runs_per_cell": n_runs, "estimates": est,
         "ci": {k: list(v) for k, v in ci.items()}, "contrast_verdicts": verdicts, "outage_calls": outage_calls,
         "cells": details, "validity": validity}
    invalid = validity_reasons(validity, th)
    if not verdicts or "NOT_ESTIMABLE" in verdicts.values():
        invalid.append("some bounded arm could not be estimated")
    s["verdict"] = ({"verdict": "INVALID", "reasons": invalid} if invalid else
                    {"verdict": "VALID", "reasons": [f"{k}: {v}" for k, v in verdicts.items()]})
    return s


def _f(x) -> str:
    if x is None:
        return "n/a"
    return f"{x:+.3f}" if isinstance(x, float) else str(x)


def verdict_markdown_e3(s: Dict[str, Any]) -> str:
    v, est = s["verdict"], s["estimates"]

    def cell(k):
        lo, hi = s["ci"].get(k, (None, None))
        return "not run" if k not in est else f"{_f(est[k])} [{_f(lo)}, {_f(hi)}]"

    lines = [f"# C4 extension E3 verdict: {v['verdict']}", "",
             f"**{s['label']}**: transport `{s['transport']}`, model `{s['model']}`; {s['n_tasks']} requests per run, "
             f"{s['runs_per_cell']} runs per cell.", ""]
    if v["verdict"] == "INVALID":
        lines += [f"- {r}" for r in v["reasons"]] + [""]
    lines += ["## Primary: does the stopping rule keep the rescue and cut the cost?", "",
              "| Arm | Verdict | Give-up rescue (vs control) | Outage calls vs plain caution | "
              "True-'temporary' success (vs control) |", "|---|---|---|---|---|"]
    for arm in BOUNDED:
        if f"{arm}|give_up_rescue" in est:
            lines.append(f"| {arm} | **{s['contrast_verdicts'].get(arm)}** | {cell(arm + '|give_up_rescue')} | "
                         f"{cell(arm + '|outage_calls_vs_caution')} | {cell(arm + '|true_temporary_success')} |")
    oc = s["outage_calls"]
    lines += ["", "## Calls per request on a true outage ('unavailable' over a permanent fault)", "",
              "The lowest cost that keeps the give-up rescue is 3 calls: the transient fault clears on the third.", ""]
    lines += [f"- {arm}: {'n/a' if oc.get(arm) is None else f'{oc[arm]:.2f}'}" for arm in ("control",) + REFERENCE]
    lines += ["", "## Reference and secondary (vs control)", "",
              "| Arm | Give-up rescue | Outage calls | True-'temporary' success | Retry trap |", "|---|---|---|---|---|"]
    for arm in REFERENCE:
        if f"{arm}|give_up_rescue" in est:
            lines.append(f"| {arm} | {cell(arm + '|give_up_rescue')} | {cell(arm + '|outage_calls_vs_control')} | "
                         f"{cell(arm + '|true_temporary_success')} | {cell(arm + '|retry_trap')} |")
    return "\n".join(lines + cell_lines(s))
