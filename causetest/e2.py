"""Extension E2: what breaks the traps? See PROTOCOL_E2.md.

C4 and E1 found two traps that hold for every request: a false "temporary" over a fixable fault (the
agent retries the identical call until the limit) and a false "unavailable" over a transient fault (it
stops after one call, so it never reaches the call that would work). E2 adds one sentence in one place
and measures how much of each trap it removes:

  control           C4 as run
  caution           the system prompt says error messages do not always state the true cause
  caution_strategy  caution, plus: if an approach keeps failing, try a different one
  mixed             the error message keeps its stated cause and adds a generic instruction
  honest            the error message states no cause: "the cause of this failure is unknown"

Cells are (arm, claim, fault). The honest arm has no claim; its cells use the claim "unknown".

Primary measure, per arm and trap: success in the arm's trap cell minus success in the control trap
cell (the share of requests answered with the figure, averaged over runs). Cost, per arm: the change in
success in the accurate "temporary" cell, and the change in calls per request in the accurate
"unavailable" cell (calls wasted on a real outage).
"""

from __future__ import annotations

import random
from statistics import mean
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

from causetest.env import CLAIM_TEXT, CLAIMS, FAULTS, World
from causetest.protocol import system_prompt
from causetest.score import _m, cell_secondary, first_responses

# Agent-facing text. Fixed here, before any E2 call.
CAUTION = "Error messages from the stock system do not always state the true cause of a failure."
STRATEGY = "If an approach keeps failing, try a different one."
INSTRUCTION = "Check the request and try again."
HONEST = "ERROR: the cause of this failure is unknown."
# Extension E3 (PROTOCOL_E3.md): the caution with a stopping rule. Fixed here, before any E3 call.
BOUND_FEW = "If the same error keeps coming back after a few different attempts, accept it."
BOUND_THREE = "If the same error comes back on three attempts in a row, accept it."
# Study W6 (PROTOCOL_W6.md): BOUND_FEW without the word "different". Fixed here, before any W6 call.
BOUND_FEW_PLAIN = "If the same error keeps coming back after a few attempts, accept it."
BOUNDS = {"caution_bounded": BOUND_FEW, "caution_three": BOUND_THREE, "caution_few": BOUND_FEW_PLAIN}

# Study R1 (PROTOCOL_R1.md): "three_only" is BOUND_THREE without the caution; "code_retry" shows the agent the
# control text, and its retries happen in the tool's client (causetest/r1.py). Fixed here, before any R1 call.
ARMS = ("control", "caution", "caution_strategy", "mixed", "honest", "caution_bounded", "caution_three", "caution_few",
        "three_only", "code_retry")
INTERVENTIONS = ARMS[1:]
ARM_NOTES = {"caution": (CAUTION,), "caution_strategy": (CAUTION, STRATEGY),
             **{arm: (CAUTION, bound) for arm, bound in BOUNDS.items()}, "three_only": (BOUND_THREE,)}
NO_CLAIM = "unknown"  # the honest arm's claim

# Each trap's misleading cell and the accurate cell with the same claim, as (claim, fault).
TRAPS = {
    "retry_trap": (("transient", "fixable"), ("transient", "transient")),
    "give_up_trap": (("permanent", "transient"), ("permanent", "permanent")),
}


def valid_cell(arm: str, claim: str, fault: str) -> bool:
    if arm not in ARMS or fault not in FAULTS:
        return False
    return claim == NO_CLAIM if arm == "honest" else claim in CLAIMS


def error_text(arm: str, claim: str) -> str:
    """The text every failure shows in this arm and claim."""
    if arm == "honest":
        return HONEST
    return f"{CLAIM_TEXT[claim]} {INSTRUCTION}" if arm == "mixed" else CLAIM_TEXT[claim]


def system_for(world: World, arm: str, native: bool = False) -> str:
    return system_prompt(world, ARM_NOTES.get(arm), native=native)


def _cell(arm: str, claim_fault: Tuple[str, str]) -> Tuple[str, str, str]:
    """The cell that plays the role of `claim_fault` in an arm: the honest arm replaces the claim."""
    claim, fault = claim_fault
    return (arm, NO_CLAIM if arm == "honest" else claim, fault)


# ---------------------------------------------------------------- measures

def _run_stats(row: Dict[str, Any]) -> Tuple[float, float]:
    """Per run: share of requests answered with the figure, and mean calls per request."""
    s = [t["summary"] for t in row["tasks"]]
    return mean(float(x["success"]) for x in s), mean(x["calls"] for x in s)


def contrasts(stats: Dict[Tuple[str, str, str], List[Tuple[float, float]]]) -> Dict[str, Optional[float]]:
    """All E2 contrasts from per-run (success, calls) lists by cell."""
    def succ(c):
        v = stats.get(c)
        return mean(x[0] for x in v) if v else None

    def calls(c):
        v = stats.get(c)
        return mean(x[1] for x in v) if v else None

    def diff(a, b):
        return None if a is None or b is None else a - b

    out: Dict[str, Optional[float]] = {}
    for arm in INTERVENTIONS:
        for trap, (mis, acc) in TRAPS.items():
            if _cell(arm, mis) in stats:
                out[f"{arm}|{trap}"] = diff(succ(_cell(arm, mis)), succ(_cell("control", mis)))
        a1, a2 = TRAPS["retry_trap"][1], TRAPS["give_up_trap"][1]
        if _cell(arm, a1) in stats:
            out[f"{arm}|cost_success_accurate_temporary"] = diff(succ(_cell(arm, a1)), succ(_cell("control", a1)))
        if _cell(arm, a2) in stats:
            out[f"{arm}|cost_calls_accurate_unavailable"] = diff(calls(_cell(arm, a2)), calls(_cell("control", a2)))
    for fault in ("fixable", "transient"):
        if ("honest", NO_CLAIM, fault) in stats:
            out[f"honest_vs_neutral|{fault}"] = diff(succ(("honest", NO_CLAIM, fault)),
                                                    succ(("control", "neutral", fault)))
    return out


def _boot(stats, reps: int, seed: int, fn: Callable = contrasts) -> Dict[str, Tuple[Optional[float], Optional[float]]]:
    """Percentile intervals for every contrast `fn` returns, resampling runs within cells."""
    rng = random.Random(seed)
    draws: Dict[str, List[float]] = {}
    for _ in range(reps):
        sample = {k: [rng.choice(v) for _ in v] for k, v in stats.items() if v}
        for k, x in fn(sample).items():
            if x is not None:
                draws.setdefault(k, []).append(x)
    out = {}
    for k, xs in draws.items():
        xs.sort()
        out[k] = (xs[int(0.025 * len(xs))], xs[min(len(xs) - 1, int(0.975 * len(xs)))])
    return out


def contrast_verdict(x: Optional[float], ci: Tuple[Optional[float], Optional[float]], th: Dict[str, float]) -> str:
    """Decision rule for one trap contrast (an arm's change in trap success over control)."""
    lo, hi = ci
    if x is None or lo is None:
        return "NOT_ESTIMABLE"
    if x >= th["e2_rescue_min"] and lo > th["e2_rescue_ci_lo"]:
        return "RESCUES"
    if x >= th["e2_helps_min"] and lo > th["e2_helps_ci_lo"]:
        return "HELPS"
    if x <= th["e2_harms_max"] and hi < th["e2_harms_ci_hi"]:
        return "HARMS"
    if abs(x) < th["e2_none_abs"] and -th["e2_none_ci"] < lo and hi < th["e2_none_ci"]:
        return "NO_EFFECT"
    return "INCONCLUSIVE"


def cost_flags(arm: str, est: Dict[str, Optional[float]], ci, th: Dict[str, float]) -> List[str]:
    flags = []
    ds, dc = est.get(f"{arm}|cost_success_accurate_temporary"), est.get(f"{arm}|cost_calls_accurate_unavailable")
    ds_ci = ci.get(f"{arm}|cost_success_accurate_temporary", (None, None))
    dc_ci = ci.get(f"{arm}|cost_calls_accurate_unavailable", (None, None))
    if ds is not None and ds_ci[1] is not None and ds <= th["e2_cost_success_drop"] and ds_ci[1] < 0:
        flags.append(f"success in the accurate 'temporary' cell fell by {-ds:.2f}")
    if dc is not None and dc_ci[0] is not None and dc >= th["e2_cost_calls_rise"] and dc_ci[0] > 0:
        flags.append(f"calls per request in the accurate 'unavailable' cell rose by {dc:.2f}")
    return flags


def cell_table(rows: List[Dict[str, Any]], cfg: Dict[str, Any]):
    """Per-run stats, per-cell details and validity counts for an (arm, claim, fault) design (E2, E3)."""
    from causetest.runner import cells_for  # local import, as in extension.py
    n_runs = cfg["runs_per_cell"]
    cells = cells_for(cfg)
    complete = [r for r in rows if r["status"] == "complete"]
    by_rows = {c: [r for r in complete if (r.get("arm"), r["claim"], r["fault"]) == c] for c in cells}
    stats = {c: [_run_stats(r) for r in rs] for c, rs in by_rows.items() if rs}
    details = {}
    for c, rs in by_rows.items():
        tasks = [t for r in rs for t in r["tasks"]]
        details["|".join(c)] = {
            "runs": len(rs),
            "success": _m([x[0] for x in stats.get(c, [])]),
            "calls_per_request": _m([x[1] for x in stats.get(c, [])]),
            "requests_reaching_third_call": sum(t["summary"]["calls"] >= 3 for t in tasks),
            "requests": len(tasks),
            "runs_ever_reformatting": sum(any("REFORMAT" in t["summary"]["responses"] for t in r["tasks"]) for r in rs),
            "secondary": cell_secondary(rs) if rs else None,
        }
    turns = sum(t["summary"]["agent_turns"] for r in complete for t in r["tasks"])
    bad = sum(t["summary"]["format_errors"] + t["summary"]["over_budget"] for r in complete for t in r["tasks"])
    first = [x for r in complete for x in first_responses(r) if x is not None]
    engagement = [_m([float(r["tasks"][0]["summary"]["calls"] > 0) for r in rs]) for rs in by_rows.values() if rs]
    validity = {
        "completion_min": min(len(rs) / n_runs for rs in by_rows.values()),
        "completion": {"|".join(c): len(rs) / n_runs for c, rs in by_rows.items()},
        "protocol_failure_share": bad / turns if turns else None,
        "engagement_min": min(engagement) if engagement else None,
        "unclassifiable_share": (sum(x == "UNCLASSIFIABLE" for x in first) / len(first)) if first else None,
    }
    return stats, details, validity


def summarize_e2(rows: List[Dict[str, Any]], cfg: Dict[str, Any]) -> Dict[str, Any]:
    th, n_runs = cfg["thresholds"], cfg["runs_per_cell"]
    stats, details, validity = cell_table(rows, cfg)
    est = contrasts(stats)
    ci = _boot(stats, cfg["bootstrap_reps"], cfg["bootstrap_seed"])
    verdicts = {k: contrast_verdict(est[k], ci.get(k, (None, None)), th)
                for k in est if k.split("|")[1] in TRAPS}
    costs = {arm: cost_flags(arm, est, ci, th) for arm in INTERVENTIONS if any(k.startswith(arm + "|") for k in est)}
    s = {"label": cfg.get("label", ""), "model": cfg["model"], "transport": cfg["transport"], "design": "E2",
         "n_tasks": int(cfg.get("n_tasks", 6)), "runs_per_cell": n_runs, "estimates": est,
         "ci": {k: list(v) for k, v in ci.items()}, "contrast_verdicts": verdicts, "cost_flags": costs,
         "cells": details, "validity": validity}
    s["verdict"] = verdict_e2(s, th)
    return s


def validity_reasons(v: Dict[str, Any], th: Dict[str, float]) -> List[str]:
    """The C4 validity rules; an empty list means valid."""
    invalid = []
    if v["completion_min"] < th["min_completion"]:
        invalid.append(f"completion {v['completion_min']:.3f} below {th['min_completion']} in some cell")
    if v["protocol_failure_share"] is None or v["protocol_failure_share"] > th["max_protocol_failure"]:
        invalid.append(f"protocol failures {v['protocol_failure_share']} above {th['max_protocol_failure']}")
    if v["engagement_min"] is None or v["engagement_min"] < th["min_engagement"]:
        invalid.append(f"tool use on request 1 {v['engagement_min']} below {th['min_engagement']} in some cell: "
                       "agents did not engage")
    if v["unclassifiable_share"] is None or v["unclassifiable_share"] > th["max_unclassifiable"]:
        invalid.append(f"unclassifiable responses {v['unclassifiable_share']} above {th['max_unclassifiable']}")
    return invalid


def verdict_e2(s: Dict[str, Any], th: Dict[str, float]) -> Dict[str, Any]:
    """INVALID on the C4 validity rules; otherwise VALID, with the per-trap verdicts as reasons."""
    invalid = validity_reasons(s["validity"], th)
    if not s["contrast_verdicts"] or "NOT_ESTIMABLE" in s["contrast_verdicts"].values():
        invalid.append("some trap contrast could not be estimated")
    if invalid:
        return {"verdict": "INVALID", "reasons": invalid}
    return {"verdict": "VALID", "reasons": [f"{k}: {x}" for k, x in s["contrast_verdicts"].items()]}


# ---------------------------------------------------------------- report

def _f(x) -> str:
    if x is None:
        return "n/a"
    return f"{x:+.3f}" if isinstance(x, float) else str(x)


def _ci(s, k) -> str:
    lo, hi = s["ci"].get(k, (None, None))
    return f"[{_f(lo)}, {_f(hi)}]"


def verdict_markdown_e2(s: Dict[str, Any]) -> str:
    v, est = s["verdict"], s["estimates"]
    lines = [f"# C4 extension E2 verdict: {v['verdict']}", "",
             f"**{s['label']}**: transport `{s['transport']}`, model `{s['model']}`; {s['n_tasks']} requests per run, "
             f"{s['runs_per_cell']} runs per cell.", ""]
    if v["verdict"] == "INVALID":
        lines += [f"- {r}" for r in v["reasons"]] + [""]
    lines += ["## Primary: change in trap success over control", "",
              "| Arm | Retry trap ('temporary' over fixable) | Give-up trap ('unavailable' over transient) |",
              "|---|---|---|"]
    for arm in INTERVENTIONS:
        if not any(f"{arm}|{trap}" in est for trap in TRAPS):
            continue
        cols = []
        for trap in TRAPS:
            k = f"{arm}|{trap}"
            cols.append("not run" if k not in est else
                        f"**{s['contrast_verdicts'].get(k)}** {_f(est[k])} {_ci(s, k)}")
        lines.append(f"| {arm} | {' | '.join(cols)} |")
    lines += ["", "## Cost on the accurate cells", "",
              "| Arm | Δ success, accurate 'temporary' | Δ calls per request, accurate 'unavailable' | Flags |",
              "|---|---|---|---|"]
    for arm in INTERVENTIONS:
        a, b = f"{arm}|cost_success_accurate_temporary", f"{arm}|cost_calls_accurate_unavailable"
        if a in est or b in est:
            flags = "; ".join(s["cost_flags"].get(arm, [])) or "none"
            lines.append(f"| {arm} | {_f(est.get(a))} {_ci(s, a)} | {_f(est.get(b))} {_ci(s, b)} | {flags} |")
    hv = [k for k in est if k.startswith("honest_vs_neutral|")]
    if hv:
        lines += ["", "## Secondary: honest message minus the neutral message ('request rejected')", ""]
        lines += [f"- {k.split('|')[1]} fault: {_f(est[k])} {_ci(s, k)}" for k in hv]
    return "\n".join(lines + cell_lines(s))


def cell_lines(s: Dict[str, Any]) -> List[str]:
    """The per-cell table and validity section shared by the E2 and E3 reports."""
    val = s["validity"]
    lines = ["", "## Per cell", "",
              "| Cell (arm, claim, fault) | Runs | Success | Calls per request | Requests reaching a 3rd call | "
              "Runs ever reformatting | First response, request 1 | Success by request |",
              "|---|---|---|---|---|---|---|---|"]
    for k, d in s["cells"].items():
        sec = d["secondary"] or {}
        sbr = " / ".join("n/a" if x is None else f"{x:.2f}" for x in sec.get("success_by_request", []))
        succ = "n/a" if d["success"] is None else f"{d['success']:.2f}"
        cpr = "n/a" if d["calls_per_request"] is None else f"{d['calls_per_request']:.2f}"
        lines.append(f"| {k.replace('|', ' / ')} | {d['runs']} | {succ} | {cpr} | {d['requests_reaching_third_call']}/{d['requests']} | "
                     f"{d['runs_ever_reformatting']}/{d['runs']} | {sec.get('first_response_request1')} | {sbr} |")
    lines += ["", "## Validity", "", f"- completion (min over cells) {val['completion_min']:.3f}; protocol failures "
              f"{val['protocol_failure_share']}; tool use on request 1 (min) {val['engagement_min']}; "
              f"unclassifiable {val['unclassifiable_share']}",
              f"- run statuses: {s.get('status_counts')}", f"- cost: {s.get('cost')}", ""]
    return lines
