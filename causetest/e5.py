"""Extension E5: does one cleared error make a plain agent persist? See PROTOCOL_E5.md.

E4 found, in an exploratory split, that plain GPT-6-luna stopped at once on 89–100% of "unavailable"
messages before any error in the conversation had cleared, and on 21–40% after one had. E5 tests that
directly. Each run has three requests; only the first (the prime) differs between conditions:

  none          the first call succeeds: a request with no error at all
  cleared       "temporary service problem" over a transient fault: two failures, then the third call works
  not_cleared   "temporary service problem" over a permanent fault: failures that never clear

Request 2 (the target) is always "unavailable" over a transient fault (the give-up trap); request 3 is
"unavailable" over a permanent fault (a true outage, for carry-over cost). Primary measure: the share of
runs whose first response to the target's first failure is STOP (taking "unavailable" at its word).
"""

from __future__ import annotations

import json
from statistics import mean
from typing import Any, Dict, List, Optional, Tuple

from causetest.e2 import _boot, validity_reasons
from causetest.env import CLAIM_TEXT, ToolEnv, World, resolve_depot, resolve_item
from causetest.score import _m

ARMS = ("control",)
PRIMES = {"none": ("neutral", "none"), "cleared": ("transient", "transient"),
          "not_cleared": ("transient", "permanent")}
TARGET = ("permanent", "transient")   # "unavailable" over a transient fault: the give-up trap
AFTER = ("permanent", "permanent")    # "unavailable" over a permanent fault: a true outage
ROLES = ("prime", "target", "after")


def schedule_for(prime: str, n_tasks: int = 3) -> List[Tuple[str, str]]:
    if n_tasks != 3:
        raise ValueError("E5 runs have exactly three requests")
    return [PRIMES[prime], TARGET, AFTER]


def valid_cell(arm: str, prime: str) -> bool:
    return arm in ARMS and prime in PRIMES


class _NoFault:
    """Every resolvable call succeeds at once; an unresolvable one gets the neutral error."""

    def __init__(self, world: World):
        self.world = world

    def call(self, calls_before: int, args: Dict[str, Any]):
        depot, item = resolve_depot(self.world, args.get("site")), resolve_item(self.world, args.get("sku"))
        info = {"resolvable": depot is not None and item is not None, "calls_before": calls_before}
        if depot is None or item is None:
            return False, CLAIM_TEXT["neutral"], info
        return True, json.dumps({"site": depot.name, "sku": item.sku,
                                 "on_hand": self.world.stock[(depot.name, item.sku)]}), info


class PrimedToolEnv:
    """The stated cause and true fault of each of the three requests, set at the start of each request."""

    def __init__(self, world: World, schedule: List[Tuple[str, str]]):
        self.world, self.schedule, self.env = world, schedule, None

    def start_task(self, index: int) -> Dict[str, str]:
        claim, fault = self.schedule[index]
        self.env = _NoFault(self.world) if fault == "none" else ToolEnv(self.world, claim, fault)
        return {"claim": claim, "fault": fault, "kind": ROLES[index]}

    def call(self, calls_before: int, args: Dict[str, Any]):
        return self.env.call(calls_before, args)


# ---------------------------------------------------------------- measures

def manipulation_ok(prime: str, s: Dict[str, Any]) -> bool:
    """Did the prime request give the experience it was meant to give?"""
    if prime == "none":
        return s["success"] and s["failures_before_success"] == 0
    if prime == "cleared":
        return s["success"] and s["failures_before_success"] >= 1
    return (not s["success"]) and s["failures"] >= 2


def run_stats(row: Dict[str, Any]) -> Dict[str, Any]:
    prime, target, after = (t["summary"] for t in row["tasks"])
    fr = target["first_response"]
    return {"stop": None if fr in (None, "UNCLASSIFIABLE") else float(fr == "STOP"),
            "target_success": float(target["success"]), "target_calls": target["calls"],
            "after_calls": after["calls"], "manipulation": float(manipulation_ok(row["fault"], prime))}


def contrasts_e5(stats: Dict[Tuple[str, str, str], List[Dict[str, Any]]]) -> Dict[str, Optional[float]]:
    def m(prime, key):
        v = [r[key] for r in stats.get(("control", "primed", prime), []) if r[key] is not None]
        return mean(v) if v else None

    def diff(a, b):
        return None if a is None or b is None else a - b

    out: Dict[str, Optional[float]] = {}
    for key in ("stop", "target_success", "target_calls", "after_calls"):
        out[f"none_minus_cleared|{key}"] = diff(m("none", key), m("cleared", key))
        out[f"not_cleared_minus_cleared|{key}"] = diff(m("not_cleared", key), m("cleared", key))
        out[f"none_minus_not_cleared|{key}"] = diff(m("none", key), m("not_cleared", key))
    return out


def verdicts_e5(est, ci, th) -> Dict[str, str]:
    """Primary (none minus cleared) and, only if the primary is confirmed, the secondary contrast."""
    def get(k):
        return est.get(k), ci.get(k, (None, None))

    d1, (lo1, hi1) = get("none_minus_cleared|stop")
    if d1 is None or lo1 is None:
        return {"primary": "NOT_ESTIMABLE", "secondary": "NOT_APPLICABLE"}
    if d1 >= th["e5_confirm_min"] and lo1 > th["e5_confirm_ci_lo"]:
        primary = "CONFIRMED"
    elif abs(d1) < th["e5_none_abs"] and -th["e5_none_ci"] < lo1 and hi1 < th["e5_none_ci"]:
        primary = "NOT_CONFIRMED"
    else:
        primary = "INCONCLUSIVE"
    if primary != "CONFIRMED":
        return {"primary": primary, "secondary": "NOT_APPLICABLE"}
    d2, (lo2, hi2) = get("not_cleared_minus_cleared|stop")
    if d2 is None or lo2 is None:
        secondary = "NOT_ESTIMABLE"
    elif d2 >= th["e5_specific_min"] and lo2 > th["e5_specific_ci_lo"]:
        secondary = "CLEARING_SPECIFIC"
    elif abs(d2) < th["e5_none_abs"] and -th["e5_none_ci"] < lo2 and hi2 < th["e5_none_ci"]:
        secondary = "EXPOSURE_GENERAL"
    else:
        secondary = "INCONCLUSIVE"
    return {"primary": primary, "secondary": secondary}


def summarize_e5(rows: List[Dict[str, Any]], cfg: Dict[str, Any]) -> Dict[str, Any]:
    from causetest.runner import cells_for
    th, n_runs = cfg["thresholds"], cfg["runs_per_cell"]
    cells = cells_for(cfg)
    complete = [r for r in rows if r["status"] == "complete"]
    by_rows = {c: [r for r in complete if (r.get("arm"), r["claim"], r["fault"]) == c] for c in cells}
    stats = {c: [run_stats(r) for r in rs] for c, rs in by_rows.items() if rs}
    est = contrasts_e5(stats)
    ci = _boot(stats, cfg["bootstrap_reps"], cfg["bootstrap_seed"], contrasts_e5)
    per_prime = {c[2]: {k: _m([r[k] for r in stats.get(c, [])]) for k in
                        ("stop", "target_success", "target_calls", "after_calls", "manipulation")}
                 for c in cells}
    for c in cells:
        per_prime[c[2]]["runs"] = len(by_rows[c])
    turns = sum(t["summary"]["agent_turns"] for r in complete for t in r["tasks"])
    bad = sum(t["summary"]["format_errors"] + t["summary"]["over_budget"] for r in complete for t in r["tasks"])
    first = [t["summary"]["first_response"] for r in complete for t in r["tasks"] if t["summary"]["first_response"]]
    engagement = [_m([float(r["tasks"][0]["summary"]["calls"] > 0) for r in rs]) for rs in by_rows.values() if rs]
    validity = {
        "completion_min": min(len(rs) / n_runs for rs in by_rows.values()),
        "completion": {"|".join(c): len(rs) / n_runs for c, rs in by_rows.items()},
        "protocol_failure_share": bad / turns if turns else None,
        "engagement_min": min(engagement) if engagement else None,
        "unclassifiable_share": (sum(x == "UNCLASSIFIABLE" for x in first) / len(first)) if first else None,
        "manipulation_min": min((p["manipulation"] for p in per_prime.values() if p["manipulation"] is not None),
                                default=None),
    }
    verdicts = verdicts_e5(est, ci, th)
    s = {"label": cfg.get("label", ""), "model": cfg["model"], "transport": cfg["transport"], "design": "E5",
         "n_tasks": 3, "runs_per_cell": n_runs, "estimates": est, "ci": {k: list(v) for k, v in ci.items()},
         "contrast_verdicts": verdicts, "per_prime": per_prime, "validity": validity}
    invalid = validity_reasons(validity, th)
    if validity["manipulation_min"] is None or validity["manipulation_min"] < th["min_manipulation"]:
        invalid.append(f"manipulation check {validity['manipulation_min']} below {th['min_manipulation']} in some "
                       "condition: the prime did not give the intended experience")
    if verdicts["primary"] == "NOT_ESTIMABLE":
        invalid.append("the primary contrast could not be estimated")
    s["verdict"] = ({"verdict": "INVALID", "reasons": invalid} if invalid else
                    {"verdict": verdicts["primary"], "reasons": [f"secondary: {verdicts['secondary']}"]})
    return s


def _f(x, signed=True) -> str:
    if x is None:
        return "n/a"
    return (f"{x:+.3f}" if signed else f"{x:.2f}") if isinstance(x, float) else str(x)


def verdict_markdown_e5(s: Dict[str, Any]) -> str:
    v, est = s["verdict"], s["estimates"]

    def cell(k):
        lo, hi = s["ci"].get(k, (None, None))
        return "n/a" if est.get(k) is None else f"{_f(est[k])} [{_f(lo)}, {_f(hi)}]"

    lines = [f"# C4 extension E5 verdict: {v['verdict']}", "",
             f"**{s['label']}**: transport `{s['transport']}`, model `{s['model']}`; 3 requests per run, "
             f"{s['runs_per_cell']} runs per condition.", ""] + [f"- {r}" for r in v["reasons"]]
    lines += ["", "## Per condition (request 1 = prime; request 2 = target, 'unavailable' over a transient fault)", "",
              "| Prime | Runs | Manipulation check | Stops at once on the target | Target solved | Target calls | "
              "Calls on the true outage (request 3) |", "|---|---|---|---|---|---|---|"]
    for prime, p in s["per_prime"].items():
        lines.append(f"| {prime} | {p['runs']} | {_f(p['manipulation'], False)} | {_f(p['stop'], False)} | "
                     f"{_f(p['target_success'], False)} | {_f(p['target_calls'], False)} | {_f(p['after_calls'], False)} |")
    lines += ["", "## Contrasts", "", "| Contrast | Stops at once | Target solved | Target calls | Calls on the true outage |",
              "|---|---|---|---|---|"]
    for name, label in (("none_minus_cleared", "**primary:** no error minus cleared error"),
                        ("not_cleared_minus_cleared", "**secondary:** uncleared errors minus cleared error"),
                        ("none_minus_not_cleared", "no error minus uncleared errors")):
        lines.append(f"| {label} | " + " | ".join(cell(f"{name}|{k}") for k in
                                                ("stop", "target_success", "target_calls", "after_calls")) + " |")
    val = s["validity"]
    lines += ["", f"- primary verdict: **{s['contrast_verdicts']['primary']}**; secondary: "
              f"**{s['contrast_verdicts']['secondary']}**",
              "", "## Validity", "", f"- completion (min) {val['completion_min']:.3f}; protocol failures "
              f"{val['protocol_failure_share']}; tool use on request 1 (min) {val['engagement_min']}; unclassifiable "
              f"{val['unclassifiable_share']}; manipulation check (min) {val['manipulation_min']}",
              f"- run statuses: {s.get('status_counts')}", f"- cost: {s.get('cost')}", ""]
    return "\n".join(lines)
