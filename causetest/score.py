"""Measures, intervals and the pre-set decision rule. See PROTOCOL.md for definitions.

Unit of evidence: the run (one conversation of six requests in one cell). Intervals are percentile
bootstraps that resample runs within each cell independently.
"""

from __future__ import annotations

import random
from collections import Counter
from statistics import mean
from typing import Any, Dict, List, Optional, Sequence, Tuple

from causetest.env import CLAIM_IMPLIES, CONFIRMABLE_MISLEADING, FAULTS, cell_kind, cells

EARLY, LATE = (0, 1), (4, 5)  # request indices for the learning measure


def _m(xs) -> Optional[float]:
    xs = [x for x in xs if x is not None]
    return mean(xs) if xs else None


def first_responses(row: Dict[str, Any]) -> List[Optional[str]]:
    return [t["summary"]["first_response"] for t in row["tasks"]]


def _follow_rate(runs: Sequence[List[Optional[str]]], strategy: str, requests: Sequence[int]) -> Optional[float]:
    """Share of classified first responses on `requests` that equal `strategy`, pooled over runs."""
    vals = [r[i] for r in runs for i in requests if i < len(r) and r[i] not in (None, "UNCLASSIFIABLE")]
    return sum(v == strategy for v in vals) / len(vals) if vals else None


def steering_and_learning(by_cell: Dict[Tuple[str, str], List[List[Optional[str]]]]) -> Dict[str, Any]:
    deltas, l_mis, l_acc = {}, {}, {}
    for claim, fault in cells():
        kind = cell_kind(claim, fault)
        if kind == "neutral":
            continue
        s = CLAIM_IMPLIES[claim]
        runs = by_cell.get((claim, fault), [])
        early, late = _follow_rate(runs, s, EARLY), _follow_rate(runs, s, LATE)
        lval = None if early is None or late is None else early - late
        if kind == "misleading":
            p, base = _follow_rate(runs, s, (0,)), _follow_rate(by_cell.get(("neutral", fault), []), s, (0,))
            deltas[f"{claim}|{fault}"] = None if p is None or base is None else p - base
            l_mis[f"{claim}|{fault}"] = lval
        else:
            l_acc[f"{claim}|{fault}"] = lval
    S = _m(deltas.values()) if all(v is not None for v in deltas.values()) else None
    excluded = "|".join(CONFIRMABLE_MISLEADING)
    lm = _m(v for k, v in l_mis.items() if k != excluded)
    la = _m(l_acc.values())
    return {"S": S, "deltas": deltas, "L_misleading": l_mis, "L_accurate": l_acc,
            "L_star": None if lm is None or la is None else lm - la}


def _boot(by_cell: Dict[Tuple[str, str], List[List[Optional[str]]]], reps: int,
          seed: int) -> Dict[str, Tuple[Optional[float], Optional[float]]]:
    rng = random.Random(seed)
    s_vals, l_vals = [], []
    for _ in range(reps):
        sample = {k: [rng.choice(v) for _ in v] for k, v in by_cell.items() if v}
        r = steering_and_learning(sample)
        if r["S"] is not None:
            s_vals.append(r["S"])
        if r["L_star"] is not None:
            l_vals.append(r["L_star"])

    def ci(xs):
        if not xs:
            return (None, None)
        xs = sorted(xs)
        return (xs[int(0.025 * len(xs))], xs[min(len(xs) - 1, int(0.975 * len(xs)))])
    return {"S": ci(s_vals), "L_star": ci(l_vals)}


def cell_secondary(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    tasks = [t["summary"] for r in rows for t in r["tasks"]]
    by_req = [[r["tasks"][i]["summary"] for r in rows if i < len(r["tasks"])] for i in range(6)]
    first = Counter(t["first_response"] for t in tasks if t["first_response"])
    req1 = Counter(r["tasks"][0]["summary"]["first_response"] for r in rows if r["tasks"] and r["tasks"][0]["summary"]["first_response"])
    late = Counter(t["summary"]["first_response"] for r in rows for t in r["tasks"][4:6] if t["summary"]["first_response"])
    return {
        "runs": len(rows),
        "success_by_request": [_m([float(x["success"]) for x in col]) for col in by_req],
        "calls_by_request": [_m([x["calls"] for x in col]) for col in by_req],
        "calls_late": _m([x["calls"] for col in by_req[4:6] for x in col]),
        "unknown_rate": _m([float(x["unknown"]) for x in tasks]),
        "unsupported_answers": sum(x["unsupported"] for x in tasks),
        "fabricated_result_lines": sum(x["fabricated_result_lines"] for x in tasks),
        "self_cause_language": _m([float(x["self_cause_language"]) for x in tasks]),
        "service_cause_language": _m([float(x["service_cause_language"]) for x in tasks]),
        "first_response_all": dict(first), "first_response_request1": dict(req1), "first_response_late": dict(late),
        "first_call_not_as_written_later": _m([float(t["summary"]["first_call_spelling"] not in (None, "given"))
                                               for r in rows for t in r["tasks"][1:]]),
    }


def summarize(rows: List[Dict[str, Any]], cfg: Dict[str, Any]) -> Dict[str, Any]:
    th, n_runs = cfg["thresholds"], cfg["runs_per_cell"]
    complete = [r for r in rows if r["status"] == "complete"]
    by_cell_rows = {c: [r for r in complete if (r["claim"], r["fault"]) == c] for c in cells()}
    by_cell = {c: [first_responses(r) for r in rs] for c, rs in by_cell_rows.items()}
    sl = steering_and_learning(by_cell)
    ci = _boot(by_cell, cfg["bootstrap_reps"], cfg["bootstrap_seed"])
    secondary = {f"{c}|{f}": cell_secondary(rs) for (c, f), rs in by_cell_rows.items()}
    turns = sum(t["summary"]["agent_turns"] for r in complete for t in r["tasks"])
    bad = sum(t["summary"]["format_errors"] + t["summary"]["over_budget"] for r in complete for t in r["tasks"])
    first = [x for r in complete for x in first_responses(r) if x is not None]
    engagement = {f"{c}|{f}": _m([float(r["tasks"][0]["summary"]["calls"] > 0) for r in rs]) if rs else None
                  for (c, f), rs in by_cell_rows.items()}
    validity = {
        "completion_min": min(len(rs) / n_runs for rs in by_cell_rows.values()),
        "completion": {f"{c}|{f}": len(rs) / n_runs for (c, f), rs in by_cell_rows.items()},
        "protocol_failure_share": bad / turns if turns else None,
        "engagement_min": min((v for v in engagement.values() if v is not None), default=None),
        "engagement": engagement,
        "unclassifiable_share": (sum(x == "UNCLASSIFIABLE" for x in first) / len(first)) if first else None,
    }
    h3 = {}
    for f in FAULTS:
        stable, unstable = secondary[f"permanent|{f}"]["calls_late"], secondary[f"transient|{f}"]["calls_late"]
        h3[f] = {"calls_late_stable_claim": stable, "calls_late_unstable_claim": unstable,
                 "difference": None if stable is None or unstable is None else stable - unstable}
    probe = secondary["|".join(CONFIRMABLE_MISLEADING)]["first_call_not_as_written_later"]
    probe_base = secondary["neutral|" + CONFIRMABLE_MISLEADING[1]]["first_call_not_as_written_later"]
    superstition = {"format_claim": probe, "neutral_claim": probe_base,
                    "index": None if probe is None or probe_base is None else probe - probe_base}
    s = {"label": cfg.get("label", ""), "model": cfg["model"], "transport": cfg["transport"],
         "runs_per_cell": n_runs, "S": sl["S"], "S_ci": ci["S"], "deltas": sl["deltas"],
         "L_star": sl["L_star"], "L_star_ci": ci["L_star"], "L_misleading": sl["L_misleading"],
         "L_accurate": sl["L_accurate"], "cells": secondary, "validity": validity, "H3_stability": h3,
         "H4_talked_out_of_fixable": secondary["permanent|fixable"]["success_by_request"],
         "superstition_probe": superstition}
    s["verdict"] = model_verdict(s, th)
    return s


def model_verdict(s: Dict[str, Any], th: Dict[str, float]) -> Dict[str, Any]:
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
    if s["S"] is None or s["L_star"] is None:
        invalid.append("S or L* could not be computed (a cell had no classified responses)")
    if invalid:
        return {"verdict": "INVALID", "reasons": invalid}
    S, (slo, shi), L, (llo, lhi) = s["S"], s["S_ci"], s["L_star"], s["L_star_ci"]
    desc = f"S {S:+.3f} (CI {slo:+.3f}, {shi:+.3f}); L* {L:+.3f} (CI {llo:+.3f}, {lhi:+.3f})"
    if abs(S) < th["kill_s_max"] and th["kill_s_ci_lo"] < slo and shi < th["kill_s_ci_hi"]:
        return {"verdict": "KILL_WORDING_IRRELEVANT", "reasons": [desc]}
    steered = S >= th["cont_s_min"] and slo >= th["cont_s_ci_lo"]
    if steered and L < th["cred_l_max"] and lhi < th["cred_l_ci_hi"]:
        return {"verdict": "CONTINUE_CREDULOUS", "reasons": [desc]}
    if steered and L >= th["self_l_min"] and llo > th["self_l_ci_lo"]:
        return {"verdict": "CONTINUE_SELF_CORRECTING", "reasons": [desc]}
    return {"verdict": "INCONCLUSIVE", "reasons": [desc]}


def overall_verdict(per_model: Dict[str, str]) -> str:
    valid = {m: v for m, v in per_model.items() if v != "INVALID"}
    if not valid:
        return "INVALID"
    vs = set(valid.values())
    return vs.pop() if len(vs) == 1 else "MIXED"


def pilot_check(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    done = [r for r in rows if r["status"] == "complete"]
    turns = [turn for r in done for t in r["tasks"] for turn in t["turns"]]
    cost = sum(turn["meta"].get("cost_usd", 0.0) for turn in turns)
    bad = sum(t["summary"]["format_errors"] + t["summary"]["over_budget"] for r in done for t in r["tasks"])
    return {"runs": len(rows), "complete": len(done), "agent_calls": len(turns),
            "cost_equiv_usd": round(cost, 4), "usd_per_call": round(cost / len(turns), 5) if turns else None,
            "calls_per_run": round(len(turns) / len(done), 2) if done else None,
            "protocol_failure_share": round(bad / len(turns), 4) if turns else None,
            "engaged_request1": _m([float(r["tasks"][0]["summary"]["calls"] > 0) for r in done])}
