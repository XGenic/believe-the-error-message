"""Study W6: does the bounded caution depend on its wording? See PROTOCOL_W6.md.

W2-B found E3's bounded caution weaker on the open-weight models than on GPT-6-luna, and on DeepSeek V4.1
Flash with reasoning it lost real successes: told to accept an error "after a few different attempts", the
agent rewrote the depot on every call, so the call on which a transient fault clears was malformed. W6 runs
three wordings of the stopping rule side by side, each after the E2 caution:

  control          C4 as run
  caution          the E2 caution, for reference
  caution_bounded  "...after a few different attempts, accept it" (E3, W2-B)
  caution_few      "...after a few attempts, accept it" (the same sentence without "different")
  caution_three    "...comes back on three attempts in a row, accept it" (E3)

Per wording, against control (primary):
  give-up rescue          success in the give-up trap, wording minus control
  outage calls            calls per request on a true outage (absolute; the floor that keeps the rescue is 3)
  true-temporary success  success in the accurate "temporary" cell, wording minus control (harm check)

Verdict per wording: HARMS_TRUE_TEMPORARY, RECOMMENDABLE (rescue at about the floor cost), RESCUE_COSTLY or
WEAK_RESCUE. E3's own verdict is reported as a secondary result. Secondary contrasts: each new wording minus
`caution_bounded`, on the give-up trap, the true "temporary" and the retry trap.
"""

from __future__ import annotations

import json
from statistics import mean
from typing import Any, Dict, List, Optional, Tuple

from causetest.compare import DIFF_MIN, SAME_CI, SAME_MAX
from causetest.e2 import TRAPS, _boot, cell_lines, cell_table, validity_reasons
from causetest.e3 import arm_verdict

WORDINGS = ("caution_bounded", "caution_few", "caution_three")
REFERENCE = ("caution",) + WORDINGS
PAIRS = ("caution_few", "caution_three")  # each compared with caution_bounded
GU_TRAP, GU_TRUE = TRAPS["give_up_trap"]   # "unavailable" over a transient fault; over a permanent one
RT_TRAP, RT_TRUE = TRAPS["retry_trap"]     # "temporary" over a fixable fault; over a transient one
PAIR_MEASURES = {"give_up_trap": GU_TRAP, "true_temporary": RT_TRUE, "retry_trap": RT_TRAP}


def contrasts_w6(stats: Dict[Tuple[str, str, str], List[Tuple[float, float]]]) -> Dict[str, Optional[float]]:
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
        out[f"{arm}|outage_calls"] = calls(arm, GU_TRUE)
        out[f"{arm}|true_temporary_success"] = diff(succ(arm, RT_TRUE), succ("control", RT_TRUE))
        out[f"{arm}|retry_trap"] = diff(succ(arm, RT_TRAP), succ("control", RT_TRAP))
        if arm in WORDINGS:
            out[f"{arm}|outage_calls_vs_caution"] = diff(calls(arm, GU_TRUE), calls("caution", GU_TRUE))
    for arm in PAIRS:
        if (arm,) + GU_TRAP not in stats:
            continue
        for name, cf in PAIR_MEASURES.items():
            out[f"{arm}_vs_bounded|{name}"] = diff(succ(arm, cf), succ("caution_bounded", cf))
    return out


def wording_verdict(arm: str, est: Dict[str, Optional[float]], ci, th: Dict[str, float]) -> str:
    """Decision rule for one wording, applied in order (PROTOCOL_W6.md)."""
    keys = [f"{arm}|give_up_rescue", f"{arm}|outage_calls", f"{arm}|true_temporary_success"]
    if any(est.get(k) is None or ci.get(k, (None, None))[0] is None for k in keys):
        return "NOT_ESTIMABLE"
    (r, c, h), (r_ci, c_ci, h_ci) = [est[k] for k in keys], [ci[k] for k in keys]
    if h <= th["e3_harm_drop"] and h_ci[1] < th["e3_harm_ci_hi"]:
        return "HARMS_TRUE_TEMPORARY"
    if not (r >= th["e3_rescue_min"] and r_ci[0] > th["e3_rescue_ci_lo"]):
        return "WEAK_RESCUE"
    if c <= th["w6_calls_max"] and c_ci[1] < th["w6_calls_ci_hi"]:
        return "RECOMMENDABLE"
    return "RESCUE_COSTLY"


def pair_label(x: Optional[float], ci: Tuple[Optional[float], Optional[float]]) -> str:
    """Study N1's fixed rule for a difference between two arms."""
    lo, hi = ci
    if x is None or lo is None:
        return "NOT_ESTIMABLE"
    if abs(x) < SAME_MAX and -SAME_CI < lo and hi < SAME_CI:
        return "SAME"
    if abs(x) >= DIFF_MIN and (lo > 0 or hi < 0):
        return "DIFFERENT"
    return "UNCLEAR"


def varied_every_call(rows: List[Dict[str, Any]], cell: Tuple[str, str, str]) -> Dict[str, int]:
    """Descriptive (W2-B's DeepSeek mechanism): requests with 2+ calls in which no call repeated an earlier one."""
    n = varied = varied_failed = 0
    for r in rows:
        if r["status"] != "complete" or (r.get("arm"), r["claim"], r["fault"]) != cell:
            continue
        for t in r["tasks"]:
            args = [json.dumps(tu["action"].get("args"), sort_keys=True) for tu in t["turns"]
                    if tu.get("action", {}).get("kind") == "call"]
            n += 1
            if len(args) >= 2 and len(set(args)) == len(args):
                varied += 1
                varied_failed += not t["summary"]["success"]
    return {"requests": n, "varied_every_call": varied, "of_which_failed": varied_failed}


def summarize_w6(rows: List[Dict[str, Any]], cfg: Dict[str, Any]) -> Dict[str, Any]:
    th, n_runs = cfg["thresholds"], cfg["runs_per_cell"]
    stats, details, validity = cell_table(rows, cfg)
    est = contrasts_w6(stats)
    ci = _boot(stats, cfg["bootstrap_reps"], cfg["bootstrap_seed"], contrasts_w6)
    present = [arm for arm in WORDINGS if f"{arm}|give_up_rescue" in est]
    verdicts = {arm: wording_verdict(arm, est, ci, th) for arm in present}
    e3_verdicts = {arm: arm_verdict(arm, est, ci, th) for arm in present}
    pairs = {k: pair_label(est[k], ci.get(k, (None, None))) for k in est if "_vs_bounded|" in k}
    mechanism = {arm: varied_every_call(rows, (arm,) + RT_TRUE) for arm in ("control",) + REFERENCE
                 if (arm,) + RT_TRUE in stats}
    s = {"label": cfg.get("label", ""), "model": cfg["model"], "transport": cfg["transport"], "design": "W6",
         "n_tasks": int(cfg.get("n_tasks", 6)), "runs_per_cell": n_runs, "estimates": est,
         "ci": {k: list(v) for k, v in ci.items()}, "contrast_verdicts": verdicts, "e3_verdicts": e3_verdicts,
         "pair_labels": pairs, "true_temporary_variation": mechanism, "cells": details, "validity": validity}
    invalid = validity_reasons(validity, th)
    if not verdicts or "NOT_ESTIMABLE" in verdicts.values():
        invalid.append("some wording could not be estimated")
    s["verdict"] = ({"verdict": "INVALID", "reasons": invalid} if invalid else
                    {"verdict": "VALID", "reasons": [f"{k}: {v}" for k, v in verdicts.items()]})
    return s


def _f(x) -> str:
    if x is None:
        return "n/a"
    return f"{x:+.3f}" if isinstance(x, float) else str(x)


def verdict_markdown_w6(s: Dict[str, Any]) -> str:
    v, est = s["verdict"], s["estimates"]

    def cell(k, signed=True):
        lo, hi = s["ci"].get(k, (None, None))
        f = _f if signed else (lambda x: "n/a" if x is None else f"{x:.2f}")
        return "not run" if k not in est else f"{f(est[k])} [{f(lo)}, {f(hi)}]"

    lines = [f"# C4 study W6 verdict: {v['verdict']}", "",
             f"**{s['label']}**: transport `{s['transport']}`, model `{s['model']}`; {s['n_tasks']} requests per run, "
             f"{s['runs_per_cell']} runs per cell.", ""]
    if v["verdict"] == "INVALID":
        lines += [f"- {r}" for r in v["reasons"]] + [""]
    lines += ["## Primary: each wording of the stopping rule", "",
              "The floor that keeps the give-up rescue is 3 calls on a true outage: the transient fault clears on "
              "the third.", "",
              "| Wording | Verdict | Give-up rescue (vs control) | Outage calls | True-'temporary' success (vs control) "
              "| E3's verdict |", "|---|---|---|---|---|---|"]
    for arm in WORDINGS:
        if f"{arm}|give_up_rescue" in est:
            lines.append(f"| {arm} | **{s['contrast_verdicts'].get(arm)}** | {cell(arm + '|give_up_rescue')} | "
                         f"{cell(arm + '|outage_calls', signed=False)} | {cell(arm + '|true_temporary_success')} | "
                         f"{s['e3_verdicts'].get(arm)} |")
    lines += ["", "## Secondary: each new wording minus `caution_bounded`", "",
              "| Wording | Give-up trap | True 'temporary' | Retry trap |", "|---|---|---|---|"]
    for arm in PAIRS:
        if f"{arm}_vs_bounded|give_up_trap" in est:
            cols = [f"{s['pair_labels'].get(k)} {cell(k)}" for k in
                    (f"{arm}_vs_bounded|{m}" for m in PAIR_MEASURES)]
            lines.append(f"| {arm} | {' | '.join(cols)} |")
    lines += ["", "## Reference and secondary (vs control)", "",
              "| Arm | Give-up rescue | Outage calls | Outage calls vs plain caution | True-'temporary' success "
              "| Retry trap |", "|---|---|---|---|---|---|"]
    for arm in REFERENCE:
        if f"{arm}|give_up_rescue" in est:
            lines.append(f"| {arm} | {cell(arm + '|give_up_rescue')} | {cell(arm + '|outage_calls', signed=False)} | "
                         f"{cell(arm + '|outage_calls_vs_caution') if arm in WORDINGS else ''} | "
                         f"{cell(arm + '|true_temporary_success')} | {cell(arm + '|retry_trap')} |")
    lines += ["", "## Descriptive: true 'temporary' requests in which every call differed from the earlier ones", ""]
    lines += [f"- {arm}: {m['varied_every_call']}/{m['requests']} requests, {m['of_which_failed']} of them failed"
              for arm, m in s["true_temporary_variation"].items()]
    return "\n".join(lines + cell_lines(s))
