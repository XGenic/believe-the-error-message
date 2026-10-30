"""Study R1: does the stopping rule depend on how long faults take to clear? See PROTOCOL_R1.md.

In every earlier study the transient fault cleared on the third call, so "three attempts in a row" named
exactly the count that recovers it. R1 draws the recovery time per request: the transient fault clears
after 1, 2, 3 or 4 failed calls to the stock system (on call 2, 3, 4 or 5). Every run meets each recovery
time at least once, and every arm and cell sees the same recovery times for the same seed. Five arms:

  control        C4 as run
  caution        the E2 caution, for reference: persistence without a count
  caution_three  the caution plus "three attempts in a row": the recommended instruction (E3, W6)
  three_only     the stopping rule without the caution
  code_retry     no instruction; the tool's client resends every failed call itself, up to three attempts
                 in all, and the agent sees only the last result: the same count, written in code

Cells: the accurate "temporary" (a true transient fault), the give-up trap ("unavailable" over a transient
fault) and the accurate "unavailable" (a true outage). Calls are counted at the stock system, so for
code_retry they include the client's own retries.

Primary, per subject: the recommended instruction minus the code retry, on give-up-trap success,
true-temporary success and calls on a true outage. Verdict: WORSE_THAN_CODE, COSTLIER_THAN_CODE,
MATCHES_CODE, BETTER_THAN_CODE or UNCLEAR. Secondary: the rule without the caution minus the instruction
(the same three measures), and each arm against control with W6's measures and, for reference, W6's verdict.
"""

from __future__ import annotations

import json
import random
from statistics import mean
from typing import Any, Dict, List, Optional, Tuple

from causetest.e2 import TRAPS, _boot, cell_table, validity_reasons
from causetest.env import CLAIM_TEXT, FAULTS, World, convention_ok, resolve_depot, resolve_item
from causetest.score import _m
from causetest.w6 import pair_label, wording_verdict

RECOVERY_FAILURES = (1, 2, 3, 4)  # failed calls before a transient fault clears; every earlier study: 2
CODE_ATTEMPTS = 3                 # the code retry's attempts per agent call, the first included
ARMS = ("control", "caution", "caution_three", "three_only", "code_retry")
INSTRUCTION, CODE, RULE_ALONE = "caution_three", "code_retry", "three_only"
GU_TRAP, GU_TRUE = TRAPS["give_up_trap"]   # "unavailable" over a transient fault; over a permanent one
RT_TRUE = TRAPS["retry_trap"][1]           # "temporary" over a transient fault
CELLS = (RT_TRUE, GU_TRAP, GU_TRUE)
SUCCESS_MEASURES = {"give_up_trap": GU_TRAP, "true_temporary": RT_TRUE}
PAIRS = {"instruction_vs_code": (INSTRUCTION, CODE), "rule_alone_vs_instruction": (RULE_ALONE, INSTRUCTION)}


def schedule_for(seed: int, n_tasks: int) -> List[int]:
    """Failed calls before the transient fault clears, per request: each recovery time once, the rest drawn
    at random, in an order drawn from the world seed alone, so every arm and cell of a run shares it."""
    if n_tasks < len(RECOVERY_FAILURES):
        raise ValueError("a run needs at least one request per recovery time")
    rng = random.Random(f"r1|{seed}")
    out = list(RECOVERY_FAILURES) + [rng.choice(RECOVERY_FAILURES) for _ in range(n_tasks - len(RECOVERY_FAILURES))]
    rng.shuffle(out)
    return out


def attempts_per_call(arm: Optional[str]) -> int:
    return CODE_ATTEMPTS if arm == CODE else 1


def valid_cell(arm: str, claim: str, fault: str) -> bool:
    return arm in ARMS and (claim, fault) in CELLS


class RecoveryToolEnv:
    """C4's tool, with a recovery time set at the start of each request and an optional retry in the tool's
    client. A transient fault fails the request's first k calls that reach the stock system, whatever they
    send. With `attempts` above 1, a failed call is resent unchanged, up to that many attempts in all, and
    the agent sees only the last result. Every failure shows the cell's one error text, as in C4."""

    def __init__(self, world: World, claim: str, fault: str, schedule: List[int], attempts: int = 1):
        if fault not in FAULTS or claim not in CLAIM_TEXT or attempts < 1:
            raise ValueError((claim, fault, attempts))
        self.world, self.claim, self.fault, self.schedule, self.attempts = world, claim, fault, schedule, attempts
        self.message = CLAIM_TEXT[claim]
        self.k, self.sent = 0, 0

    def start_task(self, index: int) -> Dict[str, int]:
        self.k, self.sent = self.schedule[index], 0
        return {"recovery_failures": self.k}

    def call(self, calls_before: int, args: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        w = self.world
        depot, item = resolve_depot(w, args.get("site")), resolve_item(w, args.get("sku"))
        resolvable = depot is not None and item is not None
        sent_before, ok = self.sent, False
        while not ok and self.sent - sent_before < self.attempts:
            if self.fault == "fixable":
                ok = convention_ok(w, args)
            elif self.fault == "transient":
                ok = resolvable and self.sent >= self.k
            self.sent += 1
        info = {"resolvable": resolvable, "convention_ok": convention_ok(w, args), "calls_before": calls_before,
                "service_calls_before": sent_before, "service_calls": self.sent - sent_before}
        if not ok:
            return False, self.message, info
        return True, json.dumps({"site": depot.name, "sku": item.sku, "on_hand": w.stock[(depot.name, item.sku)]}), info


# ---------------------------------------------------------------- measures

def service_calls(task: Dict[str, Any]) -> int:
    """Calls that reached the stock system in one request: the agent's calls, plus the code retry's own."""
    return sum(t["tool"]["info"].get("service_calls", 1) for t in task["turns"] if "tool" in t)


def run_stats(row: Dict[str, Any]) -> Tuple[float, float]:
    """Per run: share of requests answered with the figure, and calls per request at the stock system."""
    ts = row["tasks"]
    return mean(float(t["summary"]["success"]) for t in ts), mean(service_calls(t) for t in ts)


def contrasts_r1(stats: Dict[Tuple[str, str, str], List[Tuple[float, float]]]) -> Dict[str, Optional[float]]:
    def succ(arm, cf):
        v = stats.get((arm,) + cf)
        return mean(x[0] for x in v) if v else None

    def calls(arm, cf):
        v = stats.get((arm,) + cf)
        return mean(x[1] for x in v) if v else None

    def diff(a, b):
        return None if a is None or b is None else a - b

    out: Dict[str, Optional[float]] = {}
    for arm in ARMS[1:]:
        if (arm,) + GU_TRAP not in stats:
            continue
        out[f"{arm}|give_up_rescue"] = diff(succ(arm, GU_TRAP), succ("control", GU_TRAP))
        out[f"{arm}|outage_calls"] = calls(arm, GU_TRUE)
        out[f"{arm}|true_temporary_success"] = diff(succ(arm, RT_TRUE), succ("control", RT_TRUE))
    for name, (a, b) in PAIRS.items():
        if (a,) + GU_TRAP not in stats or (b,) + GU_TRAP not in stats:
            continue
        for m, cf in SUCCESS_MEASURES.items():
            out[f"{name}|{m}"] = diff(succ(a, cf), succ(b, cf))
        out[f"{name}|outage_calls"] = diff(calls(a, GU_TRUE), calls(b, GU_TRUE))
    return out


def calls_label(x: Optional[float], ci: Tuple[Optional[float], Optional[float]], th: Dict[str, float]) -> str:
    """N1's rule on a scale of calls: SAME if |Δ| < 0.5 and the interval lies within ±1.0; DIFFERENT if
    |Δ| ≥ 0.5 and the interval excludes 0; otherwise UNCLEAR."""
    lo, hi = ci
    if x is None or lo is None:
        return "NOT_ESTIMABLE"
    if abs(x) < th["r1_calls_same_max"] and -th["r1_calls_same_ci"] < lo and hi < th["r1_calls_same_ci"]:
        return "SAME"
    if abs(x) >= th["r1_calls_diff_min"] and (lo > 0 or hi < 0):
        return "DIFFERENT"
    return "UNCLEAR"


def pair_labels(name: str, est: Dict[str, Optional[float]], ci, th: Dict[str, float]) -> Dict[str, str]:
    labels = {m: pair_label(est.get(f"{name}|{m}"), ci.get(f"{name}|{m}", (None, None))) for m in SUCCESS_MEASURES}
    labels["outage_calls"] = calls_label(est.get(f"{name}|outage_calls"), ci.get(f"{name}|outage_calls", (None, None)), th)
    return labels


def primary_verdict(est: Dict[str, Optional[float]], labels: Dict[str, str]) -> str:
    """Decision rule for the instruction against the code retry, applied in order (PROTOCOL_R1.md). A loss of
    real successes comes first, as W6's harm check does."""
    if "NOT_ESTIMABLE" in labels.values():
        return "NOT_ESTIMABLE"

    def moved(m, sign):
        return labels[m] == "DIFFERENT" and sign * est[f"instruction_vs_code|{m}"] > 0
    if any(moved(m, -1) for m in SUCCESS_MEASURES):
        return "WORSE_THAN_CODE"
    if moved("outage_calls", +1):
        return "COSTLIER_THAN_CODE"
    if all(v == "SAME" for v in labels.values()):
        return "MATCHES_CODE"
    if any(moved(m, +1) for m in SUCCESS_MEASURES) or moved("outage_calls", -1):
        return "BETTER_THAN_CODE"
    return "UNCLEAR"


def count_of_three_ceiling(cfg: Dict[str, Any]) -> float:
    """The share of requests whose fault clears within three calls: what a strict count of three recovers."""
    from causetest.runner import world_seeds  # local import, as in e2.py
    ks = [k for s in world_seeds(cfg) for k in schedule_for(s, int(cfg.get("n_tasks", 6)))]
    return mean(float(k < CODE_ATTEMPTS) for k in ks)


def by_recovery(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Dict[str, float]]]:
    """Descriptive: per arm and transient cell, success, calls at the stock system, and the share of requests
    that went past three calls, by recovery time (failed calls before the fault clears)."""
    tally: Dict[str, Dict[str, List[Tuple[float, int]]]] = {}
    for r in rows:
        if r["status"] != "complete" or (r["claim"], r["fault"]) not in (RT_TRUE, GU_TRAP):
            continue
        for t in r["tasks"]:
            k = str(t.get("recovery_failures"))
            tally.setdefault(f"{r['arm']}|{r['claim']}|{r['fault']}", {}).setdefault(k, []).append(
                (float(t["summary"]["success"]), service_calls(t)))
    return {cell: {k: {"requests": len(v), "success": mean(x[0] for x in v), "calls": mean(x[1] for x in v),
                       "past_three": mean(float(x[1] > 3) for x in v)} for k, v in sorted(ks.items())}
            for cell, ks in sorted(tally.items())}


def summarize_r1(rows: List[Dict[str, Any]], cfg: Dict[str, Any]) -> Dict[str, Any]:
    from causetest.runner import cells_for  # local import, as in e2.py
    th, n_runs = cfg["thresholds"], cfg["runs_per_cell"]
    _, details, validity = cell_table(rows, cfg)
    stats: Dict[Tuple[str, str, str], List[Tuple[float, float]]] = {}
    wanted = set(cells_for(cfg))
    for r in rows:
        c = (r.get("arm"), r["claim"], r["fault"])
        if r["status"] == "complete" and c in wanted:
            stats.setdefault(c, []).append(run_stats(r))
    for c, v in stats.items():
        details["|".join(c)]["service_calls_per_request"] = _m([x[1] for x in v])
    est = contrasts_r1(stats)
    ci = _boot(stats, cfg["bootstrap_reps"], cfg["bootstrap_seed"], contrasts_r1)
    labels = {name: pair_labels(name, est, ci, th) for name in PAIRS if f"{name}|give_up_trap" in est}
    primary = primary_verdict(est, labels["instruction_vs_code"]) if "instruction_vs_code" in labels else "NOT_ESTIMABLE"
    w6_reference = {arm: wording_verdict(arm, est, ci, th) for arm in ARMS[1:] if f"{arm}|give_up_rescue" in est}
    s = {"label": cfg.get("label", ""), "model": cfg["model"], "transport": cfg["transport"], "design": "R1",
         "n_tasks": int(cfg.get("n_tasks", 6)), "runs_per_cell": n_runs, "estimates": est,
         "ci": {k: list(v) for k, v in ci.items()}, "contrast_verdicts": {"primary": primary}, "pair_labels": labels,
         "w6_reference_verdicts": w6_reference, "count_of_three_ceiling": count_of_three_ceiling(cfg),
         "by_recovery": by_recovery(rows), "cells": details, "validity": validity}
    invalid = validity_reasons(validity, th)
    if primary == "NOT_ESTIMABLE":
        invalid.append("the primary contrast could not be estimated")
    s["verdict"] = ({"verdict": "INVALID", "reasons": invalid} if invalid else
                    {"verdict": "VALID", "reasons": [f"primary: {primary}"]})
    return s


# ---------------------------------------------------------------- report

def _f(x, signed: bool = True) -> str:
    if x is None:
        return "n/a"
    return (f"{x:+.3f}" if signed else f"{x:.2f}") if isinstance(x, (int, float)) else str(x)


def verdict_markdown_r1(s: Dict[str, Any]) -> str:
    v, est, cells = s["verdict"], s["estimates"], s["cells"]

    def cell(k, signed=True):
        lo, hi = s["ci"].get(k, (None, None))
        return "not run" if k not in est else f"{_f(est[k], signed)} [{_f(lo, signed)}, {_f(hi, signed)}]"

    def level(arm, cf, field):
        return _f(cells.get("|".join((arm,) + cf), {}).get(field), signed=False)

    lines = [f"# C4 study R1 verdict: {v['verdict']}", "",
             f"**{s['label']}**: transport `{s['transport']}`, model `{s['model']}`; {s['n_tasks']} requests per run, "
             f"{s['runs_per_cell']} runs per cell.", ""]
    if v["verdict"] == "INVALID":
        lines += [f"- {r}" for r in v["reasons"]] + [""]
    lines += [f"The transient fault clears after {', '.join(map(str, RECOVERY_FAILURES))} failed calls, drawn per "
              f"request. A strict count of three recovers {s['count_of_three_ceiling']:.2f} of these requests. Calls "
              "are counted at the stock system, so the code retry's own retries are included.", "",
              f"## Primary: the instruction (`{INSTRUCTION}`) minus the same count in code (`{CODE}`): "
              f"**{s['contrast_verdicts']['primary']}**", "",
              "| Measure | Instruction | Code retry | Δ [95% interval] | Label |", "|---|---|---|---|---|"]
    rows = [("give_up_trap", "Success, give-up trap", GU_TRAP, "success"),
            ("true_temporary", "Success, true 'temporary'", RT_TRUE, "success"),
            ("outage_calls", "Calls per request, true outage", GU_TRUE, "service_calls_per_request")]
    for name, (a, b) in PAIRS.items():
        if name != "instruction_vs_code":
            lines += ["", f"## Secondary: the rule without the caution (`{a}`) minus the instruction (`{b}`)", "",
                      "| Measure | Rule alone | Instruction | Δ [95% interval] | Label |", "|---|---|---|---|---|"]
        for m, title, cf, field in rows:
            k = f"{name}|{m}"
            lines.append(f"| {title} | {level(a, cf, field)} | {level(b, cf, field)} | {cell(k, m != 'outage_calls')} | "
                         f"{s['pair_labels'].get(name, {}).get(m, 'n/a')} |")
    lines += ["", "## Secondary: each arm against control (W6's measures)", "",
              "W6's verdict is shown for reference only: its bars were set for a fault that always cleared on the third "
              "call.", "", "| Arm | Give-up rescue | Calls on a true outage | True-'temporary' success | W6's verdict |",
              "|---|---|---|---|---|"]
    for arm in ARMS[1:]:
        if f"{arm}|give_up_rescue" in est:
            lines.append(f"| {arm} | {cell(arm + '|give_up_rescue')} | {cell(arm + '|outage_calls', False)} | "
                         f"{cell(arm + '|true_temporary_success')} | {s['w6_reference_verdicts'].get(arm)} |")
    ks = [str(k) for k in RECOVERY_FAILURES]
    lines += ["", "## Descriptive: by recovery time (failed calls before the fault clears)", "",
              "Each entry: success / calls per request / share of requests past three calls.", "",
              "| Arm, claim, fault | " + " | ".join(f"k = {k}" for k in ks) + " |", "|---" * (len(ks) + 1) + "|"]
    for c, byk in s["by_recovery"].items():
        lines.append(f"| {c.replace('|', ' / ')} | " + " | ".join(
            "n/a" if k not in byk else f"{byk[k]['success']:.2f} / {byk[k]['calls']:.2f} / {byk[k]['past_three']:.2f}"
            for k in ks) + " |")
    lines += ["", "## Per cell", "", "| Cell (arm, claim, fault) | Runs | Success | Calls at the stock system | Agent calls "
              "| First response, request 1 | Success by request |", "|---|---|---|---|---|---|---|"]
    for k, d in cells.items():
        sec = d["secondary"] or {}
        sbr = " / ".join("n/a" if x is None else f"{x:.2f}" for x in sec.get("success_by_request", []))
        lines.append(f"| {k.replace('|', ' / ')} | {d['runs']} | {_f(d['success'], False)} | "
                     f"{_f(d.get('service_calls_per_request'), False)} | {_f(d['calls_per_request'], False)} | "
                     f"{sec.get('first_response_request1')} | {sbr} |")
    val = s["validity"]
    lines += ["", "## Validity", "", f"- completion (min over cells) {val['completion_min']:.3f}; protocol failures "
              f"{val['protocol_failure_share']}; tool use on request 1 (min) {val['engagement_min']}; "
              f"unclassifiable {val['unclassifiable_share']}",
              f"- run statuses: {s.get('status_counts')}", f"- cost: {s.get('cost')}", ""]
    return "\n".join(lines)
