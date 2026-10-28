"""Extension E1: longer runs (18 requests) on four cells, to see whether following a misleading stated
cause fades, persists or grows with more contrary evidence. See PROTOCOL_E1.md.

Primary measure L_E1: for each claim with one misleading and one accurate cell, the drop in following
the claim's strategy from the first three requests to the last three, misleading minus accurate; then
the mean over claims. Pairing by claim removes drift that a claim causes whatever the true fault is.
"""

from __future__ import annotations

import random
from statistics import mean
from typing import Any, Dict, List, Optional, Sequence, Tuple

from causetest.env import CLAIM_IMPLIES, cell_kind
from causetest.score import _m, cell_secondary, first_responses


def _windows(n_tasks: int) -> Tuple[Tuple[int, ...], Tuple[int, ...]]:
    return tuple(range(3)), tuple(range(n_tasks - 3, n_tasks))


def _follow(runs: Sequence[List[Optional[str]]], strategy: str, requests: Sequence[int]) -> Optional[float]:
    vals = [r[i] for r in runs for i in requests if i < len(r) and r[i] not in (None, "UNCLASSIFIABLE")]
    return sum(v == strategy for v in vals) / len(vals) if vals else None


def _pairs(cells: List[Tuple[str, str]]) -> List[Tuple[Tuple[str, str], Tuple[str, str]]]:
    """(misleading cell, accurate cell) pairs that share a claim."""
    out = []
    for claim in sorted({c for c, _ in cells}):
        mis = [x for x in cells if x[0] == claim and cell_kind(*x) == "misleading"]
        acc = [x for x in cells if x[0] == claim and cell_kind(*x) == "accurate"]
        out += [(m, acc[0]) for m in mis] if acc else []
    return out


def learning(by_cell: Dict[Tuple[str, str], List[List[Optional[str]]]], cells: List[Tuple[str, str]],
             n_tasks: int) -> Dict[str, Any]:
    early, late = _windows(n_tasks)
    L = {}
    for c in cells:
        s = CLAIM_IMPLIES.get(c[0])
        e, l = _follow(by_cell.get(c, []), s, early), _follow(by_cell.get(c, []), s, late)
        L["|".join(c)] = None if e is None or l is None else e - l
    contrasts = {}
    for m, a in _pairs(cells):
        lm, la = L["|".join(m)], L["|".join(a)]
        contrasts[f"{m[0]}: {m[1]} vs {a[1]}"] = None if lm is None or la is None else lm - la
    vals = list(contrasts.values())
    return {"L": L, "contrasts": contrasts,
            "L_E1": mean(vals) if vals and all(v is not None for v in vals) else None}


def _boot(by_cell, cells, n_tasks, reps, seed) -> Tuple[Optional[float], Optional[float]]:
    rng = random.Random(seed)
    xs = []
    for _ in range(reps):
        sample = {k: [rng.choice(v) for _ in v] for k, v in by_cell.items() if v}
        r = learning(sample, cells, n_tasks)["L_E1"]
        if r is not None:
            xs.append(r)
    if not xs:
        return (None, None)
    xs.sort()
    return (xs[int(0.025 * len(xs))], xs[min(len(xs) - 1, int(0.975 * len(xs)))])


def summarize_e1(rows: List[Dict[str, Any]], cfg: Dict[str, Any]) -> Dict[str, Any]:
    from causetest.runner import cells_for  # local import: runner imports this module lazily too
    th, n_runs, n_tasks = cfg["thresholds"], cfg["runs_per_cell"], int(cfg["n_tasks"])
    cells = cells_for(cfg)
    complete = [r for r in rows if r["status"] == "complete"]
    by_rows = {c: [r for r in complete if (r["claim"], r["fault"]) == c] for c in cells}
    by_cell = {c: [first_responses(r) for r in rs] for c, rs in by_rows.items()}
    lr = learning(by_cell, cells, n_tasks)
    ci = _boot(by_cell, cells, n_tasks, cfg["bootstrap_reps"], cfg["bootstrap_seed"])
    curves, details = {}, {}
    for c, rs in by_rows.items():
        key, s = "|".join(c), CLAIM_IMPLIES.get(c[0])
        curves[key] = [_follow(by_cell[c], s, (i,)) for i in range(n_tasks)]
        deviation = []
        for r in rs:
            fr = first_responses(r)
            deviation.append(next((i + 1 for i, x in enumerate(fr) if x not in (None, "UNCLASSIFIABLE", s)), None))
        tasks = [t for r in rs for t in r["tasks"]]
        details[key] = {
            "runs": len(rs), "kind": cell_kind(*c),
            "success_by_request": [_m([float(r["tasks"][i]["summary"]["success"]) for r in rs if i < len(r["tasks"])])
                                   for i in range(n_tasks)],
            "calls_by_request": [_m([r["tasks"][i]["summary"]["calls"] for r in rs if i < len(r["tasks"])])
                                 for i in range(n_tasks)],
            "first_deviation_request": deviation,
            "runs_ever_deviating": sum(d is not None for d in deviation),
            "runs_ever_reformatting": sum(any("REFORMAT" in t["summary"]["responses"] for t in r["tasks"]) for r in rs),
            "requests_reaching_third_call": sum(t["summary"]["calls"] >= 3 for t in tasks),
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
    s = {"label": cfg.get("label", ""), "model": cfg["model"], "transport": cfg["transport"], "design": "E1",
         "n_tasks": n_tasks, "runs_per_cell": n_runs, "L_E1": lr["L_E1"], "L_E1_ci": ci, "L": lr["L"],
         "contrasts": lr["contrasts"], "follow_curves": curves, "cells": details, "validity": validity}
    s["verdict"] = verdict_e1(s, th)
    return s


def verdict_e1(s: Dict[str, Any], th: Dict[str, float]) -> Dict[str, Any]:
    v = s["validity"]
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
    if s["L_E1"] is None:
        invalid.append("L_E1 could not be computed")
    if invalid:
        return {"verdict": "INVALID", "reasons": invalid}
    L, (lo, hi) = s["L_E1"], s["L_E1_ci"]
    desc = f"L_E1 {L:+.3f} (CI {lo:+.3f}, {hi:+.3f})"
    if L >= th["e1_learn_min"] and lo > th["e1_learn_ci_lo"]:
        return {"verdict": "LEARNS", "reasons": [desc]}
    if L <= th["e1_entrench_max"] and hi < th["e1_entrench_ci_hi"]:
        return {"verdict": "ENTRENCHMENT", "reasons": [desc]}
    if abs(L) < th["e1_none_abs"] and -th["e1_none_ci"] < lo and hi < th["e1_none_ci"]:
        return {"verdict": "NO_LEARNING", "reasons": [desc]}
    return {"verdict": "INCONCLUSIVE", "reasons": [desc]}


def _f(x) -> str:
    if x is None:
        return "n/a"
    return f"{x:.3f}" if isinstance(x, float) else str(x)


def _bins(xs: List[Optional[float]], width: int = 3) -> str:
    out = []
    for i in range(0, len(xs), width):
        chunk = [x for x in xs[i:i + width] if x is not None]
        out.append("n/a" if not chunk else f"{mean(chunk):.2f}")
    return " / ".join(out)


def verdict_markdown_e1(s: Dict[str, Any]) -> str:
    v, val, n = s["verdict"], s["validity"], s["n_tasks"]
    bins = " / ".join(f"{i + 1}–{min(i + 3, n)}" for i in range(0, n, 3))
    lines = [f"# C4 extension E1 verdict: {v['verdict']}", "",
             f"**{s['label']}**: transport `{s['transport']}`, model `{s['model']}`; {n} requests per run, "
             f"{s['runs_per_cell']} runs per cell.", ""] + [f"- {r}" for r in v["reasons"]]
    lines += ["", "## Primary: change in following the claim, requests 1–3 minus the last three", "",
              "| Cell | L |", "|---|---|"] + [f"| {k} | {_f(x)} |" for k, x in s["L"].items()]
    lines += ["", "| Claim: misleading vs accurate fault | L(misleading) − L(accurate) |", "|---|---|"]
    lines += [f"| {k} | {_f(x)} |" for k, x in s["contrasts"].items()]
    lines += ["", f"- **L_E1** (mean over claims) = {_f(s['L_E1'])} [{_f(s['L_E1_ci'][0])}, {_f(s['L_E1_ci'][1])}]", "",
              f"## Curves by request (bins {bins})", "",
              "| Cell | Kind | Follows the claim | Success | Calls per request | Runs ever deviating | Runs ever reformatting |",
              "|---|---|---|---|---|---|---|"]
    for k, d in s["cells"].items():
        lines.append(f"| {k} | {d['kind']} | {_bins(s['follow_curves'][k])} | {_bins(d['success_by_request'])} | "
                     f"{_bins(d['calls_by_request'])} | {d['runs_ever_deviating']}/{d['runs']} | "
                     f"{d['runs_ever_reformatting']}/{d['runs']} |")
    lines += ["", "## Validity", "", f"- completion (min over cells) {_f(val['completion_min'])}; protocol failures "
              f"{_f(val['protocol_failure_share'])}; tool use on request 1 (min) {_f(val['engagement_min'])}; "
              f"unclassifiable {_f(val['unclassifiable_share'])}",
              f"- run statuses: {s.get('status_counts')}", f"- cost: {s.get('cost')}", ""]
    return "\n".join(lines)
